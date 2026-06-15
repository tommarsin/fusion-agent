"""
Notion Content Calendar scan flow (Item 9.5) — Hướng B: Read → Scan → Write back.

Quy trình:
  1. Query Notion DB → lấy rows (tùy chọn filter theo Status, vd "Approve").
  2. Mỗi row: đọc Caption (rich_text), Tags (multi_select) → map platforms,
     gọi scan_content() nội bộ (KHÔNG qua HTTP /scan).
  3. Verdict == SAFE  → Legal check = ✅ True
     Verdict != SAFE  → Legal check = ☐ False + ghi note lý do (nếu có cột note).
  4. Trả summary: {total, passed, failed, errors, details[]}.

`dry_run=True`: chỉ scan + trả kết quả, KHÔNG ghi ngược Notion.

Tên cột có thể override qua scan_options để không hardcode theo 1 DB:
  caption_prop (default "Caption"), tags_prop ("Tags"),
  legal_check_prop ("Legal check"), note_prop ("Legal note"),
  status_prop ("Status").
"""

import base64
import logging
import re
from typing import Optional

import requests as http_requests

from integrations import notion

logger = logging.getLogger(__name__)

# Verdict được coi là "hợp lệ" (tick Legal check)
_PASS_VERDICTS = {"SAFE"}

# Map giá trị Tags (content type) → platforms cho scanner.
# Banner/Video là loại nội dung, không phải nền tảng — mặc định coi như đăng web/social.
_TAG_PLATFORM_MAP = {
    "banner": ["meta", "website"],
    "video": ["tiktok", "meta"],
    "post": ["meta", "group"],
}

_DEFAULT_PLATFORMS = ["website"]

_GDRIVE_FILE_RE = re.compile(r"/d/([a-zA-Z0-9_-]+)")
_MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB — skip ảnh quá nặng
_IMAGE_CONTENT_TYPES = {"image/png", "image/jpeg", "image/webp", "image/gif"}


def _resize_image_bytes(data: bytes, max_side: int = 1024) -> bytes:
    """Resize ảnh về max 1024px cạnh dài nhất, trả JPEG bytes. Fallback trả nguyên."""
    try:
        from io import BytesIO
        from PIL import Image
        img = Image.open(BytesIO(data))
        img.thumbnail((max_side, max_side), Image.LANCZOS)
        buf = BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=80)
        return buf.getvalue()
    except Exception:
        return data


def _download_gdrive_image(url: str) -> Optional[str]:
    """
    Download ảnh từ Google Drive public link → resize → base64 string.
    Trả None nếu không download được hoặc không phải ảnh.
    """
    m = _GDRIVE_FILE_RE.search(url or "")
    if not m:
        return None
    file_id = m.group(1)
    dl_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    try:
        resp = http_requests.get(dl_url, timeout=20, allow_redirects=True)
        if resp.status_code != 200:
            logger.debug("GDrive download %s → %d", file_id[:12], resp.status_code)
            return None
        ctype = (resp.headers.get("content-type") or "").split(";")[0].strip().lower()
        if ctype not in _IMAGE_CONTENT_TYPES:
            logger.debug("GDrive %s not image: %s", file_id[:12], ctype)
            return None
        if len(resp.content) > _MAX_IMAGE_SIZE:
            logger.debug("GDrive %s too large: %d bytes", file_id[:12], len(resp.content))
            return None
        resized = _resize_image_bytes(resp.content)
        return base64.b64encode(resized).decode("ascii")
    except Exception as e:
        logger.debug("GDrive download failed %s: %s", file_id[:12], e)
        return None


def _read_asset_url(page: dict, asset_prop: str) -> str:
    """Đọc URL từ Asset property (hỗ trợ url / rich_text / files type)."""
    prop = (page.get("properties") or {}).get(asset_prop) or {}
    ptype = prop.get("type", "")
    if ptype == "url":
        return prop.get("url") or ""
    if ptype == "rich_text":
        return "".join(p.get("plain_text", "") for p in prop.get("rich_text", []))
    if ptype == "files":
        files = prop.get("files", [])
        if files:
            f = files[0]
            return (
                f.get("external", {}).get("url", "")
                or f.get("file", {}).get("url", "")
                or ""
            )
    return ""


def _resolve_platforms(tags: list[str], default_platforms: list[str]) -> list[str]:
    """Suy ra platforms từ Tags; nếu không khớp → dùng default."""
    plats: list[str] = []
    for tag in tags:
        mapped = _TAG_PLATFORM_MAP.get(tag.strip().lower())
        if mapped:
            plats.extend(mapped)
    # unique giữ thứ tự
    seen = set()
    out = [p for p in plats if not (p in seen or seen.add(p))]
    return out or list(default_platforms)


def _build_note(result: dict, max_len: int = 1800) -> str:
    """Tạo note ngắn gọn từ violations để ghi ngược Notion."""
    verdict = result.get("verdict", "?")
    violations = result.get("violations", []) or []
    if not violations:
        return f"[{verdict}] Không có vi phạm cụ thể."
    lines = [f"[{verdict}] {len(violations)} vấn đề:"]
    for v in violations[:5]:
        doc = v.get("rule_doc_id", "")
        reason = (v.get("reason", "") or "").strip()
        quote = (v.get("quote", "") or "").strip()
        prefix = f"• {doc}: " if doc else "• "
        snippet = reason or quote
        lines.append(f"{prefix}{snippet}")
    note = "\n".join(lines)
    return note[:max_len]


def _write_back(
    page_id: str,
    passed: bool,
    note: str,
    legal_check_prop: str,
    note_prop: Optional[str],
) -> None:
    """
    Ghi ngược: checkbox Legal check + (tùy chọn) note.
    Nếu cột note không tồn tại → Notion trả 400; retry chỉ với checkbox.
    """
    props_with_note = {legal_check_prop: {"checkbox": passed}}
    if note_prop:
        props_with_note[note_prop] = {
            "rich_text": [{"type": "text", "text": {"content": note[:2000]}}]
        }
    try:
        notion.update_page(page_id, props_with_note)
    except notion.NotionError as e:
        # Có thể do cột note không tồn tại / sai kiểu → thử lại chỉ checkbox
        if note_prop and (e.status_code == 400):
            logger.warning(
                "Ghi note thất bại (cột '%s' có thể không tồn tại) — retry chỉ checkbox: %s",
                note_prop, e,
            )
            notion.update_page(page_id, {legal_check_prop: {"checkbox": passed}})
        else:
            raise


def scan_notion_calendar(database_id: str, scan_options: Optional[dict] = None) -> dict:
    """
    Quét Content Calendar trên Notion.

    scan_options (đều optional):
      filter_status: str  — chỉ scan rows có Status = giá trị này (vd "Approve")
      dry_run: bool       — True = không ghi ngược Notion (default False)
      platforms: list[str]— platforms mặc định khi Tags không map được
      caption_prop / tags_prop / legal_check_prop / note_prop / status_prop: str
      tenant_id: int      — truyền xuống scan_content (audit/RAG context)

    Returns:
      {total, passed, failed, errors, dry_run, details: [
         {page_id, caption_preview, verdict, violations, written, error}
      ]}
    """
    from tools.scanner import scan_content

    opts = scan_options or {}
    dry_run = bool(opts.get("dry_run", False))
    filter_status = (opts.get("filter_status") or "").strip()
    scan_images = bool(opts.get("scan_images", False))
    asset_prop = opts.get("asset_prop") or "Asset"
    caption_prop = opts.get("caption_prop") or "Caption"
    tags_prop = opts.get("tags_prop") or "Tags"
    legal_check_prop = opts.get("legal_check_prop") or "Legal check"
    note_prop = opts.get("note_prop", "Legal note")  # set None để tắt note
    status_prop = opts.get("status_prop") or "Status"
    default_platforms = opts.get("platforms") or _DEFAULT_PLATFORMS
    tenant_id = opts.get("tenant_id")

    # Filter theo Status (nếu có). Hỗ trợ cả status & select type → thử status trước.
    notion_filter = None
    if filter_status:
        notion_filter = {
            "or": [
                {"property": status_prop, "status": {"equals": filter_status}},
                {"property": status_prop, "select": {"equals": filter_status}},
            ]
        }

    try:
        rows = notion.query_database(database_id, filter=notion_filter)
    except notion.NotionError as e:
        # Filter có thể sai kiểu property → thử lại không filter (scan hết, lọc sau)
        if notion_filter:
            logger.warning("Query có filter thất bại (%s) — thử lại không filter", e)
            rows = notion.query_database(database_id, filter=None)
            if filter_status:
                rows = [
                    r for r in rows
                    if notion.read_status_property(r, status_prop) == filter_status
                ]
        else:
            raise

    total = len(rows)
    passed = 0
    failed = 0
    errors = 0
    details: list[dict] = []

    for page in rows:
        page_id = page.get("id", "")
        caption = notion.read_text_property(page, caption_prop)
        if not caption:
            # fallback: dùng title property nếu Caption trống
            title_name = notion.find_title_property_name(page)
            if title_name:
                caption = notion.read_text_property(page, title_name)

        if not caption.strip():
            errors += 1
            details.append({
                "page_id": page_id,
                "caption_preview": "",
                "verdict": None,
                "violations": 0,
                "written": False,
                "error": f"Không tìm thấy nội dung ở cột '{caption_prop}'",
            })
            continue

        tags = notion.read_multiselect_property(page, tags_prop)
        platforms = _resolve_platforms(tags, default_platforms)

        # Asset image download (Phase 4)
        images: Optional[list[str]] = None
        if scan_images:
            asset_url = _read_asset_url(page, asset_prop)
            if asset_url and "drive.google.com" in asset_url:
                img_b64 = _download_gdrive_image(asset_url)
                if img_b64:
                    images = [img_b64]

        try:
            result = scan_content(
                content=caption,
                platforms=platforms,
                tenant_id=tenant_id,
                images=images,
                actor_role="mod",
            )
        except Exception as e:
            errors += 1
            logger.error("scan_content lỗi cho page %s: %s", page_id, e)
            details.append({
                "page_id": page_id,
                "caption_preview": caption[:80],
                "verdict": None,
                "violations": 0,
                "written": False,
                "error": f"scan_content lỗi: {e}",
            })
            continue

        verdict = result.get("verdict", "WARNING")
        is_pass = verdict in _PASS_VERDICTS
        if is_pass:
            passed += 1
        else:
            failed += 1

        note = _build_note(result)
        written = False
        write_error = None

        if not dry_run and page_id:
            try:
                _write_back(page_id, is_pass, note, legal_check_prop, note_prop)
                written = True
            except notion.NotionError as e:
                write_error = str(e)
                errors += 1
                logger.warning("Ghi ngược page %s thất bại: %s", page_id, e)

        details.append({
            "page_id": page_id,
            "caption_preview": caption[:80],
            "has_image": bool(images),
            "verdict": verdict,
            "violations": len(result.get("violations", []) or []),
            "platforms": platforms,
            "note": note,
            "written": written,
            "error": write_error,
        })

    summary = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "dry_run": dry_run,
        "details": details,
    }
    logger.info(
        "scan_notion_calendar %s → total=%d passed=%d failed=%d errors=%d dry_run=%s",
        database_id, total, passed, failed, errors, dry_run,
    )
    return summary
