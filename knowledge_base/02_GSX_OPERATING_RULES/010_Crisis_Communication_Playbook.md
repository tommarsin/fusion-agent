---
doc_id: GSX-OP-010
title: "Crisis Communication Playbook - Xử lý khủng hoảng truyền thông"
version: 1.0
status: draft
created: 2026-06-03
last_updated: 2026-06-03
last_reviewed_by: Hub Owner
legal_owner: PR Manager + Dept Head Game Studio X
next_review_date: 2026-09-03
applies_to: Community Team, PR Team, Marketing Lead, mọi nhân sự Game Studio X tiếp xúc bên ngoài
related_legal_sources:
  - GSX-LEGAL-005: VNG Communication Policy
related_case_studies:
  - GSX-CASE-004: Crisis truyền thông "VNG bị TQ thâu tóm" (Năm N+2)
  - GSX-CASE-006: cơ quan quản lý địa phương yêu cầu (Năm N)
  - GSX-CASE-007: Một tờ báo lớn tấn công ngành game (Năm N)
related_tools:
  - GSX-TOOL-006: Escalation Decision Tree
  - GSX-TOOL-007: Scripts Library
  - GSX-TOOL-008: Incident Report Template
tags: [crisis, communication, escalation, cooling-rule, media, threats]
---

# GSX-OP-010: Crisis Communication Playbook

## 1. Mục đích & Phạm vi

### 1.1. Tại sao có rule này?

Khủng hoảng truyền thông là **inevitable** trong ngành game/community. VNG đã trải qua nhiều case (xem `GSX-CASE-004`, `GSX-CASE-006`, `GSX-CASE-007`).

Khi xảy ra crisis, sai lầm phổ biến của team trẻ:
- **Phản ứng cảm xúc tức thời** → leo thang khủng hoảng
- **Tự ý xin lỗi/hứa hẹn** → tạo precedent xấu
- **Im lặng vĩnh viễn** vì sợ → mất kiểm soát narrative
- **Tranh luận với troll** → cung cấp ammo cho phía đối lập

Rule này codify 7 bước xử lý + script chuẩn + escalation chain.

**Triết lý gốc** (từ anh Năm N+2): *"Niềm tin được thể hiện rõ ràng nhất vào những thời điểm khó khăn nhất. Chính vào những lúc như thế này, Minh luôn có niềm tin mạnh mẽ nhất vào những gì VNG đã và đang làm."*

### 1.2. Áp dụng cho ai?

- Mọi nhân sự Game Studio X khi tiếp xúc bên ngoài (Community, KOL Mgmt, PR, Brand, Event)
- Đặc biệt: người trực Fanpage, Group, Discord trong giờ hành chính + ngoài giờ
- Lead/Manager khi nhận escalation

### 1.3. Không áp dụng cho?

- Comment tiêu cực thông thường của user (xử lý theo `GSX-OP-006`)
- Tranh luận học thuật, feedback xây dựng (không phải crisis)

### 1.4. Viết tắt & Thuật ngữ trong tài liệu này

| Viết tắt/Thuật ngữ | Giải thích |
|---|---|
| **Cooling Rule** | Nguyên tắc không phản ứng tức thời - chờ vài giờ/ngày trước khi response, để có data + tránh emotional reaction |
| **Information Gate** | Nguyên tắc thông tin chỉ chia sẻ khi đã verify - không "đoán mò" hay "bàn bạc tùm lum" |
| **Narrative leadership** | Chủ động kể câu chuyện của mình thay vì defensive với từng cáo buộc |
| **Escalation chain** | Chuỗi báo cáo lên cấp cao hơn: L1 (CTV) → L2 (Lead) → L3 (Manager) → L4 (Dept Head) → L5 (BLĐ + LCCA) |
| **3 nhóm đối tượng** | Phân loại người tấn công: (1) không có info, (2) bóp méo vô tình, (3) cố tình kích động |
| **SLA** | Service Level Agreement - cam kết thời gian phản hồi |
| **CBC** | Bộ phận Truyền thông Doanh nghiệp của VNG |
| **LCCA** | Bộ phận Pháp chế của VNG |
| **PR Manager** | Public Relations Manager - phụ trách truyền thông bên ngoài, thuộc CBC |
| **BLĐ** | Ban Lãnh Đạo VNGGames |
| **A05** | Cục An ninh mạng - Bộ Công an |
| **cơ quan quản lý** | Sở Thông tin và Truyền thông cấp tỉnh/thành phố |

> 📖 Tra cứu thêm: `00_INDEX_VERSION/GLOSSARY.md`

---

## 2. Nguyên tắc cốt lõi

1. **Cooling Rule**: Không phản ứng tức thời khi bị áp lực. Lưu bằng chứng → escalate → chờ chỉ đạo.

2. **Silence is not failure, wrong reaction is**: *"Im lặng không phải là thất bại. Phản ứng sai mới là vũ khí của đối phương."*

3. **Cooling rồi phải có response**: Sau cooling không phải im lặng vĩnh viễn. Phải phản hồi bằng **data + transparency** (bài học từ Năm N+2).

4. **Phân biệt 3 nhóm phản ứng**:
   - Người không có info → cung cấp data
   - Người bóp méo info vô tình → correct với data
   - Người cố tình kích động → không thuyết phục được, không cố

5. **Mọi phát ngôn chính thức phải qua approval**: PR Manager/CBC duyệt trước khi publish.

---

## 3. Quy định chi tiết

### 3.1. Định nghĩa "crisis" - khi nào áp dụng rule này?

**Quy định**: Tình huống được coi là crisis cần escalate khi có ≥ 1 dấu hiệu:

- User/KOL đe doạ bóc phốt công khai
- Comment tiêu cực có dấu hiệu lan truyền (>10 share trong 1h)
- Báo chí/blogger liên hệ bất ngờ về vấn đề nhạy cảm
- Bên thứ 3 claim bản quyền, đe doạ kiện
- Cơ quan chức năng (cơ quan quản lý, A05) liên hệ
- Livestream/video viral chứa nội dung chỉ trích brand
- KOL/đối tác có scandal có thể liên đới VNGGames
- Tin đồn sai sự thật về VNG lan trên MXH

Không phải crisis (xử lý normal):
- Feedback tiêu cực thông thường
- Comment chửi không có lan truyền
- Drama cá nhân giữa user không liên quan brand

### 3.2. Quy trình 7 bước xử lý crisis

```
BƯỚC 1: Phát hiện sự cố
   ↓
BƯỚC 2: Lưu bằng chứng (screenshot + URL)
   ↓
BƯỚC 3: Ngừng phản hồi (dùng câu chuẩn 1 lần duy nhất)
   ↓
BƯỚC 4: Báo cáo Line Manager trong 30 phút
   ↓
BƯỚC 5: Đánh giá mức độ (Line Manager xác định Cấp 1-4)
   ↓
BƯỚC 6: Phối hợp xử lý theo chỉ đạo
   ↓
BƯỚC 7: Lưu hồ sơ sự cố trong 24h sau giải quyết
```

#### Bước 1: Phát hiện sự cố
- Nhận diện dấu hiệu bất thường trong giao tiếp với bên ngoài
- Bình tĩnh - **không panic, không tự đánh giá là chuyện nhỏ**
- Không bàn luận với đồng nghiệp trước khi báo Lead

#### Bước 2: Lưu bằng chứng
- **Screenshot toàn bộ cuộc trò chuyện**, không cắt xén
- Lưu **URL** bài đăng/tin nhắn/comment
- **CẤM xóa** bất kỳ tin nhắn/comment nào kể cả tin mình đã gửi
- Backup vào folder riêng có timestamp

#### Bước 3: Ngừng phản hồi (1 câu chuẩn)
Dùng câu duy nhất:
> "Cảm ơn bạn đã phản hồi. Mình sẽ chuyển vấn đề này đến đúng bộ phận để hỗ trợ bạn tốt hơn."

- Gửi **1 lần duy nhất**
- Không gửi thêm câu nào kể cả khi đối phương khiêu khích tiếp
- Không phản biện, không xin lỗi tràn lan, không hứa hẹn bồi thường

#### Bước 4: Báo cáo Line Manager
- **SLA: 30 phút** - không để qua ngày
- Kênh: **Zalo hoặc phone** - tránh email nếu khẩn
- Format: AI - CHUYỆN GÌ - KÊNH NÀO - BẰNG CHỨNG Ở ĐÂU - CẦN GÌ
- Đính kèm screenshot + URL đã lưu

Template báo cáo nhanh:
```
[TÊN] - Sự cố [Cấp ước tính]
AI: [Tên/tài khoản đối phương]
CHUYỆN GÌ: [Tóm tắt 1-2 câu]
KÊNH: [DM Facebook / Comment / Email / Zalo / Livestream / Bài đăng...]
BẰNG CHỨNG: [Đã chụp màn hình / Đã lưu email / Link URL]
CẦN GÌ: [Hỗ trợ xử lý / Chỉ báo cáo để biết]
```

#### Bước 5: Đánh giá mức độ
**Line Manager xác định Cấp 1-4** dựa trên tiêu chí:

| Cấp | Đặc điểm | Người xử lý |
|---|---|---|
| **Cấp 1** | Drama cá nhân, chưa lan truyền, chỉ 1 user | Tự xử (Line Manager + nhân sự) |
| **Cấp 2** | Bắt đầu lan truyền (>5 share/comment đồng tình), nhiều user join | Marketing Lead vào cuộc |
| **Cấp 3** | Lan rộng (>50 share, có influencer comment), báo chí bắt đầu hỏi | PR Manager + Marketing Lead + Dept Head |
| **Cấp 4** | Viral cấp quốc gia, báo lớn đưa tin, cơ quan chức năng liên hệ | Dept Head + BLĐ + LCCA |

#### Bước 6: Phối hợp xử lý
- Nhân sự **chỉ cung cấp thêm thông tin khi được yêu cầu**
- **CẤM tự ý hành động thêm** - mọi action theo chỉ đạo Manager
- Sẵn sàng cập nhật diễn biến mới ngay khi phát sinh
- Có thể được giao soạn statement (qua Marketing/PR review)

#### Bước 7: Lưu hồ sơ sự cố
- **SLA: trong 24h sau khi giải quyết**
- Format: Incident Report (xem `GSX-TOOL-008`)
  - Bối cảnh
  - Diễn biến
  - Action đã thực hiện
  - Kết quả
  - Bài học
- Lưu Drive nội bộ Game Studio X với quyền truy cập theo cấp

### 3.3. Các tình huống cụ thể với script chuẩn

**Quy định**: Dùng script chuẩn để đảm bảo nhất quán và tránh sai lầm.

| Tình huống | Script chuẩn |
|---|---|
| User hỏi thông tin chưa có | "Cảm ơn bạn đã quan tâm. Thông tin này mình cần xác nhận lại với team. Mình sẽ phản hồi bạn trong [X tiếng] nhé." |
| KOL đòi thêm quyền lợi | "Mình ghi nhận và sẽ báo cáo với bộ phận có thẩm quyền. Hiện tại mình không có quyền quyết định thêm ngoài nội dung đã ký kết." |
| Báo chí hỏi thông tin nhạy cảm | "Cảm ơn bạn đã liên hệ. Mình sẽ chuyển câu hỏi này đến bộ phận PR để có phản hồi chính thức nhất." |
| User đe doạ bóc phốt | "Cảm ơn bạn đã phản hồi. Mình hiểu bạn đang không hài lòng và mình sẽ chuyển vấn đề này đến đúng bộ phận để hỗ trợ bạn tốt hơn." |
| Bị hỏi thông tin nội bộ | "Xin lỗi bạn, thông tin đó thuộc nội bộ công ty và mình không được phép chia sẻ. Nếu cần hỗ trợ gì khác mình sẵn sàng giúp." |
| Đối tác gây áp lực deadline | "Mình hiểu yêu cầu của bạn. Tuy nhiên mình cần xác nhận lại với team trước khi cam kết timeline. Mình sẽ phản hồi bạn trước [giờ/ngày cụ thể]." |

### 3.4. Sau cooling - phản hồi có data

**Quy định**: Sau khi cool down (vài giờ đến 1 ngày tuỳ cấp độ), phải có response **có cấu trúc + có data**, không phải im lặng vĩnh viễn.

**Bài học từ Case Năm N+2 (nhà sáng lập)**:
- VNG bị cáo buộc "bị Trung Quốc thâu tóm" → phản ứng bằng **thông cáo báo chí có số liệu cụ thể**
- Đưa ra: tỷ lệ cổ phần ≤49%, nhà sáng lập giữ 19%, 5/6 BGD là người Việt
- Đảo ngược narrative: dẫn chứng VNG đã export game ra TQ, Nhật

**Format response sau cooling**:
1. Acknowledge concern (không phủ nhận có vấn đề)
2. Provide facts/data có thể verify
3. State VNG position rõ ràng
4. Khẳng định tiếp tục focus vào mục tiêu chính
5. Không cố thuyết phục người cố tình kích động

### 3.5. Phân loại 3 nhóm đối tượng trong crisis

**Quy định**: Phân biệt trước khi response để tránh waste resource:

| Nhóm | Đặc điểm | Cách xử lý |
|---|---|---|
| **Nhóm 1: Không có info** | Hỏi vô tư, có thiện chí, đọc post chưa kỹ | Cung cấp data đầy đủ, giải thích kỹ |
| **Nhóm 2: Bóp méo info vô tình** | Nghe rumor, chia sẻ không kiểm chứng | Correct bằng data, không tấn công cá nhân |
| **Nhóm 3: Cố tình kích động** | Có agenda riêng, troll professional, đối thủ cạnh tranh | Không thuyết phục được - không waste effort, chỉ đảm bảo narrative cho audience xem |

### 3.6. Khi báo chí/cơ quan chức năng liên hệ

**Quy định**: Đặc biệt strict với 2 nhóm này:

- **Báo chí**: KHÔNG trả lời trực tiếp dù phóng viên quen biết. Chuyển ngay PR Manager (CBC).
- **Cơ quan chức năng** (cơ quan quản lý, A05, Cục Phát thanh Truyền hình): Escalate L4 (Manager Community + LCCA + Dept Head) NGAY, không qua trung gian.

**Không có "off the record"**: Câu nói tưởng riêng tư với phóng viên vẫn có thể bị dùng. Bài học từ nhà sáng lập Communication Policy: *"Bất cứ điều gì bản thân nói đều có thể bị phóng viên sử dụng trong bài viết. Hãy luôn thận trọng với mọi điều chia sẻ."*

---

## 4. Red Lines (Cấm tuyệt đối)

- ❌ Tự ý phản hồi public với báo chí khi chưa có approval PR Manager
- ❌ Xóa tin nhắn / comment / bài đăng khi đang có dấu hiệu sự cố
- ❌ Block đối phương khi đang có dấu hiệu sự cố
- ❌ Phản biện công khai dù bị chỉ đích danh
- ❌ Xin lỗi tràn lan / nhận trách nhiệm khi chưa rõ tình huống
- ❌ Hứa hẹn bồi thường, ưu đãi để xoa dịu (không có approval)
- ❌ Trả lời "off the record" với báo chí
- ❌ Tự ý phát ngôn với cơ quan chức năng không qua escalation
- ❌ Để case escalate qua ngày mà không báo Lead

---

## 5. Quy trình áp dụng

### Khi nào cần check rule này?

- Bất kỳ tình huống nào match định nghĩa "crisis" ở mục 3.1
- Trong giờ hành chính: ngay khi phát hiện
- Ngoài giờ: trong 30 phút (qua Zalo Lead/Manager)

### Decision tree nhanh
Xem `GSX-TOOL-006: Escalation Decision Tree`

### Khi không chắc - hỏi ai?

| Loại câu hỏi | Liên hệ |
|---|---|
| Đây có phải crisis không? | Line Manager (ưu tiên hỏi sớm hơn muộn) |
| Cấp độ bao nhiêu? | Line Manager hoặc Marketing Lead |
| Soạn statement | PR Manager (CBC) |
| Liên hệ cơ quan chức năng | LCCA + Dept Head NGAY |
| Báo chí liên hệ | PR Manager (CBC) NGAY |

### Escalation chain (cho crisis)

```
L1 - CTV/Nhân viên Community
    ↓ trong 30 phút
L2 - Line Manager / Community Lead
    ↓ nếu cấp 2-3
L3 - Marketing Lead + PR Manager
    ↓ nếu cấp 3-4
L4 - Dept Head Game Studio X
    ↓ nếu cấp 4
L5 - BLĐ VNGGames + LCCA + CBC
```

---

## 6. Chế tài khi vi phạm

| Cấp độ | Hành vi | Hình thức xử lý | Người quyết |
|---|---|---|---|
| Cấp 1 | Không báo Lead trong 30 phút, tự xử case nhỏ | Nhắc nhở, đào tạo lại | Line Manager |
| Cấp 2 | Phản hồi public không qua approval, xóa bằng chứng | Cảnh cáo văn bản, performance review | Manager Community |
| Cấp 3 | Phát ngôn với báo chí/cơ quan chức năng không có approval, hứa hẹn bồi thường lớn | Có thể thôi việc theo Nội quy lao động, có thể bồi thường thiệt hại | Dept Head + BLĐ + HR |

---

## 7. Tham chiếu

### Pháp lý gốc
- `GSX-LEGAL-005`: VNG Communication Policy (CS-CBC-001/01) - quy trình phỏng vấn báo chí

### Case study liên quan
- `GSX-CASE-004`: Crisis "VNG bị TQ thâu tóm" (Năm N+2) - **case study quan trọng nhất**, dạy cách response với data
- `GSX-CASE-006`: cơ quan quản lý địa phương yêu cầu (Năm N) - precedent về regulatory pressure
- `GSX-CASE-007`: Một tờ báo lớn tấn công ngành game (Năm N) - precedent về industry-wide attack

### Tool/Checklist liên quan
- `GSX-TOOL-006`: Escalation Decision Tree
- `GSX-TOOL-007`: Scripts Library (đầy đủ script chuẩn)
- `GSX-TOOL-008`: Incident Report Template

### Rule liên quan
- `GSX-OP-003`: Partner SOP KOL (KOL gây crisis)
- `GSX-OP-006`: Community Engagement Rules (user gây crisis)
- `GSX-OP-011`: Information Classification (cần biết thông tin gì share được)

---

## 8. Changelog

| Version | Date | Changed by | Notes |
|---|---|---|---|
| 1.0 | 2026-06-03 | Hub Owner | Initial - ghép từ Game Studio X SOP Phần escalation + Case Studies nhà sáng lập |
