"""
Item 3.2 / 3.4 — Shared checklist generator.
Dùng chung bởi scanner (bước 4) và POST /checklist.

generate_checklist(context) → list[{item, risk, doc_id}]

context = {
    "content": str,
    "platforms": list[str],
    "violations": list[dict],      # từ scanner step EXPLAIN
    "activity_description": str,   # mô tả hoạt động (cho /checklist endpoint)
    "tenant_id": int | None,
    "chunks": list[dict],          # retrieved KB chunks
}
"""

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

# ── Checklist cứng theo platform ─────────────────────────────────────────────
# Mỗi entry: {item, risk, doc_id, platforms} — platforms=[] nghĩa là mọi nền tảng

_PLATFORM_CHECKLIST: list[dict] = [
    # ── Mọi nền tảng ─────────────────────────────────────────────────────────
    {
        "item": "Kiểm tra không có bản đồ hình dạng lãnh thổ Việt Nam (kể cả infographic địa lý)",
        "risk": "high",
        "doc_id": "GSX-OP-002",
        "platforms": [],
    },
    {
        "item": "Kiểm tra không yêu cầu hoặc thu thập CCCD/CMND/số căn cước công dân",
        "risk": "high",
        "doc_id": "GSX-LEGAL-001",
        "platforms": [],
    },
    {
        "item": "Kiểm tra không có nội dung quảng bá cờ bạc, cá độ, casino, kèo nhà cái",
        "risk": "high",
        "doc_id": "GSX-OP-002",
        "platforms": [],
    },
    {
        "item": "Kiểm tra từ ngữ tuyệt đối (nhất/duy nhất/tốt nhất/số một): nếu có → cần tài liệu chứng minh hợp pháp hoặc thay bằng cụm từ khác",
        "risk": "high",
        "doc_id": "GSX-LEGAL-010",
        "platforms": [],
    },
    {
        "item": "Kiểm tra không có chửi tục, kể cả viết tắt cách quãng (c.ú.t, đ.m, v~l)",
        "risk": "high",
        "doc_id": "GSX-OP-002",
        "platforms": [],
    },
    {
        "item": "Kiểm tra ngôn ngữ không xúc phạm trí tuệ người khác (não cá vàng, IQ âm, óc lợn)",
        "risk": "medium",
        "doc_id": "GSX-OP-002",
        "platforms": [],
    },
    {
        "item": "Kiểm tra không vi phạm bản quyền (nhạc, ảnh, watermark bên thứ 3 không phép)",
        "risk": "high",
        "doc_id": "GSX-OP-008",
        "platforms": [],
    },
    {
        "item": "Xác nhận nội dung không quảng bá boost rank, cày thuê, mua bán tài khoản game",
        "risk": "high",
        "doc_id": "GSX-OP-002",
        "platforms": [],
    },
    # ── Meta (Fanpage / Facebook Ads) ─────────────────────────────────────────
    {
        "item": "Meta Ads: Kiểm tra không có claim 'số 1', 'tốt nhất', misleading về kết quả game — Meta từ chối quảng cáo có superlative không chứng minh được",
        "risk": "high",
        "doc_id": "GSX-PLAT-001",
        "platforms": ["meta"],
    },
    {
        "item": "Meta Ads: Không thu thập dữ liệu cá nhân qua form nếu thiếu Privacy Policy rõ ràng (Lead Ads phải có)",
        "risk": "high",
        "doc_id": "GSX-PLAT-001",
        "platforms": ["meta"],
    },
    {
        "item": "Meta: Không có ngôn ngữ sensational / alarmist (KHỦNG, SỐC, kích động)",
        "risk": "medium",
        "doc_id": "GSX-PLAT-001",
        "platforms": ["meta"],
    },
    # ── TikTok ────────────────────────────────────────────────────────────────
    {
        "item": "TikTok: Branded content (hợp tác KOL/brand) phải dùng tính năng Branded Content Toggle trong app",
        "risk": "high",
        "doc_id": "GSX-PLAT-002",
        "platforms": ["tiktok"],
    },
    {
        "item": "TikTok: Không dùng nhạc trending bản quyền trong TikTok Ads (chỉ dùng Commercial Music Library)",
        "risk": "high",
        "doc_id": "GSX-PLAT-002",
        "platforms": ["tiktok"],
    },
    {
        "item": "TikTok: Không mô tả gameplay misleading (kết quả thực tế không đạt được trong game)",
        "risk": "medium",
        "doc_id": "GSX-PLAT-002",
        "platforms": ["tiktok"],
    },
    # ── Google ────────────────────────────────────────────────────────────────
    {
        "item": "Google Ads: Destination URL phải hoạt động, landing page khớp nội dung quảng cáo",
        "risk": "medium",
        "doc_id": "GSX-PLAT-003",
        "platforms": ["google"],
    },
    {
        "item": "Google Ads: Không có misleading claims về tính năng game, giải thưởng, xếp hạng",
        "risk": "high",
        "doc_id": "GSX-PLAT-003",
        "platforms": ["google"],
    },
    # ── App Store ─────────────────────────────────────────────────────────────
    {
        "item": "App Store: Nếu có loot box / gacha → phải khai báo tỷ lệ trúng thưởng rõ ràng (Apple guideline 3.1.1b)",
        "risk": "high",
        "doc_id": "GSX-PLAT-004",
        "platforms": ["store"],
    },
    {
        "item": "App Store: Không có keywords gây hiểu lầm trong metadata (title, subtitle, keywords field)",
        "risk": "medium",
        "doc_id": "GSX-PLAT-004",
        "platforms": ["store"],
    },
    # ── Website (Formal tier) ─────────────────────────────────────────────────
    {
        "item": "Website: Kiểm tra chính tả và ngữ pháp toàn bộ nội dung trước khi đăng",
        "risk": "low",
        "doc_id": "GSX-TOOL-005",
        "platforms": ["website"],
    },
    {
        "item": "Website: Kiểm tra tone văn phong phù hợp thương hiệu, không dùng slang informal",
        "risk": "low",
        "doc_id": "GSX-TOOL-005",
        "platforms": ["website"],
    },
    {
        "item": "Website: Kiểm tra mọi thông tin (ngày, giải thưởng, điều kiện) chính xác và đã được duyệt",
        "risk": "medium",
        "doc_id": "GSX-TOOL-005",
        "platforms": ["website"],
    },
]


def _build_violation_items(violations: list[dict]) -> list[dict]:
    """Chuyển violation thành checklist action item."""
    items = []
    for v in violations:
        severity = v.get("severity", "minor")
        rule_doc_id = v.get("rule_doc_id", "GSX-OP-002")
        quote = v.get("quote", "")
        reason = v.get("reason", "")

        risk = "high" if severity == "redline" else ("high" if severity == "major" else "medium")
        item_text = f"XỬ LÝ VI PHẠM: Loại bỏ hoặc sửa cụm '{quote}' — {reason}"
        items.append({"item": item_text, "risk": risk, "doc_id": rule_doc_id})
    return items


def generate_checklist(context: dict) -> list[dict]:
    """
    Tạo checklist pre-publish từ context.

    context keys:
        content: str
        platforms: list[str]
        violations: list[dict]        # [{rule_doc_id, quote, reason, severity}]
        activity_description: str     # mô tả hoạt động (POST /checklist endpoint)
        tenant_id: int | None
        chunks: list[dict]            # retrieved KB chunks (dùng cho LLM expansion)

    Returns list[{"item": str, "risk": "high|medium|low", "doc_id": str}]
    """
    platforms = context.get("platforms") or []
    violations = context.get("violations") or []
    content = context.get("content") or ""
    activity_description = context.get("activity_description") or ""
    chunks = context.get("chunks") or []

    # 1. Items từ vi phạm đã phát hiện (ưu tiên đầu)
    result: list[dict] = _build_violation_items(violations)
    seen_items: set[str] = {item["item"] for item in result}

    # 2. Checklist cứng theo platform
    for entry in _PLATFORM_CHECKLIST:
        entry_platforms = entry.get("platforms") or []
        # Thêm nếu: áp dụng mọi nền tảng (platforms=[]) hoặc khớp ít nhất 1 platform được request
        if not entry_platforms or bool(set(entry_platforms) & set(platforms)):
            if entry["item"] not in seen_items:
                result.append({
                    "item": entry["item"],
                    "risk": entry["risk"],
                    "doc_id": entry["doc_id"],
                })
                seen_items.add(entry["item"])

    # 3. Extra items từ scanner's merged LLM call (nếu có) hoặc LLM expansion riêng
    extra_items = context.get("_extra_items")
    if extra_items is None:
        # Chỉ gọi LLM riêng khi không có pre-computed items (vd: POST /checklist endpoint)
        extra_items = _llm_expand_checklist(content, platforms, violations, activity_description, chunks)

    for item in extra_items:
        if item.get("item") and item["item"] not in seen_items:
            result.append(item)
            seen_items.add(item["item"])

    return result


# ── LLM expansion ─────────────────────────────────────────────────────────────

_CHECKLIST_SYSTEM = """Bạn là chuyên gia compliance nội dung ngành game tại Việt Nam.
Nhiệm vụ: Tạo thêm checklist hành động CỤ THỂ mà team marketing cần làm TRƯỚC KHI ĐĂNG nội dung này.

YÊU CẦU:
- Trả về JSON array: [{"item": "mô tả hành động cụ thể", "risk": "high|medium|low", "doc_id": "GSX-xxx hoặc GSX-PLAT-xxx"}]
- Tối đa 5 items bổ sung (không lặp lại items đã có)
- Mỗi item phải CỤ THỂ, có thể thực hiện được
- doc_id phải là doc_id thực có trong context (GSX-LEGAL-001, GSX-OP-002, GSX-OP-013, GSX-PLAT-001/002/003, GSX-LEGAL-010, v.v.)
- Ưu tiên các vi phạm tiềm ẩn CHƯA được phát hiện bởi rule cứng
- Nếu không có gì thêm: trả về []
- Trả về JSON thuần túy, không markdown code block"""


def _llm_expand_checklist(
    content: str,
    platforms: list[str],
    violations: list[dict],
    activity_description: str,
    chunks: list[dict],
) -> list[dict]:
    """Gọi LLM để bổ sung checklist items từ context."""
    api_key = os.environ.get("LLM_API_KEY", "").strip()
    base_url = os.environ.get("LLM_BASE_URL", "https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1").strip()
    model = os.environ.get("LLM_MODEL", "").strip()

    if not api_key or not model:
        logger.warning("LLM chưa config — bỏ qua LLM checklist expansion")
        return []

    # Build context từ KB chunks (tối đa 3 chunk để tiết kiệm token)
    context_snippets = []
    for c in chunks[:3]:
        doc_id = c.get("doc_id", "")
        body = c.get("body", "")[:300]
        if doc_id and body:
            context_snippets.append(f"[{doc_id}] {body}")
    context_text = "\n---\n".join(context_snippets) if context_snippets else "(Không có context KB)"

    violations_summary = ""
    if violations:
        v_lines = [f"- {v.get('rule_doc_id', '')}: {v.get('reason', '')[:100]}" for v in violations]
        violations_summary = "Vi phạm đã phát hiện:\n" + "\n".join(v_lines)
    else:
        violations_summary = "Không có vi phạm được phát hiện."

    user_msg = f"""Nội dung cần đăng:
{content[:800]}

Nền tảng: {', '.join(platforms) if platforms else 'chưa xác định'}
{"Mô tả hoạt động: " + activity_description if activity_description else ""}

{violations_summary}

Context tài liệu:
{context_text}

Trả về thêm checklist actions (tối đa 5 items) cần thực hiện TRƯỚC KHI ĐĂNG nội dung này."""

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": _CHECKLIST_SYSTEM},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.1,
            max_tokens=600,
        )
        raw = (response.choices[0].message.content or "").strip()
        return _parse_checklist_json(raw)

    except Exception as e:
        logger.warning(f"LLM checklist expansion thất bại: {e}")
        return []


def _parse_checklist_json(raw: str) -> list[dict]:
    """Parse JSON array từ LLM output, graceful fallback."""
    import json, re

    # Strip markdown code blocks
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:])
        raw = raw.rstrip("`").strip()

    # Try direct parse
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return [
                {
                    "item": str(item.get("item", ""))[:300],
                    "risk": item.get("risk", "medium") if item.get("risk") in ("high", "medium", "low") else "medium",
                    "doc_id": str(item.get("doc_id", "GSX-OP-002"))[:30],
                }
                for item in data if isinstance(item, dict) and item.get("item")
            ]
    except Exception:
        pass

    # Try extract array
    match = re.search(r"\[[\s\S]*\]", raw)
    if match:
        try:
            data = json.loads(match.group())
            if isinstance(data, list):
                return [
                    {
                        "item": str(item.get("item", ""))[:300],
                        "risk": item.get("risk", "medium") if item.get("risk") in ("high", "medium", "low") else "medium",
                        "doc_id": str(item.get("doc_id", "GSX-OP-002"))[:30],
                    }
                    for item in data if isinstance(item, dict) and item.get("item")
                ]
        except Exception:
            pass

    return []
