"""
Test Item 3.5 — Role gate middleware + Audit log
Kiểm tra 18 ô ma trận quyền + audit_log ghi đủ trường.

Chạy: venv/Scripts/python.exe scripts/test_role_gate.py
(cần server KHÔNG chạy — test trực tiếp middleware logic)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.WARNING)

PASS = "[PASS]"
FAIL = "[FAIL]"
results = []


def ok(label, cond, got=""):
    status = PASS if cond else FAIL
    msg = f"{status} {label}"
    if not cond and got:
        msg += f"  | got: {got}"
    print(msg)
    results.append(cond)
    return cond


# ── 1: normalize_role ─────────────────────────────────────────────────────────

print("\n=== Test 1: normalize_role ===")
from tools.role_gate import normalize_role

ok("admin → Admin", normalize_role("admin") == "Admin")
ok("Mod → Mod", normalize_role("Mod") == "Mod")
ok("USER → User", normalize_role("USER") == "User")
ok("None → User", normalize_role(None) == "User")
ok("garbage → User", normalize_role("hacker") == "User")


# ── 2: Permission matrix (18 cells) ──────────────────────────────────────────

print("\n=== Test 2: Permission matrix ===")
from tools.role_gate import _ROLE_RANK, _MIN_RANK


def check_access(role: str, path: str) -> bool:
    """True = allowed, False = blocked (403)."""
    rank = _ROLE_RANK.get(normalize_role(role), 0)
    min_rank = _MIN_RANK.get(path, 0)
    return rank >= min_rank


# open endpoints (all roles: 200)
for path in ["/ask", "/scan", "/checklist"]:
    for role in ["User", "Mod", "Admin"]:
        ok(f"{role} → {path} = allowed", check_access(role, path))

# /ingest: User → 403; Mod, Admin → allowed
ok("User → /ingest = blocked", not check_access("User", "/ingest"))
ok("Mod  → /ingest = allowed", check_access("Mod", "/ingest"))
ok("Admin → /ingest = allowed", check_access("Admin", "/ingest"))

# /approve: User, Mod → 403; Admin → allowed
ok("User → /approve = blocked", not check_access("User", "/approve"))
ok("Mod  → /approve = blocked", not check_access("Mod", "/approve"))
ok("Admin → /approve = allowed", check_access("Admin", "/approve"))

# /audit: User, Mod → 403; Admin → allowed
ok("User → /audit = blocked", not check_access("User", "/audit"))
ok("Mod  → /audit = blocked", not check_access("Mod", "/audit"))
ok("Admin → /audit = allowed", check_access("Admin", "/audit"))

# Total so far: 18 cells ✓


# ── 3: ensure_checklist_action + list_audit_log ───────────────────────────────

print("\n=== Test 3: DB functions ===")
from db.store import ensure_checklist_action, list_audit_log, insert_audit

ensure_checklist_action()
ok("ensure_checklist_action runs without exception", True)

# Check 'checklist' in enum
try:
    from db.store import _get_conn
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM pg_enum "
        "WHERE enumtypid = 'audit_action_enum'::regtype AND enumlabel = 'checklist'"
    )
    row = cur.fetchone()
    cur.close(); conn.close()
    ok("'checklist' in audit_action_enum", row is not None)
except Exception as e:
    ok("'checklist' in audit_action_enum", False, str(e))

# list_audit_log returns list
entries = list_audit_log(limit=5)
ok("list_audit_log returns list", isinstance(entries, list))

# Each entry has required fields
if entries:
    entry = entries[0]
    ok("audit entry has actor_role", "actor_role" in entry)
    ok("audit entry has action", "action" in entry)
    ok("audit entry has summary", "summary" in entry)
    ok("audit entry has created_at", "created_at" in entry)
    print(f"  Sample entry: role={entry.get('actor_role')}, action={entry.get('action')}, "
          f"ts={str(entry.get('created_at',''))[:19]}")
else:
    print("  (No entries yet — skipping field checks)")

# Write a 'checklist' audit entry
try:
    insert_audit(
        actor_role="User",
        action="checklist",
        summary="test 3.5 — checklist audit write",
        verdict="ok",
    )
    ok("insert_audit with action='checklist' OK", True)
except Exception as e:
    ok("insert_audit with action='checklist' OK", False, str(e))


# ── 4: GET /audit returns data ────────────────────────────────────────────────

print("\n=== Test 4: list_audit_log content ===")
entries_after = list_audit_log(limit=10)
checklist_entries = [e for e in entries_after if e.get("action") == "checklist"]
ok("checklist audit entry persisted", len(checklist_entries) > 0,
   f"found {len(checklist_entries)}")
print(f"  Total entries in DB (limit 10): {len(entries_after)}")


# ── Summary ───────────────────────────────────────────────────────────────────

passed = sum(results)
total = len(results)
print(f"\n=== Done: {passed}/{total} passed ===")
if passed < total:
    sys.exit(1)
