"""Smoke test for Item 3.4 — POST /checklist (generate_checklist standalone)."""
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Ensure project root on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.checklist import generate_checklist

print("=== TEST 1: standalone /checklist (meta + tiktok, no violations) ===")
ctx = {
    "content": "Tham gia giai dau Wild Rift mua giai moi. Dang ky ngay!",
    "platforms": ["meta", "tiktok"],
    "violations": [],
    "activity_description": "Quang ba giai dau esports",
    "tenant_id": None,
    "chunks": [],
    "_extra_items": [],  # bypass LLM
}
result = generate_checklist(ctx)
print(f"  Checklist items: {len(result)}")
for item in result[:6]:
    print(f"  [{item['risk']}] {item['item'][:70]}")

assert len(result) >= 5, "expected >= 5 items"
assert any("meta" in item["doc_id"].lower() or "PLAT-001" in item["doc_id"] for item in result), "expected meta-specific item"
assert any("PLAT-002" in item["doc_id"] for item in result), "expected tiktok-specific item"
print("  PASS\n")

print("=== TEST 2: /checklist with violations (violations become first items) ===")
ctx2 = {
    "content": "Lien he 123456789012 de nhan thuong",
    "platforms": ["website"],
    "violations": [
        {"rule_doc_id": "GSX-LEGAL-001", "quote": "123456789012", "reason": "Co the la so CCCD", "severity": "redline"}
    ],
    "activity_description": "",
    "tenant_id": None,
    "chunks": [],
    "_extra_items": [],
}
result2 = generate_checklist(ctx2)
print(f"  Checklist items: {len(result2)}")
print(f"  First item: {result2[0]['item'][:80]}")
assert result2[0]["doc_id"] == "GSX-LEGAL-001", "violation item should be first"
assert result2[0]["risk"] == "high"
print("  PASS\n")

print("=== TEST 3: /checklist store platform ===")
ctx3 = {
    "content": "Download game ngay de nhan qua",
    "platforms": ["store"],
    "violations": [],
    "activity_description": "",
    "tenant_id": None,
    "chunks": [],
    "_extra_items": [],
}
result3 = generate_checklist(ctx3)
has_store = any("PLAT-004" in item["doc_id"] for item in result3)
print(f"  Store items found: {has_store}")
assert has_store, "expected store-specific items"
print("  PASS\n")

print("All tests PASSED")
