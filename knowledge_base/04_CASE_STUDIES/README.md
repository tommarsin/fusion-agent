# 04 - Case Studies

## Mục đích folder

Lưu trữ **bài học từ sự cố thực tế** - cả trong Game Studio X và rộng hơn trong VNG. Đây là folder **append-only** (chỉ thêm, không xoá - trừ trường hợp cần re-classify hoặc redact nhân sự).

> **Triết lý**: Mỗi case là một bài học đắt giá. Không document = bài học mất đi khi nhân sự cũ rời đi. Document chi tiết = giảm khả năng tái phạm.

---

## Nguyên tắc viết case study

1. **Anonymize khi cần** - không cần dùng tên thật nếu sensitive, dùng role (CTV, Lead, Supervisor)
2. **Đầy đủ 5W1H** - khi nào, ở đâu, ai, làm gì, tại sao, kết quả thế nào
3. **Tách rõ Facts vs Lessons** - sự việc và bài học là 2 phần khác nhau
4. **Link forward** - case này dẫn đến rule mới nào trong Layer 2?
5. **Self-check questions** - giúp người đọc tự phản chiếu

Template chuẩn: `99_TEMPLATES/TEMPLATE_Case_Study.md`

---

## Phân loại case studies

### Theo loại vi phạm
- `data-privacy` - liên quan NĐ13 / privacy
- `content-moderation` - duyệt nội dung sai
- `partner-management` - sự cố với KOL/Brand
- `tournament` - giải đấu vi phạm
- `financial` - trục lợi, hoá đơn khống
- `workplace-conduct` - hành vi không phù hợp
- `crisis-communication` - khủng hoảng truyền thông

### Theo mức độ
- `critical` - dẫn đến thôi việc / kỷ luật nặng / khủng hoảng cấp tập đoàn
- `high` - ảnh hưởng đáng kể (post bị gỡ, fanpage warning, vi phạm pháp luật)
- `medium` - nhỏ hơn nhưng vẫn có bài học
- `low` - lưu để tham khảo

---

## Files dự kiến

| File | Doc ID | Severity | Loại |
|---|---|---|---|
| `001_UGC_Contest_ND13_Violation.md` | GSX-CASE-001 | high | data-privacy |
| `002_Map_Violation_Content_Moderation.md` | GSX-CASE-002 | critical | content-moderation |
| `003_Fraud_FakeInvoice_AbuseOfPower_case.md` | GSX-CASE-003 | critical | financial |
| `004_Crisis_Acquisition_Rumor_case.md` | GSX-CASE-004 | critical | crisis-communication |
| `005_Sexual_Harassment_Workplace_case.md` | GSX-CASE-005 | high | workplace-conduct |
| `006_Regulatory_Inspection_case.md` | GSX-CASE-006 | medium | crisis-communication |
| `007_Media_Attack_Gaming_case.md` | GSX-CASE-007 | medium | crisis-communication |

---

## Đọc case theo role

Khi onboard CTV mới, recommended reading theo thứ tự:

**Day 1 (bắt buộc)**:
1. GSX-CASE-001 (UGC NĐ13) - hiểu data privacy
2. GSX-CASE-002 (Bản đồ) - hiểu content moderation

**Week 1 (recommended)**:
3. GSX-CASE-003 (Hoá đơn khống) - hiểu integrity
4. GSX-CASE-005 (Harassment) - hiểu workplace conduct

**Month 1 (advanced)**:
5. GSX-CASE-004 (Khủng hoảng thâu tóm) - hiểu crisis comm
6. GSX-CASE-006-007 - bối cảnh ngành game

---

## Khi nào thêm case mới?

**BẮT BUỘC document** khi:
- Có vi phạm dẫn đến kỷ luật (mọi cấp)
- Có sự cố cấp 3 trở lên trong escalation chain
- Có phản ánh từ cơ quan chức năng
- Có khủng hoảng truyền thông cấp fanpage/cộng đồng

**Timeline**: document trong **24h** sau khi giải quyết xong sự cố.

**Owner**: Hub Owner + người trực tiếp xử lý case
