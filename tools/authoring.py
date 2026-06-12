"""
Authoring Engine — phân loại artifact và điền template.
Item 3.3 — Fusion Agent.

Pipeline: raw_text → classify_and_extract (LLM) → build_body_md → validate → generate doc_id
"""
import json
import logging
import os
import re
from typing import Optional

logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────

LAYER_PREFIX_MAP = {
    "legal_source":    "GSX-LEGAL",
    "operating_rule":  "GSX-OP",
    "daily_tool":      "GSX-TOOL",
    "platform_policy": "GSX-PLAT",
    "case_study":      "GSX-CASE",
}

VALID_LAYERS = set(LAYER_PREFIX_MAP.keys())
VALID_PRIORITIES = {"critical", "high", "medium", "low"}
VALID_PLATFORMS = {"meta", "tiktok", "google", "store", "website", "group", "all"}

# Required fields per layer (để validate)
REQUIRED_FIELDS: dict[str, list[str]] = {
    "legal_source":    ["title", "priority", "tags"],
    "operating_rule":  ["title", "tags"],
    "daily_tool":      ["title", "tags"],
    "platform_policy": ["title", "priority", "tags"],
    "case_study":      ["title", "tags"],
}

# ── LLM prompt ────────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = (
    "Bạn là chuyên gia phân tích văn bản pháp lý và chính sách ngành game Việt Nam. "
    "Nhiệm vụ: phân tích văn bản và trả về JSON cấu trúc."
)

_CLASSIFY_TEMPLATE = """Phân tích văn bản dưới đây và trả về JSON hợp lệ (không có markdown fence, không giải thích thêm):

{{
  "content_layer": "<legal_source|operating_rule|daily_tool|platform_policy|case_study>",
  "title": "<tiêu đề ngắn gọn, tối đa 120 ký tự>",
  "issuing_authority": "<cơ quan ban hành, hoặc null>",
  "issued_date": "<YYYY-MM-DD hoặc null>",
  "effective_date": "<YYYY-MM-DD hoặc null>",
  "official_link": "<URL nguồn chính thức hoặc null>",
  "priority": "<critical|high|medium|low>",
  "platforms": ["<meta|tiktok|google|store|website|group|all>"],
  "tags": ["<tag1>", "<tag2>"],
  "summary": "<tóm tắt nội dung quan trọng cho compliance ngành game, 4-6 câu. KHÔNG copy nguyên văn — chỉ diễn giải>",
  "key_obligations": ["<yêu cầu/nghĩa vụ bắt buộc>"],
  "key_prohibitions": ["<điều cấm tuyệt đối>"],
  "related_doc_ids": ["<doc_id liên quan nếu biết, ví dụ GSX-LEGAL-001 — để [] nếu không chắc>"]
}}

Quy tắc phân loại:
- legal_source: luật, nghị định, thông tư, quyết định nhà nước Việt Nam
- platform_policy: policy chính thức của Meta/TikTok/Google/Apple/Steam/Riot
- operating_rule: quy trình, SOP, guideline vận hành nội bộ
- daily_tool: checklist, template, hướng dẫn thực hành hàng ngày
- case_study: tình huống, sự cố, bài học thực tiễn

QUAN TRỌNG:
- summary: tóm tắt/diễn giải, KHÔNG copy nguyên văn (repo public, vấn đề bản quyền)
- platforms: nếu áp dụng toàn bộ → ["all"]; nếu chỉ một số nền tảng → liệt kê
- Văn bản tiếng Việt hoặc tiếng Anh đều phân tích được

--- VĂN BẢN ---
{text}
"""


# ── LLM helper ────────────────────────────────────────────────────────────────


def _call_llm(prompt: str, use_fallback: bool = False) -> str:
    """Gọi LLM (main hoặc Qwen fallback). Raise nếu fail."""
    api_key = os.environ.get("LLM_API_KEY", "").strip()
    base_url = os.environ.get(
        "LLM_BASE_URL", "https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1"
    ).strip()

    if use_fallback:
        model = (
            os.environ.get("LLM_MODEL_AUTHORING", "")
            or os.environ.get("LLM_MODEL", "")
        ).strip()
    else:
        model = os.environ.get("LLM_MODEL", "").strip()

    if not api_key or not model:
        raise RuntimeError("LLM_API_KEY hoặc LLM_MODEL chưa set trong .env")

    from openai import OpenAI  # type: ignore

    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=2500,
    )
    return response.choices[0].message.content or ""


def _parse_llm_json(text: str) -> dict:
    """
    Bóc JSON từ output LLM.
    Xử lý cả trường hợp LLM bọc trong markdown fence.
    """
    # Bỏ markdown fences
    text = re.sub(r"^```(?:json)?\s*\n?", "", text.strip(), flags=re.MULTILINE)
    text = re.sub(r"\n?```\s*$", "", text.strip(), flags=re.MULTILINE)
    text = text.strip()

    # Tìm JSON object { ... }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        text = text[start : end + 1]

    return json.loads(text)


# ── Core extraction ───────────────────────────────────────────────────────────


def classify_and_extract(raw_text: str, source_url: Optional[str] = None) -> dict:
    """
    Phân loại artifact và trích xuất metadata qua LLM.
    Thử LLM chính trước, fallback Qwen nếu fail.

    Returns dict với các trường: content_layer, title, issuing_authority,
    issued_date, effective_date, official_link, priority, platforms, tags,
    summary, key_obligations, key_prohibitions, related_doc_ids.
    """
    # Cắt text để tránh token limit (8K ký tự ≈ ~2K tokens cho tiếng Việt)
    sample = raw_text[:8000]
    if source_url:
        sample = f"[Nguồn: {source_url}]\n\n{sample}"

    prompt = _CLASSIFY_TEMPLATE.format(text=sample)

    # Thử model chính trước
    last_error = None
    for use_fallback in (False, True):
        try:
            raw_response = _call_llm(prompt, use_fallback=use_fallback)
            result = _parse_llm_json(raw_response)
            break
        except Exception as e:
            last_error = e
            if not use_fallback:
                logger.warning(f"LLM chính thất bại ({e}), thử Qwen fallback...")
            else:
                logger.error(f"Cả 2 LLM thất bại: {e}")
                raise RuntimeError(f"Authoring LLM thất bại: {last_error}") from e

    # Normalize + defaults
    result.setdefault("content_layer", "operating_rule")
    result.setdefault("title", "Rule chưa có tiêu đề")
    result.setdefault("priority", "medium")
    result.setdefault("platforms", ["all"])
    result.setdefault("tags", [])
    result.setdefault("summary", "")
    result.setdefault("key_obligations", [])
    result.setdefault("key_prohibitions", [])
    result.setdefault("related_doc_ids", [])

    # Validate enum values
    if result["content_layer"] not in VALID_LAYERS:
        result["content_layer"] = "operating_rule"
    if result["priority"] not in VALID_PRIORITIES:
        result["priority"] = "medium"

    # Lọc platforms về enum hợp lệ
    cleaned_platforms = [p for p in result["platforms"] if p in VALID_PLATFORMS]
    result["platforms"] = cleaned_platforms or ["all"]

    # Override official_link nếu chưa có nhưng có source_url
    if source_url and not result.get("official_link"):
        result["official_link"] = source_url

    return result


# ── Template body builder ─────────────────────────────────────────────────────


def build_body_md(extracted: dict) -> str:
    """
    Xây body markdown từ metadata đã extract.
    KHÔNG copy nguyên văn — tóm tắt diễn giải (repo public).
    """
    layer = extracted.get("content_layer", "operating_rule")
    title = extracted.get("title", "")
    summary = extracted.get("summary", "")
    obligations = extracted.get("key_obligations", [])
    prohibitions = extracted.get("key_prohibitions", [])
    official_link = extracted.get("official_link", "")
    issuing_authority = extracted.get("issuing_authority", "")
    issued_date = extracted.get("issued_date", "")
    effective_date = extracted.get("effective_date", "")

    lines = [f"# {title}", ""]

    if layer in ("legal_source", "platform_policy"):
        lines += [
            "## 1. Thông tin cơ bản",
            "",
            f"- **Cơ quan ban hành**: {issuing_authority or 'N/A'}",
            f"- **Ngày ban hành**: {issued_date or 'N/A'}",
            f"- **Ngày hiệu lực**: {effective_date or 'N/A'}",
        ]
        if official_link:
            lines.append(f"- **Link gốc**: [{official_link}]({official_link})")
        lines += ["", "---", ""]
        lines += [
            "## 2. Tóm tắt nội dung quan trọng",
            "",
            "> ⚠️ Đây KHÔNG phải bản dịch/copy toàn văn. Chỉ tóm tắt điều/khoản liên quan.",
            "",
            summary or "_Chưa có tóm tắt._",
            "",
        ]
    elif layer == "case_study":
        lines += [
            "## 1. Tình huống & Bài học",
            "",
            summary or "_Chưa có tóm tắt._",
            "",
            "---",
            "",
        ]
    else:  # operating_rule, daily_tool
        lines += [
            "## 1. Mục đích & Phạm vi",
            "",
            summary or "_Chưa có tóm tắt._",
            "",
            "---",
            "",
        ]

    if obligations:
        lines += ["## 3. Yêu cầu bắt buộc", ""]
        for ob in obligations:
            lines.append(f"- {ob}")
        lines.append("")

    if prohibitions:
        lines += ["## 4. Điều cấm", ""]
        for pr in prohibitions:
            lines.append(f"- ❌ {pr}")
        lines.append("")

    if official_link:
        lines += [
            "## 5. Nguồn gốc",
            "",
            f"- [Xem văn bản gốc]({official_link})",
            "",
        ]

    return "\n".join(lines)


# ── Validation ────────────────────────────────────────────────────────────────


def validate_artifact(extracted: dict, body_md: str) -> list[str]:
    """
    Validate artifact. Trả list error strings (rỗng = pass).
    """
    errors: list[str] = []
    layer = extracted.get("content_layer", "")

    if layer not in VALID_LAYERS:
        errors.append(f"content_layer không hợp lệ: '{layer}'")
        return errors  # fail fast

    for field in REQUIRED_FIELDS.get(layer, []):
        val = extracted.get(field)
        if not val or (isinstance(val, list) and len(val) == 0):
            errors.append(f"Thiếu trường bắt buộc: '{field}'")

    if not body_md or len(body_md.strip()) < 50:
        errors.append("body_md quá ngắn (< 50 ký tự) — authoring có thể đã thất bại")

    return errors


# ── Full pipeline ─────────────────────────────────────────────────────────────


def run_authoring_pipeline(
    raw_text: str,
    source_url: Optional[str] = None,
    kb_dir: Optional[str] = None,
) -> dict:
    """
    Full authoring pipeline: classify → build body → validate → gen doc_id.

    Returns:
    {
        success       : bool,
        errors        : list[str],
        doc_id        : str | None,
        content_layer : str,
        title         : str,
        body_md       : str,
        platforms     : list[str],
        tags          : list[str],
        metadata_json : dict,
        source_url    : str | None,
        related_doc_ids: list[str],
    }
    """
    from db import store

    # 1. Classify + extract
    try:
        extracted = classify_and_extract(raw_text, source_url)
    except Exception as e:
        return {
            "success": False,
            "errors": [str(e)],
            "doc_id": None,
            "content_layer": "operating_rule",
            "title": "",
            "body_md": "",
            "platforms": ["all"],
            "tags": [],
            "metadata_json": {},
            "source_url": source_url,
            "related_doc_ids": [],
        }

    # 2. Build body_md
    body_md = build_body_md(extracted)

    # 3. Validate
    errors = validate_artifact(extracted, body_md)

    # 4. Generate doc_id
    layer = extracted["content_layer"]
    doc_id = store.get_next_doc_id(layer, kb_dir)

    # 5. Build metadata_json
    metadata_json: dict = {
        k: extracted.get(k)
        for k in ("issuing_authority", "issued_date", "effective_date",
                  "official_link", "priority")
    }

    final_source_url = extracted.get("official_link") or source_url

    return {
        "success": len(errors) == 0,
        "errors": errors,
        "doc_id": doc_id,
        "content_layer": layer,
        "title": extracted.get("title", ""),
        "body_md": body_md,
        "platforms": extracted.get("platforms", ["all"]),
        "tags": extracted.get("tags", []),
        "metadata_json": metadata_json,
        "source_url": final_source_url,
        "related_doc_ids": extracted.get("related_doc_ids", []),
    }
