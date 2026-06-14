"""
Fusion Agent — Game Content Compliance AI System
FastAPI server, binds 0.0.0.0:8080 (AgentBase platform requirement).

Routes implemented here are stubs (HTTP 501). Logic filled in per WS3 items:
  3.1 → /ask   3.2 → /scan   3.3 → /ingest + /approve
  3.4 → /checklist   3.5 → role gate + /audit
  4.1 → /ui (static demo UI) + /submissions (list pending)
"""

import json
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
import uvicorn

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

KB_DIR = str(Path(__file__).parent / "knowledge_base")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup: load KB + build BM25 index ──────────────────────────────────
    from rag import loader, retriever

    retriever.set_kb_dir(KB_DIR)

    # tools/ingest.py added by item 3.3 — graceful if not yet present
    try:
        from tools import ingest as ingest_tool
        ingest_tool.set_kb_dir(KB_DIR)
    except ImportError:
        logger.info("tools.ingest not found — /ingest và /approve stubs (item 3.3 pending)")

    # Ensure audit_action_enum has 'checklist' (item 3.5)
    try:
        from db.store import ensure_checklist_action
        ensure_checklist_action()
    except Exception as e:
        logger.debug(f"ensure_checklist_action startup (non-fatal): {e}")

    chunks = loader.load_all_chunks(KB_DIR)
    retriever.build_index(chunks)
    logger.info("RAG layer sẵn sàng.")
    yield
    # ── Shutdown ──────────────────────────────────────────────────────────────


app = FastAPI(
    title="Fusion Agent — Game Content Compliance AI System",
    lifespan=lifespan,
)

# ── CORS (item 4.1 — POC, allow all origins) ─────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Role gate + audit middleware (item 3.5) ───────────────────────────────────
try:
    from tools.role_gate import RoleGateMiddleware
    app.add_middleware(RoleGateMiddleware)
    logger.info("RoleGateMiddleware đã đăng ký.")
except ImportError:
    logger.warning("tools.role_gate không tìm thấy — role gate bỏ qua.")


# ── Platform hard requirement ─────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok"}


# ── Demo UI (item 4.1) ────────────────────────────────────────────────────────
_UI_FILE = Path(__file__).parent / "frontend" / "index.html"


@app.get("/ui", include_in_schema=False)
async def serve_ui():
    """Serve demo UI — không ghi audit, không gate role."""
    if not _UI_FILE.exists():
        return JSONResponse(status_code=404, content={"error": "UI file not found. Run item 4.1 setup."})
    return FileResponse(str(_UI_FILE), media_type="text/html")


# ── Submissions list (item 4.1 — Mod+ xem pending để duyệt) ──────────────────
@app.get("/submissions")
async def list_submissions_route(request: Request):
    """
    GET /submissions — liệt kê submissions (Mod+).
    Role gate enforced by RoleGateMiddleware (min rank Mod).
    Query param: status (pending|approved|rejected|all), default pending.
    """
    from db.store import list_submissions

    status_param = request.query_params.get("status", "pending").strip().lower()
    if status_param == "all":
        status_param = None
    elif status_param not in ("pending", "approved", "rejected"):
        status_param = "pending"

    submissions = list_submissions(status=status_param)
    return JSONResponse(status_code=200, content={"submissions": submissions, "count": len(submissions)})


# ── /ask + /invocations (item 3.1) ───────────────────────────────────────────

async def _handle_ask(request: Request):
    """
    Shared handler cho /ask và /invocations alias.

    Mặc định trả JSON (non-stream) — giữ tương thích cho client cũ (vd Notion 5.1).
    Nếu body có "stream": true (hoặc query ?stream=1) → trả SSE token streaming (item 8.8).
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=422, content={"error": "invalid JSON body"})

    question = (body.get("question") or "").strip()
    if not question:
        return JSONResponse(status_code=422, content={"error": "'question' is required"})

    tenant_id = body.get("tenant_id")  # int | None
    platforms = body.get("platforms")  # list[str] | None
    actor_role = request.headers.get("X-Role", "user").lower()

    want_stream = bool(body.get("stream")) or (
        request.query_params.get("stream", "").lower() in ("1", "true", "yes")
    )

    if want_stream:
        from tools.ask import answer_question_stream

        def event_gen():
            try:
                for ev in answer_question_stream(
                    question=question,
                    tenant_id=tenant_id,
                    platforms=platforms,
                    actor_role=actor_role,
                ):
                    yield "data: " + json.dumps(ev, ensure_ascii=False) + "\n\n"
            except Exception as e:  # phòng hờ — generator không nên raise
                logger.error(f"/ask stream error: {e}")
                yield "data: " + json.dumps(
                    {"type": "error", "answer": f"Lỗi stream: {e}"}, ensure_ascii=False
                ) + "\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(
            event_gen(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",  # tắt buffering của reverse proxy (nginx)
                "Connection": "keep-alive",
            },
        )

    from tools.ask import answer_question

    result = answer_question(
        question=question,
        tenant_id=tenant_id,
        platforms=platforms,
        actor_role=actor_role,
    )
    return JSONResponse(status_code=200, content=result)


@app.post("/ask")
async def ask(request: Request):
    return await _handle_ask(request)


@app.post("/invocations")
async def invocations(request: Request):
    """AgentBase SDK convention alias → delegates to /ask handler."""
    return await _handle_ask(request)


@app.post("/scan")
async def scan(request: Request):
    """
    POST /scan — Content Scanner 4 bước (Item 3.2).

    Body JSON:
      {
        "content": "...",
        "platforms": ["meta", "tiktok", "google", "store", "website", "group"],
        "tenant_id": null,
        "campaign_id": null,
        "image_description": null
      }
    Header: X-Role (user | mod | admin)
    """
    from tools.scanner import scan_content

    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=422, content={"error": "invalid JSON body"})

    content = (body.get("content") or "").strip()
    if not content:
        return JSONResponse(status_code=422, content={"error": "'content' is required"})

    platforms = body.get("platforms") or []
    if isinstance(platforms, str):
        platforms = [platforms]

    # Validate platform values
    valid_platforms = {"meta", "tiktok", "google", "store", "website", "group"}
    platforms = [p.lower().strip() for p in platforms if p.lower().strip() in valid_platforms]

    tenant_id = body.get("tenant_id")
    campaign_id = body.get("campaign_id")
    image_description = body.get("image_description")
    images = body.get("images")
    if isinstance(images, list):
        images = [img for img in images if isinstance(img, str) and len(img) > 100][:5]
    else:
        images = None
    actor_role = request.headers.get("X-Role", "user").lower()

    result = scan_content(
        content=content,
        platforms=platforms,
        tenant_id=tenant_id,
        campaign_id=campaign_id,
        image_description=image_description,
        images=images,
        actor_role=actor_role,
    )
    return JSONResponse(status_code=200, content=result)


@app.post("/ingest")
async def ingest(request: Request):
    """
    POST /ingest — Authoring Engine + Web Fetch (Item 3.3).

    Body JSON:
      {
        "source": "<URL hoặc text thô>",
        "scope": "core|tenant|campaign",
        "tenant_id": null,
        "campaign_id": null,
        "note": null,
        "related_core_doc_id": null   -- khi rule tenant siết 1 core rule (siết-only)
      }
    Header: X-Role (Admin | Mod | User)

    Routing:
      - User          → 403
      - Mod + core    → submission pending (Admin duyệt qua /approve)
      - Mod + tenant  → rule live ngay + reindex
      - Admin         → rule live ngay (bất kỳ scope) + reindex
    """
    from tools.ingest import handle_ingest

    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=422, content={"error": "invalid JSON body"})

    source = (body.get("source") or "").strip()
    if not source:
        return JSONResponse(status_code=422, content={"error": "'source' là bắt buộc (URL hoặc text)"})

    scope = (body.get("scope") or "core").strip().lower()
    tenant_id = body.get("tenant_id")
    campaign_id = body.get("campaign_id")
    note = body.get("note")
    related_core_doc_id = body.get("related_core_doc_id")
    actor_role = request.headers.get("X-Role", "User")

    status_code, result = handle_ingest(
        source=source,
        scope=scope,
        actor_role=actor_role,
        tenant_id=tenant_id,
        campaign_id=campaign_id,
        note=note,
        related_core_doc_id=related_core_doc_id,
    )
    return JSONResponse(status_code=status_code, content=result)


@app.post("/approve")
async def approve(request: Request):
    """
    POST /approve — Duyệt/từ chối submission (Item 3.3, Admin only).

    Body JSON:
      {
        "submission_id": 1,
        "decision": "approve|reject"
      }
    Header: X-Role: Admin

    Khi approve: chạy authoring pipeline → insert rule core → reindex.
    """
    from tools.ingest import handle_approve

    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=422, content={"error": "invalid JSON body"})

    submission_id = body.get("submission_id")
    decision = (body.get("decision") or "").strip().lower()
    actor_role = request.headers.get("X-Role", "User")

    if not submission_id or not isinstance(submission_id, int):
        return JSONResponse(status_code=422, content={"error": "'submission_id' phải là số nguyên"})
    if not decision:
        return JSONResponse(status_code=422, content={"error": "'decision' là bắt buộc (approve|reject)"})

    status_code, result = handle_approve(
        submission_id=submission_id,
        decision=decision,
        actor_role=actor_role,
    )
    return JSONResponse(status_code=status_code, content=result)


@app.post("/checklist")
async def checklist(request: Request):
    """
    POST /checklist — Pre-publish checklist generator (Item 3.4).

    Body JSON:
      {
        "content": "...",                    -- nội dung cần đăng (bắt buộc)
        "platforms": ["meta", "tiktok", ...],
        "activity_description": "...",       -- mô tả hoạt động (tùy chọn, bổ sung context)
        "tenant_id": null,
        "campaign_id": null
      }
    Header: X-Role (user | mod | admin)

    Returns:
      {
        "checklist": [{"item": str, "risk": "high|medium|low", "doc_id": str}, ...]
      }
    """
    from tools.checklist import generate_checklist
    from rag import retriever

    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=422, content={"error": "invalid JSON body"})

    content = (body.get("content") or "").strip()
    if not content:
        return JSONResponse(status_code=422, content={"error": "'content' là bắt buộc"})

    platforms = body.get("platforms") or []
    if isinstance(platforms, str):
        platforms = [platforms]

    valid_platforms = {"meta", "tiktok", "google", "store", "website", "group"}
    platforms = [p.lower().strip() for p in platforms if p.lower().strip() in valid_platforms]

    activity_description = (body.get("activity_description") or "").strip()
    tenant_id = body.get("tenant_id")
    campaign_id = body.get("campaign_id")

    # Retrieve KB chunks for LLM expansion context
    query = f"{content[:200]} {activity_description}".strip()
    chunks = retriever.retrieve(query, tenant_id=tenant_id, campaign_id=campaign_id,
                                platforms=platforms or None, top_k=4)

    context = {
        "content": content,
        "platforms": platforms,
        "violations": [],           # No violations — this is a standalone checklist call
        "activity_description": activity_description,
        "tenant_id": tenant_id,
        "chunks": chunks,
        # _extra_items NOT set → generate_checklist will call LLM expansion
    }

    checklist_items = generate_checklist(context)
    return JSONResponse(status_code=200, content={"checklist": checklist_items})


@app.post("/draft")
async def draft(request: Request):
    """
    POST /draft — Generate draft from summary (Item 7.4 guided authoring).

    Body JSON:
      {
        "summary": "tóm tắt ý định...",
        "content_layer": "operating_rule|daily_tool|case_study|legal_source|platform_policy"
      }
    """
    from tools.authoring import generate_draft_from_summary

    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=422, content={"error": "invalid JSON body"})

    summary = (body.get("summary") or "").strip()
    content_layer = (body.get("content_layer") or "").strip()

    if not summary:
        return JSONResponse(status_code=422, content={"error": "'summary' là bắt buộc"})
    if not content_layer:
        return JSONResponse(status_code=422, content={"error": "'content_layer' là bắt buộc"})

    result = generate_draft_from_summary(summary=summary, content_layer=content_layer)

    status_code = 200 if result["success"] else 500
    return JSONResponse(status_code=status_code, content=result)


@app.get("/rules")
async def list_rules_route(request: Request):
    """GET /rules — danh sách custom rules từ DB (tất cả role)."""
    from db.store import list_rules

    content_layer = request.query_params.get("content_layer")
    scope = request.query_params.get("scope")
    tenant_id_str = request.query_params.get("tenant_id")
    tenant_id = int(tenant_id_str) if tenant_id_str else None

    rules = list_rules(content_layer=content_layer, scope=scope, tenant_id=tenant_id)
    return JSONResponse(status_code=200, content={"rules": rules, "count": len(rules)})


@app.get("/audit")
async def audit(request: Request):
    """
    GET /audit — Admin only: danh sách audit_log gần nhất (Item 3.5).
    Role gate enforced by RoleGateMiddleware trước khi đến đây.

    Query param: limit (default 50, max 200).
    """
    from db.store import list_audit_log

    try:
        limit = int(request.query_params.get("limit", 50))
        limit = min(max(limit, 1), 200)
    except (ValueError, TypeError):
        limit = 50

    entries = list_audit_log(limit=limit)
    return JSONResponse(status_code=200, content={"entries": entries, "count": len(entries)})


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
