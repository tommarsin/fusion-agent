"""
DB store — abstraction layer cho Fusion Agent (Item 1.3b / 3.3).
Mọi write về rules / submissions / versions / audit đi qua đây.
Kết nối trực tiếp vDB Postgres (psycopg2); graceful fail khi thiếu creds.
"""
import json
import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# ── Layer → doc_id prefix ─────────────────────────────────────────────────────

LAYER_PREFIX: dict[str, str] = {
    "legal_source":    "GSX-LEGAL",
    "operating_rule":  "GSX-OP",
    "daily_tool":      "GSX-TOOL",
    "platform_policy": "GSX-PLAT",
    "case_study":      "GSX-CASE",
}

# ── Connection ────────────────────────────────────────────────────────────────


def _get_conn():
    """Mở kết nối psycopg2 tới vDB."""
    import psycopg2  # type: ignore

    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "").strip(),
        port=int(os.environ.get("DB_PORT", "5432").strip()),
        dbname=os.environ.get("DB_NAME", "fusionagent").strip(),
        user=os.environ.get("DB_USER", "").strip(),
        password=os.environ.get("DB_PASSWORD", "").strip(),
        sslmode=os.environ.get("DB_SSLMODE", "disable").strip(),
        connect_timeout=5,
    )


# ── Schema migration helpers ──────────────────────────────────────────────────


def ensure_raw_text_column() -> None:
    """
    Thêm cột raw_text vào rule_submissions nếu chưa có.
    Idempotent — chạy nhiều lần vẫn OK.
    """
    try:
        conn = _get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            ALTER TABLE rule_submissions
            ADD COLUMN IF NOT EXISTS raw_text TEXT
            """
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logger.debug(f"ensure_raw_text_column (non-fatal): {e}")


# ── doc_id generation ─────────────────────────────────────────────────────────


def get_next_doc_id(layer: str, kb_dir: Optional[str] = None) -> str:
    """
    Sinh doc_id tiếp theo cho layer đã chỉ định.
    Scan cả DB lẫn KB folder để tránh trùng.

    Ví dụ: get_next_doc_id("legal_source") → "GSX-LEGAL-011"
    """
    prefix = LAYER_PREFIX.get(layer, "GSX-RULE")
    max_num = 0

    # Scan DB
    try:
        conn = _get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT doc_id FROM rules WHERE doc_id LIKE %s",
            (f"{prefix}-%",),
        )
        for (doc_id,) in cur.fetchall():
            m = re.search(r"-(\d+)$", doc_id)
            if m:
                max_num = max(max_num, int(m.group(1)))
        cur.close()
        conn.close()
    except Exception as e:
        logger.warning(f"get_next_doc_id DB scan lỗi: {e}")

    # Scan KB folder (500 bytes đầu mỗi file — chỉ cần frontmatter)
    if kb_dir:
        try:
            for md_file in Path(kb_dir).rglob("*.md"):
                try:
                    sample = md_file.read_text(encoding="utf-8", errors="ignore")[:600]
                    for m in re.finditer(rf"{re.escape(prefix)}-(\d+)", sample):
                        max_num = max(max_num, int(m.group(1)))
                except OSError:
                    pass
        except Exception as e:
            logger.warning(f"get_next_doc_id KB scan lỗi: {e}")

    return f"{prefix}-{max_num + 1:03d}"


# ── Rule operations ───────────────────────────────────────────────────────────


def insert_rule(
    doc_id: str,
    content_layer: str,
    scope: str,
    title: str,
    body_md: str,
    *,
    tenant_id: Optional[int] = None,
    campaign_id: Optional[int] = None,
    platforms: Optional[list] = None,
    metadata_json: Optional[dict] = None,
    source_url: Optional[str] = None,
    related_core_doc_id: Optional[str] = None,
    created_by_role: str = "Admin",
) -> int:
    """Insert rule vào bảng rules (status=approved). Trả rule_id."""
    if platforms is None:
        platforms = ["all"]
    if metadata_json is None:
        metadata_json = {}

    # Postgres array literal: {meta,tiktok}
    platforms_pg = "{" + ",".join(str(p) for p in platforms) + "}"

    conn = _get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO rules
              (doc_id, content_layer, scope, tenant_id, campaign_id,
               platforms, status, title, body_md, metadata_json,
               source_url, related_core_doc_id, version, created_by_role)
            VALUES (%s, %s::content_layer_enum, %s::rule_scope_enum,
                    %s, %s, %s::platform_enum[],
                    'approved'::rule_status_enum,
                    %s, %s, %s::jsonb,
                    %s, %s, 1, %s::role_enum)
            RETURNING id
            """,
            (
                doc_id,
                content_layer,
                scope,
                tenant_id,
                campaign_id,
                platforms_pg,
                title,
                body_md,
                json.dumps(metadata_json, ensure_ascii=False),
                source_url,
                related_core_doc_id,
                created_by_role,
            ),
        )
        rule_id = cur.fetchone()[0]
        conn.commit()
    finally:
        cur.close()
        conn.close()

    logger.info(f"insert_rule: {doc_id} (layer={content_layer}, scope={scope}) → id={rule_id}")
    return rule_id


# ── Rule version ──────────────────────────────────────────────────────────────


def insert_rule_version(
    rule_id: int,
    version: int,
    raw_text: str,
    structured_md: Optional[str] = None,
    source_url: Optional[str] = None,
    fetched_at: Optional[datetime] = None,
) -> int:
    """Ghi bản rule_version. Trả version_id."""
    if fetched_at is None:
        fetched_at = datetime.now(timezone.utc)

    conn = _get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO rule_versions
              (rule_id, version, raw_text, structured_md, source_url, fetched_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (rule_id, version, raw_text, structured_md, source_url, fetched_at),
        )
        vid = cur.fetchone()[0]
        conn.commit()
    finally:
        cur.close()
        conn.close()

    return vid


# ── Submission operations ─────────────────────────────────────────────────────


def insert_submission(
    link: str,
    note: Optional[str],
    submitted_by_role: str,
    tenant_id: Optional[int],
    raw_text: Optional[str] = None,
) -> int:
    """Insert rule_submission (status=pending). Trả submission_id."""
    ensure_raw_text_column()

    conn = _get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO rule_submissions
              (link, note, submitted_by_role, tenant_id, status, raw_text)
            VALUES (%s, %s, %s::role_enum, %s, 'pending'::submission_status_enum, %s)
            RETURNING id
            """,
            (link, note, submitted_by_role, tenant_id, raw_text),
        )
        sub_id = cur.fetchone()[0]
        conn.commit()
    finally:
        cur.close()
        conn.close()

    logger.info(f"insert_submission: id={sub_id}, link={str(link)[:60]}")
    return sub_id


def get_submission(submission_id: int) -> Optional[dict]:
    """Lấy submission theo id. Trả None nếu không tìm thấy."""
    ensure_raw_text_column()
    try:
        conn = _get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, link, note, submitted_by_role, tenant_id, status, raw_text, created_at
            FROM rule_submissions WHERE id = %s
            """,
            (submission_id,),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            return None
        return {
            "id": row[0],
            "link": row[1],
            "note": row[2],
            "submitted_by_role": row[3],
            "tenant_id": row[4],
            "status": row[5],
            "raw_text": row[6],
            "created_at": row[7].isoformat() if row[7] else None,
        }
    except Exception as e:
        logger.error(f"get_submission({submission_id}): {e}")
        return None


def approve_submission(submission_id: int, result_rule_id: int) -> None:
    """Cập nhật submission → approved, gắn result_rule_id."""
    conn = _get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE rule_submissions
            SET status = 'approved'::submission_status_enum,
                reviewed_at = NOW(),
                result_rule_id = %s
            WHERE id = %s
            """,
            (result_rule_id, submission_id),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


def reject_submission(submission_id: int) -> None:
    """Cập nhật submission → rejected."""
    conn = _get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE rule_submissions
            SET status = 'rejected'::submission_status_enum,
                reviewed_at = NOW()
            WHERE id = %s
            """,
            (submission_id,),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


def list_submissions(status: Optional[str] = None) -> list:
    """Liệt kê submissions theo status (hoặc tất cả nếu status=None)."""
    ensure_raw_text_column()
    try:
        conn = _get_conn()
        cur = conn.cursor()
        if status:
            cur.execute(
                """
                SELECT id, link, note, submitted_by_role, tenant_id, status, created_at
                FROM rule_submissions
                WHERE status = %s::submission_status_enum
                ORDER BY created_at DESC
                """,
                (status,),
            )
        else:
            cur.execute(
                """
                SELECT id, link, note, submitted_by_role, tenant_id, status, created_at
                FROM rule_submissions
                ORDER BY created_at DESC
                """
            )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [
            {
                "id": r[0],
                "link": r[1],
                "note": r[2],
                "submitted_by_role": r[3],
                "tenant_id": r[4],
                "status": r[5],
                "created_at": r[6].isoformat() if r[6] else None,
            }
            for r in rows
        ]
    except Exception as e:
        logger.error(f"list_submissions: {e}")
        return []


# ── Audit ─────────────────────────────────────────────────────────────────────


def insert_audit(
    actor_role: str,
    action: str,
    summary: str,
    tenant_id: Optional[int] = None,
    input_hash: Optional[str] = None,
    verdict: Optional[str] = None,
) -> None:
    """Ghi audit_log. Non-blocking — log warning nếu DB fail."""
    try:
        conn = _get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO audit_log
              (actor_role, tenant_id, action, input_hash, verdict, summary)
            VALUES (%s::role_enum, %s, %s::audit_action_enum, %s, %s, %s)
            """,
            (
                actor_role,
                tenant_id,
                action,
                input_hash,
                verdict,
                summary[:500] if summary else None,
            ),
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logger.warning(f"insert_audit thất bại (non-blocking): {e}")
