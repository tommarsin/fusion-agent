"""Verify table columns match concept.md spec."""
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")
import psycopg2

conn = psycopg2.connect(
    host=os.environ["DB_HOST"],
    port=int(os.environ.get("DB_PORT", "5432")),
    dbname=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    sslmode=os.environ.get("DB_SSLMODE", "disable"),
    connect_timeout=10,
)

EXPECTED = {
    "tenants": ["id", "name", "slug"],
    "campaigns": ["id", "tenant_id", "name", "platforms", "period", "status"],
    "rules": [
        "id", "doc_id", "content_layer", "scope",
        "tenant_id", "campaign_id", "platforms", "status",
        "title", "body_md", "metadata_json", "source_url",
        "related_core_doc_id", "version", "created_by_role",
        "created_at", "updated_at",
    ],
    "rule_versions": ["id", "rule_id", "version", "raw_text", "structured_md",
                      "source_url", "fetched_at", "created_at"],
    "rule_submissions": ["id", "link", "note", "submitted_by_role", "tenant_id",
                         "status", "reviewed_at", "result_rule_id"],
    "audit_log": ["id", "actor_role", "tenant_id", "action",
                  "input_hash", "verdict", "summary", "created_at"],
    "ai_config": ["id", "detect_mode", "on_violation", "explanation_style"],
}

with conn.cursor() as cur:
    all_ok = True
    for table, expected_cols in EXPECTED.items():
        cur.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_schema='public' AND table_name=%s ORDER BY ordinal_position",
            (table,)
        )
        actual = [r[0] for r in cur.fetchall()]
        missing = [c for c in expected_cols if c not in actual]
        status = "OK" if not missing else f"MISSING: {missing}"
        print(f"  {table:25s} {status}")
        if missing:
            all_ok = False
            print(f"    actual cols: {actual}")

print()
print("All columns OK" if all_ok else "SOME COLUMNS MISSING — schema needs patching")

conn.close()
