"""
Apply schema.sql to the database (idempotent).
Run from D:/fusion-agent/fusion-agent/:
    venv/Scripts/python.exe db/apply_schema.py

Idempotent (CREATE IF NOT EXISTS, INSERT ... ON CONFLICT DO NOTHING).
"""

import os
import sys
from pathlib import Path

env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

import psycopg2

def apply():
    host     = os.environ.get("DB_HOST", "")
    port     = int(os.environ.get("DB_PORT", "5432"))
    dbname   = os.environ.get("DB_NAME", "postgres")
    user     = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "")

    sql_file = Path(__file__).parent / "schema.sql"
    if not sql_file.exists():
        print(f"ERROR: {sql_file} không tìm thấy")
        sys.exit(1)

    sql = sql_file.read_text(encoding="utf-8")

    sslmode = os.environ.get("DB_SSLMODE", "require")
    print(f"Ket noi {host}:{port}/{dbname} (sslmode={sslmode}) ...")
    conn = psycopg2.connect(
        host=host, port=port, dbname=dbname,
        user=user, password=password,
        sslmode=sslmode, connect_timeout=10,
    )
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
        print("Schema áp thành công (idempotent).")
    except Exception as e:
        conn.rollback()
        print(f"FAIL: {e}")
        sys.exit(1)
    finally:
        conn.close()

    # Verify tables
    conn2 = psycopg2.connect(
        host=host, port=port, dbname=dbname,
        user=user, password=password,
        sslmode=sslmode, connect_timeout=10,
    )
    with conn2.cursor() as cur:
        cur.execute("""
            SELECT table_name,
                   (SELECT COUNT(*) FROM information_schema.columns
                    WHERE table_name = t.table_name AND table_schema = 'public') AS col_count
            FROM information_schema.tables t
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        rows = cur.fetchall()
        print("\nBảng đã tạo:")
        for r in rows:
            print(f"  {r[0]:30s} ({r[1]} cột)")

    # Quick seed check
    with conn2.cursor() as cur:
        cur.execute("SELECT id, detect_mode, on_violation FROM ai_config")
        row = cur.fetchone()
        if row:
            print(f"\nai_config seed: id={row[0]}, detect_mode={row[1]}, on_violation={row[2]}")

        cur.execute("SELECT slug FROM tenants ORDER BY id")
        tenants = [r[0] for r in cur.fetchall()]
        print(f"tenants: {tenants}")

        cur.execute("SELECT doc_id, content_layer FROM rules ORDER BY id")
        rules = [(r[0], r[1]) for r in cur.fetchall()]
        print(f"rules seed: {rules}")

    conn2.close()
    print("\nDone.")

if __name__ == "__main__":
    apply()
