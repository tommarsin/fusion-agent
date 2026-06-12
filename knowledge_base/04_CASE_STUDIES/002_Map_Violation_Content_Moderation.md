---
doc_id: GSX-CASE-002
title: "Bản đồ vi phạm trong content moderation - Nhân viên bị thôi việc"
classification: content-moderation
severity: critical
status: closed
incident_date: unknown
documented_date: 2026-06-03
documented_by: Hub Owner
source: internal
share_scope: gsx-internal
related_operating_rules:
  - GSX-OP-002: Content Moderation Rules
related_legal_sources:
  - GSX-LEGAL-004: Luật An ninh mạng
keywords_for_search: [ban-do, map, content-moderation, sovereignty, thoi-viec, an-ninh-mang]
---

# Case Study: Vi phạm bản đồ trong content moderation

> **TL;DR**: 1 nhân viên duyệt bài viết có hình ảnh bản đồ không hợp lệ → nhân viên bị thôi việc + team bị xử lý hành chính. Bài học: bản đồ = Red Line tuyệt đối, không có "ngoại lệ vì sơ ý".

---

## 1. Tình huống

### 1.1. Bối cảnh
Một nhân viên Game Studio X duyệt và đăng bài viết lên kênh chính thức của VNGGames. Trong bài viết có hình ảnh bản đồ không hợp lệ (vi phạm về thể hiện chủ quyền lãnh thổ Việt Nam).

### 1.2. Diễn biến
- Bài đăng go-live trên kênh chính thức
- Bài bị phát hiện vi phạm về thể hiện bản đồ
- Cơ quan chức năng tuýt còi → team xử lý gỡ bài
- Quy trình xử lý kỷ luật được triển khai

### 1.3. Quy mô hậu quả
- **Nhân viên trực tiếp duyệt bài: bị thôi việc**
- **Team Community bị xử lý hành chính** (cảnh cáo + có thể phạt tài chính)
- Tổn thất uy tín với cơ quan chức năng
- Bài học làm tiền lệ trong toàn team

> ⚠️ Đây là case có mức chế tài cao nhất trong lịch sử Community Game Studio X - vi phạm bản đồ = chế tài nặng hơn cả vi phạm tài chính.

---

## 2. Vi phạm xác định

### 2.1. Vi phạm pháp luật

**Luật An ninh mạng (Luật số 24/2018/QH14)**:
- **Điều 8**: Cấm các hành vi sử dụng không gian mạng để xuyên tạc về chủ quyền lãnh thổ
- **Điều 16**: Cấm thông tin xuyên tạc, bôi nhọ, sai sự thật về chủ quyền lãnh thổ, biên giới, hải đảo Việt Nam

### 2.2. Vi phạm chính sách nội bộ
- VNG Communication Policy - đăng nội dung có vấn đề pháp lý qua kênh chính thức
- Quy chuẩn content moderation chưa đủ chặt tại thời điểm xảy ra

### 2.3. Vi phạm tiêu chuẩn nền tảng (gián tiếp)
- Mặc dù Facebook chưa có rule riêng về bản đồ Việt Nam, nhưng việc bị cơ quan quản lý yêu cầu gỡ tạo tiền lệ xấu cho platform

---

## 3. Nguyên nhân gốc rễ

### 3.1. Lỗi nhận thức
- Nhân viên duyệt bài **không nhận diện được mức độ nghiêm trọng** của vi phạm bản đồ
- Có thể nghĩ rằng "chỉ là background, không phải nội dung chính" → không kiểm tra kỹ
- Thiếu training về sensitivity của vấn đề chủ quyền lãnh thổ

### 3.2. Lỗi quy trình
- Không có scanner tool tự động để flag bản đồ
- Không có checklist 7 bước cho hình ảnh tại thời điểm xảy ra
- Không có vòng review chéo 2nd-eye cho bài có hình ảnh phức tạp

### 3.3. Lỗi văn hóa
- Tốc độ go-live ưu tiên hơn compliance check
- Áp lực KPI có thể khiến rút ngắn quy trình duyệt

### 3.4. Lỗi monitoring sau go-live
- Không có spot-check ngay sau khi đăng → phát hiện muộn

---

## 4. Chế tài đã áp dụng

### 4.1. Chế tài cá nhân
- **Nhân viên trực tiếp duyệt bài: thôi việc ngay lập tức**
- Không có ngoại lệ vì đóng góp quá khứ - principle "đóng góp quá khứ ≠ miễn trừ vi phạm" (echo case quấy rối tại văn phòng (Năm N+9))

### 4.2. Chế tài team
- **Team bị xử lý hành chính**
- Phải submit incident report đầy đủ
- Phải tham gia training compliance bắt buộc
- Review lại toàn bộ process content moderation

### 4.3. Hành động khắc phục
- Gỡ bài vi phạm ngay
- Submit báo cáo cho cơ quan chức năng
- Triển khai content scanner tool

---

## 5. Bài học rút ra

### Bài học 1: Bản đồ = Red Line tuyệt đối
**Không có "ngoại lệ vì sơ ý"** với bản đồ. Mọi hình dạng lãnh thổ (Việt Nam hoặc quốc tế) trong content phải qua scrutiny tuyệt đối.

Ngoại lệ duy nhất: bản đồ fiction game thuần túy (Summoner's Rift, Runeterra) - đây là tài sản IP của Riot, không phải bản đồ địa lý thực.

### Bài học 2: Background ảnh cũng cần check
Bản đồ có thể xuất hiện trong:
- Wallpaper game có bản đồ thế giới
- Screenshot trận đấu có UI mini-map
- Ảnh quay phỏng vấn có poster bản đồ
- Banner sự kiện có world map decoration
- Ảnh meme có map fragment

→ Checklist 7 bước cho hình ảnh bắt buộc, không skip vì "chỉ là background".

### Bài học 3: Đóng góp quá khứ ≠ miễn trừ
Dù nhân viên có lâu năm, đóng góp nhiều - vi phạm cấp 3 vẫn dẫn đến thôi việc. Pattern lặp lại từ case quấy rối tại văn phòng Năm N+9 (nhà sáng lập).

### Bài học 4: Tool > Vigilance
Con người sẽ luôn có moment lơ là. **Tool scanner tự động** là layer bảo vệ cuối cùng. Game Studio X đã đầu tư xây Content Scanner tool sau case này.

### Bài học 5: Văn hóa "tốc độ vs compliance"
Áp lực go-live nhanh là nguyên nhân hệ thống. Lead/Manager phải tạo culture "thà chậm 1 ngày còn hơn vi phạm pháp luật".

---

## 6. Rule phòng ngừa (sau case này)

### Rule mới được tạo
- **`GSX-OP-002` Content Moderation Rules**: 9 nhóm tiêu chí (4A-4I), trong đó 4A có Red Line bản đồ tuyệt đối
- Checklist 7 bước cho hình ảnh: Bước 1 = check bản đồ

### Tool mới được build
- **Game Studio X Content Scanner tool**: auto-flag bản đồ + 9 nhóm vi phạm
- **`GSX-TOOL-005` Content Scanner Guide**: hướng dẫn dùng scanner

### Checklist được cập nhật
- Pre-Launch Checklist (`GSX-TOOL-001`): Bản đồ là item check đầu tiên
- Quick Reference 1-pager (`GSX-TOOL-011`): Bản đồ liệt kê #1 trong 6 Red Lines

### Culture change
- Lead/Manager tạo permission rõ ràng: **được phép trì hoãn go-live** để check kỹ
- Đào tạo bản đồ là module bắt buộc cho mọi CTV mới (`GSX-TRAIN-001`)

---

## 7. Câu hỏi self-check cho team

Sau khi đọc case này, mỗi thành viên tự hỏi:

- [ ] Mình đã chạy Game Studio X Scanner cho TẤT CẢ ảnh trong bài, kể cả background chưa?
- [ ] Mình có nhận diện được các loại bản đồ "ẩn" (background, mini-map, decoration)?
- [ ] Mình có thật sự dám trì hoãn go-live khi có nghi ngờ về compliance?
- [ ] Lead/team của mình có culture đề cao compliance hơn tốc độ?
- [ ] Mình đã hoàn thành module training về bản đồ chưa?

---

## 8. Tham chiếu

### Tài liệu nội bộ
- `GSX-OP-002`: Content Moderation Rules
- `GSX-TOOL-005`: Content Scanner Guide
- `GSX-TOOL-011`: Quick Reference 1-pager

### Tài liệu pháp lý
- `GSX-LEGAL-004`: Luật An ninh mạng - Điều 8, 16

### Tài liệu liên quan
- Bản đồ chuẩn từ Cục Đo đạc, Bản đồ và Thông tin địa lý Việt Nam (chính phủ)

---

## 9. Changelog của case study

| Version | Date | Changed by | Notes |
|---|---|---|---|
| 1.0 | 2026-06-03 | Hub Owner | Initial documentation - based on Hub Owner recollection + team verification |
