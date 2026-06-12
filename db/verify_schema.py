"""Verify schema and seed data in vDB."""
import os, sys
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

with conn.cursor() as cur:
    cur.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema='public' AND table_type='BASE TABLE' ORDER BY table_name"
    )
    tables = [r[0] for r in cur.fetchall()]
    print("Tables:", tables)

    try:
        cur.execute("SELECT id, detect_mode, on_violation, explanation_style FROM ai_config")
        row = cur.fetchone()
        print("ai_config row 1:", row)
    except Exception as e:
        print("ai_config:", e)

    try:
        cur.execute("SELECT id, name, slug FROM tenants ORDER BY id")
        print("tenants:", cur.fetchall())
    except Exception as e:
        print("tenants:", e)

    try:
        cur.execute("SELECT doc_id, content_layer, scope FROM rules ORDER BY id")
        print("rules:", cur.fetchall())
    except Exception as e:
        print("rules:", e)

    try:
        cur.execute("SELECT COUNT(*) FROM audit_log")
        print("audit_log rows:", cur.fetchone()[0])
    except Exception as e:
        print("audit_log:", e)

conn.close()
print("\nVerification complete.")
