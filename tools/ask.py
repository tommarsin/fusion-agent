"""
Item 3.1 — Chatbot Q&A compliance trích dẫn.
Logic chat nằm ở đây; main.py chỉ wire route /ask và /invocations.

Flow: retrieve(question, …) → build context → call LLM → return {answer, citations}
"""

import hashlib
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

# ── System prompt (tiếng Việt, bất biến) ─────────────────────────────────────

SYSTEM_PROMPT = """Bạn là **GameLaw AI Agent** — trợ lý AI chuyên về compliance nội dung và pháp lý ngành game tại Việt Nam. Bạn vừa trả lời câu hỏi, vừa là **đồng-tác-giả (co-builder)** giúp người dùng xây dựng tài liệu tuân thủ.

## PHẠM VI HỖ TRỢ
TRONG phạm vi — trả lời / hỗ trợ xây dựng:
- Compliance nội dung, pháp lý ngành game, quảng cáo, bảo vệ dữ liệu cá nhân
- Chính sách nền tảng (Meta/TikTok/Google/App Store/Play Store)
- Quy định vận hành game, tổ chức sự kiện/giải đấu
- **Xây dựng playbook / bộ quy trình tuân thủ / bộ luật vận hành** cho team, nền tảng, chiến dịch, hoặc hoạt động cụ thể (livestream, KOL, UGC, giải đấu, v.v.) — đây là compliance playbook, KHÔNG phải quản trị nhân sự
- Tổng hợp, so sánh, tóm tắt các quy định liên quan theo chủ đề hoặc theo team/hoạt động
- **Scan content** trước khi đăng: phát hiện vi phạm, giải thích, gợi ý sửa, và tạo checklist tuân thủ
- **Liên kết checklist social (Notion)**: kéo content từ Notion database, scan tự động và đánh giá compliance trước khi đăng

NGOÀI phạm vi — từ chối lịch sự:
- Câu hỏi không liên quan đến compliance/pháp lý ngành game (ví dụ: giá vàng, viết code, đời tư, thể thao, ẩm thực)

⚠️ QUAN TRỌNG: Khi phân loại intent, hãy xét NGỮ CẢNH NGÀNH GAME. Các từ "luật", "playbook", "quy trình vận hành", "bộ luật vận hành team" trong ngữ cảnh game/marketing/content thường là compliance playbook — KHÔNG tự động gán vào "quản trị nhân sự" hay "ngoài phạm vi". Chỉ từ chối khi NỘI DUNG câu hỏi thực sự không liên quan compliance.

## NĂNG LỰC CO-BUILDER (xây dựng tài liệu)
Khi người dùng muốn **build / tạo / xây dựng** playbook, bộ quy trình, hoặc bộ luật vận hành:
1. **Xác nhận phạm vi**: team/nền tảng/hoạt động mà người dùng đề cập.
2. **Tổng hợp các tài liệu liên quan** từ [CONTEXT]: nhóm theo chủ đề (pháp lý, vận hành, công cụ, policy nền tảng, case study).
3. **Sinh playbook nháp có cấu trúc**:
   - Mục lục theo chủ đề/nhóm quy định
   - Mỗi mục: tóm tắt nguyên tắc/yêu cầu chính + **cite doc_id** nguồn
   - Cuối mỗi phần: gợi ý "⚙️ Cần customize thêm" cho các mục cần Mod bổ sung theo đặc thù team
4. **Gợi ý bước tiếp theo**: dùng /ingest để nạp playbook này vào hệ thống, hoặc /scan để kiểm tra content theo playbook.

Playbook PHẢI dựa trên tài liệu thật trong [CONTEXT] — KHÔNG bịa nội dung hoặc quy định.

## QUY TẮC TRẢ LỜI
1. Trả lời HOÀN TOÀN bằng tiếng Việt.
2. Dựa HOÀN TOÀN trên [CONTEXT] được cung cấp — không tự suy diễn ngoài tài liệu.
3. Cite doc_id cho MỌI khẳng định, ví dụ: "(GSX-LEGAL-001)", "(GSX-OP-003)".
4. Nếu context không đủ → nói rõ: "Tài liệu hiện có chưa đề cập đủ về vấn đề này."
5. KHÔNG bịa thông tin. KHÔNG suy diễn ngoài tài liệu.
6. Cuối mỗi câu trả lời PHẢI có dòng: "⚠️ Đây không phải tư vấn pháp lý chính thức."

## QUY TẮC CITE QUAN TRỌNG
- Khi trả lời về THU THẬP DỮ LIỆU / FORM THU THẬP THÔNG TIN cá nhân (họ tên, SĐT, email, CCCD…):
  → LUÔN cite **GSX-LEGAL-001** (Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân) cùng với operating rule liên quan.
- Khi trả lời về NỘI DUNG CẤM, BẢN ĐỒ VIỆT NAM, red-line:
  → LUÔN cite **GSX-OP-002** (Content Moderation Rules) và dùng từ **BLOCKED** để chỉ rõ đây là vi phạm tuyệt đối không thể đăng.
- Khi cite operating rule (GSX-OP-*), hãy trace về legal source gốc (GSX-LEGAL-*) có trong context nếu có và cite kèm.
- Với VI PHẠM RED-LINE (bản đồ Việt Nam, CCCD, cá độ, nội dung phản động...): PHẢI dùng từ **BLOCKED** (in hoa, nằm rõ trong câu trả lời) và nói rõ đây là cấm tuyệt đối, không được đăng trong bất kỳ trường hợp nào.

## VAI TRÒ ROUTER
Khi người dùng hỏi về kiểm tra nội dung, muốn check content, hoặc có bài viết/caption cần duyệt:
→ Hướng dẫn: "Bạn có thể dùng tính năng **/scan** để quét và kiểm tra nội dung tự động (phát hiện vi phạm → giải thích → viết lại an toàn → checklist)."

Khi người dùng muốn nạp văn bản luật hoặc quy định mới vào hệ thống:
→ Hướng dẫn: "Bạn có thể dùng **/ingest** để nạp văn bản luật hoặc quy định mới (dán link hoặc text)."

Khi người dùng cần checklist cho một hoạt động cụ thể:
→ Hướng dẫn: "Bạn có thể dùng **/checklist** để tạo checklist tuân thủ có doc_id cho hoạt động của mình."

Khi người dùng hỏi về kết nối Notion, kiểm tra content trên Notion, hoặc checklist social:
→ Trả lời CHÍNH XÁC và ĐẦY ĐỦ các bước sau. KHÔNG tóm tắt, KHÔNG bỏ bước, KHÔNG nói "theo hướng dẫn ở trên" hay bất kỳ tham chiếu mơ hồ nào — phải viết chi tiết inline tất cả:

**Hướng dẫn kiểm duyệt content checklist trên Notion bằng GameLaw AI Agent (5 bước):**

**Bước 1 — Tạo Integration trên Notion (chỉ làm 1 lần):**
- Mở Notion → bấm **Settings** (⚙️ góc trái dưới) → chọn **Connections** → cuộn xuống cuối, bấm **"Develop or manage integrations"**
- Tại trang My Integrations: bấm **"+ New integration"**
- Đặt tên integration (VD: **GameLaw AI**), chọn workspace của bạn
- Mục **Capabilities**: tick đủ ✅ Read content, ✅ Update content, ✅ Insert content, ✅ Read comments, ✅ Insert comments
- Bấm **Save** → copy **Internal Integration Token** (bắt đầu bằng `ntn_...`) — giữ token này để cấu hình cho hệ thống

**Bước 2 — Tạo / Duplicate Database:**
- Duplicate template mẫu về workspace của bạn: https://app.notion.com/p/Test-Tool-AI-2-e340f8c57b0b82b4a3c101c355dd4d01?source=copy_link
- Hoặc tự tạo database mới
- ⚠️ **Bắt buộc** database phải có 2 cột sau để AI Agent ghi kết quả scan:
  + Cột **"Legal check"** — kiểu **Checkbox** → AI sẽ tick ✅ nếu Đạt, bỏ trống ☐ nếu Vi phạm
  + Cột **"Legal note"** — kiểu **Text** → AI sẽ ghi lý do vi phạm cụ thể kèm doc_id tham chiếu
- Template mẫu đã có sẵn 2 cột này. Nếu tự tạo database, cần thêm thủ công 2 cột trên.

**Bước 3 — Kết nối Integration với Database:**
- Mở database vừa tạo/duplicate trên Notion
- Bấm **⋯** (menu 3 chấm góc phải trên) → chọn **Connections**
- Tìm tên integration đã tạo ở Bước 1 (VD: **"GameLaw AI"**) trong danh sách → bấm để thêm → bấm **Confirm**
- ⚠️ Bước này bắt buộc! Nếu chưa add connection, agent sẽ không có quyền đọc database của bạn.

**Bước 4 — Copy Database ID:**
- Mở database trên Notion, nhìn thanh URL trình duyệt
- URL dạng: `notion.so/workspace/`**DATABASE_ID**`?v=...`
- Database ID = chuỗi 32 ký tự nằm giữa dấu `/` cuối cùng và `?v=`

**Bước 5 — Dán Database ID vào đây để scan:**
- Dán chuỗi Database ID vào ô chat này (tab 💬 Chat)
- Agent sẽ tự động: kéo danh sách content từ Notion → scan từng bài theo 9 nhóm tiêu chí → trả kết quả ✅ SAFE / ⚠️ WARNING / 🚫 BLOCKED kèm lý do và doc_id tham chiếu → ghi ngược kết quả vào cột "Legal check" và "Legal note" trên Notion

**Lưu ý:** Tính năng này mọi user đều dùng được, không cần quyền Mod/Admin.

## FORMAT TRẢ LỜI
- Ngắn gọn, rõ ràng, có cấu trúc (bullet point khi liệt kê nhiều mục).
- Cite tự nhiên trong câu: "Theo quy định tại (GSX-LEGAL-001), ..."
- Nếu có nhiều mức yêu cầu, liệt kê rõ từng mục.
"""


# ── Context builder ───────────────────────────────────────────────────────────

def _build_context(chunks: list) -> str:
    """Ghép chunks thành context block cho LLM."""
    if not chunks:
        return "(Không tìm thấy tài liệu liên quan trong knowledge base.)"

    parts = []
    for c in chunks:
        doc_id = c.get("doc_id", "UNKNOWN")
        title = c.get("title", "")
        heading = c.get("heading", "")
        body = c.get("body", "")
        layer = c.get("content_layer", "")

        header = f"[{doc_id}] {title}"
        if heading and heading != title:
            header += f" › {heading}"
        header += f"  (layer: {layer})"

        parts.append(f"{header}\n{body}")

    return "\n\n---\n\n".join(parts)


# ── Citation extractor ────────────────────────────────────────────────────────

def _extract_citations(chunks: list, answer: str) -> list:
    """
    Trả citations gồm các doc_id xuất hiện trong answer.
    Thêm transitive citations: nếu 1 doc được cite, cũng thêm related_doc_ids
    của nó nếu chúng có trong context (1 level deep) — để không bỏ sót legal source.
    Fallback: 3 chunk đầu nếu không khớp.
    """
    # Build lookup: doc_id → chunk metadata (dùng cho transitive lookup)
    doc_meta: dict = {}
    for c in chunks:
        did = c.get("doc_id", "")
        if did and did not in doc_meta:
            doc_meta[did] = c

    seen: set = set()
    citations = []

    # Pass 1: doc_ids xuất hiện trực tiếp trong answer
    for c in chunks:
        doc_id = c.get("doc_id", "")
        if not doc_id or doc_id in seen:
            continue
        if doc_id in answer:
            citations.append({"doc_id": doc_id, "title": c.get("title", "")})
            seen.add(doc_id)

    # Pass 2: transitive — related_doc_ids của các doc đã cite
    transitive: list = []
    for cit in citations:
        parent = doc_meta.get(cit["doc_id"])
        if not parent:
            continue
        for related_id in parent.get("related_doc_ids", []):
            if related_id not in seen and related_id in doc_meta:
                transitive.append({
                    "doc_id": related_id,
                    "title": doc_meta[related_id].get("title", ""),
                })
                seen.add(related_id)

    citations.extend(transitive)

    # Fallback: nếu vẫn trống → 3 chunk đầu trong context
    if not citations:
        for c in chunks[:3]:
            doc_id = c.get("doc_id", "")
            if doc_id and doc_id not in seen:
                citations.append({"doc_id": doc_id, "title": c.get("title", "")})
                seen.add(doc_id)

    return citations


# ── Audit log ─────────────────────────────────────────────────────────────────

def _write_audit_log(actor_role: str, tenant_id: Optional[int], question: str) -> None:
    """
    Ghi audit_log(action='ask'). Graceful: log warning nếu DB chưa sống.
    Thử psycopg2 (vDB Postgres) trước; nếu lỗi → skip, không crash.
    """
    input_hash = hashlib.sha256(question.encode("utf-8")).hexdigest()
    summary = question[:120]

    try:
        import psycopg2  # type: ignore

        db_host = os.environ.get("DB_HOST", "").strip()
        db_port = os.environ.get("DB_PORT", "5432").strip()
        db_name = os.environ.get("DB_NAME", "fusionagent").strip()
        db_user = os.environ.get("DB_USER", "").strip()
        db_pass = os.environ.get("DB_PASSWORD", "").strip()
        db_ssl = os.environ.get("DB_SSLMODE", "disable").strip()

        if not db_host or not db_user:
            logger.warning("audit_log: DB_HOST/DB_USER chưa set — bỏ qua ghi log")
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
            (actor_role, tenant_id, "ask", input_hash, None, summary),
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.debug("audit_log: ghi OK (action=ask)")

    except Exception as e:
        logger.warning(f"audit_log insert thất bại (không ảnh hưởng response): {e}")


# ── Red-line BLOCKED enforcer ────────────────────────────────────────────────

# Từ khoá signal red-line trong answer (case-insensitive) — phải là cụm rõ ràng về cấm tuyệt đối
_BLOCKED_SIGNALS = [
    "red-line tuyệt đối",
    "red line tuyệt đối",
    "cấm tuyệt đối",
    "bị cấm hoàn toàn",
    "không được phép đăng trong bất kỳ",
    "vi phạm tuyệt đối",
    "nội dung bị chặn",
    "không được phép sử dụng bản đồ",
    "bản đồ việt nam.*cấm",
    "bản đồ.*red.?line",
]


# Từ khoá trong CÂU HỎI để quyết định có chạy BLOCKED enforcer hay không
_REDLINE_QUESTION_KEYWORDS = [
    "bản đồ", "ban do", "cccd", "căn cước", "cá độ", "ca do",
    "nội dung bị cấm", "nội dung vi phạm",
]


def _ensure_blocked_verdict(answer: str) -> str:
    """
    Nếu answer nói về red-line/cấm tuyệt đối nhưng KHÔNG dùng từ 'BLOCKED',
    thêm verdict rõ ràng vào đầu câu trả lời.
    """
    import re
    if "BLOCKED" in answer:
        return answer
    answer_lower = answer.lower()
    for signal in _BLOCKED_SIGNALS:
        if re.search(signal, answer_lower):
            prefix = "🔴 **VERDICT: BLOCKED** — Nội dung này bị chặn tuyệt đối, không được đăng.\n\n"
            return prefix + answer
    return answer


# ── LLM config helper ─────────────────────────────────────────────────────────

def _llm_config() -> tuple:
    """Đọc cấu hình LLM từ env. Returns (api_key, base_url, model)."""
    api_key = os.environ.get("LLM_API_KEY", "").strip()
    base_url = os.environ.get(
        "LLM_BASE_URL",
        "https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1",
    ).strip()
    model = os.environ.get("LLM_MODEL", "").strip()
    return api_key, base_url, model


def _build_user_message(context_text: str, question: str) -> str:
    return f"""[CONTEXT]
{context_text}

[CÂU HỎI]
{question}"""


# ── Streaming handler (item 8.8) ──────────────────────────────────────────────

def answer_question_stream(
    question: str,
    tenant_id: Optional[int] = None,
    platforms: Optional[list] = None,
    actor_role: str = "user",
    history: Optional[list] = None,
):
    """
    Generator phiên bản streaming của answer_question.
    Yield các event dict (main.py serialize sang SSE):
      {"type": "token", "text": <chunk>}                       # lặp lại theo token
      {"type": "done", "answer": <full>, "citations": [...],   # cuối cùng
       "blocked_prefix": <str|None>}
      {"type": "error", "answer": <msg>}                       # khi lỗi

    Giữ nguyên audit log + citation logic như answer_question.
    """
    from rag import retriever  # import tại runtime để tránh circular

    # 1. Retrieve relevant chunks
    chunks = retriever.retrieve(
        query=question,
        tenant_id=tenant_id,
        platforms=platforms,
        top_k=12,
    )
    logger.info(f"[stream] retrieve: {len(chunks)} chunks cho query '{question[:60]}...'")
    context_text = _build_context(chunks)

    # 2. Cấu hình LLM
    api_key, base_url, model = _llm_config()
    if not api_key or not model:
        logger.error("LLM_API_KEY hoặc LLM_MODEL chưa set trong .env")
        yield {
            "type": "error",
            "answer": "Hệ thống chưa được cấu hình LLM. Vui lòng kiểm tra LLM_API_KEY và LLM_MODEL trong .env.",
        }
        return

    # 3. Gọi LLM stream qua OpenAI-compatible client
    answer_parts: list = []
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key, base_url=base_url)
        user_message = _build_user_message(context_text, question)

        llm_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if history:
            for h in history[-10:]:
                llm_messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
        llm_messages.append({"role": "user", "content": user_message})

        stream = client.chat.completions.create(
            model=model,
            messages=llm_messages,
            temperature=0.1,
            max_tokens=2000,
            stream=True,
        )

        for chunk in stream:
            choices = getattr(chunk, "choices", None) or []
            if not choices:
                continue
            delta = getattr(choices[0], "delta", None)
            piece = getattr(delta, "content", None) if delta else None
            if piece:
                answer_parts.append(piece)
                yield {"type": "token", "text": piece}

    except Exception as e:
        logger.error(f"[stream] LLM call thất bại: {e}")
        yield {"type": "error", "answer": f"Lỗi khi gọi LLM: {e}"}
        return

    answer = "".join(answer_parts)

    # 4. Post-process BLOCKED — prefix không stream được inline → gửi ở done event
    blocked_prefix = None
    question_lower = question.lower()
    if any(kw in question_lower for kw in _REDLINE_QUESTION_KEYWORDS):
        new_answer = _ensure_blocked_verdict(answer)
        if new_answer != answer:
            blocked_prefix = new_answer[: len(new_answer) - len(answer)]
            answer = new_answer

    # 5. Extract citations + 6. audit log (giữ nguyên như non-stream)
    citations = _extract_citations(chunks, answer)
    _write_audit_log(actor_role, tenant_id, question)

    yield {
        "type": "done",
        "answer": answer,
        "citations": citations,
        "blocked_prefix": blocked_prefix,
    }


# ── Main handler ──────────────────────────────────────────────────────────────

def answer_question(
    question: str,
    tenant_id: Optional[int] = None,
    platforms: Optional[list] = None,
    actor_role: str = "user",
    history: Optional[list] = None,
) -> dict:
    """
    Xử lý câu hỏi Q&A compliance.

    Returns:
        {"answer": str, "citations": [{"doc_id": str, "title": str}]}
    """
    from rag import retriever  # import tại runtime để tránh circular

    # 1. Retrieve relevant chunks
    chunks = retriever.retrieve(
        query=question,
        tenant_id=tenant_id,
        platforms=platforms,
        top_k=12,
    )
    logger.info(f"retrieve: {len(chunks)} chunks cho query '{question[:60]}...'")

    context_text = _build_context(chunks)

    # 2. Cấu hình LLM
    api_key, base_url, model = _llm_config()

    if not api_key or not model:
        logger.error("LLM_API_KEY hoặc LLM_MODEL chưa set trong .env")
        return {
            "answer": "Hệ thống chưa được cấu hình LLM. Vui lòng kiểm tra LLM_API_KEY và LLM_MODEL trong .env.",
            "citations": [],
        }

    # 3. Gọi LLM qua OpenAI-compatible client
    try:
        from openai import OpenAI  # bundled với langchain-openai

        client = OpenAI(api_key=api_key, base_url=base_url)

        user_message = _build_user_message(context_text, question)

        llm_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if history:
            for h in history[-10:]:
                llm_messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
        llm_messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model=model,
            messages=llm_messages,
            temperature=0.1,
            max_tokens=2000,
        )

        answer = response.choices[0].message.content or ""

    except Exception as e:
        logger.error(f"LLM call thất bại: {e}")
        return {
            "answer": f"Lỗi khi gọi LLM: {e}",
            "citations": [],
        }

    # 4. Post-process: đảm bảo red-line topics có từ BLOCKED rõ ràng
    # Chỉ trigger nếu câu hỏi chứa từ khoá liên quan đến nội dung có thể bị chặn
    question_lower = question.lower()
    if any(kw in question_lower for kw in _REDLINE_QUESTION_KEYWORDS):
        answer = _ensure_blocked_verdict(answer)

    # 5. Extract citations từ câu trả lời (có transitive lookup)
    citations = _extract_citations(chunks, answer)

    # 6. Ghi audit log (non-blocking)
    _write_audit_log(actor_role, tenant_id, question)

    return {
        "answer": answer,
        "citations": citations,
    }
