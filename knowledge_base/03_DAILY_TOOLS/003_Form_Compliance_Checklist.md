---
doc_id: GSX-TOOL-003
title: "Form Compliance Checklist (NĐ13)"
tool_type: checklist
audience: community-team
use_when: Trước khi tạo bất kỳ form thu data (Google Form / Promotion Tool / form đăng ký event)
estimated_time: 5 phút
version: 1.0
last_updated: 2026-06-03
maintained_by: Community Lead + LCCA
related_operating_rules:
  - GSX-OP-001
related_legal_sources:
  - GSX-LEGAL-001
---

# Form Compliance Checklist (NĐ13)

## 🎯 Khi nào dùng tool này?

Trước khi:
- Tạo Google Form thu data user
- Setup Promotion Tool campaign
- Review form đăng ký từ BTC giải đấu bên thứ 3
- Setup form đăng ký event/contest

## ⚡ Cách dùng nhanh

1. **Bước 1**: Xác định loại data (Decision Tree)
2. **Bước 2**: Chọn tool phù hợp (Form vs Promotion Tool)
3. **Bước 3**: Verify 3 element bắt buộc (consent, purpose, retention)
4. **Bước 4**: Cross-check Red Lines
5. Lưu checklist + screenshot form trước go-live

---

## 🔀 BƯỚC 1: Decision Tree - Tool nào dùng?

```
Form có thu loại data nào dưới đây?
│
├── Họ tên thật + email/SĐT/địa chỉ kết hợp
│   └─→ BẮT BUỘC Promotion Tool nội bộ
│
├── CCCD/CMND (số hoặc ảnh)
│   └─→ ❌ KHÔNG ĐƯỢC dùng Google Form
│   └─→ Chỉ Promotion Tool, và chỉ khi value reward > 500k
│   └─→ Cân nhắc: có thực sự cần CCCD không?
│
├── Email + tên IGN (không có tên thật)
│   └─→ Google Form OK (nhưng vẫn cần 3 element bắt buộc)
│
├── IGN, rank, Discord username, server
│   └─→ Google Form OK
│
├── Feedback/survey/vote (không định danh)
│   └─→ Google Form OK
│
└── Ảnh giấy tờ (giấy khen, học bạ, bằng cấp, sổ hộ khẩu...)
    └─→ ❌ TUYỆT ĐỐI KHÔNG (Red Line GSX-OP-007)
```

**Test "Real-world Harm"**: Nếu data leak có thể gây hại cho user ngoài đời thực → Promotion Tool. Không Google Form.

---

## 📋 BƯỚC 2: 3 Element bắt buộc (mọi form)

### 2.1. Consent Checkbox

```
[ ] Có checkbox bắt buộc?
[ ] Checkbox KHÔNG default-checked?
[ ] Checkbox đặt ở ĐẦU form (không cuối form)?
[ ] Text checkbox rõ ràng: "Tôi đã đọc và đồng ý..."?
```

**Template chuẩn**:
> ☐ Tôi đã đọc và đồng ý với [Mục đích thu thập + Cách sử dụng + Thời gian lưu trữ] dữ liệu của tôi.

Xem `GSX-TOOL-009` để có template chi tiết cho từng loại form.

### 2.2. Statement of Purpose

```
[ ] Có nói rõ data dùng cho mục đích cụ thể nào?
[ ] Mục đích KHÔNG dùng từ chung chung ("phục vụ marketing", "phục vụ user")?
[ ] Có nêu tên hoạt động cụ thể?
```

**Bad example**:
> ❌ "Thông tin của bạn sẽ được dùng để phục vụ marketing và các hoạt động liên quan."

**Good example**:
> ✅ "Thông tin của bạn sẽ được dùng để: (1) Xác minh người chiến thắng cuộc thi Wild Rift Cosplay 2026, (2) Liên hệ trao thưởng, (3) Thông báo kết quả qua email."

### 2.3. Deletion Timeline

```
[ ] Có nói rõ data lưu bao lâu?
[ ] Có nói rõ ngày/thời điểm xóa?
[ ] Có kênh để user request xóa sớm?
```

**Template chuẩn**:
> "Thông tin của bạn sẽ được lưu trữ trong [X ngày/tháng] kể từ khi kết thúc hoạt động, sau đó sẽ được xóa hoàn toàn. Bạn có quyền yêu cầu truy cập/sửa/xóa thông tin của mình qua email: [email-support@vnggames.vn]"

**Recommend**: 30 ngày sau khi event/campaign kết thúc.

---

## 🚨 BƯỚC 3: Red Lines Cross-check

```
[ ] Form KHÔNG thu CCCD/CMND (số hoặc ảnh)?
[ ] Form KHÔNG thu họ tên thật + SĐT + email + địa chỉ kết hợp (qua Google Form)?
[ ] Form KHÔNG yêu cầu upload ảnh giấy tờ?
[ ] Form KHÔNG default-checked consent?
[ ] Form CÓ statement of purpose cụ thể?
[ ] Form CÓ deletion timeline?
[ ] Data KHÔNG share với bên thứ 3 không có NDA?
```

Bất kỳ ❌ nào trong 7 items này = **không go-live**, fix trước.

---

## 🔍 BƯỚC 4: Review form BTC bên thứ 3

Khi review form từ BTC giải đấu/event có VNG hỗ trợ:

```
[ ] Yêu cầu BTC gửi link/screenshot form?
[ ] Rà các trường thông tin form đang thu (matrix dưới)?
[ ] Đối chiếu với rule 3.1 (Decision Tree)?
[ ] Nếu BTC thu data nhạy cảm bằng Google Form:
    □ Yêu cầu chuyển tool có compliance đầy đủ?
    □ Yêu cầu loại bỏ các trường định danh?
    □ BTC ký xác nhận tự chịu trách nhiệm pháp lý?
```

**Matrix kiểm tra trường thông tin BTC**:

| Trường BTC thu | Vi phạm NĐ13? | Action |
|---|---|---|
| IGN | ❌ Không | OK |
| Rank | ❌ Không | OK |
| Discord username | ❌ Không | OK |
| Họ tên thật | ⚠️ Risk khi kết hợp | Nên hỏi BTC vì sao cần |
| SĐT | ⚠️ Risk khi kết hợp | Yêu cầu Promotion Tool |
| Email | ⚠️ Risk khi kết hợp | Yêu cầu Promotion Tool |
| CCCD/CMND | ✅ Vi phạm | Yêu cầu remove, nếu cần verify → Promotion Tool |
| Địa chỉ nhà | ✅ Vi phạm | Yêu cầu remove |
| Ảnh giấy tờ | ✅ Vi phạm Red Line | **KHÔNG được approve giải này** |

---

## ✅ Final Sign-off

```
Form created by: ___________________________ Date: ___________
Tool used: □ Google Form  □ Promotion Tool  □ Other: __________
Data classification: □ Public  □ Restricted  □ Internal  □ Confidential
Reviewer: __________________________________ Date: ___________
Lead Approve: ______________________________ Date: ___________

Screenshot form before go-live: [link/path]
Approval email: [link/path]
```

**Lưu vào**: `Drive/Compliance/Forms/[YYYY-MM]_[Form-Name]/checklist-signed.md`

---

## 🚨 Nếu phát hiện vi phạm sau go-live

1. **Dừng form ngay** (close submission)
2. Nếu có data sensitive đã thu: **migrate sang Promotion Tool** trong 24h
3. **DM user đã submit** thông báo + xin lỗi + giải thích
4. Log incident, escalate Lead nếu có CCCD/giấy tờ định danh
5. **Incident report** trong 24h (GSX-TOOL-008)

---

## 🔗 Tham chiếu

- **Rule gốc**: GSX-OP-001 (Data Collection Policy)
- **Legal source**: GSX-LEGAL-001 (NĐ13/2023)
- **Case study minh hoạ**: GSX-CASE-001 (UGC ND13 violation)
- **Template**: GSX-TOOL-009 (Consent Checkbox Templates)

---

## Changelog

| Version | Date | Changed by | Notes |
|---|---|---|---|
| 1.0 | 2026-06-03 | Hub Owner | Initial - codify từ GSX-OP-001 + NĐ13 |
