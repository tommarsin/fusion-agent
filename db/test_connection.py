"""
Quick connection test for VNG Cloud vDB (Postgres).
Run from D:/fusion-agent/fusion-agent/:
    venv/Scripts/python.exe db/test_connection.py

Đọc credentials từ .env (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD).
Thử kết nối, chạy SELECT 1, in kết quả.
"""

import os
import sys
from pathlib import Path

# Load .env từ project root
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

import psycopg2

def test():
    host     = os.environ.get("DB_HOST", "")
    port     = int(os.environ.get("DB_PORT", "5432"))
    dbname   = os.environ.get("DB_NAME", "postgres")
    user     = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "")

    sslmode = os.environ.get("DB_SSLMODE", "require")

    if not host:
        print("ERROR: DB_HOST chưa được set trong .env")
        sys.exit(1)
    if not password:
        print("ERROR: DB_PASSWORD chưa được set trong .env")
        sys.exit(1)

    print(f"Đang kết nối tới {host}:{port}/{dbname} (user={user}, sslmode={sslmode}) ...")
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            sslmode=sslmode,
            connect_timeout=10,
        )
        cur = conn.cursor()
        cur.execute("SELECT 1 AS ping, version() AS pg_version")
        row = cur.fetchone()
        print(f"OK: ping={row[0]}")
        print(f"PostgreSQL version: {row[1]}")
        cur.close()
        conn.close()
        print("Kết nối thành công!")
        return True
    except Exception as e:
        print(f"FAIL: {e}")
        print()
        print("Gợi ý xử lý:")
        print("  - 'connection refused' → kiểm tra public endpoint đã bật chưa")
        print("  - 'SSL required'       → thêm ?sslmode=require (đã có trong script)")
        print("  - 'password auth fail' → kiểm tra DB_PASSWORD trong .env")
        print("  - 'timeout'            → kiểm tra IP whitelist / security group")
        return False

if __name__ == "__main__":
    ok = test()
    sys.exit(0 if ok else 1)
