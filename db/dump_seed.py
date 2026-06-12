"""Dump seed data từ vDB để đồng bộ với schema.sql."""
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

with conn.cursor() as cur:
    print("=== TENANTS ===")
    cur.execute("SELECT id, name, slug FROM tenants ORDER BY id")
    for r in cur.fetchall():
        print(r)

    print("\n=== CAMPAIGNS ===")
    cur.execute("SELECT id, tenant_id, name, platforms, period, status FROM campaigns ORDER BY id")
    for r in cur.fetchall():
        print(r)

    print("\n=== RULES (core) ===")
    cur.execute(
        "SELECT doc_id, content_layer, scope, platforms, status, title, source_url, version "
        "FROM rules WHERE scope='core' ORDER BY id"
    )
    for r in cur.fetchall():
        print(r)

    print("\n=== AI_CONFIG ===")
    cur.execute("SELECT * FROM ai_config")
    print(cur.fetchone())

conn.close()
