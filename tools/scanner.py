"""
Item 3.2 — Content Scanner 4 bước: Detect → Explain → Rewrite → Checklist
Endpoint: POST /scan

Flow:
  1. DETECT  — rule cứng (regex/keyword, không cần LLM) + LLM-assisted cho nuance
  2. EXPLAIN — mỗi vi phạm: reason + rule_doc_id; quyết định verdict
  3. REWRITE — LLM viết lại bản an toàn (chỉ khi WARNING / BLOCKED có thể sửa)
  4. CHECKLIST — gọi tools/checklist.py:generate_checklist() (hàm dùng chung với 3.4)

Quyết định thiết kế (ghi vào update-log):
  - Rule cứng hardcode kèm comment doc_id (ổn định hơn parse md cho demo)
  - LLM call: 1 call detect+explain (JSON), 1 call rewrite (text)
  - ai_config: đọc từ vDB; fallback = strict / warn_explain_suggest / detailed
"""

import hashlib
import json
import logging
import os
import re
from typing import Optional

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
# RULE CỨng — hardcode (nguồn: GSX-TOOL-005, GSX-OP-002, GSX-LEGAL-001/010)
# ══════════════════════════════════════════════════════════════════════════════

# ── Red-lines (BLOCK tuyệt đối) ───────────────────────────────────────────────

# Từ khoá CCCD/CMND — red-line NĐ13/2023 (GSX-LEGAL-001) + GSX-OP-002
_CCCD_KEYWORDS = re.compile(
    r"\b(cccd|cmnd|căn cước|chứng minh (thư|nhân dân)|giấy tờ tùy thân"
    r"|số căn cước|mã số thuế cá nhân|số bảo hiểm xã hội"
    r"|gửi cccd|nộp cccd|chụp cccd|upload cccd|photo cccd"
    r"|gửi cmnd|nộp cmnd|chụp cmnd)\b",
    re.IGNORECASE | re.UNICODE,
)
# Pattern số 12 chữ số (CCCD) hoặc 9 chữ số (CMND cũ) đứng độc lập
_CCCD_NUMBER_PATTERN = re.compile(r"(?<!\d)\d{12}(?!\d)|(?<!\d)\d{9}(?!\d)")

# Cá độ / cờ bạc — red-line GSX-OP-002 4E + 4F
_GAMBLING_KEYWORDS = re.compile(
    r"\b(cá độ|ca do|cá cược|ca cuoc|đặt cược|dat cuoc|kèo nhà cái|keo nha cai"
    r"|casino|slot machine|nhà cái|nha cai|baccarat|poker có tiền"
    r"|cược thể thao|cuoc the thao|link cá độ|link ca do"
    r"|quảng bá cá độ|tham gia cá độ)\b",
    re.IGNORECASE | re.UNICODE,
)

# Bản đồ lãnh thổ — red-line GSX-OP-002 4A
_MAP_KEYWORDS = re.compile(
    r"\b(bản đồ việt nam|ban do viet nam|bản đồ vn|hình dạng lãnh thổ"
    r"|đường cơ sở|lãnh hải việt nam|bản đồ khu vực|infographic địa lý"
    r"|bản đồ đông nam á|map vietnam|vietnam map)\b",
    re.IGNORECASE | re.UNICODE,
)

# ── Từ tuyệt đối — WARNING / BLOCKED (nguồn: GSX-LEGAL-010 Luật QC Khoản 11 Điều 8) ──
# NĐ87/2026 hiệu lực 05/07/2026 (sau demo) → chỉ ghi chú, không dùng làm căn cứ chính
_SUPERLATIVE_PATTERN = re.compile(
    r"\b(nhất\b|duy nhất|tốt nhất|số một|số 1|hàng đầu|đỉnh nhất|mạnh nhất"
    r"|khủng nhất|lớn nhất|hot nhất|nhanh nhất|rẻ nhất|ngon nhất|hay nhất"
    r"|chuyên nghiệp nhất|uy tín nhất|đáng tin nhất|phổ biến nhất"
    r"|best\b|top 1\b|#1\b|number one|leading|ultimate|greatest"
    r"|only one|exclusive deal|unmatched|unrivaled|unbeatable)\b",
    re.IGNORECASE | re.UNICODE,
)

# Whitelist: tên game / context game — từ "nhất" trong game context thường là hợp lệ
# (vd "tướng mạnh nhất meta" = mô tả gameplay, không phải quảng cáo thương mại)
_GAME_WHITELIST = {
    "wild rift", "tốc chiến", "liên minh huyền thoại", "lol", "tft",
    "đấu trường chân lý", "valorant", "pubg mobile",
    "tướng", "skin", "rank", "meta", "buff", "nerf", "patch", "gank",
    "jungler", "support", "carry", "cosplay tướng", "fan art", "esport",
    "vcs", "wild rounds", "quân đoàn tốc chiến", "cắm mắt bắt view",
    "gameplay", "champion", "hero", "ability",
}

# ── Chửi tục — red-line GSX-OP-002 4I ────────────────────────────────────────
_PROFANITY_PATTERN = re.compile(
    r"\b(đ[._\-\s*]*m|d[._\-\s*]*m|c[._\-\s*]*ú[._\-\s*]*t"
    r"|v[._\-\s*]*l|đ[._\-\s*]*c|đ[._\-\s*]*k|cl\b|đl\b"
    r"|đéo|đụ|mẹ kiếp|đmm|vcl|vkl|cặc|lồn|buồi)\b",
    re.IGNORECASE | re.UNICODE,
)


# ── Các vi phạm tinh vi được phát hiện bởi rule cứng ─────────────────────────

def _hard_rule_detect(content: str, platforms: list[str]) -> list[dict]:
    """
    Phát hiện vi phạm bằng regex/keyword (không dùng LLM).
    Trả list violations: {rule_doc_id, quote, reason, severity}.
    """
    violations: list[dict] = []
    content_lower = content.lower()

    # 1. CCCD / giấy tờ tùy thân — red-line NĐ13 (GSX-LEGAL-001) + GSX-OP-002
    match_cccd_kw = _CCCD_KEYWORDS.search(content)
    if match_cccd_kw:
        violations.append({
            "rule_doc_id": "GSX-LEGAL-001",
            "quote": match_cccd_kw.group(0),
            "reason": (
                "Yêu cầu/đề cập đến CCCD/CMND là thu thập dữ liệu cá nhân nhạy cảm "
                "vi phạm NĐ13/2023 về Bảo vệ dữ liệu cá nhân (GSX-LEGAL-001) và "
                "quy định nội bộ GSX-OP-002. Đây là red-line tuyệt đối."
            ),
            "severity": "redline",
        })
    elif _CCCD_NUMBER_PATTERN.search(content):
        # Số 9/12 chữ số — cảnh báo, có thể là CCCD/CMND
        match_num = _CCCD_NUMBER_PATTERN.search(content)
        violations.append({
            "rule_doc_id": "GSX-LEGAL-001",
            "quote": match_num.group(0),
            "reason": (
                "Số 9–12 chữ số có thể là CCCD/CMND — cần xem lại. "
                "Nếu là số giấy tờ tùy thân: vi phạm NĐ13/2023 (GSX-LEGAL-001)."
            ),
            "severity": "major",
        })

    # 2. Cá độ / cờ bạc — red-line GSX-OP-002 4F
    match_gambling = _GAMBLING_KEYWORDS.search(content)
    if match_gambling:
        violations.append({
            "rule_doc_id": "GSX-OP-002",
            "quote": match_gambling.group(0),
            "reason": (
                "Quảng bá/đề cập cờ bạc, cá độ vi phạm GSX-OP-002 nhóm 4E/4F "
                "và policy nền tảng (GSX-PLAT-001/002). Đây là red-line tuyệt đối."
            ),
            "severity": "redline",
        })

    # 3. Bản đồ lãnh thổ — red-line GSX-OP-002 4A
    match_map = _MAP_KEYWORDS.search(content)
    if match_map:
        violations.append({
            "rule_doc_id": "GSX-OP-002",
            "quote": match_map.group(0),
            "reason": (
                "Đề cập bản đồ hình dạng lãnh thổ Việt Nam vi phạm GSX-OP-002 nhóm 4A. "
                "Không thể xác minh Hoàng Sa/Trường Sa chỉ bằng mắt thường. Red-line tuyệt đối."
            ),
            "severity": "redline",
        })

    # 4. Từ tuyệt đối — GSX-LEGAL-010 (Luật Quảng cáo Khoản 11 Điều 8)
    matches_sup = _SUPERLATIVE_PATTERN.findall(content)
    if matches_sup:
        # Kiểm tra whitelist: nếu nội dung chứa từ game whitelist → có thể là gameplay context
        has_game_context = any(kw in content_lower for kw in _GAME_WHITELIST)
        # Loại bỏ trùng lặp
        unique_sups = list(dict.fromkeys(m.strip() for m in matches_sup))

        # Xác định severity: commercial platform (meta/google/tiktok/store) → higher risk
        is_commercial_platform = bool(
            set(platforms) & {"meta", "google", "tiktok", "store"}
        )

        if not has_game_context or is_commercial_platform:
            severity = "major" if has_game_context else "major"
            # Nếu là commercial platform và không có game context → gần BLOCKED
            if is_commercial_platform and not has_game_context:
                severity = "major"  # sẽ escalate lên BLOCKED nếu kết hợp với vi phạm khác
            violations.append({
                "rule_doc_id": "GSX-LEGAL-010",
                "quote": ", ".join(unique_sups[:3]),
                "reason": (
                    f"Từ tuyệt đối '{', '.join(unique_sups[:3])}' trong nội dung {'thương mại ' if is_commercial_platform else ''}"
                    f"vi phạm Luật Quảng cáo 16/2012/QH13 Khoản 11 Điều 8 (GSX-LEGAL-010): "
                    f"cấm dùng từ 'nhất/duy nhất/tốt nhất/số một' hoặc tương tự mà không có "
                    f"tài liệu hợp pháp chứng minh. "
                    f"Lưu ý: NĐ87/2026 tăng chế tài (hiệu lực 05/07/2026 — chưa áp dụng tại thời điểm này)."
                ),
                "severity": "major",
            })
        else:
            # Game context, non-commercial platform → WARNING nhẹ
            violations.append({
                "rule_doc_id": "GSX-LEGAL-010",
                "quote": ", ".join(unique_sups[:3]),
                "reason": (
                    f"Từ tuyệt đối '{', '.join(unique_sups[:3])}' — có vẻ là mô tả gameplay/character "
                    f"nhưng vẫn cần xem xét (GSX-LEGAL-010). Nên thay bằng cụm từ không tuyệt đối."
                ),
                "severity": "minor",
            })

    # 5. Chửi tục — red-line GSX-OP-002 4I
    match_prof = _PROFANITY_PATTERN.search(content)
    if match_prof:
        violations.append({
            "rule_doc_id": "GSX-OP-002",
            "quote": match_prof.group(0),
            "reason": "Ngôn ngữ tục tĩu vi phạm GSX-OP-002 nhóm 4I. Red-line tuyệt đối.",
            "severity": "redline",
        })

    return violations


# ══════════════════════════════════════════════════════════════════════════════
# LLM-assisted DETECT + EXPLAIN (1 call)
# ══════════════════════════════════════════════════════════════════════════════

_DETECT_SYSTEM = """Bạn là AI Compliance Analyst chuyên về nội dung marketing ngành game tại Việt Nam.
Nhiệm vụ: Phân tích nội dung để phát hiện CÁC VI PHẠM TINH VI mà rule cứng chưa bắt được.

PHẠM VI PHÂN TÍCH — các nhóm vi phạm tinh vi:
- So sánh ngầm với đối thủ mang tính công kích (GSX-OP-002 4H)
- Claim không chứng minh được về tính năng/giải thưởng/xếp hạng (GSX-OP-013)
- Nội dung nhạy cảm tôn giáo/dân tộc tinh tế (GSX-OP-002 4B)
- Fan art/content bên thứ 3 chưa credit (GSX-OP-008)
- Thông tin cá nhân ẩn (SĐT trong chuỗi văn bản) (GSX-LEGAL-001)
- Vi phạm platform policy cụ thể theo platforms[] (GSX-PLAT-001 đến 005)
- Gacha/loot box được mô tả bằng ngôn từ đánh bạc hóa (GSX-OP-002 4E)
- Ngôn ngữ kích động, gây lo sợ bất hợp lý (sensational/alarmist)
- Claim "đầu tiên tại Việt Nam", "độc quyền" mà không có bằng chứng

KHÔNG phân tích lại các vi phạm sau (đã được rule cứng xử lý):
- CCCD/CMND đã phát hiện, cờ bạc/cá độ rõ ràng, bản đồ rõ, chửi tục rõ, từ tuyệt đối rõ

FORMAT TRẢ VỀ — JSON ARRAY THUẦN TÚY (không có markdown, không có text bên ngoài):
[
  {
    "rule_doc_id": "GSX-OP-002",
    "quote": "trích dẫn chính xác từ nội dung gốc",
    "reason": "giải thích rõ tại sao vi phạm, trích dẫn rule/luật cụ thể",
    "severity": "major|minor"
  }
]

Nếu không phát hiện vi phạm tinh vi: trả về []
Giới hạn: tối đa 5 vi phạm. Chỉ trả JSON, không có text khác."""


def _llm_detect(
    content: str,
    platforms: list[str],
    image_description: Optional[str],
    hard_violations: list[dict],
    chunks: list[dict],
) -> list[dict]:
    """Gọi LLM để detect vi phạm tinh vi (không thay thế hard rule detect)."""
    api_key = os.environ.get("LLM_API_KEY", "").strip()
    base_url = os.environ.get("LLM_BASE_URL", "https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1").strip()
    model = os.environ.get("LLM_MODEL", "").strip()

    if not api_key or not model:
        logger.warning("LLM chưa config — bỏ qua LLM detect")
        return []

    # Context KB từ chunks (top 5, ưu tiên platform policy + operating rules)
    platform_chunks = [c for c in chunks if c.get("content_layer") == "platform_policy"]
    op_chunks = [c for c in chunks if c.get("content_layer") in ("operating_rule", "legal_source")]
    selected = (platform_chunks + op_chunks)[:5]

    context_parts = []
    for c in selected:
        doc_id = c.get("doc_id", "")
        body = c.get("body", "")[:400]
        if doc_id and body:
            context_parts.append(f"[{doc_id}] {body}")
    context_text = "\n---\n".join(context_parts) if context_parts else "(Không có context KB)"

    # Tóm tắt hard violations để LLM biết KHÔNG phân tích lại
    hard_summary = ""
    if hard_violations:
        lines = [f"- {v['rule_doc_id']}: {v['quote'][:50]}" for v in hard_violations]
        hard_summary = "\n\nĐã phát hiện bởi rule cứng (KHÔNG phân tích lại):\n" + "\n".join(lines)

    image_note = f"\nMô tả hình ảnh kèm theo: {image_description}" if image_description else ""

    user_msg = f"""Nội dung cần kiểm duyệt:
{content}

Nền tảng đăng: {', '.join(platforms) if platforms else 'chưa xác định'}{image_note}
{hard_summary}

Context tài liệu áp dụng:
{context_text}

Phân tích và trả về các vi phạm TINH VI (nếu có) dưới dạng JSON array."""

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": _DETECT_SYSTEM},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.0,
            max_tokens=1000,
        )
        raw = (response.choices[0].message.content or "").strip()
        return _parse_violations_json(raw)

    except Exception as e:
        logger.warning(f"LLM detect thất bại: {e}")
        return []


def _parse_violations_json(raw: str) -> list[dict]:
    """Parse JSON violations từ LLM output, graceful fallback."""
    raw = raw.strip()
    # Strip markdown code blocks
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:])
        raw = raw.rstrip("`").strip()

    def _valid_violation(item: dict) -> bool:
        return (
            isinstance(item, dict)
            and item.get("rule_doc_id")
            and item.get("quote")
            and item.get("reason")
            and item.get("severity") in ("redline", "major", "minor")
        )

    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return [v for v in data if _valid_violation(v)]
    except Exception:
        pass

    match = re.search(r"\[[\s\S]*\]", raw)
    if match:
        try:
            data = json.loads(match.group())
            if isinstance(data, list):
                return [v for v in data if _valid_violation(v)]
        except Exception:
            pass

    return []


# ══════════════════════════════════════════════════════════════════════════════
# CONFIDENCE + EVIDENCE (Item 8.9 — transparency)
# Chỉ THÊM metadata, KHÔNG đổi verdict logic (verdict đọc `severity`).
# ══════════════════════════════════════════════════════════════════════════════

# Trích nguồn tĩnh cho các doc gốc hard-rule (fallback khi KB chunk không có doc_id).
_STATIC_EVIDENCE: dict[str, str] = {
    "GSX-LEGAL-001": (
        "NĐ13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân: CCCD/CMND, số giấy tờ tùy thân là "
        "dữ liệu cá nhân nhạy cảm — cấm thu thập, yêu cầu hoặc hiển thị khi chưa có cơ sở pháp lý."
    ),
    "GSX-OP-002": (
        "Quy tắc vận hành Game Studio X (GSX-OP-002) — red-line: cờ bạc/cá độ (4E/4F), "
        "bản đồ hình dạng lãnh thổ VN không rõ Hoàng Sa/Trường Sa (4A), nội dung nhạy cảm "
        "tôn giáo/dân tộc (4B), ngôn ngữ tục tĩu (4I)."
    ),
    "GSX-LEGAL-010": (
        "Luật Quảng cáo 16/2012/QH13, Khoản 11 Điều 8: cấm dùng từ 'nhất', 'duy nhất', "
        "'tốt nhất', 'số một' hoặc tương tự khi không có tài liệu hợp pháp chứng minh."
    ),
}


def _confidence_for(v: dict) -> str:
    """
    Heuristic mức độ chắc chắn theo layer phát hiện (cao | vừa | thấp).
      - source=rule  (hard-rule layer 1): red-line CCCD/bản đồ/cá độ/chửi tục = CAO;
        các match mềm hơn (số nghi CCCD, từ tuyệt đối) = VỪA.
      - source=vision (model đa phương thức): diễn giải ảnh → VỪA (nặng) / THẤP (nhẹ).
      - source=llm    (nuance phụ thuộc ngữ cảnh): VỪA (nặng) / THẤP (nhẹ).
    """
    source = v.get("source", "rule")
    sev = v.get("severity", "major")
    if source == "rule":
        return "cao" if sev == "redline" else "vừa"
    # llm + vision đều là model-based → không bao giờ "cao"
    return "vừa" if sev in ("redline", "major") else "thấp"


def _evidence_for(v: dict, chunks: list[dict]) -> str:
    """Trích đoạn luật/doc gốc giải thích vì sao vi phạm (ưu tiên KB chunk đúng doc_id)."""
    doc_id = v.get("rule_doc_id", "")
    if doc_id:
        for c in chunks:
            if c.get("doc_id") == doc_id:
                body = (c.get("body") or "").strip()
                if body:
                    return body[:320] + ("…" if len(body) > 320 else "")
    fallback = _STATIC_EVIDENCE.get(doc_id)
    if fallback:
        return fallback
    return (v.get("reason", "") or "")[:320]


def _enrich_confidence_evidence(violations: list[dict], chunks: list[dict]) -> list[dict]:
    """Gắn `confidence` + `evidence` cho từng vi phạm (idempotent, không đụng severity/verdict)."""
    for v in violations:
        if not v.get("confidence"):
            v["confidence"] = _confidence_for(v)
        if not v.get("evidence"):
            v["evidence"] = _evidence_for(v, chunks)
    return violations


# ══════════════════════════════════════════════════════════════════════════════
# VERDICT
# ══════════════════════════════════════════════════════════════════════════════

def _compute_verdict(violations: list[dict]) -> str:
    if not violations:
        return "SAFE"
    if any(v.get("severity") == "redline" for v in violations):
        return "BLOCKED"
    if any(v.get("severity") == "major" for v in violations):
        return "WARNING"
    return "WARNING"  # có minor violations → WARNING


# ══════════════════════════════════════════════════════════════════════════════
# REWRITE (bước 3)
# ══════════════════════════════════════════════════════════════════════════════

_REWRITE_AND_CHECKLIST_SYSTEM = """Bạn là copywriter & compliance analyst chuyên ngành game tại Việt Nam.
Nhiệm vụ: (1) Viết lại nội dung AN TOÀN, (2) Đề xuất thêm checklist action.

QUY TẮC REWRITE:
1. Giữ NGUYÊN ý nghĩa, mục đích, tone của nội dung gốc
2. Loại bỏ/thay thế TỪNG vi phạm được liệt kê
3. Thay từ tuyệt đối: "lớn nhất" → "một trong những giải lớn", "số 1" → "đông đảo người chơi yêu thích"
4. Nếu vi phạm là CCCD/CMND/bản đồ/cá độ (red-line không thể sửa): rewrite = "KHÔNG THỂ REWRITE: [lý do]"
5. Tiếng Việt, giọng marketing tự nhiên

FORMAT TRẢ VỀ — JSON THUẦN TÚY (không markdown):
{
  "rewrite": "bản rewrite an toàn hoặc 'KHÔNG THỂ REWRITE: [lý do]'",
  "extra_checklist": [
    {"item": "action cụ thể", "risk": "high|medium|low", "doc_id": "GSX-xxx"}
  ]
}
extra_checklist: tối đa 5 items, chỉ bổ sung những gì CHƯA có trong vi phạm đã liệt kê."""

_REWRITE_CANNOT_PREFIX = "⚠️ Không thể rewrite tự động — cần loại bỏ các yếu tố sau:\n"


def _llm_rewrite_and_checklist(
    content: str,
    violations: list[dict],
    platforms: list[str],
    chunks: list[dict],
) -> tuple[str, list[dict]]:
    """
    Gộp rewrite + extra checklist thành 1 LLM call để giảm latency.
    Returns (rewrite_text, extra_checklist_items).
    """
    # Phát hiện non-rewritable red-lines trước khi gọi LLM
    non_rewritable_keywords = ("cccd", "cmnd", "căn cước", "bản đồ", "cờ bạc", "cá độ")
    non_rewritable = [
        v for v in violations
        if v.get("severity") == "redline"
        and any(kw in v.get("reason", "").lower() for kw in non_rewritable_keywords)
    ]
    if non_rewritable:
        cannot_msg = _REWRITE_CANNOT_PREFIX + "\n".join(
            f"- '{v['quote']}': {v['reason'][:120]}" for v in non_rewritable
        )
        return cannot_msg, []

    api_key = os.environ.get("LLM_API_KEY", "").strip()
    base_url = os.environ.get("LLM_BASE_URL", "https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1").strip()
    model = os.environ.get("LLM_MODEL", "").strip()

    if not api_key or not model:
        return "(Rewrite không khả dụng — LLM chưa cấu hình)", []

    violations_list = "\n".join(
        f"- [{v.get('rule_doc_id', '')}] '{v.get('quote', '')}': {v.get('reason', '')[:120]}"
        for v in violations
    )

    # Context KB tóm tắt (1-2 chunks để tiết kiệm token)
    context_snippet = ""
    for c in chunks[:2]:
        doc_id = c.get("doc_id", "")
        body = c.get("body", "")[:200]
        if doc_id and body:
            context_snippet += f"[{doc_id}] {body}\n"

    user_msg = f"""Nội dung gốc:
{content}

Nền tảng: {', '.join(platforms) if platforms else 'chưa xác định'}

Vi phạm cần xử lý:
{violations_list}

Context tài liệu:
{context_snippet or '(không có)'}

Trả về JSON với rewrite an toàn và extra_checklist:"""

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": _REWRITE_AND_CHECKLIST_SYSTEM},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.15,
            max_tokens=900,
        )
        raw = (response.choices[0].message.content or "").strip()
        return _parse_rewrite_and_checklist(raw)

    except Exception as e:
        logger.warning(f"LLM rewrite+checklist thất bại: {e}")
        return f"(Rewrite thất bại: {e})", []


def _parse_rewrite_and_checklist(raw: str) -> tuple[str, list[dict]]:
    """Parse JSON output từ combined rewrite+checklist LLM call."""
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:]).rstrip("`").strip()

    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            rewrite = str(data.get("rewrite", "")).strip()
            extra = data.get("extra_checklist", [])
            if isinstance(extra, list):
                validated = [
                    {
                        "item": str(item.get("item", ""))[:300],
                        "risk": item.get("risk", "medium") if item.get("risk") in ("high", "medium", "low") else "medium",
                        "doc_id": str(item.get("doc_id", "GSX-OP-002"))[:30],
                    }
                    for item in extra if isinstance(item, dict) and item.get("item")
                ]
                return rewrite, validated
            return rewrite, []
    except Exception:
        pass

    # Fallback: tìm object trong text
    match = re.search(r"\{[\s\S]*\}", raw)
    if match:
        try:
            data = json.loads(match.group())
            if isinstance(data, dict):
                return str(data.get("rewrite", raw)).strip(), []
        except Exception:
            pass

    # Cuối cùng: coi toàn bộ text là rewrite
    return raw, []


# ══════════════════════════════════════════════════════════════════════════════
# PER-PLATFORM VERDICT
# ══════════════════════════════════════════════════════════════════════════════

# Platform-specific aggravating rules (tạo violation nặng hơn ở 1 platform)
_PLATFORM_EXTRA_CHECKS: dict[str, dict] = {
    "meta": {
        "doc_id": "GSX-PLAT-001",
        "strict_superlative": True,   # Meta từ chối superlative claim
        "strict_data_collection": True,
    },
    "tiktok": {
        "doc_id": "GSX-PLAT-002",
        "strict_superlative": True,
    },
    "google": {
        "doc_id": "GSX-PLAT-003",
        "strict_superlative": True,
    },
    "store": {
        "doc_id": "GSX-PLAT-004",
        "strict_superlative": True,
    },
    "website": {
        "doc_id": "GSX-TOOL-005",
        "strict_superlative": False,
        "check_formal_tone": True,
    },
    "group": {
        "doc_id": "GSX-TOOL-005",
        "strict_superlative": False,  # Group/Discord: casual — lỏng hơn
        "allow_casual": True,
    },
}


def _per_platform_verdict(
    violations: list[dict],
    platforms: list[str],
    content: str,
) -> dict[str, dict]:
    """Tính verdict + notes riêng cho từng platform."""
    result: dict[str, dict] = {}
    content_lower = content.lower()

    for platform in platforms:
        # Base: áp dụng toàn bộ violations
        platform_violations = list(violations)
        notes: list[str] = []

        pconf = _PLATFORM_EXTRA_CHECKS.get(platform, {})
        doc_id = pconf.get("doc_id", "GSX-TOOL-005")

        if platform == "group" and pconf.get("allow_casual"):
            # Group: loại bỏ minor violations (casual platform)
            platform_violations = [v for v in violations if v.get("severity") != "minor"]
            notes.append("Nền tảng Group/Discord: tiêu chuẩn casual — vi phạm minor được bỏ qua.")

        if pconf.get("strict_superlative") and any(
            v.get("rule_doc_id") == "GSX-LEGAL-010" for v in violations
        ):
            # Trên commercial platform: superlative escalate lên BLOCKED (nếu là quảng cáo)
            sup_viols = [v for v in platform_violations if v.get("rule_doc_id") == "GSX-LEGAL-010"]
            if sup_viols:
                notes.append(
                    f"Nền tảng {platform.upper()}: từ tuyệt đối trong quảng cáo bị từ chối "
                    f"tự động (GSX-PLAT-001/002/003 — {doc_id}). Cần sửa trước khi boost/ads."
                )
                # Escalate major → redline-level cho platform này
                for v in platform_violations:
                    if v.get("rule_doc_id") == "GSX-LEGAL-010":
                        v = dict(v)  # copy
                        v["severity"] = "redline"

        if platform == "website" and pconf.get("check_formal_tone"):
            notes.append("Website: yêu cầu formal — kiểm tra thêm chính tả, ngữ pháp, tone văn phong thương hiệu.")

        verdict = _compute_verdict(platform_violations)
        result[platform] = {
            "verdict": verdict,
            "notes": " | ".join(notes) if notes else f"Áp dụng tiêu chuẩn {platform.upper()}.",
        }

    return result


# ══════════════════════════════════════════════════════════════════════════════
# AI CONFIG (đọc từ vDB, fallback = strict)
# ══════════════════════════════════════════════════════════════════════════════

_ai_config_cache: Optional[dict] = None


def _get_ai_config() -> dict:
    """Đọc ai_config row 1 từ vDB. Cache in-process. Fallback = strict/default."""
    global _ai_config_cache
    if _ai_config_cache is not None:
        return _ai_config_cache

    default = {
        "detect_mode": "strict",
        "on_violation": "warn_explain_suggest",
        "explanation_style": "detailed",
    }

    try:
        import psycopg2  # type: ignore

        db_host = os.environ.get("DB_HOST", "").strip()
        db_port = os.environ.get("DB_PORT", "5432").strip()
        db_name = os.environ.get("DB_NAME", "fusionagent").strip()
        db_user = os.environ.get("DB_USER", "").strip()
        db_pass = os.environ.get("DB_PASSWORD", "").strip()
        db_ssl = os.environ.get("DB_SSLMODE", "disable").strip()

        if not db_host or not db_user:
            logger.info("ai_config: DB_HOST/USER chưa set — dùng default strict")
            _ai_config_cache = default
            return default

        conn = psycopg2.connect(
            host=db_host,
            port=int(db_port),
            dbname=db_name,
            user=db_user,
            password=db_pass,
            sslmode=db_ssl,
            connect_timeout=3,
        )
        cur = conn.cursor()
        cur.execute(
            "SELECT detect_mode, on_violation, explanation_style FROM ai_config WHERE id = 1 LIMIT 1"
        )
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            config = {
                "detect_mode": row[0] or default["detect_mode"],
                "on_violation": row[1] or default["on_violation"],
                "explanation_style": row[2] or default["explanation_style"],
            }
            _ai_config_cache = config
            logger.info(f"ai_config loaded từ vDB: {config}")
            return config

    except Exception as e:
        logger.warning(f"ai_config đọc DB thất bại — dùng default: {e}")

    _ai_config_cache = default
    return default


# ══════════════════════════════════════════════════════════════════════════════
# AUDIT LOG
# ══════════════════════════════════════════════════════════════════════════════

def _normalize_role(actor_role: str) -> str:
    """Map lowercase role header → DB enum value ('Admin'|'Mod'|'User')."""
    mapping = {"admin": "Admin", "mod": "Mod", "user": "User"}
    return mapping.get(actor_role.lower(), "User")


def _write_audit_log(
    actor_role: str,
    tenant_id: Optional[int],
    content: str,
    verdict: str,
    violations_count: int,
) -> None:
    input_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    summary = f"verdict={verdict} violations={violations_count} content_preview={content[:80]}"
    db_role = _normalize_role(actor_role)

    try:
        import psycopg2  # type: ignore

        db_host = os.environ.get("DB_HOST", "").strip()
        db_port = os.environ.get("DB_PORT", "5432").strip()
        db_name = os.environ.get("DB_NAME", "fusionagent").strip()
        db_user = os.environ.get("DB_USER", "").strip()
        db_pass = os.environ.get("DB_PASSWORD", "").strip()
        db_ssl = os.environ.get("DB_SSLMODE", "disable").strip()

        if not db_host or not db_user:
            logger.warning("audit_log: DB chưa set — bỏ qua")
            return

        conn = psycopg2.connect(
            host=db_host,
            port=int(db_port),
            dbname=db_name,
            user=db_user,
            password=db_pass,
            sslmode=db_ssl,
            connect_timeout=3,
        )
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO audit_log (actor_role, tenant_id, action, input_hash, verdict, summary)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (db_role, tenant_id, "scan", input_hash, verdict, summary),
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.debug("audit_log scan ghi OK")

    except Exception as e:
        logger.warning(f"audit_log scan thất bại (không ảnh hưởng response): {e}")


# ══════════════════════════════════════════════════════════════════════════════
# VISION DETECT — Gemma 4 31B (multimodal, MaaS)
# ══════════════════════════════════════════════════════════════════════════════

_VISION_MODEL = "google/gemma-4-31b-it"

_VISION_DETECT_SYSTEM = """Bạn là AI kiểm duyệt hình ảnh marketing game tại Việt Nam.
Nhiệm vụ: Phân tích hình ảnh để phát hiện nội dung vi phạm.

CÁC LOẠI VI PHẠM CẦN PHÁT HIỆN TRONG ẢNH:
- CCCD/CMND/giấy tờ tùy thân hiển thị trong ảnh (GSX-LEGAL-001) — red-line
- Bản đồ hình dạng lãnh thổ Việt Nam không rõ Hoàng Sa/Trường Sa (GSX-OP-002 4A) — red-line
- Nội dung cá độ/cờ bạc (GSX-OP-002 4E/4F) — red-line
- Hình ảnh bạo lực, máu me quá mức (GSX-OP-002 4C)
- Nội dung khiêu dâm, phản cảm (GSX-OP-002 4D)
- Text trong ảnh chứa từ tuyệt đối: "nhất", "số 1", "best" (GSX-LEGAL-010)
- Text trong ảnh chứa chửi tục (GSX-OP-002 4I)
- Logo/thương hiệu bên thứ 3 chưa được phép (GSX-OP-008)
- Nội dung nhạy cảm tôn giáo/dân tộc (GSX-OP-002 4B)

FORMAT TRẢ VỀ — JSON ARRAY THUẦN TÚY (không markdown):
[
  {
    "image_index": 0,
    "rule_doc_id": "GSX-OP-002",
    "quote": "mô tả ngắn phần vi phạm trong ảnh",
    "reason": "giải thích tại sao vi phạm",
    "severity": "redline|major|minor"
  }
]

Nếu không phát hiện vi phạm: trả về []
Giới hạn: tối đa 5 vi phạm mỗi ảnh. Chỉ trả JSON."""


def _vision_detect(images: list[str], platforms: list[str]) -> list[dict]:
    """Gọi Gemma 4 31B (vision) để phát hiện vi phạm trong ảnh."""
    api_key = os.environ.get("LLM_API_KEY", "").strip()
    base_url = os.environ.get("LLM_BASE_URL", "").strip()

    if not api_key or not images:
        return []

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url)

        all_violations: list[dict] = []

        for idx, img_b64 in enumerate(images[:5]):
            if not img_b64 or not img_b64.strip():
                continue

            img_url = img_b64 if img_b64.startswith("data:") else f"data:image/png;base64,{img_b64}"

            user_content = [
                {"type": "text", "text": (
                    f"Phân tích ảnh #{idx+1} (nền tảng đăng: {', '.join(platforms) if platforms else 'chưa xác định'}). "
                    "Phát hiện vi phạm nếu có. Trả về JSON array."
                )},
                {"type": "image_url", "image_url": {"url": img_url}},
            ]

            try:
                response = client.chat.completions.create(
                    model=_VISION_MODEL,
                    messages=[
                        {"role": "system", "content": _VISION_DETECT_SYSTEM},
                        {"role": "user", "content": user_content},
                    ],
                    temperature=0.0,
                    max_tokens=600,
                )
                raw = (response.choices[0].message.content or "").strip()
                violations = _parse_violations_json(raw)
                for v in violations:
                    v["image_index"] = idx
                    v["source"] = "vision"
                all_violations.extend(violations)
            except Exception as e:
                logger.warning(f"Vision detect ảnh #{idx+1} thất bại: {e}")
                continue

        return all_violations

    except Exception as e:
        logger.warning(f"Vision detect thất bại: {e}")
        return []


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def scan_content(
    content: str,
    platforms: list[str],
    tenant_id: Optional[int] = None,
    campaign_id: Optional[int] = None,
    image_description: Optional[str] = None,
    images: Optional[list[str]] = None,
    actor_role: str = "user",
) -> dict:
    """
    Content Scanner 4 bước.

    Returns:
    {
        "verdict": "SAFE|WARNING|BLOCKED",
        "violations": [{rule_doc_id, quote, reason, severity, source, confidence, evidence}],
        "rewrite": str | None,
        "checklist": [{item, risk, doc_id}],
        "per_platform": {platform: {verdict, notes}},
    }
    """
    from rag import retriever
    from tools.checklist import generate_checklist

    # ── Đọc ai_config (read-only) ─────────────────────────────────────────────
    # TODO: sử dụng detect_mode/on_violation khi có thêm behavior variant
    _ai_config = _get_ai_config()
    logger.info(f"Scanner ai_config: {_ai_config}")

    # ── Retrieve KB chunks liên quan ──────────────────────────────────────────
    query = content[:500]
    chunks = retriever.retrieve(
        query=query,
        tenant_id=tenant_id,
        campaign_id=campaign_id,
        platforms=platforms if platforms else None,
        top_k=6,  # giảm top_k để tăng tốc retrieve
    )
    logger.info(f"Retrieve: {len(chunks)} chunks cho scan")

    # ══ BƯỚC 1 — DETECT ══════════════════════════════════════════════════════

    # Layer 1: Rule cứng (instant, không cần LLM)
    hard_violations = _hard_rule_detect(content, platforms)

    # Nếu đã có red-line từ hard rule → BLOCKED confirmed, bỏ qua LLM detect
    # (tiết kiệm ~15s latency cho các trường hợp red-line rõ ràng)
    has_hard_redline = any(v.get("severity") == "redline" for v in hard_violations)

    if has_hard_redline:
        llm_violations = []
        logger.info("Skip LLM detect: red-line đã được xác nhận bởi rule cứng")
    else:
        # Layer 2: LLM-assisted detect nuance (chỉ khi không có red-line rõ ràng)
        llm_violations = _llm_detect(
            content=content,
            platforms=platforms,
            image_description=image_description,
            hard_violations=hard_violations,
            chunks=chunks,
        )

    # Layer 3: Vision detect (Gemma 4 31B — chỉ khi có ảnh)
    vision_violations: list[dict] = []
    if images:
        logger.info(f"Vision detect: {len(images)} ảnh")
        vision_violations = _vision_detect(images, platforms)
        logger.info(f"Vision detect: {len(vision_violations)} vi phạm từ ảnh")

    # Gắn nhãn nguồn phát hiện (vision đã tự set source="vision")
    for v in hard_violations:
        v.setdefault("source", "rule")
    for v in llm_violations:
        v.setdefault("source", "llm")

    # Hợp nhất: hard violations trước, LLM, rồi vision
    all_violations = hard_violations + llm_violations + vision_violations

    # Item 8.9: thêm confidence + evidence (transparency) — KHÔNG đổi verdict
    all_violations = _enrich_confidence_evidence(all_violations, chunks)

    # ══ BƯỚC 2 — EXPLAIN / VERDICT ═══════════════════════════════════════════
    verdict = _compute_verdict(all_violations)

    # ══ BƯỚC 3 + 4 — REWRITE & CHECKLIST (1 LLM call gộp) ════════════════════
    rewrite: Optional[str] = None
    extra_checklist_items: list[dict] = []

    if verdict in ("WARNING", "BLOCKED") and all_violations:
        rewrite, extra_checklist_items = _llm_rewrite_and_checklist(
            content, all_violations, platforms, chunks
        )

    checklist = generate_checklist({
        "content": content,
        "platforms": platforms,
        "violations": all_violations,
        "activity_description": None,
        "tenant_id": tenant_id,
        "chunks": chunks,
        "_extra_items": extra_checklist_items,  # pre-computed từ LLM gộp
    })

    # ── Per-platform verdict ──────────────────────────────────────────────────
    per_platform = _per_platform_verdict(all_violations, platforms, content) if platforms else {}

    # ── Audit log ─────────────────────────────────────────────────────────────
    _write_audit_log(actor_role, tenant_id, content, verdict, len(all_violations))

    return {
        "verdict": verdict,
        "violations": all_violations,
        "rewrite": rewrite,
        "checklist": checklist,
        "per_platform": per_platform,
        "images_scanned": len(images) if images else 0,
    }
