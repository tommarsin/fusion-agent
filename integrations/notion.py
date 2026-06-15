"""
Notion API client (Item 9.5).

Gọi Notion REST API trực tiếp bằng `requests` — không cần SDK nặng
(notion-client). Chỉ phụ thuộc `requests` (đã có trong requirements.txt).

Config qua env:
  NOTION_API_KEY  — Internal Integration Secret (bắt buộc)
  NOTION_VERSION  — Notion-Version header (mặc định 2022-06-28)

Public API:
  query_database(database_id, filter=None, page_size=100) -> list[dict]
  get_database(database_id)                               -> dict
  get_page_property(page_id, property_id)                 -> dict
  update_page(page_id, properties)                        -> dict

Mọi hàm raise NotionError khi thiếu config hoặc API trả lỗi — caller
(notion_scan / endpoint) chịu trách nhiệm bắt và trả message thân thiện.
"""

import logging
import os
from typing import Optional

import requests

logger = logging.getLogger(__name__)

_API_BASE = "https://api.notion.com/v1"
_DEFAULT_VERSION = "2022-06-28"
_TIMEOUT = 30


class NotionError(RuntimeError):
    """Lỗi từ Notion API hoặc cấu hình thiếu."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


def _headers() -> dict:
    api_key = os.environ.get("NOTION_API_KEY", "").strip()
    if not api_key:
        raise NotionError("NOTION_API_KEY chưa được cấu hình (xem .env / .env.deploy).")
    version = os.environ.get("NOTION_VERSION", _DEFAULT_VERSION).strip() or _DEFAULT_VERSION
    return {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": version,
        "Content-Type": "application/json",
    }


def is_configured() -> bool:
    """True nếu NOTION_API_KEY đã set — dùng để gate sớm, tránh raise."""
    return bool(os.environ.get("NOTION_API_KEY", "").strip())


def _request(method: str, path: str, *, json_body: Optional[dict] = None) -> dict:
    url = f"{_API_BASE}{path}"
    try:
        resp = requests.request(
            method, url, headers=_headers(), json=json_body, timeout=_TIMEOUT
        )
    except requests.RequestException as e:
        raise NotionError(f"Không kết nối được Notion API: {e}") from e

    if resp.status_code >= 400:
        # Notion trả {object:"error", status, code, message}
        detail = ""
        try:
            body = resp.json()
            detail = body.get("message") or body.get("code") or ""
        except Exception:
            detail = (resp.text or "")[:300]
        raise NotionError(
            f"Notion API {resp.status_code}: {detail or 'lỗi không xác định'}",
            status_code=resp.status_code,
        )

    try:
        return resp.json()
    except Exception as e:
        raise NotionError(f"Notion trả response không phải JSON: {e}") from e


def get_database(database_id: str) -> dict:
    """Lấy metadata database (gồm `properties` schema)."""
    return _request("GET", f"/databases/{database_id}")


def query_database(
    database_id: str,
    filter: Optional[dict] = None,
    page_size: int = 100,
) -> list[dict]:
    """
    Đọc tất cả rows của 1 database, tự xử lý pagination (has_more / next_cursor).

    `filter`: object filter theo chuẩn Notion (vd lọc Status). None = lấy hết.
    Trả về list page objects (mỗi page có `id` + `properties`).
    """
    results: list[dict] = []
    cursor: Optional[str] = None

    while True:
        body: dict = {"page_size": min(max(page_size, 1), 100)}
        if filter:
            body["filter"] = filter
        if cursor:
            body["start_cursor"] = cursor

        data = _request("POST", f"/databases/{database_id}/query", json_body=body)
        results.extend(data.get("results", []))

        if data.get("has_more") and data.get("next_cursor"):
            cursor = data["next_cursor"]
        else:
            break

    logger.info("query_database %s → %d rows", database_id, len(results))
    return results


def get_page_property(page_id: str, property_id: str) -> dict:
    """
    Đọc 1 property item của 1 page (endpoint /pages/{id}/properties/{prop_id}).
    Dùng khi property quá dài bị truncate trong query_database.
    """
    return _request("GET", f"/pages/{page_id}/properties/{property_id}")


def update_page(page_id: str, properties: dict) -> dict:
    """
    Cập nhật properties của 1 page (ghi ngược checkbox + note).

    `properties`: dict theo chuẩn Notion, vd:
      {"Legal check": {"checkbox": True}}
      {"Legal note":  {"rich_text": [{"text": {"content": "..."}}]}}
    """
    return _request("PATCH", f"/pages/{page_id}", json_body={"properties": properties})


# ── Property value helpers ────────────────────────────────────────────────────


def read_text_property(page: dict, prop_name: str) -> str:
    """
    Đọc giá trị text từ property `prop_name` (hỗ trợ title / rich_text).
    Trả "" nếu không có.
    """
    prop = (page.get("properties") or {}).get(prop_name) or {}
    ptype = prop.get("type", "")
    if ptype == "rich_text":
        return "".join(p.get("plain_text", "") for p in prop.get("rich_text", []))
    if ptype == "title":
        return "".join(p.get("plain_text", "") for p in prop.get("title", []))
    return ""


def read_multiselect_property(page: dict, prop_name: str) -> list[str]:
    """Đọc list tên option từ multi_select / select property."""
    prop = (page.get("properties") or {}).get(prop_name) or {}
    ptype = prop.get("type", "")
    if ptype == "multi_select":
        return [o.get("name", "") for o in prop.get("multi_select", []) if o.get("name")]
    if ptype == "select":
        sel = prop.get("select") or {}
        return [sel["name"]] if sel.get("name") else []
    return []


def read_status_property(page: dict, prop_name: str) -> str:
    """Đọc giá trị status / select property (vd cột Status = Approve)."""
    prop = (page.get("properties") or {}).get(prop_name) or {}
    ptype = prop.get("type", "")
    if ptype == "status":
        return (prop.get("status") or {}).get("name", "")
    if ptype == "select":
        return (prop.get("select") or {}).get("name", "")
    return ""


def find_title_property_name(page: dict) -> Optional[str]:
    """Tìm tên property kiểu `title` của page (dùng làm fallback caption)."""
    for name, prop in (page.get("properties") or {}).items():
        if prop.get("type") == "title":
            return name
    return None
