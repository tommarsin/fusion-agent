"""
BM25 retriever cho Fusion Agent.

Interface thiết kế để sau có thể swap sang embedding+FAISS mà không đổi chữ ký hàm:
  build_index(chunks)
  retrieve(query, tenant_id, campaign_id, platforms, top_k) → list[dict]
  reindex(kb_dir)
  set_kb_dir(kb_dir)
"""

import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)

# Module-level state (singleton index)
_chunks: list[dict] = []
_bm25 = None  # BM25Okapi instance
_kb_dir: str = ""
# doc_id → list of chunk indices (for related-doc expansion)
_doc_idx: dict[str, list[int]] = {}


# ── Tokenizer ─────────────────────────────────────────────────────────────────

def _tokenize(text: str) -> list[str]:
    """
    Tokenize cho BM25 POC:
    - Lowercase
    - Tách theo whitespace + dấu câu / non-word Unicode
    Đủ cho tiếng Việt ở quy mô POC (corpus nhỏ, không cần underthesea).
    """
    text = text.lower()
    tokens = re.split(r"[^\w]+", text, flags=re.UNICODE)
    return [t for t in tokens if len(t) > 1]  # bỏ token 1 ký tự


def _chunk_to_text(chunk: dict) -> str:
    """Ghép heading + body + tags thành chuỗi để index."""
    parts = [
        chunk.get("title", ""),
        chunk.get("heading", ""),
        chunk.get("body", ""),
        " ".join(chunk.get("tags", [])),
    ]
    return " ".join(p for p in parts if p)


# ── Index ─────────────────────────────────────────────────────────────────────

def build_index(chunks: list[dict]) -> None:
    """Build BM25 index từ chunks. Ghi log số chunk."""
    global _chunks, _bm25

    try:
        from rank_bm25 import BM25Okapi  # type: ignore
    except ImportError:
        logger.error(
            "rank_bm25 chưa cài — BM25 index bị tắt. "
            "Thêm 'rank-bm25' vào requirements.txt."
        )
        _chunks = chunks
        _bm25 = None
        return

    _chunks = chunks
    tokenized = [_tokenize(_chunk_to_text(c)) for c in _chunks]
    _bm25 = BM25Okapi(tokenized)

    # Build doc_id → chunk indices lookup (dùng cho related-doc expansion)
    global _doc_idx
    _doc_idx = {}
    for i, c in enumerate(_chunks):
        did = c.get("doc_id", "")
        if did:
            _doc_idx.setdefault(did, []).append(i)

    logger.info(f"BM25 index built: {len(_chunks)} chunks, {len(_doc_idx)} unique doc_ids")


def set_kb_dir(kb_dir: str) -> None:
    """Lưu kb_dir để reindex() dùng lại."""
    global _kb_dir
    _kb_dir = kb_dir


def reindex(kb_dir: Optional[str] = None) -> None:
    """
    Reload KB + DB và rebuild index.
    Gọi sau khi approve/insert rule mới (item 3.3).
    """
    from rag.loader import load_all_chunks

    dir_ = kb_dir or _kb_dir
    if not dir_:
        logger.warning("reindex() gọi nhưng kb_dir chưa set")
        return
    chunks = load_all_chunks(dir_)
    build_index(chunks)


# ── Filter helpers ────────────────────────────────────────────────────────────

def _platforms_match(chunk_platforms: list[str], filter_platforms: list[str]) -> bool:
    """
    True nếu chunk liên quan đến ít nhất 1 platform được yêu cầu,
    hoặc chunk gắn 'all' (áp dụng mọi nơi).
    """
    if "all" in chunk_platforms:
        return True
    return bool(set(chunk_platforms) & set(filter_platforms))


def _scope_match(
    chunk: dict,
    tenant_id: Optional[int],
    campaign_id: Optional[int],
) -> bool:
    """
    Quy tắc scope (siết-only):
    - core → luôn include
    - tenant → chỉ include nếu tenant_id khớp
    - campaign → chỉ include nếu campaign_id khớp
    """
    scope = chunk.get("scope", "core")
    if scope == "core":
        return True
    if scope == "tenant":
        return tenant_id is not None and chunk.get("tenant_id") == tenant_id
    if scope == "campaign":
        return campaign_id is not None and chunk.get("campaign_id") == campaign_id
    return False


# ── Retrieve ──────────────────────────────────────────────────────────────────

def retrieve(
    query: str,
    tenant_id: Optional[int] = None,
    campaign_id: Optional[int] = None,
    platforms: Optional[list[str]] = None,
    top_k: int = 8,
) -> list[dict]:
    """
    Retrieve top_k chunk liên quan từ core KB ∪ tenant rules.

    Trả list dict với các key bắt buộc cho các item 3.x:
      doc_id, title, content_layer, heading, body, platforms, scope,
      tenant_id, campaign_id, _score (BM25 score)

    Nếu platforms=None → không filter platform.
    """
    if _bm25 is None:
        logger.warning("BM25 index chưa build hoặc rank_bm25 thiếu — trả []")
        return []

    if not _chunks:
        return []

    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    scores = _bm25.get_scores(query_tokens)

    # Lọc candidate pool theo scope + platform
    candidates: list[tuple[int, float]] = []
    for i, chunk in enumerate(_chunks):
        if not _scope_match(chunk, tenant_id, campaign_id):
            continue
        if platforms and not _platforms_match(chunk.get("platforms", ["all"]), platforms):
            continue
        candidates.append((i, float(scores[i])))

    # Sort theo BM25 score giảm dần
    candidates.sort(key=lambda x: x[1], reverse=True)

    results: list[dict] = []
    seen_indices: set[int] = set()
    for idx, score in candidates[:top_k]:
        results.append({**_chunks[idx], "_score": score})
        seen_indices.add(idx)

    # Related-doc expansion: kéo thêm legal sources được tham chiếu
    # bởi chunks trong kết quả (không thay thế — chỉ thêm nếu chưa có).
    # Giới hạn expansion để không vượt quá top_k * 2.
    max_total = top_k * 2
    related_to_add: set[str] = set()
    for r in results:
        for rdid in r.get("related_doc_ids", []):
            if rdid not in {c["doc_id"] for c in results}:
                related_to_add.add(rdid)

    for rdid in related_to_add:
        if len(results) >= max_total:
            break
        indices = _doc_idx.get(rdid, [])
        if not indices:
            continue
        # Lấy chunk đầu tiên (intro/title chunk) của doc đó
        first_idx = indices[0]
        if first_idx not in seen_indices:
            # Platform filter áp dụng cho expansion chunks cũng vậy
            c = _chunks[first_idx]
            if platforms and not _platforms_match(c.get("platforms", ["all"]), platforms):
                continue
            results.append({**c, "_score": 0.0, "_expanded": True})
            seen_indices.add(first_idx)

    return results
