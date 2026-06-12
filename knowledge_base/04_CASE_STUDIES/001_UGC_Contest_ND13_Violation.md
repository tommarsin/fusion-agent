---
doc_id: GSX-CASE-001
title: "UGC Contest - Vi phạm NĐ13/2023 về Bảo vệ dữ liệu cá nhân"
classification: data-privacy
severity: high
status: closed
incident_date: 2025
documented_date: 2025
documented_by: Game Studio X Community Team
source: internal
share_scope: gsx-internal
related_operating_rules:
  - GSX-OP-001: Data Collection Policy
  - GSX-OP-007: UGC Event Rules
related_legal_sources:
  - GSX-LEGAL-001: Nghị định 13/2023/NĐ-CP
  - GSX-LEGAL-008: Facebook Community Standards
keywords_for_search: [ugc, contest, nd13, cccd, giay-to, data-privacy, facebook-community-standards]
---

# Case Study: UGC Contest - Vi phạm NĐ13/2023

> **TL;DR**: UGC contest yêu cầu user đăng ảnh giấy khen/giấy tờ → 90 user tham gia trong 3 ngày → 22 case vi phạm phải xóa, trong đó 1 case lộ CCCD. Vi phạm NĐ13 + Facebook Community Standards. Bài học: cấm tuyệt đối UGC liên quan giấy tờ định danh.

---

## 0. Viết tắt & Thuật ngữ trong case study này

| Viết tắt/Thuật ngữ | Giải thích |
|---|---|
| **UGC** (User-Generated Content) | Nội dung do user tạo (fan art, cosplay, video, story...) |
| **NĐ13** | Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân |
| **CCCD** | Căn Cước Công Dân - giấy tờ tùy thân định danh |
| **A05** | Cục An ninh mạng - Bộ Công an |
| **Worst-case design** | Nguyên tắc: user sẽ tự lộ thông tin nhạy cảm hơn yêu cầu - phải lường được |
| **2nd-eye review** | Vòng kiểm tra chéo bởi người thứ 2 (không phải designer ban đầu) |

> 📖 Tra cứu thêm: `00_INDEX_VERSION/GLOSSARY.md`

---

## 1. Tình huống

### 1.1. Bối cảnh
Năm 2025, Game Studio X triển khai sự kiện UGC contest trên Group cộng đồng và Fanpage game, kêu gọi user đăng ảnh các loại giấy tờ (giấy khen, bằng lái xe, giấy nhập học/trúng tuyển, chứng nhận Cháu Ngoan Bác Hồ, mầm non, v.v.) kèm hashtag để nhận thưởng (gói nạp game).

### 1.2. Diễn biến
- **Ngày 1**: Event launch, 20-30 bài đăng đầu tiên
- **Ngày 2**: User tham gia tăng nhanh, một số bài có giấy tờ chưa che thông tin định danh
- **Ngày 3**: Team Community phát hiện 1 case lộ CCCD nguyên bản → escalate Lead → quyết định gỡ toàn bộ contest

### 1.3. Quy mô hậu quả
- **90 user** đã tham gia trong 3 ngày
- **22 case vi phạm** phải xóa, breakdown:
  - 1 case giấy báo trúng tuyển lộ số CCCD
  - 3 case giấy tờ tùy thân chưa che ngày tháng năm sinh
  - 2 case giấy tờ tùy thân có che một phần (xóa toàn bộ để đồng bộ)
  - 16 case bằng khen/chứng nhận chưa che ngày tháng năm sinh hoặc năm sinh
- Phải làm **giải trình bằng email** cho cấp trên về sự cố
- Mất uy tín với cộng đồng (user feel bị "lừa" để lộ thông tin cá nhân)

---

## 2. Vi phạm xác định

### 2.1. Vi phạm pháp luật

**Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân**:

- **Điều 3 - Nguyên tắc giới hạn mục đích và tối thiểu hóa dữ liệu**: Việc thu thập dữ liệu cá nhân phải phù hợp và giới hạn trong phạm vi cần thiết. Yêu cầu user đăng tải công khai ảnh CCCD/giấy tờ tùy thân để tham gia event là thu thập/xử lý dữ liệu vượt quá mức cần thiết.

- **Điều 3 - Trách nhiệm bảo mật dữ liệu cá nhân**: Tổ chức/nhãn hàng tạo ra sân chơi khuyến khích hoặc ép buộc user phơi bày dữ liệu tùy thân trên không gian mạng là hành vi thiếu trách nhiệm bảo vệ dữ liệu, có thể bị Cục An ninh mạng A05 tuýt còi.

### 2.2. Vi phạm chính sách nội bộ
- Game Studio X chưa có rule cấm rõ ràng cho UGC contest có liên quan giấy tờ tại thời điểm xảy ra → đã trigger việc tạo rule (`GSX-OP-007`)

### 2.3. Vi phạm tiêu chuẩn nền tảng

**Facebook Community Standards - Privacy Violations**:
- Cấm đăng government-issued ID (CCCD/passport) của người khác hoặc của chính mình
- Cấm đăng thông tin cá nhân nhạy cảm

→ Bài có giấy tờ định danh có thể bị Facebook gỡ tự động + warning Fanpage.

---

## 3. Nguyên nhân gốc rễ

### 3.1. Lỗi nhận thức
- Team thiết kế contest **không nhận diện được** rằng giấy khen/giấy chứng nhận cũng thuộc "data cá nhân nhạy cảm" (chứa họ tên thật, ngày sinh, địa chỉ trường học/đơn vị)
- Nghĩ rằng "giấy khen, bằng cấp không phải CCCD nên không sao"

### 3.2. Lỗi quy trình
- Không có review chéo nội bộ trước khi go-live
- Không có checklist compliance cho UGC contest tại thời điểm đó
- Không có cảnh báo rõ ràng tới user về việc che thông tin nhạy cảm

### 3.3. Lỗi thiết kế concept
- Concept event **bản chất rủi ro cao** - kêu gọi đăng giấy tờ thì user sẽ có xu hướng đăng cả những giấy tờ chưa được nghĩ tới (như giấy báo trúng tuyển kèm CCCD)
- Mặc dù caption có cảnh báo nhưng user không đọc kỹ, vẫn đăng ảnh chưa che thông tin

### 3.4. Lỗi monitoring
- Phát hiện vi phạm muộn (sau 3 ngày) - lẽ ra phải có spot-check mỗi 4-6h trong 24h đầu

---

## 4. Chế tài đã áp dụng

### 4.1. Action ngay
- Dừng contest, gỡ post launch
- Xóa toàn bộ 22 post vi phạm (kèm DM giải thích cho user)
- Liên hệ riêng user lộ CCCD → hướng dẫn thay đổi giấy tờ nếu cần thiết

### 4.2. Chế tài nội bộ
- Team Community gửi **giải trình bằng email** cho cấp trên
- Đào tạo lại team về NĐ13
- Tạo rule mới (`GSX-OP-007`) + checklist (`GSX-TOOL-002`) để phòng ngừa tái diễn

### 4.3. Hậu quả uy tín
- Cộng đồng có thread thảo luận về việc bị "lừa lộ data"
- VNGGames mất nhiều niềm tin trong cộng đồng game đó

---

## 5. Bài học rút ra

### Bài học 1: "Dữ liệu cá nhân" rộng hơn ta nghĩ
Mọi giấy tờ chứa **ít nhất 1 trong**: họ tên thật, ngày sinh, địa chỉ, số định danh, ảnh khuôn mặt → đều thuộc data cá nhân cần bảo vệ. Không có khái niệm "giấy tờ phụ".

### Bài học 2: User sẽ làm nhiều hơn thể lệ yêu cầu
Dù thể lệ chỉ yêu cầu giấy khen, user vẫn tự đăng:
- Giấy khen kèm ảnh chân dung
- Bằng cấp kèm CCCD ở mặt sau
- Giấy báo trúng tuyển - không nghĩ rằng có CCCD bên trong

→ **Worst-case design**: thiết kế phải lường được user sẽ tự lộ thông tin nhạy cảm hơn yêu cầu.

### Bài học 3: Cảnh báo phải ở chỗ user thực sự đọc
Cảnh báo "che thông tin nhạy cảm" trong caption + comment phụ → user thường bỏ qua. Phải:
- Cảnh báo trong **caption chính** (3 dòng đầu)
- Cảnh báo trong **visual thể lệ** (banner)
- KHÔNG chỉ ở comment phụ

### Bài học 4: Tốc độ phát hiện > tốc độ xử lý
Mất 3 ngày mới phát hiện = 22 case lộ data. Nếu spot-check mỗi 4-6h trong 24h đầu, có thể giảm còn 3-5 case.

### Bài học 5: Review chéo là không thương lượng
Mọi UGC contest phải có 2nd-eye review trong team trước go-live. Không exception "bài nhỏ", "đã làm tương tự trước".

---

## 6. Rule phòng ngừa (sau case này)

### Rule mới được tạo
- **`GSX-OP-007` UGC Event Rules**: codify Red Line cấm UGC liên quan giấy tờ định danh + workflow review chéo + plan moderation 24h
- **`GSX-OP-001` Data Collection Policy**: codify phân loại Form vs Promotion Tool + 3 element bắt buộc

### Tool mới được build
- **`GSX-TOOL-002` UGC Event Compliance Checklist**: 4 stage check với Red Line ở đầu
- **`GSX-TOOL-003` Form Compliance Checklist**: decision tree tool + verify 3 elements
- **`GSX-TOOL-009` Consent Checkbox Templates**: 5 template chuẩn cho 5 loại form

### Checklist được cập nhật
- Pre-Launch Checklist (`GSX-TOOL-001`) thêm section Data Privacy
- Mọi UGC concept phải pass Red Line check trước khi nhận tài nguyên triển khai

---

## 7. Câu hỏi self-check cho team

Sau khi đọc case này, mỗi thành viên tự hỏi:

- [ ] Mình có đang thiết kế UGC concept tương tự không? (kêu gọi user đăng ảnh có thông tin định danh)
- [ ] Mình có biết phân biệt "data cá nhân" rộng vs "CCCD/giấy tờ" hẹp không?
- [ ] Concept của mình có lường được user sẽ tự lộ nhiều hơn yêu cầu không?
- [ ] Cảnh báo trong contest của mình có ở caption chính + visual không?
- [ ] Có ai trong team review chéo concept của mình chưa?
- [ ] Plan moderation 24h đầu đã có chưa?

---

## 8. Tham chiếu

### Tài liệu nội bộ
- `GSX-OP-001`: Data Collection Policy
- `GSX-OP-007`: UGC Event Rules
- `GSX-TOOL-002`: UGC Event Compliance Checklist
- `GSX-TOOL-003`: Form Compliance Checklist

### Tài liệu pháp lý
- `GSX-LEGAL-001`: Nghị định 13/2023/NĐ-CP - Điều 3
- `GSX-LEGAL-008`: Facebook Community Standards - Privacy Violations

---

## 9. Changelog của case study

| Version | Date | Changed by | Notes |
|---|---|---|---|
| 1.0 | 2025 | Game Studio X Community Team | Initial documentation |
| 2.0 | 2026-06-03 | Hub Owner | Reformat theo template Hub, link cross-reference |
