"""
KB loader cho Fusion Agent.

Nguồn 1: knowledge_base/*.md (core — từ kb-clean)
Nguồn 2: bảng rules trong vDB (tenant/campaign, status=approved)

Graceful degradation: nếu DB chưa sống hoặc thiếu env → chỉ dùng KB md.
"""

import logging
import os
import re
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

# Map tên thư mục → enum content_layer
FOLDER_TO_LAYER: dict[str, str] = {
    "01_LEGAL_SOURCE": "legal_source",
    "02_GSX_OPERATING_RULES": "operating_rule",
    "03_DAILY_TOOLS": "daily_tool",
    "04_CASE_STUDIES": "case_study",
    # "06_PLATFORM_POLICY" gộp vào 01_LEGAL_SOURCE (Item 9.3)
}

# Các thư mục bỏ qua (template + index không có giá trị retrieve)
SKIP_FOLDERS = {"99_TEMPLATES", "00_INDEX_VERSION"}


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Tách YAML frontmatter và body. Trả (meta, body)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip()
    body = text[end + 4:].strip()
    try:
        meta = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as e:
        logger.debug(f"YAML parse warning: {e}")
        meta = {}
    return meta, body


def _normalize_list_field(value) -> list[str]:
    """Chuẩn hóa field có thể là str, list, hoặc None về list[str]."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value]
    return [v.strip() for v in str(value).split(",") if v.strip()]


def _chunk_by_headings(body: str, meta: dict, source_path: str, content_layer: str) -> list[dict]:
    """
    Chunk body theo heading ## / ###.
    Mỗi chunk gắn metadata từ frontmatter.
    """
    doc_id = str(meta.get("doc_id", Path(source_path).stem))
    title = str(meta.get("title", doc_id))
    tags = _normalize_list_field(meta.get("tags"))
    platforms = _normalize_list_field(meta.get("platforms")) or ["all"]

    # Parse related doc_ids từ nhiều frontmatter field.
    # YAML parse các item kiểu "GSX-LEGAL-001: Title" thành dict {doc_id: title}.
    related_doc_ids: list[str] = []
    for field in ("related_legal_sources", "related_operating_rules",
                  "related_case_studies", "related_tools"):
        raw = meta.get(field, [])
        if isinstance(raw, list):
            for item in raw:
                if isinstance(item, dict):
                    # {"GSX-LEGAL-001": "Title"} → lấy key đầu
                    candidate = str(next(iter(item.keys()), "")).strip()
                else:
                    # "GSX-LEGAL-001: Title" hoặc "GSX-LEGAL-001"
                    candidate = str(item).split(":")[0].strip()
                if candidate and candidate not in related_doc_ids:
                    related_doc_ids.append(candidate)
        elif isinstance(raw, str):
            candidate = raw.split(":")[0].strip()
            if candidate and candidate not in related_doc_ids:
                related_doc_ids.append(candidate)

    base_meta = {
        "doc_id": doc_id,
        "title": title,
        "content_layer": content_layer,
        "tags": tags,
        "platforms": platforms,
        "scope": "core",
        "source_path": source_path,
        "tenant_id": None,
        "campaign_id": None,
        "related_doc_ids": related_doc_ids,
    }

    heading_pattern = re.compile(r"^(#{2,3})\s+(.+)$", re.MULTILINE)
    matches = list(heading_pattern.finditer(body))

    chunks: list[dict] = []

    if not matches:
        if body.strip():
            chunks.append({**base_meta, "heading": title, "body": body.strip()})
        return chunks

    # Text trước heading đầu tiên (intro)
    intro = body[: matches[0].start()].strip()
    if intro:
        chunks.append({**base_meta, "heading": title, "body": intro})

    for i, m in enumerate(matches):
        heading_text = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        section_body = body[start:end].strip()
        if section_body:
            chunks.append({**base_meta, "heading": heading_text, "body": section_body})

    return chunks


def load_kb_chunks(kb_dir: str) -> list[dict]:
    """
    Load và chunk toàn bộ .md file đủ điều kiện trong kb_dir.
    Bỏ qua: 99_TEMPLATES/, 00_INDEX_VERSION/, README.md, root README.md.
    """
    kb_path = Path(kb_dir)
    if not kb_path.exists():
        logger.warning(f"knowledge_base không tìm thấy tại: {kb_dir}")
        return []

    chunks: list[dict] = []
    skipped = 0

    for md_file in sorted(kb_path.rglob("*.md")):
        rel = md_file.relative_to(kb_path)
        parts = rel.parts

        # Bỏ qua root README.md
        if len(parts) == 1:
            skipped += 1
            continue

        top_folder = parts[0]

        if top_folder in SKIP_FOLDERS:
            skipped += 1
            continue

        # Bỏ qua README.md trong mọi thư mục
        if md_file.name == "README.md":
            skipped += 1
            continue

        content_layer = FOLDER_TO_LAYER.get(top_folder)
        if content_layer is None:
            logger.debug(f"Thư mục '{top_folder}' không có mapping layer, bỏ qua {md_file.name}")
            skipped += 1
            continue

        try:
            text = md_file.read_text(encoding="utf-8")
        except OSError as e:
            logger.warning(f"Không đọc được {md_file}: {e}")
            skipped += 1
            continue

        meta, body = _parse_frontmatter(text)
        file_chunks = _chunk_by_headings(body, meta, str(md_file), content_layer)
        chunks.extend(file_chunks)

    logger.info(
        f"KB loader (md): {len(chunks)} chunks từ {len(chunks)} sections "
        f"({skipped} files bỏ qua)"
    )
    return chunks


def load_db_rules() -> list[dict]:
    """
    Load rules đã approved từ vDB (bảng rules, status='approved').
    Trả [] và log warning nếu DB chưa sống / thiếu env — KHÔNG raise.
    """
    try:
        import psycopg2  # type: ignore
        import psycopg2.extras  # type: ignore
    except ImportError:
        logger.warning("psycopg2 chưa cài — DB loader bị tắt")
        return []

    db_host = os.environ.get("DB_HOST", "").strip()
    db_port = os.environ.get("DB_PORT", "5432").strip()
    db_name = os.environ.get("DB_NAME", "fusion_agent").strip()
    db_user = os.environ.get("DB_USER", "").strip()
    db_pass = os.environ.get("DB_PASSWORD", "").strip()
    db_sslmode = os.environ.get("DB_SSLMODE", "prefer").strip()

    if not db_host or not db_user:
        logger.warning("DB_HOST hoặc DB_USER chưa set — DB loader bỏ qua, dùng KB md only")
        return []

    try:
        conn = psycopg2.connect(
            host=db_host,
            port=int(db_port),
            dbname=db_name,
            user=db_user,
            password=db_pass,
            sslmode=db_sslmode,
            connect_timeout=5,
        )
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            "SELECT doc_id, content_layer, scope, tenant_id, campaign_id, "
            "platforms, title, body_md "
            "FROM rules WHERE status = 'approved'"
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.warning(f"DB kết nối/query thất bại ({e}) — tiếp tục với KB md only")
        return []

    chunks: list[dict] = []
    for row in rows:
        platforms = list(row["platforms"]) if row["platforms"] else ["all"]
        body = row["body_md"] or ""
        chunks.append(
            {
                "doc_id": str(row["doc_id"]),
                "title": str(row["title"]),
                "content_layer": str(row["content_layer"]),
                "tags": [],
                "platforms": platforms,
                "scope": str(row["scope"]),
                "source_path": "db:rules",
                "heading": str(row["title"]),
                "body": body,
                "tenant_id": row["tenant_id"],
                "campaign_id": row["campaign_id"],
            }
        )

    logger.info(f"DB loader: {len(chunks)} rules approved được load")
    return chunks


def load_all_chunks(kb_dir: str) -> list[dict]:
    """Load KB md + DB rules. Degrade gracefully nếu DB chưa sống."""
    md_chunks = load_kb_chunks(kb_dir)
    db_chunks = load_db_rules()
    total = len(md_chunks) + len(db_chunks)
    logger.info(f"Tổng chunks sẵn sàng: {total} (md={len(md_chunks)}, db={len(db_chunks)})")
    return md_chunks + db_chunks
