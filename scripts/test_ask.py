"""
scripts/test_ask.py — Acceptance test cho item 3.1 (POST /ask).

Chạy: python scripts/test_ask.py [--url http://localhost:8080]

Kiểm tra:
  - 5 câu hỏi compliance (+ doc_id kỳ vọng trong citations)
  - 2 câu hành vi (out-of-scope từ chối, router hướng dẫn /scan)
"""

import argparse
import json
import sys
import urllib.request

BASE_URL = "http://localhost:8080"

# ── Test cases ────────────────────────────────────────────────────────────────
# Mỗi case: (tên, câu hỏi, doc_ids kỳ vọng, kiểm tra trong answer)
TEST_CASES = [
    {
        "name": "TC1 — Thu dữ liệu form đăng ký event",
        "question": "Form đăng ký event thu họ tên + SĐT người chơi cần những gì để đúng luật?",
        "expected_doc_ids": ["GSX-LEGAL-001", "GSX-OP-001"],
        "answer_must_contain": [],
        "answer_must_not_contain": [],
    },
    {
        "name": "TC2 — Từ 'số 1' trong caption quảng cáo",
        "question": "Tôi được dùng từ 'số 1' trong caption quảng cáo không?",
        "expected_doc_ids": ["GSX-LEGAL-010", "GSX-OP-013"],
        "answer_must_contain": [],
        "answer_must_not_contain": [],
    },
    {
        "name": "TC3 — Ảnh có bản đồ Việt Nam",
        "question": "Ảnh có bản đồ Việt Nam thì sao?",
        "expected_doc_ids": ["GSX-OP-002"],
        "answer_must_contain": ["BLOCKED", "tuyệt đối"],
        "answer_must_not_contain": [],
    },
    {
        "name": "TC4 — KOL approval",
        "question": "Mời KOL quảng bá giải đấu cần approval của ai?",
        "expected_doc_ids": ["GSX-OP-003"],
        "answer_must_contain": [],
        "answer_must_not_contain": [],
    },
    {
        "name": "TC5 — Giải đấu cộng đồng Riot policy",
        "question": "Tổ chức giải đấu cộng đồng cần check policy gì của Riot?",
        "expected_doc_ids": ["GSX-OP-009"],
        "answer_must_contain": [],
        "answer_must_not_contain": [],
    },
    {
        "name": "TC6 (hành vi) — Out-of-scope: giá vàng",
        "question": "giá vàng hôm nay?",
        "expected_doc_ids": [],
        "answer_must_contain": ["ngoài phạm vi"],
        "answer_must_not_contain": [],
        "behavior_check": "refuse",
    },
    {
        "name": "TC7 (hành vi) — Router: có content muốn kiểm tra",
        "question": "Tôi có content muốn kiểm tra thì làm gì?",
        "expected_doc_ids": [],
        "answer_must_contain": ["/scan"],
        "answer_must_not_contain": [],
        "behavior_check": "router",
    },
]


# ── HTTP helper ───────────────────────────────────────────────────────────────

def post_ask(base_url: str, question: str, role: str = "user") -> dict:
    url = f"{base_url}/ask"
    payload = json.dumps({"question": question}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "X-Role": role},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ── Runner ────────────────────────────────────────────────────────────────────

def run_tests(base_url: str) -> None:
    passed = 0
    failed = 0

    print(f"\n{'=' * 65}")
    print(f"  GameLaw AI Agent — Acceptance Test: POST /ask")
    print(f"  Endpoint: {base_url}/ask")
    print(f"{'=' * 65}\n")

    for tc in TEST_CASES:
        name = tc["name"]
        question = tc["question"]
        expected_ids = tc.get("expected_doc_ids", [])
        must_contain = tc.get("answer_must_contain", [])

        print(f"▶ {name}")
        print(f"  Q: {question}")

        try:
            result = post_ask(base_url, question)
        except Exception as e:
            print(f"  ✗ HTTP error: {e}\n")
            failed += 1
            continue

        answer = result.get("answer", "")
        citations = result.get("citations", [])
        cited_ids = [c["doc_id"] for c in citations]

        print(f"  Answer (100 chars): {answer[:100]}...")
        print(f"  Citations: {cited_ids}")

        errors = []

        # Kiểm tra doc_ids kỳ vọng
        for doc_id in expected_ids:
            if doc_id not in cited_ids and doc_id not in answer:
                errors.append(f"doc_id kỳ vọng '{doc_id}' không có trong citations hoặc answer")

        # Kiểm tra answer contains
        for phrase in must_contain:
            if phrase.lower() not in answer.lower():
                errors.append(f"answer không chứa cụm '{phrase}'")

        # Kiểm tra disclaimer
        if "tư vấn pháp lý" not in answer.lower() and tc.get("behavior_check") != "refuse":
            errors.append("Thiếu disclaimer 'không phải tư vấn pháp lý chính thức'")

        if errors:
            for err in errors:
                print(f"  ✗ {err}")
            print()
            failed += 1
        else:
            print("  ✓ PASS\n")
            passed += 1

    print(f"{'=' * 65}")
    print(f"  Kết quả: {passed}/{len(TEST_CASES)} PASSED, {failed} FAILED")
    print(f"{'=' * 65}\n")

    if failed > 0:
        sys.exit(1)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Acceptance test cho /ask endpoint")
    parser.add_argument("--url", default=BASE_URL, help="Base URL của agent (mặc định: http://localhost:8080)")
    args = parser.parse_args()
    run_tests(args.url)
