---
doc_id: GSX-TOOL-002
title: "UGC Event Compliance Checklist"
tool_type: checklist
audience: community-team
use_when: Trước khi go-live UGC contest hoặc event yêu cầu user upload content
estimated_time: 10 phút
version: 1.0
last_updated: 2026-06-03
maintained_by: Community Lead
related_operating_rules:
  - GSX-OP-001
  - GSX-OP-007
related_case_studies:
  - GSX-CASE-001
---

# UGC Event Compliance Checklist

## 🎯 Khi nào dùng tool này?

Trước khi go-live UGC contest hoặc event yêu cầu user:
- Upload ảnh, video, fan art
- Comment + tag bạn
- Tham gia challenge (cosplay, gameplay, story)
- Submit content cho judging

## ⚡ Cách dùng nhanh

1. Đi qua 4 stage check theo thứ tự
2. **Stage 1 - Red Line: FAIL = không triển khai contest** (redesign)
3. Stage 2-4: fix các item ❌ trước go-live
4. Submit Lead approve cùng checklist này
5. Sau go-live: dùng lào template tracking moderation 24h

---

## 📋 4 Stage Check

### 🛑 STAGE 1 - RED LINE (Critical - không exception)

**Nếu BẤT KỲ item nào dưới đây = CÓ → DỪNG, redesign concept**

```
[ ] Event yêu cầu user đăng giấy tờ tùy thân (CCCD/CMND/passport)?
[ ] Event yêu cầu user đăng giấy khen/bằng/chứng nhận có thông tin định danh?
[ ] Event yêu cầu user đăng giấy nhập học/giấy báo trúng tuyển/học bạ?
[ ] Event yêu cầu user đăng sổ hộ khẩu/giấy khai sinh?
[ ] Event yêu cầu user đăng ảnh chân dung kèm thông tin định danh cá nhân?
[ ] Event yêu cầu user đăng hóa đơn/biên lai/vé có tên thật + thông tin cá nhân?
```

❌ Nếu CÓ bất kỳ item nào: **Concept vi phạm Red Line, không được triển khai.**
- Thay bằng UGC creative (gameplay, fan art, cosplay theo skin gốc, story text-only)
- Tham khảo Case Study GSX-CASE-001 để hiểu hậu quả

---

### 📝 STAGE 2 - Loại UGC (Verify scope)

```
[ ] Loại UGC nào? Tick chính xác:
    □ Creative gameplay content (highlight, screenshot, build)
    □ Fan art / cosplay (theo skin gốc tướng)
    □ Story & testimonial (text only)
    □ Meme & humor
    □ Khác: _______________ (cần escalate Lead)

[ ] Nếu user upload ảnh đời thực → vẫn chạy Content Scanner 7 bước (GSX-TOOL-005)?
[ ] Nếu là cosplay → có trung thành với skin gốc tướng không? (skip nếu không phải cosplay)
```

---

### 🛡️ STAGE 3 - Compliance Setup

#### 3.1. Cảnh báo bảo vệ data
```
[ ] Cảnh báo "Không đăng giấy tờ cá nhân" có ở CAPTION CHÍNH (dòng 1-3)?
[ ] Cảnh báo có ở VISUAL THỂ LỆ (banner)?
[ ] KHÔNG đặt cảnh báo chỉ ở comment phụ?
[ ] KHÔNG đặt cảnh báo chỉ ở link out?
```

#### 3.2. Thể lệ rõ ràng
```
[ ] Thể lệ nêu rõ: loại content được phép submit
[ ] Thể lệ nêu rõ: loại content KHÔNG được submit (red line)
[ ] Thể lệ nêu rõ: tiêu chí chấm
[ ] Thể lệ nêu rõ: timeline (start, end, công bố kết quả)
[ ] Thể lệ nêu rõ: phần thưởng cụ thể
[ ] Thể lệ có disclaimer quyền tác giả (UGC clause)?
```

#### 3.3. Phần thưởng & risk
```
[ ] Phần thưởng là in-game items? → Low risk
[ ] Phần thưởng gift card/voucher giá trị nhỏ (< 500k)? → Medium risk
[ ] Phần thưởng > 500k? → BẮT BUỘC dùng Promotion Tool verify (xem GSX-OP-001)
```

#### 3.4. Form/process thu winner info (sau khi có kết quả)
```
[ ] Form chỉ thu data tối thiểu cần để trao thưởng?
[ ] Form không thu CCCD ở giai đoạn early-screening?
[ ] Có consent checkbox bắt buộc?
[ ] Có purpose statement rõ ràng?
[ ] Có deletion timeline?
```

---

### 👁️ STAGE 4 - Plan Moderation 24h

#### 4.1. Assignment
```
[ ] Có người chính + người backup được assign moderate?
[ ] Lịch trực rõ ràng (ai trực giờ nào)?
[ ] Lead có thông tin lịch trước go-live?
```

#### 4.2. SLA & process
```
[ ] Spot-check mỗi 4-6 tiếng trong 24h đầu? (TỐI THIỂU)
[ ] Action plan khi phát hiện vi phạm:
    □ Ai có quyền hide/delete post user?
    □ Ai có quyền ban user vi phạm repeat?
    □ Threshold escalate Lead là gì?
[ ] Có template DM gửi user khi yêu cầu xóa post sai?
```

#### 4.3. Auto-monitor (nếu có)
```
[ ] Keyword scan ("CCCD", "giấy tờ", "ảnh cá nhân") đã setup?
[ ] Có report tổng kết hàng ngày trong 7 ngày đầu?
```

---

## ✅ Final Sign-off

Sau khi pass 4 stage:

```
Designer: ___________________________ Date: ___________
Reviewer (mandatory 2nd-eye): _______________________ Date: ___________
Lead Approve: _______________________ Date: ___________

Comment/notes:
_____________________________________________________
_____________________________________________________
```

**Lưu checklist này vào**: `Drive/Compliance/UGC-Events/[YYYY-MM]_[Event-Name]/checklist-signed.md`

---

## 🚨 Nếu phát hiện vi phạm sau go-live

1. **Hide/Delete post user vi phạm NGAY**
2. **DM user**: hướng dẫn submit lại đúng format
3. **Log incident**: `Drive/Compliance/UGC-Events/[Event]/incidents.log`
4. **Nếu lộ data nhạy cảm (CCCD, SĐT) → escalate Crisis Playbook** (GSX-OP-010)
5. **Trong 24h sau giải quyết**: viết Incident Report (GSX-TOOL-008)

---

## 🔗 Tham chiếu

- **Rule gốc**: GSX-OP-007 (UGC Event Rules), GSX-OP-001 (Data Collection)
- **Case study minh hoạ**: GSX-CASE-001 (UGC ND13 violation - đọc trước khi thiết kế contest đầu tiên)
- **Tool liên quan**: GSX-TOOL-003 (Form Compliance), GSX-TOOL-009 (Consent Templates)

---

## Changelog

| Version | Date | Changed by | Notes |
|---|---|---|---|
| 1.0 | 2026-06-03 | Hub Owner | Initial - codify từ Case Study GSX-CASE-001 |
