"""
Fusion Agent — Game Content Compliance AI System
FastAPI server, binds 0.0.0.0:8080 (AgentBase platform requirement).

Routes implemented here are stubs (HTTP 501). Logic filled in per WS3 items:
  3.1 → /ask   3.2 → /scan   3.3 → /ingest + /approve
  3.4 → /checklist   3.5 → role gate + /audit
"""

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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

    chunks = loader.load_all_chunks(KB_DIR)
    retriever.build_index(chunks)
    logger.info("RAG layer sẵn sàng.")
    yield
    # ── Shutdown ──────────────────────────────────────────────────────────────


app = FastAPI(
    title="Fusion Agent — Game Content Compliance AI System",
    lifespan=lifespan,
)


# ── Platform hard requirement ─────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok"}


# ── /ask + /invocations (item 3.1) ───────────────────────────────────────────

async def _handle_ask(request: Request) -> JSONResponse:
    """Shared handler cho /ask và /invocations alias."""
    from tools.ask import answer_question

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
    actor_role = request.headers.get("X-Role", "user").lower()

    result = scan_content(
        content=content,
        platforms=platforms,
        tenant_id=tenant_id,
        campaign_id=campaign_id,
        image_description=image_description,
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
    return JSONResponse(status_code=501, content={"error": "not implemented"})


@app.get("/audit")
async def audit(request: Request):
    return JSONResponse(status_code=501, content={"error": "not implemented"})


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
