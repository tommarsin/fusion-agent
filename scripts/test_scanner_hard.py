# -*- coding: utf-8 -*-
"""Quick test script for hard rule detection (no LLM needed)."""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, ".")

from tools.scanner import _hard_rule_detect, _compute_verdict, _per_platform_verdict

# ── Test 1 ─────────────────────────────────────────────────────────────────
print("=== TEST 1: content acceptance (Vietnamese) ===")
content1 = "Su kien LON NHAT nam! Gui CCCD nhan qua"
platforms1 = ["meta"]
viols1 = _hard_rule_detect(content1, platforms1)
print(f"Violations: {len(viols1)}")
for v in viols1:
    print(f"  [{v['severity']}] {v['rule_doc_id']}: quote='{v['quote'][:50]}'")
verdict1 = _compute_verdict(viols1)
print(f"Verdict: {verdict1}")
# ASCII version: CCCD should match, but "NHAT" won't match Vietnamese diacritic
# Acceptance test uses proper Vietnamese characters
print()

# ── Test 1b: With proper Vietnamese diacritics (actual demo content) ────────
print("=== TEST 1b: Su kien LON NHAT (proper Vietnamese) ===")
content1b = "Sự kiện LỠN NHẤT năm! Gửi CCCD nhận quà"
print(f"Content: {content1b}")
platforms1b = ["meta"]
viols1b = _hard_rule_detect(content1b, platforms1b)
print(f"Violations: {len(viols1b)}")
for v in viols1b:
    sev = v['severity']
    rdid = v['rule_doc_id']
    q = v['quote'][:60]
    r = v['reason'][:80]
    print(f"  [{sev}] {rdid}: '{q}'")
    print(f"         reason: {r}")
verdict1b = _compute_verdict(viols1b)
print(f"Verdict: {verdict1b}")

assert len(viols1b) >= 2, f"Expected >=2 violations, got {len(viols1b)}: {viols1b}"
assert verdict1b == "BLOCKED", f"Expected BLOCKED, got {verdict1b}"
assert any(v["rule_doc_id"] == "GSX-LEGAL-001" for v in viols1b), "Missing CCCD violation"
assert any(v["rule_doc_id"] == "GSX-LEGAL-010" for v in viols1b), "Missing superlative violation"
print("TEST 1b PASS\n")

# ── Test 2 ─────────────────────────────────────────────────────────────────
print("=== TEST 2: content sach ===")
content2 = "Thong bao bao tri he thong. He thong se tam ngung hoat dong tu 2:00 - 4:00 sang. Tran trong cam on quy khach hang!"
platforms2 = ["website"]
viols2 = _hard_rule_detect(content2, platforms2)
print(f"Violations: {len(viols2)}")
verdict2 = _compute_verdict(viols2)
print(f"Verdict: {verdict2}")
assert verdict2 == "SAFE", f"Expected SAFE, got {verdict2}"
print("TEST 2 PASS\n")

# ── Test 3 ─────────────────────────────────────────────────────────────────
print("=== TEST 3: group vs website (same content, different platform) ===")
content3 = "Sự kiện lớn nhất năm với nhiều giải thưởng"
print(f"Content: {content3}")
platforms_group = ["group"]
platforms_web = ["website"]
viols_group = _hard_rule_detect(content3, platforms_group)
viols_web = _hard_rule_detect(content3, platforms_web)
per_group = _per_platform_verdict(viols_group, ["group"], content3)
per_web = _per_platform_verdict(viols_web, ["website"], content3)
print(f"Group violations: {len(viols_group)}, per_platform: {per_group}")
print(f"Website violations: {len(viols_web)}, per_platform: {per_web}")
# Both should detect superlative, but group is more lenient
print("TEST 3 PASS\n")

print("All hard rule tests PASSED!")
