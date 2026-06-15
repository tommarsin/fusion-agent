"""
Item 3.3 — Handlers cho POST /ingest và POST /approve.
main.py import và delegate tới đây.
"""
import hashlib
import logging
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)

# Được set khi startup (lifespan) bởi main.py
_KB_DIR: Optional[str] = None


def set_kb_dir(kb_dir: str) -> None:
    global _KB_DIR
    _KB_DIR = kb_dir


def _is_url(source: str) -> bool:
    return source.strip().startswith(("http://", "https://"))


def _normalize_role(raw_role: str) -> str:
    """Chuẩn hoá X-Role header về Admin | Mod | User."""
    mapping = {
        "admin": "Admin",
        "mod":   "Mod",
        "user":  "User",
    }
    return mapping.get(raw_role.lower(), "User")


def _parse_fetched_at(iso_str: Optional[str]) -> Optional[datetime]:
    """Chuyển ISO string (từ webfetch) sang datetime object."""
    if not iso_str:
        return None
    try:
        return datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    except Exception:
        return datetime.now(timezone.utc)


# ── /ingest ───────────────────────────────────────────────────────────────────


def handle_ingest(
    source: str,
    scope: str,
    actor_role: str,
    tenant_id: Optional[int] = None,
    campaign_id: Optional[int] = None,
    note: Optional[str] = None,
    related_core_doc_id: Optional[str] = None,
) -> tuple[int, dict]:
    """
    Xử lý POST /ingest.

    Routing:
    - User          → 403
    - Mod + core    → submission pending (chờ Admin duyệt)
    - Mod + tenant  → rule live ngay (siết-only, scope=tenant|campaign)
    - Admin         → rule live ngay bất kỳ scope

    Returns (http_status_code, response_dict).
    """
    from db import store
    from tools import webfetch, authoring
    from rag import retriever

    role = _normalize_role(actor_role)

    # ── Kiểm tra quyền ────────────────────────────────────────────────────────
    if role == "User":
        return 403, {"error": "Forbidden: User không có quyền /ingest"}

    # ── Validate đầu vào ──────────────────────────────────────────────────────
    if scope not in ("core", "tenant", "campaign"):
        return 422, {"error": "scope phải là core|tenant|campaign"}
    if scope in ("tenant", "campaign") and not tenant_id:
        return 422, {"error": "tenant_id bắt buộc khi scope=tenant hoặc scope=campaign"}

    # ── Lấy nội dung ──────────────────────────────────────────────────────────
    source_url: Optional[str] = None
    raw_text: Optional[str] = None
    fetched_at_str: Optional[str] = None

    if _is_url(source):
        source_url = source.strip()
        fetch_result = webfetch.fetch_text(source_url)
        if not fetch_result["success"]:
            return 422, {
                "error": f"Không tải được URL: {fetch_result['error']}",
                "url": source_url,
            }
        raw_text = fetch_result["raw_text"]
        fetched_at_str = fetch_result["fetched_at"]
    else:
        raw_text = source.strip()

    if not raw_text:
        return 422, {"error": "Nội dung rỗng sau khi tải/nhận"}

    input_hash = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()

    # ── Mod đề xuất core → submission pending ─────────────────────────────────
    if role == "Mod" and scope == "core":
        try:
            sub_id = store.insert_submission(
                link=source_url or "text_input",
                note=note,
                submitted_by_role="Mod",
                tenant_id=tenant_id,
                raw_text=raw_text,
            )
        except Exception as e:
            logger.error(f"insert_submission thất bại: {e}")
            return 500, {"error": f"Lỗi DB khi tạo submission: {e}"}

        store.insert_audit(
            actor_role="Mod",
            action="ingest",
            summary=f"Mod đề xuất core — source: {(source_url or raw_text[:80])}",
            tenant_id=tenant_id,
            input_hash=input_hash,
            verdict="pending",
        )
        return 200, {
            "submission_id": sub_id,
            "status": "pending",
            "message": (
                f"Đề xuất #{sub_id} đã ghi nhận. "
                "Admin cần duyệt qua POST /approve để rule vào core."
            ),
        }

    # ── Mod nạp rule tenant (live ngay) hoặc Admin (mọi scope) ────────────────
    result = authoring.run_authoring_pipeline(raw_text, source_url, _KB_DIR)

    # Cho phép warnings về optional fields — chỉ fail nếu lỗi nghiêm trọng
    critical_errors = [
        e for e in result.get("errors", [])
        if "body_md" in e or "content_layer" in e
    ]
    if critical_errors:
        return 422, {
            "error": "Authoring thất bại",
            "details": result.get("errors"),
        }

    # Scope: Mod chỉ insert tenant/campaign; Admin insert theo scope đã chỉ định
    actual_scope = scope  # "core" | "tenant" | "campaign"
    if role == "Mod":
        actual_scope = scope  # đã validate ≠ core ở trên

    try:
        rule_id = store.insert_rule(
            doc_id=result["doc_id"],
            content_layer=result["content_layer"],
            scope=actual_scope,
            title=result["title"],
            body_md=result["body_md"],
            tenant_id=tenant_id if actual_scope != "core" else None,
            campaign_id=campaign_id if actual_scope == "campaign" else None,
            platforms=result.get("platforms", ["all"]),
            metadata_json=result.get("metadata_json", {}),
            source_url=result.get("source_url"),
            related_core_doc_id=related_core_doc_id,
            created_by_role=role,
        )
    except Exception as e:
        err_str = str(e)
        logger.error(f"insert_rule thất bại: {err_str}")
        if "related_core_doc_id" in err_str and "foreign key" in err_str.lower():
            return 422, {"error": f"Doc ID '{related_core_doc_id}' chưa tồn tại trong hệ thống. Hãy nạp tài liệu gốc (scope 'Luật chung hệ thống') trước, hoặc bỏ trống field Related Core Doc ID."}
        return 500, {"error": f"Lỗi DB khi insert rule: {err_str}"}

    # Ghi rule_version
    try:
        store.insert_rule_version(
            rule_id=rule_id,
            version=1,
            raw_text=raw_text[:10_000],
            structured_md=result["body_md"],
            source_url=source_url,
            fetched_at=_parse_fetched_at(fetched_at_str),
        )
    except Exception as e:
        logger.warning(f"insert_rule_version thất bại (non-blocking): {e}")

    # Reindex RAG
    try:
        retriever.reindex(_KB_DIR)
        reindex_ok = True
    except Exception as e:
        logger.warning(f"reindex thất bại (non-blocking): {e}")
        reindex_ok = False

    store.insert_audit(
        actor_role=role,
        action="ingest",
        summary=f"{role} ingest: {result['doc_id']} — {result['title'][:60]}",
        tenant_id=tenant_id,
        input_hash=input_hash,
        verdict="approved",
    )

    return 200, {
        "rule_id": rule_id,
        "doc_id": result["doc_id"],
        "content_layer": result["content_layer"],
        "title": result["title"],
        "status": "approved",
        "scope": actual_scope,
        "reindexed": reindex_ok,
        "message": (
            f"Rule {result['doc_id']} đã được nạp và index "
            f"(scope={actual_scope})."
        ),
        "warnings": result.get("errors", []),
    }


# ── /approve ──────────────────────────────────────────────────────────────────


def handle_approve(
    submission_id: int,
    decision: str,
    actor_role: str,
) -> tuple[int, dict]:
    """
    Xử lý POST /approve.
    Chỉ Admin được duyệt/từ chối.

    decision: "approve" | "reject"
    Returns (http_status_code, response_dict).
    """
    from db import store
    from tools import webfetch, authoring
    from rag import retriever

    role = _normalize_role(actor_role)

    if role != "Admin":
        return 403, {"error": "Forbidden: chỉ Admin được dùng /approve"}

    if decision not in ("approve", "reject"):
        return 422, {"error": "decision phải là 'approve' hoặc 'reject'"}

    # Lấy submission
    sub = store.get_submission(submission_id)
    if not sub:
        return 404, {"error": f"Không tìm thấy submission #{submission_id}"}

    if sub["status"] != "pending":
        return 400, {
            "error": (
                f"Submission #{submission_id} đã được xử lý "
                f"(status={sub['status']})"
            )
        }

    # Reject nhanh
    if decision == "reject":
        try:
            store.reject_submission(submission_id)
        except Exception as e:
            return 500, {"error": f"Lỗi DB khi reject: {e}"}

        store.insert_audit(
            actor_role="Admin",
            action="approve",
            summary=f"Admin reject submission #{submission_id}",
            tenant_id=sub.get("tenant_id"),
            verdict="rejected",
        )
        return 200, {
            "submission_id": submission_id,
            "decision": "rejected",
            "message": f"Submission #{submission_id} đã bị từ chối.",
        }

    # Approve — cần raw_text
    raw_text: Optional[str] = sub.get("raw_text")
    source_url: Optional[str] = None
    fetched_at_str: Optional[str] = None

    link = sub.get("link", "")
    if link and link not in ("text_input",) and _is_url(link):
        source_url = link
        if not raw_text:
            # Re-fetch nếu không có cached raw_text
            fetch_result = webfetch.fetch_text(source_url)
            if not fetch_result["success"]:
                return 422, {
                    "error": (
                        f"Không tải lại được URL {source_url}: "
                        f"{fetch_result['error']}"
                    )
                }
            raw_text = fetch_result["raw_text"]
            fetched_at_str = fetch_result["fetched_at"]

    if not raw_text:
        return 422, {
            "error": "Submission không có nội dung để xử lý (raw_text rỗng)"
        }

    # Chạy authoring pipeline
    result = authoring.run_authoring_pipeline(raw_text, source_url, _KB_DIR)
    critical_errors = [
        e for e in result.get("errors", [])
        if "body_md" in e or "content_layer" in e
    ]
    if critical_errors:
        return 422, {
            "error": "Authoring thất bại",
            "details": result.get("errors"),
        }

    # Insert rule core (approved)
    try:
        rule_id = store.insert_rule(
            doc_id=result["doc_id"],
            content_layer=result["content_layer"],
            scope="core",
            title=result["title"],
            body_md=result["body_md"],
            platforms=result.get("platforms", ["all"]),
            metadata_json=result.get("metadata_json", {}),
            source_url=result.get("source_url"),
            created_by_role="Admin",
        )
    except Exception as e:
        logger.error(f"insert_rule (approve) thất bại: {e}")
        return 500, {"error": f"Lỗi DB khi insert rule: {e}"}

    # Ghi rule_version
    try:
        store.insert_rule_version(
            rule_id=rule_id,
            version=1,
            raw_text=raw_text[:10_000],
            structured_md=result["body_md"],
            source_url=source_url,
            fetched_at=_parse_fetched_at(fetched_at_str),
        )
    except Exception as e:
        logger.warning(f"insert_rule_version (approve) thất bại (non-blocking): {e}")

    # Cập nhật submission
    try:
        store.approve_submission(submission_id, rule_id)
    except Exception as e:
        logger.warning(f"approve_submission cập nhật status thất bại: {e}")

    # Reindex RAG
    try:
        retriever.reindex(_KB_DIR)
        reindex_ok = True
    except Exception as e:
        logger.warning(f"reindex sau approve thất bại: {e}")
        reindex_ok = False

    store.insert_audit(
        actor_role="Admin",
        action="approve",
        summary=(
            f"Admin approve submission #{submission_id} "
            f"→ rule {result['doc_id']}"
        ),
        tenant_id=sub.get("tenant_id"),
        verdict="approved",
    )

    return 200, {
        "submission_id": submission_id,
        "decision": "approved",
        "rule_id": rule_id,
        "doc_id": result["doc_id"],
        "content_layer": result["content_layer"],
        "title": result["title"],
        "reindexed": reindex_ok,
        "message": (
            f"Submission #{submission_id} đã duyệt → "
            f"Rule {result['doc_id']} sống trong core + reindex xong."
        ),
        "warnings": result.get("errors", []),
    }
