---
doc_id: GSX-CASE-003
title: "Gian lận tài chính + Trục lợi quyền hạn vận hành (case hư cấu)"
classification: financial
severity: critical
status: closed
incident_date: "Năm N"
documented_date: "Năm N"
documented_by: Game Studio X Community Team
source: fictional
share_scope: gsx-internal
related_operating_rules:
  - GSX-OP-003: Partner SOP - KOL
  - GSX-OP-012: Financial Integrity
related_legal_sources:
  - GSX-LEGAL-003: BLHS Điều 174, 175
keywords_for_search: [hoa-don-khong, fraud, truc-loi, vendor-fraud, thoi-viec, marketing-supervisor, game-operator]
---

# Case Study: Gian lận tài chính + Trục lợi quyền hạn vận hành (case hư cấu)

> **Lưu ý:** Đây là tình huống hư cấu được xây dựng dựa trên các kịch bản vi phạm điển hình trong ngành, nhằm mục đích đào tạo và phòng ngừa rủi ro.

> **TL;DR**: Tại một studio game, 2 nhóm nhân viên bị thôi việc ngay lập tức vì (1) lập hóa đơn khống cho thuê thiết bị + CTV, (2) lợi dụng quyền vận hành game tạo vật phẩm bán cho gamer. Bài học: lòng tin xây nhiều năm, mất chỉ vì lợi ích nhỏ. Test minh bạch: "Không dám public = không được làm".

---

## 0. Viết tắt & Thuật ngữ trong case study này

| Viết tắt/Thuật ngữ | Giải thích |
|---|---|
| **BLHS** | Bộ luật Hình sự |
| **Test minh bạch** | Nguyên tắc: "Bất kỳ điều gì mình làm trong công việc - nếu mình 'không dám' thông báo cho cấp trên hay đồng nghiệp - thì đó là một điều không nên làm" |
| **Test transparency** | Synonym của "Test minh bạch" (cách viết tiếng Anh) |
| **CTV** | Cộng tác viên |
| **Game Operator** | Nhân viên vận hành game, có quyền can thiệp vào hệ thống/items |
| **Vendor** | Nhà cung cấp dịch vụ bên ngoài |
| **Hóa đơn khống** | Hóa đơn lập ra cho dịch vụ không thực sự phát sinh - thủ đoạn gian dối |
| **Server local** | Máy chủ thử nghiệm/dev nội bộ (khác với server chính cho user) |
| **Whistleblowing** | Báo cáo nội bộ về dấu hiệu vi phạm - có cơ chế bảo vệ người báo cáo |
| **Proportionality** | Nguyên tắc chế tài tỉ lệ với mức độ tham gia vi phạm |

> 📖 Tra cứu thêm: `00_INDEX_VERSION/GLOSSARY.md`

---

## 1. Tình huống

### 1.1. Bối cảnh
Vào Năm N, tại một studio game, phát sinh 2 sự việc vi phạm nội bộ liên quan trục lợi tài chính. Ban lãnh đạo quyết định công bố rộng rãi để làm bài học chung — đây là lần đầu tiên công ty thông báo kỷ luật thôi việc đến toàn bộ nhân viên (các case trước không thông báo).

### 1.2. Diễn biến

**Case A - Marketing Supervisor**:
- Một Marketing Supervisor, là thành viên lâu năm của team, cùng 4 đồng nghiệp trong nhóm marketing **thông đồng lập hóa đơn khống** cho việc thuê thiết bị và cộng tác viên.
- Chi phí thực tế không phát sinh hoặc rất thấp so với hóa đơn.
- Sau khi thanh toán với công ty, khoản tiền chênh lệch bị dùng cho mục đích cá nhân.

**Case B - Game Operator**:
- Một Game Operator cùng 2 đồng nghiệp lợi dụng quyền hạn quản lý hệ thống game **tạo vật phẩm trong server local**, chuyển sang server chính và bán cho gamer lấy tiền.
- Vi phạm nguyên tắc vận hành và bảo mật game.

### 1.3. Quy mô hậu quả
- Giá trị chiếm đoạt nhỏ hơn mức thưởng cuối năm đã bị cắt.
- Ảnh hưởng uy tín với khách hàng (case B - người chơi).
- Lòng tin nội bộ team bị tổn thương.

---

## 2. Vi phạm xác định

### 2.1. Vi phạm pháp luật

**Bộ luật Hình sự**:
- **Điều 174 - Tội lừa đảo chiếm đoạt tài sản**: Lập hóa đơn khống = thủ đoạn gian dối.
- **Điều 175 - Tội lạm dụng tín nhiệm chiếm đoạt tài sản**: Lợi dụng quyền hạn vận hành để trục lợi.

→ Mặc dù công ty không truy tố hình sự (chỉ kỷ luật nội bộ), hành vi này có thể cấu thành tội theo luật hiện hành.

### 2.2. Vi phạm chính sách nội bộ
- Vi phạm Nội quy lao động.
- Vi phạm nguyên tắc vận hành game (case B - tạo vật phẩm trái phép).
- Vi phạm nguyên tắc minh bạch tài chính.

### 2.3. Vi phạm nguyên tắc đạo đức nghề
- Lạm dụng quyền hạn được công ty tin tưởng giao phó.
- Phá vỡ lòng tin với đồng nghiệp + công ty.

---

## 3. Nguyên nhân gốc rễ

### 3.1. Lỗi cá nhân
- Đặt **lợi ích ngắn hạn** (tiền chênh lệch nhỏ) lên trên **lợi ích dài hạn** (career + cơ hội tại công ty).
- *"Đáng tiếc hơn, là niềm tin bị đánh mất vì những món lợi nhỏ trước mắt."*

### 3.2. Lỗi quy trình
- Chưa có cross-check ≥ 2 người độc lập cho mọi hóa đơn.
- Quyền vận hành game tập trung quá lớn vào ít người.
- Audit log hệ thống game chưa chặt.

### 3.3. Lỗi văn hóa
- Một số thành viên nghĩ rằng vi phạm "nhỏ" sẽ không bị phát hiện.
- Tâm lý "ai cũng vậy" trong team có thể tồn tại.
- Thiếu cơ chế whistleblowing rõ ràng.

---

## 4. Chế tài đã áp dụng

### 4.1. Chế tài chủ mưu

| Vai trò | Chế tài |
|---|---|
| Marketing Supervisor (chủ mưu Case A) | **Thôi việc ngay lập tức + bồi hoàn khoản tiền đã vi phạm** |
| Game Operator (chủ mưu Case B) | **Thôi việc ngay lập tức** |

### 4.2. Chế tài thành viên liên đới

| Nhóm | Chế tài |
|---|---|
| 4 thành viên marketing còn lại | Cảnh cáo + cắt thưởng cuối năm + thử thách 6 tháng trong vị trí hiện tại |
| 2 Game Operator còn lại | Cảnh cáo + cắt thưởng cuối năm + **chuyển vị trí khác** + thử thách 6 tháng |

### 4.3. Communication
- Ban lãnh đạo công bố email toàn công ty.
- Không công bố mức tiền vi phạm cụ thể (để bảo vệ identity).
- Mục đích: làm bài học chung, không phải để chê bai cá nhân.

---

## 5. Bài học rút ra

### Bài học 1: Test minh bạch (Golden Rule)

> *"Bất kỳ điều gì mình làm trong công việc - nếu mình 'không dám' thông báo (hay nói rõ ràng) cho cấp trên hay đồng nghiệp - thì đó là một điều không nên làm."*

Đây là **kim chỉ nam** cho mọi quyết định, không chỉ tài chính. Áp dụng được cho:
- Duyệt bài
- Hợp tác KOL
- Chi phí dự án
- Conflict of interest
- Mod action

### Bài học 2: Lòng tin xây dài, mất nhanh

> *"Lòng tin được tạo dựng trong khoảng thời gian rất dài, nhưng chỉ cần 1 chút sai lầm thì rất nhiều công sức của mình trước đó sẽ bị mất hết."*

- Career path lâu dài tại công ty > vài triệu chênh lệch.
- Reputation trong ngành > short-term gain.

### Bài học 3: Vi phạm nhỏ trong context lớn = vẫn nặng
Một số thành viên nghĩ rằng vi phạm của mình "quá nhỏ để bị kỷ luật như vậy" — nhưng **bản chất hành vi quan trọng hơn giá trị tiền**.

### Bài học 4: Đóng góp quá khứ ≠ miễn trừ
Dù là nhân viên lâu năm, có nhiều đóng góp — **vẫn thôi việc ngay lập tức**. Pattern này lặp lại trong nhiều case khác (bản đồ, quấy rối nơi làm việc).

### Bài học 5: Chế tài tỉ lệ với vai trò (**Proportionality**)
- Chủ mưu/Supervisor: thôi việc.
- Liên đới: cảnh cáo + cắt thưởng + thử thách 6 tháng.
- Liên đới có lạm dụng quyền hạn (Game Op): thêm chuyển vị trí.

### Bài học 6: Whistleblowing là khả thi
Case này được nội bộ tự phát hiện, không phải qua external audit → môi trường công ty có cơ chế phát hiện vi phạm.

---

## 6. Rule phòng ngừa (sau case này)

### Rule đã codify trong Game Studio X Hub
- **`GSX-OP-012` Financial Integrity**: codify Test minh bạch + cross-check ≥ 2 người + whistleblowing.
- **`GSX-OP-003` Partner SOP KOL**: codify conflict of interest declaration + cấm hóa đơn khống.
- **`GSX-OP-011` Information Classification**: codify need-to-know basis cho data sensitive.

### Tools đã build
- Self-check 5 câu trước khi xử lý tài chính (trong `GSX-OP-012`).
- Quy trình thuê CTV/Vendor chuẩn (trong `GSX-OP-012`).
- Whistleblowing channels (HR, Anti-Fraud, Dept Head).

### Lessons codified cho mọi rule
- Mỗi rule trong Hub có Section 6 "Chế tài khi vi phạm" với 3 cấp — lấy nguyên tắc proportionality từ case này.

---

## 7. Câu hỏi self-check cho team

Sau khi đọc case này, mỗi thành viên tự hỏi:

- [ ] Mình có đang ở vị trí có thể trục lợi (quyền duyệt chi, quyền vận hành) không?
- [ ] Khi xử lý 1 giao dịch, mình có dám **public nó với toàn team** không?
- [ ] Mình có khai báo conflict of interest khi engage người thân/bạn thân không?
- [ ] Mình có biết kênh whistleblowing khi phát hiện đồng nghiệp vi phạm không?
- [ ] Mình có hiểu rằng vi phạm nhỏ vẫn dẫn đến thôi việc nếu cấu thành test minh bạch không?

---

## 8. Tham chiếu

### Tài liệu nội bộ
- `GSX-OP-003`: Partner SOP - KOL
- `GSX-OP-012`: Financial Integrity (codify hoàn toàn từ case này)

### Tài liệu pháp lý
- `GSX-LEGAL-003`: Bộ luật Hình sự - Điều 174 (Lừa đảo), Điều 175 (Lạm dụng tín nhiệm)

---

## 9. Changelog của case study

| Version | Date | Changed by | Notes |
|---|---|---|---|
| 1.0 | Năm N | Game Studio X Community Team | Initial documentation |
| 2.0 | 2026-06-03 | Hub Owner | Reformat theo template Hub |
| 3.0 | 2026-06-12 | Hub Owner | Fictionalized cho public KB |
