# -*- coding: utf-8 -*-
"""Full acceptance test cho scanner 4 bước (cần LLM config)."""
import sys, io, os, time, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv()

# Build BM25 index trước
from rag import loader, retriever
from pathlib import Path
KB_DIR = str(Path('.') / 'knowledge_base')
chunks = loader.load_all_chunks(KB_DIR)
retriever.build_index(chunks)
print(f"Index built: {len(chunks)} chunks\n")

from tools.scanner import scan_content

def pretty(result):
    print(f"  VERDICT: {result['verdict']}")
    print(f"  Violations ({len(result['violations'])}):")
    for v in result['violations']:
        print(f"    [{v.get('severity')}] {v.get('rule_doc_id')}: '{v.get('quote','')[:50]}' — {v.get('reason','')[:80]}")
    if result.get('rewrite'):
        print(f"  Rewrite: {result['rewrite'][:150]}...")
    print(f"  Checklist ({len(result.get('checklist',[]))}):")
    for item in result.get('checklist', [])[:5]:
        print(f"    [{item.get('risk')}] {item.get('doc_id')}: {item.get('item','')[:80]}")
    print(f"  Per-platform: {json.dumps(result.get('per_platform',{}), ensure_ascii=False)[:200]}")


# ── TEST 1 ──────────────────────────────────────────────────────────────────
print("="*60)
print("TEST 1: 'Sự kiện LỚN NHẤT năm! Gửi CCCD nhận quà' + [meta]")
print("="*60)
t0 = time.time()
result1 = scan_content(
    content="Sự kiện LỚN NHẤT năm! Gửi CCCD nhận quà",
    platforms=["meta"],
    actor_role="user",
)
elapsed1 = time.time() - t0
pretty(result1)
print(f"  Latency: {elapsed1:.1f}s")
assert result1['verdict'] == 'BLOCKED', f"TEST 1 FAIL: expected BLOCKED got {result1['verdict']}"
assert len(result1['violations']) >= 2, f"TEST 1 FAIL: expected >=2 violations"
assert any(v['rule_doc_id'] == 'GSX-LEGAL-001' for v in result1['violations']), "TEST 1 FAIL: missing CCCD"
assert any(v['rule_doc_id'] == 'GSX-LEGAL-010' for v in result1['violations']), "TEST 1 FAIL: missing superlative"
assert result1.get('rewrite'), "TEST 1 FAIL: missing rewrite"
assert len(result1.get('checklist', [])) > 0, "TEST 1 FAIL: missing checklist"
print("TEST 1 PASS\n")


# ── TEST 2 ──────────────────────────────────────────────────────────────────
print("="*60)
print("TEST 2: Content sach (bao tri server)")
print("="*60)
t0 = time.time()
result2 = scan_content(
    content="Thông báo bảo trì server: Hệ thống sẽ tạm ngưng hoạt động từ 02:00 - 04:00 sáng ngày 16/06. Trân trọng cảm ơn quý khách hàng.",
    platforms=["website"],
    actor_role="user",
)
elapsed2 = time.time() - t0
pretty(result2)
print(f"  Latency: {elapsed2:.1f}s")
assert result2['verdict'] == 'SAFE', f"TEST 2 FAIL: expected SAFE got {result2['verdict']}"
print("TEST 2 PASS\n")


# ── TEST 3 ──────────────────────────────────────────────────────────────────
print("="*60)
print("TEST 3: group vs website — per_platform difference")
print("="*60)
content3 = "Tham gia sự kiện đặc biệt nhất năm tại cộng đồng game của chúng tôi!"
t0 = time.time()
result3_group = scan_content(content=content3, platforms=["group"], actor_role="user")
result3_web = scan_content(content=content3, platforms=["website"], actor_role="user")
elapsed3 = time.time() - t0
print(f"Group verdict: {result3_group['verdict']}")
print(f"  Per-platform: {json.dumps(result3_group.get('per_platform',{}), ensure_ascii=False)}")
print(f"Website verdict: {result3_web['verdict']}")
print(f"  Per-platform: {json.dumps(result3_web.get('per_platform',{}), ensure_ascii=False)}")
print(f"  Latency: {elapsed3:.1f}s")
# per_platform notes phải khác nhau
group_notes = result3_group.get('per_platform', {}).get('group', {}).get('notes', '')
web_notes = result3_web.get('per_platform', {}).get('website', {}).get('notes', '')
assert group_notes != web_notes, f"TEST 3 FAIL: per_platform notes identical"
print("TEST 3 PASS\n")


print("="*60)
print("ALL ACCEPTANCE TESTS PASSED!")
print(f"Latencies: T1={elapsed1:.1f}s  T2={elapsed2:.1f}s  T3={elapsed3:.1f}s")
if max(elapsed1, elapsed2, elapsed3) > 30:
    print("WARNING: Latency > 30s — consider reducing top_k or merging LLM calls")
