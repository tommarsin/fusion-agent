"""
Web fetch tool — tải URL và bóc text chính bằng trafilatura.
Item 3.3 — Fusion Agent.
"""
import logging
import re
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)

# Giới hạn text để không quá lớn khi gửi LLM (50K ký tự ≈ ~12K tokens)
MAX_TEXT_LENGTH = 50_000


def fetch_text(url: str, timeout: int = 15) -> dict:
    """
    Tải URL và bóc main content text.

    Returns dict:
        raw_text  : str — nội dung bóc được
        url       : str — URL đã tải
        fetched_at: str — ISO timestamp
        success   : bool
        error     : str | None
    """
    fetched_at = datetime.now(timezone.utc).isoformat()

    try:
        import trafilatura  # type: ignore

        # 1. Tải HTML
        html = trafilatura.fetch_url(url)
        if html is None:
            # Thử lại bằng requests (một số site cần User-Agent cụ thể)
            html = _fetch_with_requests(url, timeout)

        if not html:
            return {
                "raw_text": "",
                "url": url,
                "fetched_at": fetched_at,
                "success": False,
                "error": "Không tải được HTML (site cần JS hoặc bị anti-bot)",
            }

        # 2. Bóc text chính
        text = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=True,
            favor_recall=True,
            no_fallback=False,
        )

        if not text:
            # Fallback: strip HTML tags thủ công
            text = _strip_html(html)

        raw_text = (text or "")[:MAX_TEXT_LENGTH]

        if not raw_text.strip():
            return {
                "raw_text": "",
                "url": url,
                "fetched_at": fetched_at,
                "success": False,
                "error": "Bóc được HTML nhưng không trích xuất được text",
            }

        return {
            "raw_text": raw_text,
            "url": url,
            "fetched_at": fetched_at,
            "success": True,
            "error": None,
        }

    except ImportError:
        # trafilatura chưa cài — thử requests + strip
        html = _fetch_with_requests(url, timeout)
        if not html:
            return {
                "raw_text": "",
                "url": url,
                "fetched_at": fetched_at,
                "success": False,
                "error": "trafilatura chưa cài và requests fetch thất bại",
            }
        raw_text = _strip_html(html)[:MAX_TEXT_LENGTH]
        return {
            "raw_text": raw_text,
            "url": url,
            "fetched_at": fetched_at,
            "success": bool(raw_text.strip()),
            "error": None if raw_text.strip() else "trafilatura chưa cài — text rỗng",
        }

    except Exception as e:
        logger.error(f"fetch_text({url}): {e}")
        return {
            "raw_text": "",
            "url": url,
            "fetched_at": fetched_at,
            "success": False,
            "error": str(e),
        }


def _fetch_with_requests(url: str, timeout: int = 15) -> Optional[str]:
    """Fallback fetch bằng requests với User-Agent chuẩn."""
    try:
        import requests  # type: ignore

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
        }
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        return resp.text
    except Exception as e:
        logger.warning(f"_fetch_with_requests({url}): {e}")
        return None


def _strip_html(html: str) -> str:
    """Strip HTML tags và normalize whitespace."""
    text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
