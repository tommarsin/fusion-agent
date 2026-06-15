"""
Test Item 3.3 — Authoring Engine + /ingest + /approve
Chạy: python scripts/test_ingest.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.WARNING)

# ── Helpers ───────────────────────────────────────────────────────────────────

PASS = "[PASS]"
FAIL = "[FAIL]"


def ok(label, cond, got=""):
    status = PASS if cond else FAIL
    msg = f"{status} {label}"
    if not cond and got:
        msg += f" | got: {got}"
    print(msg)
    return cond


# ── Test 1: doc_id generation ─────────────────────────────────────────────────

print("\n=== Test 1: doc_id generation ===")
from db.store import get_next_doc_id

did_legal = get_next_doc_id("legal_source", "knowledge_base")
did_op = get_next_doc_id("operating_rule", "knowledge_base")
ok("legal_source prefix GSX-LEGAL", did_legal.startswith("GSX-LEGAL-"), did_legal)
ok("operating_rule prefix GSX-OP", did_op.startswith("GSX-OP-"), did_op)
ok("legal doc_id >= 011", int(did_legal.split("-")[-1]) >= 11, did_legal)
ok("op doc_id >= 014", int(did_op.split("-")[-1]) >= 14, did_op)
print(f"  Generated: {did_legal}, {did_op}")


# ── Test 2: webfetch với text input ──────────────────────────────────────────

print("\n=== Test 2: webfetch ===")
from tools.webfetch import fetch_text

# Test với Meta Ads (site cho phép fetch)
r = fetch_text("https://www.facebook.com/policies/ads/", timeout=15)
ok("Meta Ads fetch success", r["success"], r.get("error"))
ok("Meta Ads raw_text len > 100", len(r.get("raw_text", "")) > 100,
   f"len={len(r.get('raw_text',''))}")
ok("fetched_at present", bool(r.get("fetched_at")))
print(f"  Meta Ads: {len(r.get('raw_text',''))} chars, fetched_at={r.get('fetched_at','')[:25]}")


# ── Test 3: classify_and_extract ─────────────────────────────────────────────

print("\n=== Test 3: classify_and_extract (LLM) ===")
from tools.authoring import classify_and_extract, build_body_md, validate_artifact

ND13_TEXT = """
Nghi dinh 13/2023/ND-CP ve bao ve du lieu ca nhan
Chinh phu ban hanh ngay 17/4/2023, hieu luc 1/7/2023.

Dieu 9: Du lieu ca nhan nhay cam bao gom CCCD, so tai khoan ngan hang,
du lieu y te. Can xu ly can than, can co su dong y ro rang truoc khi thu thap.

Dieu 16: Chu the du lieu co quyen yeu cau xoa du lieu, chinh sua thong tin.
To chuc vi pham co the bi phat den 5% doanh thu hang nam.
"""

extracted = classify_and_extract(ND13_TEXT, "https://thuvienphapluat.vn/nd13")
ok("content_layer = legal_source", extracted.get("content_layer") == "legal_source",
   extracted.get("content_layer"))
ok("title not empty", bool(extracted.get("title")))
ok("priority valid", extracted.get("priority") in ("critical", "high", "medium", "low"),
   extracted.get("priority"))
ok("tags list", isinstance(extracted.get("tags"), list))
ok("summary not empty", bool(extracted.get("summary")))
print(f"  Layer: {extracted.get('content_layer')}, Priority: {extracted.get('priority')}")
print(f"  Title: {extracted.get('title','')[:80]}")


# ── Test 4: build_body_md + validate ──────────────────────────────────────────

print("\n=== Test 4: build_body_md + validate ===")
body_md = build_body_md(extracted)
errors = validate_artifact(extracted, body_md)

ok("body_md len > 200", len(body_md) > 200, f"len={len(body_md)}")
ok("body_md has title header", "# " in body_md)
ok("validate pass (0 errors)", len(errors) == 0, str(errors))


# ── Test 5: full run_authoring_pipeline ───────────────────────────────────────

print("\n=== Test 5: run_authoring_pipeline ===")
from tools.authoring import run_authoring_pipeline

PLATFORM_TEXT = """
Meta Advertising Policies - Prohibited Content
Meta prohibits: gambling and lottery ads without permission, misleading claims,
collection of personal ID documents (passport, national ID, CCCD).
All game ads must comply with Meta Community Standards.
Advertisers targeting Vietnam must follow local advertising laws.
"""

result = run_authoring_pipeline(PLATFORM_TEXT, "https://www.facebook.com/policies/ads/", "knowledge_base")
ok("pipeline success or warnings only", result.get("doc_id") is not None)
ok("doc_id generated", bool(result.get("doc_id")))
ok("content_layer valid", result.get("content_layer") in (
    "legal_source", "operating_rule", "daily_tool", "case_study"))
ok("body_md not empty", len(result.get("body_md", "")) > 50)
print(f"  Result: doc_id={result.get('doc_id')}, layer={result.get('content_layer')}")
print(f"  Success: {result.get('success')}, Errors: {result.get('errors')}")


# ── Test 6: ingest handler (Mod + core → submission) ─────────────────────────

print("\n=== Test 6: ingest handler routing ===")
from tools.ingest import handle_ingest, set_kb_dir

set_kb_dir("knowledge_base")

# 6a: User → 403
status, resp = handle_ingest(
    source="Test nội dung luật",
    scope="core",
    actor_role="User",
)
ok("User → 403", status == 403, f"got {status}")

# 6b: Mod + scope=core → submission pending
status, resp = handle_ingest(
    source=ND13_TEXT,
    scope="core",
    actor_role="Mod",
)
ok("Mod + core → 200", status == 200, f"got {status}, resp={resp}")
ok("Mod + core → submission_id", "submission_id" in resp, str(resp.get("status")))
ok("Mod + core → status=pending", resp.get("status") == "pending")
sub_id = resp.get("submission_id")
print(f"  Submission created: id={sub_id}")

# 6c: Mod + scope=tenant → live rule
status, resp = handle_ingest(
    source=PLATFORM_TEXT,
    scope="tenant",
    actor_role="Mod",
    tenant_id=1,
)
ok("Mod + tenant → 200", status == 200, f"got {status}")
ok("Mod + tenant → rule_id", "rule_id" in resp, str(resp))
ok("Mod + tenant → status=approved", resp.get("status") == "approved")
print(f"  Tenant rule created: doc_id={resp.get('doc_id')}, rule_id={resp.get('rule_id')}")


# ── Test 7: approve handler ───────────────────────────────────────────────────

print("\n=== Test 7: approve handler ===")
from tools.ingest import handle_approve

# 7a: Non-admin → 403
status, resp = handle_approve(sub_id or 1, "approve", "Mod")
ok("Mod approve → 403", status == 403, f"got {status}")

# 7b: Admin approve → rule created + reindex
if sub_id:
    status, resp = handle_approve(sub_id, "approve", "Admin")
    ok("Admin approve → 200", status == 200, f"got {status}, {resp}")
    ok("Admin approve → rule_id", "rule_id" in resp, str(resp))
    ok("Admin approve → reindexed", resp.get("reindexed") is True)
    print(f"  Approved rule: doc_id={resp.get('doc_id')}, rule_id={resp.get('rule_id')}")
else:
    print("[SKIP] sub_id not available")


# ── Test 8: query chatbot về rule vừa approve ─────────────────────────────────

print("\n=== Test 8: chatbot retrieve sau approve ===")
from rag import retriever

chunks = retriever.retrieve("du lieu ca nhan CCCD thu thap", top_k=5)
approved_doc_ids = [c.get("doc_id") for c in chunks]
print(f"  Retrieved doc_ids: {approved_doc_ids}")

# Check nếu có rule từ DB (scope core hoặc tenant) trong kết quả
db_chunks = [c for c in chunks if c.get("source_path") == "db:rules"]
ok("DB rules present in retrieval sau reindex", len(db_chunks) > 0,
   f"db_chunks={len(db_chunks)}, total={len(chunks)}")


# ── Summary ───────────────────────────────────────────────────────────────────

print("\n=== Done ===")
