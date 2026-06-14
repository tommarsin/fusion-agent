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

    # title có thể bị LLM trả về null/"" (setdefault KHÔNG thay None) → ép non-empty
    # tránh vi phạm NOT NULL ở cột rules.title + tránh "# None" trong body_md.
    if not str(result.get("title") or "").strip():
        result["title"] = "Tài liệu chưa đặt tiêu đề"

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
    title = extracted.get("title") or "Tài liệu chưa đặt tiêu đề"
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
        "title": extracted.get("title") or "Tài liệu chưa đặt tiêu đề",
        "body_md": body_md,
        "platforms": extracted.get("platforms", ["all"]),
        "tags": extracted.get("tags", []),
        "metadata_json": metadata_json,
        "source_url": final_source_url,
        "related_doc_ids": extracted.get("related_doc_ids", []),
    }


# ── Draft generation from summary ───────────────────────────────────────────

LAYER_TEMPLATES = {
    "operating_rule": {
        "label": "Luật vận hành",
        "sections": ["Phạm vi áp dụng", "Quy định chi tiết", "Lý do / Căn cứ pháp lý", "Chế tài xử lý"],
        "placeholder": "## Phạm vi áp dụng\n\n## Quy định chi tiết\n\n## Lý do / Căn cứ pháp lý\n\n## Chế tài xử lý\n",
    },
    "daily_tool": {
        "label": "Daily tool / Checklist",
        "sections": ["Mục đích", "Khi nào sử dụng", "Các bước thực hiện", "Mẫu output / Kết quả mong đợi"],
        "placeholder": "## Mục đích\n\n## Khi nào sử dụng\n\n## Các bước thực hiện\n\n## Mẫu output / Kết quả mong đợi\n",
    },
    "case_study": {
        "label": "Case study",
        "sections": ["Bối cảnh tình huống", "Vi phạm / Sự cố", "Hậu quả", "Bài học rút ra", "Tài liệu liên quan"],
        "placeholder": "## Bối cảnh tình huống\n\n## Vi phạm / Sự cố\n\n## Hậu quả\n\n## Bài học rút ra\n\n## Tài liệu liên quan\n",
    },
    "legal_source": {
        "label": "Nguồn luật pháp",
        "sections": ["Thông tin cơ bản", "Tóm tắt nội dung quan trọng", "Yêu cầu bắt buộc", "Điều cấm"],
        "placeholder": "## Thông tin cơ bản\n- Cơ quan ban hành:\n- Ngày hiệu lực:\n\n## Tóm tắt nội dung quan trọng\n\n## Yêu cầu bắt buộc\n\n## Điều cấm\n",
    },
    "platform_policy": {
        "label": "Policy nền tảng",
        "sections": ["Thông tin cơ bản", "Tóm tắt nội dung quan trọng", "Yêu cầu bắt buộc", "Điều cấm"],
        "placeholder": "## Thông tin cơ bản\n- Nền tảng:\n- Link gốc:\n\n## Tóm tắt nội dung quan trọng\n\n## Yêu cầu bắt buộc\n\n## Điều cấm\n",
    },
}

_DRAFT_SYSTEM_PROMPT = (
    "Bạn là chuyên gia soạn tài liệu compliance ngành game Việt Nam. "
    "Nhiệm vụ: từ ý tóm tắt của người dùng, viết bản nháp đầy đủ theo đúng format cấu trúc yêu cầu. "
    "Viết tiếng Việt, rõ ràng, chuyên nghiệp. Nội dung phải hữu ích và cụ thể — không viết placeholder chung chung."
)

_DRAFT_TEMPLATE = """Người dùng muốn tạo tài liệu loại **{layer_label}** ({content_layer}).

Họ mô tả tóm tắt ý định như sau:
---
{summary}
---

Hãy viết bản nháp đầy đủ theo đúng cấu trúc sau (giữ nguyên heading ##):

{structure}

Quy tắc:
- Viết nội dung CỤ THỂ dựa trên tóm tắt, KHÔNG để placeholder "điền vào đây"
- Nếu thiếu thông tin, suy luận hợp lý từ ngữ cảnh ngành game/compliance VN
- Trả về ĐÚNG format markdown với các heading ## như trên
- KHÔNG bọc trong code fence
- Độ dài: 300–800 từ
"""


def generate_draft_from_summary(summary: str, content_layer: str) -> dict:
    """
    Từ tóm tắt ngắn + loại tài liệu, sinh bản nháp đầy đủ đúng format.
    Tái dụng _call_llm từ authoring engine.

    Returns: {success, draft_text, content_layer, error}
    """
    if content_layer not in LAYER_TEMPLATES:
        return {"success": False, "draft_text": "", "content_layer": content_layer,
                "error": f"Loại tài liệu không hợp lệ: {content_layer}"}

    tmpl = LAYER_TEMPLATES[content_layer]
    structure = "\n".join(f"## {s}\n" for s in tmpl["sections"])

    prompt = _DRAFT_TEMPLATE.format(
        layer_label=tmpl["label"],
        content_layer=content_layer,
        summary=summary.strip(),
        structure=structure,
    )

    for use_fallback in (False, True):
        try:
            from openai import OpenAI
            api_key = os.environ.get("LLM_API_KEY", "").strip()
            base_url = os.environ.get("LLM_BASE_URL",
                                      "https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1").strip()
            if use_fallback:
                model = (os.environ.get("LLM_MODEL_AUTHORING", "")
                         or os.environ.get("LLM_MODEL", "")).strip()
            else:
                model = os.environ.get("LLM_MODEL", "").strip()

            if not api_key or not model:
                raise RuntimeError("LLM_API_KEY hoặc LLM_MODEL chưa set")

            client = OpenAI(api_key=api_key, base_url=base_url)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": _DRAFT_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
                max_tokens=3000,
            )
            draft = response.choices[0].message.content or ""
            draft = draft.strip()
            # Remove markdown fences if LLM wraps
            draft = re.sub(r"^```(?:markdown)?\s*\n?", "", draft, flags=re.MULTILINE)
            draft = re.sub(r"\n?```\s*$", "", draft, flags=re.MULTILINE)

            return {"success": True, "draft_text": draft.strip(),
                    "content_layer": content_layer, "error": None}
        except Exception as e:
            if not use_fallback:
                logger.warning(f"Draft LLM chính thất bại ({e}), thử fallback...")
            else:
                logger.error(f"Draft LLM thất bại: {e}")
                return {"success": False, "draft_text": "", "content_layer": content_layer,
                        "error": str(e)}

    return {"success": False, "draft_text": "", "content_layer": content_layer,
            "error": "Unexpected error"}
