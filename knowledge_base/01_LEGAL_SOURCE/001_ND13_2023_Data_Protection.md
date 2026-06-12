---
doc_id: GSX-LEGAL-001
title: "Nghị định 13/2023/NĐ-CP - Bảo vệ dữ liệu cá nhân"
type: decree
issuing_authority: Chính phủ Việt Nam
issued_date: 2023-04-17
effective_date: 2023-07-01
status: active
last_summarized: 2026-06-03
summarized_by: Hub Owner
official_link: https://thuvienphapluat.vn/van-ban/Cong-nghe-thong-tin/Nghi-dinh-13-2023-ND-CP-bao-ve-du-lieu-ca-nhan-465185.aspx
applies_to_gsx: yes
priority: critical
related_operating_rules:
  - GSX-OP-001: Data Collection Policy
  - GSX-OP-006: Community Engagement Rules
  - GSX-OP-007: UGC Event Rules
  - GSX-OP-011: Information Classification
tags: [data-privacy, pdpa, nd13, personal-data, cross-border]
---

# Nghị định 13/2023/NĐ-CP - Bảo vệ dữ liệu cá nhân

## 1. Thông tin cơ bản

- **Số hiệu**: 13/2023/NĐ-CP
- **Tên đầy đủ**: Nghị định quy định về bảo vệ dữ liệu cá nhân
- **Cơ quan ban hành**: Chính phủ Việt Nam
- **Ngày ban hành**: 17/04/2023
- **Ngày hiệu lực**: 01/07/2023
- **Phạm vi**: Điều chỉnh việc xử lý dữ liệu cá nhân của cá nhân, tổ chức hoạt động tại Việt Nam hoặc xử lý dữ liệu cá nhân của công dân Việt Nam

---

## 2. Tóm tắt nội dung quan trọng cho Game Studio X

> ⚠️ Đây KHÔNG phải bản dịch toàn văn. Chỉ tóm tắt các điều liên quan công việc Community.

### 2.1. Các điều khoản liên quan trực tiếp

| Điều | Nội dung tóm tắt | Áp dụng vào việc gì |
|---|---|---|
| **Điều 2** | Định nghĩa "Dữ liệu cá nhân" rộng - bao gồm cả thông tin định danh được | Mọi form thu thập, mọi UGC contest |
| **Điều 3** | Nguyên tắc bảo vệ DLCN: minh bạch, giới hạn mục đích, tối thiểu hóa, chính xác, bảo mật, có thời hạn | Mọi hoạt động thu data của Community |
| **Điều 9** | Quyền của chủ thể dữ liệu: truy cập, sửa, xóa, rút lại đồng ý | Form phải có kênh để user thực thi quyền này |
| **Điều 11** | Đồng ý của chủ thể dữ liệu phải rõ ràng, tự nguyện, có thể rút lại | Consent checkbox bắt buộc, không default-checked |
| **Điều 13** | Mục đích xử lý phải cụ thể, rõ ràng | Form phải nói rõ data dùng làm gì |
| **Điều 25** | Chuyển dữ liệu ra nước ngoài - phải đăng ký hồ sơ đánh giá tác động | Lý do Promotion Tool nội bộ (lưu trong nước) tốt hơn Google Form |
| **Điều 28** | Bảo mật xử lý dữ liệu - kiểm soát truy cập, audit log | Promotion Tool có access control + log; Google Form không có |
| **Điều 38** | Trách nhiệm Bên Kiểm soát dữ liệu (Data Controller) | VNGGames là Data Controller khi thu data user |
| **Điều 43** | Thông báo vi phạm bảo vệ DLCN trong 72h | Khi có data breach phải report A05 trong 72h |

### 2.2. Định nghĩa quan trọng

**"Dữ liệu cá nhân"** (Điều 2.1): Thông tin dưới dạng ký hiệu, chữ viết, chữ số, hình ảnh, âm thanh hoặc dạng tương tự **trên môi trường điện tử gắn liền với một con người cụ thể hoặc giúp xác định một con người cụ thể**.

→ Diễn giải cho Game Studio X: bao gồm cả họ tên thật, ngày sinh, địa chỉ, số định danh, ảnh khuôn mặt, IP address kết hợp với hoạt động, v.v.

**"Dữ liệu cá nhân nhạy cảm"** (Điều 2.4): Liên quan đến quan điểm chính trị, tôn giáo, sức khỏe, giới tính, sinh trắc học, di truyền, tài chính, vị trí địa lý hiện tại, **dữ liệu trẻ em**, dữ liệu về tội phạm, v.v.

→ Cảnh báo cho Game Studio X: UGC liên quan đến minor (dưới 16t) thuộc category nhạy cảm - phải có sự đồng ý của người giám hộ.

**"Bên Kiểm soát dữ liệu cá nhân" (Data Controller)** (Điều 2.9): Tổ chức/cá nhân **quyết định mục đích và phương tiện xử lý** dữ liệu cá nhân.

→ VNGGames là Data Controller khi:
- Thu data user qua form
- Quyết định tool nào thu, mục đích gì, lưu bao lâu

**"Bên Xử lý dữ liệu" (Data Processor)** (Điều 2.10): Tổ chức/cá nhân thực hiện việc xử lý dữ liệu **thay mặt cho Bên Kiểm soát**.

→ Agency, vendor xử lý data thay VNG là Data Processor - cần có hợp đồng/NDA rõ ràng.

---

## 3. Ý nghĩa thực tế với team Community

### 3.1. Việc gì BẮT BUỘC phải làm?

- ✅ Mọi form thu data cá nhân phải có **consent checkbox bắt buộc** (không default-checked)
- ✅ Form phải nói rõ **mục đích xử lý** (Điều 13)
- ✅ Form phải nói rõ **thời gian lưu trữ + khi nào xóa** (nguyên tắc có thời hạn - Điều 3)
- ✅ Phải có **kênh để user truy cập/sửa/xóa data** của họ (Điều 9)
- ✅ Data nhạy cảm (CCCD, SĐT định danh, địa chỉ): **bắt buộc Promotion Tool** (Điều 25, 28)
- ✅ Khi engage agency xử lý data: phải có hợp đồng Data Processor (Điều 38)
- ✅ Khi có data breach: report A05 + chủ thể bị ảnh hưởng trong 72h (Điều 43)

### 3.2. Việc gì BỊ CẤM?

- ❌ Thu data quá phạm vi mục đích đã nêu (vi phạm nguyên tắc tối thiểu hóa)
- ❌ Sử dụng data ngoài mục đích đã consent
- ❌ Chuyển data ra nước ngoài không qua đánh giá tác động (Điều 25)
- ❌ Lưu data quá thời hạn cần thiết
- ❌ Bỏ qua khi user yêu cầu xóa data
- ❌ Share data với bên thứ 3 không có hợp đồng Data Processor

### 3.3. Chế tài nếu vi phạm

**Chế tài hành chính** (theo Nghị định xử phạt vi phạm hành chính trong lĩnh vực):
- Phạt tiền: cá nhân vài chục triệu, tổ chức lên đến vài trăm triệu VND
- Có thể đình chỉ hoạt động xử lý dữ liệu

**Chế tài hình sự** (theo Bộ luật Hình sự):
- Điều 288: Tội đưa hoặc sử dụng trái phép thông tin mạng máy tính - phạt tù đến 7 năm cho vi phạm nghiêm trọng

**Chế tài nội bộ VNG**:
- Thôi việc theo Nội quy lao động nếu vi phạm gây thiệt hại
- Bồi thường thiệt hại cho công ty

**Hệ quả uy tín**:
- Bị Cục An ninh mạng A05 tuýt còi (đã từng xảy ra với Game Studio X - xem `GSX-CASE-001`)
- Cộng đồng mất niềm tin
- Đối tác (Riot) có thể đánh giá lại quan hệ

---

## 4. Liên hệ với Operating Rules

Luật này đã được diễn giải thành các rule cụ thể sau:

- `GSX-OP-001`: Data Collection Policy - phân loại Form vs Promotion Tool theo loại data
- `GSX-OP-006`: Community Engagement Rules - xử lý data nhạy cảm trong comment user
- `GSX-OP-007`: UGC Event Rules - Red Line cấm thu giấy tờ định danh
- `GSX-OP-011`: Information Classification - PII = Confidential level

---

## 5. Tài liệu tham khảo

- [Văn bản gốc NĐ13/2023/NĐ-CP - Thư viện Pháp luật](https://thuvienphapluat.vn/van-ban/Cong-nghe-thong-tin/Nghi-dinh-13-2023-ND-CP-bao-ve-du-lieu-ca-nhan-465185.aspx)
- Hồ sơ đăng ký xử lý dữ liệu cá nhân (template từ Bộ Công an)
- VNGGames Data Policy (internal)

---

## 6. Lịch sử cập nhật

| Version | Date | Updated by | Notes |
|---|---|---|---|
| 1.0 | 2026-06-03 | Hub Owner | Initial summary - dựa trên NĐ13 + thực tiễn áp dụng Game Studio X |
