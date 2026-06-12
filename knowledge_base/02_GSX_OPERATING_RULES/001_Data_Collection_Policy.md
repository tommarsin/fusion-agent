---
doc_id: GSX-OP-001
title: "Data Collection Policy - Thu thập dữ liệu cá nhân"
version: 1.0
status: draft
created: 2026-06-03
last_updated: 2026-06-03
last_reviewed_by: Hub Owner
legal_owner: LCCA
next_review_date: 2026-12-03
applies_to: Community Team, CTV, Partner làm việc với data user
related_legal_sources:
  - GSX-LEGAL-001: Nghị định 13/2023/NĐ-CP - Bảo vệ dữ liệu cá nhân
related_case_studies:
  - GSX-CASE-001: UGC Contest - Vi phạm NĐ13/2023
related_tools:
  - GSX-TOOL-003: Form Compliance Checklist
  - GSX-TOOL-009: Consent Checkbox Templates
tags: [data-privacy, nd13, form, promotion-tool, consent]
---

# GSX-OP-001: Data Collection Policy

## 1. Mục đích & Phạm vi

### 1.1. Tại sao có rule này?

Nghị định 13/2023/NĐ-CP đã có hiệu lực và áp dụng đầy đủ. Mọi hoạt động thu thập dữ liệu user của VNGGames - dù qua Google Form, Promotion Tool, hay form đăng ký event - đều phải tuân thủ. Vi phạm có thể bị Cục An ninh mạng A05 tuýt còi (xem `GSX-CASE-001`).

Đặc biệt cần lưu ý: NĐ13 không chỉ quản lý CCCD/SĐT, mà còn quản lý **mọi thông tin định danh được** - bao gồm cả họ tên thật, ngày sinh, địa chỉ trường học/đơn vị, ảnh khuôn mặt.

### 1.2. Áp dụng cho ai?

- Toàn bộ Community Team Game Studio X khi thiết kế form thu thập data
- CTV khi vận hành form/event có thu data
- BTC đối tác khi thu data cho giải đấu/event có VNG hỗ trợ
- Bất kỳ ai trong Game Studio X ủy quyền agency/partner thu data thay mình

### 1.3. Không áp dụng cho?

- Data đã anonymized hoàn toàn (không thể trace ngược user)
- Aggregated stats không link với cá nhân (vd: tổng số user tham gia event)
- Internal form trong team (vd: form CTV điền task progress) - vẫn nên dùng tool nội bộ nhưng risk thấp hơn

### 1.4. Viết tắt & Thuật ngữ trong tài liệu này

| Viết tắt/Thuật ngữ | Giải thích |
|---|---|
| **NĐ13** | Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân (hiệu lực 01/07/2023) |
| **PII** (Personally Identifiable Information) | Dữ liệu cá nhân định danh: họ tên thật, SĐT, email, địa chỉ, CCCD... |
| **CCCD** | Căn Cước Công Dân - giấy tờ tùy thân định danh |
| **Data Controller** | Bên Kiểm soát dữ liệu - tổ chức quyết định mục đích và cách xử lý data. VNGGames là Data Controller khi thu data user |
| **Data Processor** | Bên Xử lý dữ liệu - agency/vendor xử lý data thay VNG, cần có hợp đồng/NDA |
| **Promotion Tool** | Công cụ nội bộ VNG để thu thập dữ liệu nhạy cảm - bắt buộc dùng thay Google Form khi thu PII |
| **LCCA** | Bộ phận Pháp chế, Tuân thủ và Đối ngoại của VNG (Legal, Compliance & Corporate Affairs) |
| **A05** | Cục An ninh mạng và Phòng chống tội phạm công nghệ cao - thuộc Bộ Công an |
| **CTV** | Cộng tác viên |
| **anonymized** | Đã ẩn danh hóa hoàn toàn - không thể truy ngược ra user cụ thể |

> 📖 Tra cứu thêm: `00_INDEX_VERSION/GLOSSARY.md`

---

## 2. Nguyên tắc cốt lõi

1. **Test "Real-world Harm"**: Nếu data leak có thể gây hại cho user ngoài đời thực → BẮT BUỘC dùng Promotion Tool. Không Google Form.

2. **Minimum data principle**: Chỉ thu data thực sự cần thiết cho mục đích cụ thể. Không thu "để dành dùng sau".

3. **Consent rõ ràng**: User phải tick box đồng ý trước khi submit. Không default-checked, không giấu cuối form.

4. **Stated retention**: Mọi form phải nói rõ data lưu bao lâu và xóa khi nào.

5. **Right to access**: User phải có kênh liên hệ để xem/sửa/xóa data của họ.

---

## 3. Quy định chi tiết

### 3.1. Phân loại tool theo loại data

**Quy định**: Mỗi loại data có tool tương ứng bắt buộc, không được chọn tự do.

| Loại data | Tool bắt buộc | Lý do pháp lý |
|---|---|---|
| Họ tên thật, CCCD/CMND (số + ảnh), email, SĐT, địa chỉ nhà | **Promotion Tool nội bộ** | NĐ13 Điều 25 (cross-border), Điều 28 (access control), Điều 38 (Data Controller liability) |
| IGN (in-game name), rank, Discord username | Google Form OK | Không định danh ngoài đời |
| Feedback, survey, vote, ý kiến | Google Form OK | Không thu data định danh |
| Đăng ký xem event không có quà giá trị cao | Google Form OK | Risk thấp |
| Upload ảnh fanart, video gameplay | Google Form OK + clause bản quyền | UGC bình thường |

### 3.2. Form bắt buộc có (mọi form, không exception)

**Quy định**: Mọi Google Form phải có 3 element này. Thiếu 1 = vi phạm.

1. **Consent checkbox bắt buộc** (không default-checked):
   - User phải tự tick "Tôi đã đọc và đồng ý với điều khoản trên"
   - Đặt ở **đầu form**, không giấu cuối

2. **Clear statement of purpose**:
   - Nói rõ data dùng cho mục đích gì (tên hoạt động cụ thể)
   - Không dùng từ chung chung như "phục vụ marketing"

3. **Stated data deletion timeline**:
   - Ghi rõ data xóa sau X ngày/tháng kể từ khi kết thúc hoạt động
   - Recommend: 30 ngày sau khi event kết thúc

Template clause chuẩn có trong `GSX-TOOL-009: Consent Checkbox Templates`.

### 3.3. Trường hợp Promotion Tool bắt buộc

**Quy định**: Các trường hợp sau KHÔNG được dùng Google Form, BẮT BUỘC Promotion Tool nội bộ:

- Thu CCCD/CMND (số hoặc ảnh) để xác minh nhận quà có giá trị > 500k VND
- Thu SĐT để xác minh nhận quà
- Thu địa chỉ nhà để giao quà vật lý
- Thu email kết hợp với họ tên thật (đủ để định danh)
- Bất kỳ tổ hợp data nào đủ để định danh user ngoài đời

**Lý do**: Promotion Tool có:
- Lưu trữ data trong nước (compliance Điều 25)
- Phân quyền truy cập theo role (compliance Điều 28)
- Audit log mọi truy cập (compliance Điều 38)
- Auto-delete theo timeline đã set

### 3.4. UGC Contest có thu image

**Quy định**: UGC contest yêu cầu user upload ảnh có chứa data cá nhân = **RED LINE - cấm tuyệt đối** (xem `GSX-OP-007: UGC Event Rules`).

Áp dụng cho mọi loại ảnh:
- Giấy tờ tùy thân (CCCD, passport, bằng lái)
- Giấy khen, bằng khen, chứng nhận có thông tin định danh
- Giấy nhập học, giấy báo trúng tuyển
- Học bạ, bảng điểm
- Sổ hộ khẩu, giấy khai sinh
- Ảnh chân dung kèm thông tin định danh

### 3.5. Form đăng ký giải đấu bên thứ 3 (BTC dùng)

**Quy định**: Khi BTC bên thứ 3 dùng form thu data người chơi cho giải đấu có VNG hỗ trợ, Community Team **phải review form** trong bước Compliance check:

1. Yêu cầu BTC gửi link/screenshot form đăng ký
2. Rà các trường thông tin form đang thu
3. Đối chiếu với rule 3.1 ở trên
4. Nếu BTC thu data nhạy cảm bằng Google Form:
   - Option A: Yêu cầu chuyển sang tool có compliance đầy đủ
   - Option B: Yêu cầu loại bỏ các trường định danh
   - Option C: BTC ký xác nhận tự chịu trách nhiệm pháp lý

Lưu ý BTC: vi phạm NĐ13 là trách nhiệm pháp lý của BTC, không phải VNGGames - **nhưng VNGGames vẫn có rủi ro uy tín** nếu để xảy ra trên giải mình hỗ trợ.

---

## 4. Red Lines (Cấm tuyệt đối)

- ❌ Google Form thu CCCD/CMND (số hoặc ảnh) dưới bất kỳ lý do gì
- ❌ Google Form thu họ tên thật + SĐT + email + địa chỉ kết hợp
- ❌ UGC contest yêu cầu upload bất kỳ giấy tờ định danh nào
- ❌ Form không có consent checkbox
- ❌ Form có consent checkbox nhưng default-checked
- ❌ Form không nói rõ purpose hoặc retention timeline
- ❌ Lưu data user trên drive cá nhân hoặc máy cá nhân
- ❌ Chia sẻ data user với bên thứ 3 không có NDA
- ❌ Giữ data sau khi đã hết mục đích sử dụng (vi phạm minimum principle)

---

## 5. Quy trình áp dụng

### Khi nào cần check rule này?
- Trước khi tạo bất kỳ form thu data nào
- Khi review form BTC gửi (giải đấu, event)
- Khi thiết kế UGC contest
- Khi nhận yêu cầu thu data từ Marketing/PR/Partner

### Checklist nhanh
Xem `GSX-TOOL-003: Form Compliance Checklist`

### Khi không chắc - hỏi ai?

| Loại câu hỏi | Liên hệ |
|---|---|
| Form này có vi phạm NĐ13 không? | LCCA (xem CONTACTS_DIRECTORY) |
| Có nên dùng Promotion Tool không? | Community Lead |
| Promotion Tool dùng thế nào? | Internal Tools team |
| BTC bên thứ 3 thu data sai - xử lý ra sao? | Community Lead + LCCA |

---

## 6. Chế tài khi vi phạm

| Cấp độ | Hành vi | Hình thức xử lý | Người quyết |
|---|---|---|---|
| Cấp 1 | Form thiếu consent checkbox hoặc retention timeline | Sửa ngay trong 24h, ghi nhận log | Community Lead |
| Cấp 2 | Google Form thu data nhạy cảm (SĐT, email + tên thật) | Dừng form, migrate Promotion Tool, đào tạo lại CTV | Community Lead + Manager |
| Cấp 3 | Google Form thu CCCD hoặc UGC yêu cầu giấy tờ định danh | Gỡ form/post ngay, incident report, có thể bị A05 tuýt còi, kỷ luật theo Nội quy lao động | Manager + LCCA + Dept Head |

> **Lưu ý**: Nếu để A05 tuýt còi → chế tài nội bộ sẽ tăng cấp tự động.

---

## 7. Tham chiếu

### Pháp lý gốc
- `GSX-LEGAL-001`: Nghị định 13/2023/NĐ-CP - đặc biệt Điều 3 (nguyên tắc), Điều 25 (cross-border), Điều 28 (access control), Điều 38 (Data Controller liability)

### Case study liên quan
- `GSX-CASE-001`: UGC Contest 2025 - vi phạm NĐ13 do thu hình giấy tờ tùy thân qua bài đăng công khai

### Tool/Checklist liên quan
- `GSX-TOOL-003`: Form Compliance Checklist
- `GSX-TOOL-009`: Consent Checkbox Templates (template clause chuẩn)
- `GSX-TOOL-002`: UGC Event Compliance Checklist

### Tài liệu nội bộ VNG
- VNGGames Data Policy
- Internal Promotion Tool documentation

---

## 8. Changelog

| Version | Date | Changed by | Notes |
|---|---|---|---|
| 1.0 | 2026-06-03 | Hub Owner | Initial version - ghép từ memory + Case Study UGC ND13 + Tournament Playbook |
