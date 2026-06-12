"""
Role gate middleware + audit logging (Item 3.5).

Ma trận quyền:
  User  → /ask /scan /checklist OK; /ingest /approve /audit BLOCKED
  Mod   → /ask /scan /checklist /ingest OK; /approve /audit BLOCKED
  Admin → tất cả OK

Middleware enforces gate TRƯỚC khi request đến handler.
/ingest và /approve tự ghi audit trong handler; middleware ghi cho /ask /scan /checklist.
"""
import logging
from typing import Optional

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)

_ROLE_RANK: dict[str, int] = {"User": 0, "Mod": 1, "Admin": 2}

# Minimum role rank cần thiết — paths không có = mở cho tất cả
_MIN_RANK: dict[str, int] = {
    "/ingest": 1,        # Mod+
    "/approve": 2,       # Admin only
    "/audit": 2,         # Admin only
    "/submissions": 1,   # Mod+ (item 4.1)
}

# Paths mà middleware tự ghi audit_log (ingest/approve tự ghi trong handler)
_MIDDLEWARE_AUDIT: dict[str, str] = {
    "/ask": "ask",
    "/invocations": "ask",
    "/scan": "scan",
    "/checklist": "checklist",
}


def normalize_role(raw: Optional[str]) -> str:
    if not raw:
        return "User"
    return {"admin": "Admin", "mod": "Mod", "user": "User"}.get(raw.strip().lower(), "User")


class RoleGateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        role = normalize_role(request.headers.get("X-Role"))
        path = request.url.path
        rank = _ROLE_RANK.get(role, 0)
        min_rank = _MIN_RANK.get(path, 0)

        if rank < min_rank:
            needed = "Admin" if min_rank >= 2 else "Mod hoặc Admin"
            # Log blocked attempt (skip /audit path để tránh recursive entries)
            if path != "/audit":
                action = {"ingest": "ingest", "/approve": "approve"}.get(path, "ask")
                _try_audit(role, action, f"403 blocked — {path}", verdict="blocked")
            return JSONResponse(
                status_code=403,
                content={"error": f"Yêu cầu quyền {needed}", "your_role": role},
            )

        response = await call_next(request)

        # Ghi audit cho các open routes (không ghi /health, /audit)
        action = _MIDDLEWARE_AUDIT.get(path)
        if action:
            verdict = "ok" if response.status_code < 400 else "blocked"
            _try_audit(role, action, f"{path} → {response.status_code}", verdict=verdict)

        return response


def _try_audit(
    role: str,
    action: str,
    summary: str,
    tenant_id: Optional[int] = None,
    verdict: Optional[str] = None,
) -> None:
    """Ghi audit_log non-blocking."""
    try:
        from db.store import insert_audit
        insert_audit(
            actor_role=role,
            action=action,
            summary=summary[:500],
            tenant_id=tenant_id,
            verdict=verdict,
        )
    except Exception as e:
        logger.debug(f"audit write failed (non-fatal): {e}")
