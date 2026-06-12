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


# ── AI endpoints (stubs — WS3 will fill these) ───────────────────────────────
async def _ask_stub(request: Request) -> JSONResponse:
    """Shared handler for /ask and /invocations alias."""
    return JSONResponse(status_code=501, content={"error": "not implemented"})


@app.post("/ask")
async def ask(request: Request):
    return await _ask_stub(request)


@app.post("/invocations")
async def invocations(request: Request):
    """AgentBase SDK convention alias → delegates to /ask handler."""
    return await _ask_stub(request)


@app.post("/scan")
async def scan(request: Request):
    return JSONResponse(status_code=501, content={"error": "not implemented"})


@app.post("/ingest")
async def ingest(request: Request):
    return JSONResponse(status_code=501, content={"error": "not implemented"})


@app.post("/approve")
async def approve(request: Request):
    return JSONResponse(status_code=501, content={"error": "not implemented"})


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
