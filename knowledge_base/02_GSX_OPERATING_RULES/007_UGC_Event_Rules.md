---
doc_id: GSX-OP-007
title: "UGC Event Rules - Quy tắc tổ chức UGC contest/event"
version: 1.0
status: draft
created: 2026-06-03
last_updated: 2026-06-03
last_reviewed_by: Hub Owner
legal_owner: LCCA
next_review_date: 2026-12-03
applies_to: Community Team, Marketing Lead, người thiết kế UGC contest
related_legal_sources:
  - GSX-LEGAL-001: Nghị định 13/2023/NĐ-CP
  - GSX-LEGAL-008: Facebook Community Standards
related_case_studies:
  - GSX-CASE-001: UGC Contest - Vi phạm NĐ13/2023
related_tools:
  - GSX-TOOL-002: UGC Event Compliance Checklist
  - GSX-TOOL-001: Pre-Launch Checklist
tags: [ugc, contest, event, nd13, data-privacy, review-process]
---

# GSX-OP-007: UGC Event Rules

## 1. Mục đích & Phạm vi

### 1.1. Tại sao có rule này?

Năm 2025 Game Studio X đã có sự cố nghiêm trọng (xem `GSX-CASE-001`): UGC contest yêu cầu user đăng ảnh giấy khen/giấy tờ → 90 user tham gia trong 3 ngày → 22 case vi phạm NĐ13/Facebook Standards phải xóa, trong đó 1 case lộ CCCD.

Rule này codify **mọi điều phải làm và không được làm** khi thiết kế UGC contest, để sự cố tương tự không lặp lại.

### 1.2. Áp dụng cho ai?

- Mọi người thiết kế UGC contest trong Game Studio X
- Mọi người duyệt thể lệ contest trước go-live
- CTV moderate contest trong 24h đầu

### 1.3. Không áp dụng cho?

- Survey/feedback đơn thuần (không phải UGC)
- Comment contest đơn giản kiểu "tag bạn" không upload ảnh
- Mini-game không yêu cầu user tạo nội dung

### 1.4. Viết tắt & Thuật ngữ trong tài liệu này

| Viết tắt/Thuật ngữ | Giải thích |
|---|---|
| **UGC** (User-Generated Content) | Nội dung do user tạo (fan art, cosplay, video gameplay, story, meme...) |
| **CCCD** | Căn Cước Công Dân - giấy tờ tùy thân định danh |
| **NĐ13** | Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân |
| **Worst-case design** | Nguyên tắc thiết kế UGC: user sẽ tự lộ thông tin nhạy cảm hơn yêu cầu - phải lường được |
| **Dữ liệu cá nhân nhạy cảm** | Theo NĐ13: SĐT, email, địa chỉ, CCCD, ảnh khuôn mặt, dữ liệu sinh trắc, trẻ em... |
| **2nd-eye review** | Vòng kiểm tra chéo bởi người thứ 2 (không phải designer ban đầu) trước khi go-live |
| **Spot-check** | Kiểm tra ngẫu nhiên định kỳ trong 24h đầu sau khi đăng |
| **Promotion Tool** | Công cụ nội bộ VNG để thu data nhạy cảm (thay Google Form) |
| **LCCA** | Bộ phận Pháp chế của VNG |
| **A05** | Cục An ninh mạng - Bộ Công an |

> 📖 Tra cứu thêm: `00_INDEX_VERSION/GLOSSARY.md`

---

## 2. Nguyên tắc cốt lõi

1. **Định nghĩa rộng "dữ liệu cá nhân"**: Mọi giấy tờ chứa ít nhất 1 trong: họ tên thật, ngày sinh, địa chỉ, số định danh, ảnh khuôn mặt → đều thuộc data cá nhân cần bảo vệ. **Không có khái niệm "giấy tờ phụ"**.

2. **Worst-case design**: User sẽ làm nhiều hơn yêu cầu. Thiết kế phải lường tình huống user tự lộ giấy tờ nhạy cảm hơn cả thể lệ yêu cầu.

3. **Cảnh báo ở chỗ user thực sự đọc**: Caption chính + Visual thể lệ. Không chỉ comment phụ.

4. **Tốc độ phát hiện > tốc độ xử lý**: Sự cố Game Studio X 2025 mất 3 ngày mới phát hiện. Phải có monitor 4-6h trong 24h đầu.

5. **Review chéo bắt buộc**: Không UGC nào go-live mà không có 2nd-eye trong team.

---

## 3. Quy định chi tiết

### 3.1. Red Line - Cấm hoàn toàn

**Quy định**: Mọi UGC contest liên quan đến giấy tờ, ảnh cá nhân, thông tin định danh đều **KHÔNG được phép triển khai**.

Bao gồm nhưng không giới hạn:
- Giấy tờ tùy thân (CCCD, CMND, passport, bằng lái xe)
- Giấy khen, bằng khen, chứng nhận có thông tin định danh
- Giấy nhập học, giấy báo trúng tuyển
- Học bạ, bảng điểm
- Sổ hộ khẩu, giấy khai sinh
- Ảnh chân dung cá nhân kèm thông tin định danh
- Hóa đơn, biên lai có thông tin cá nhân
- Vé máy bay, vé tàu kèm tên thật

**Lý do**: Dù thể lệ có "yêu cầu che thông tin", thực tế user sẽ:
- Bỏ qua cảnh báo (như đã xảy ra 16/22 case năm 2025)
- Tự đăng thêm giấy tờ khác không yêu cầu (như case lộ CCCD)
- Bị Facebook gỡ post + ban account
- VNGGames Fanpage có nguy cơ bị warning vi phạm tiêu chuẩn cộng đồng

### 3.2. UGC được phép - 4 loại

**Quy định**: Các loại UGC sau được phép triển khai (vẫn cần qua quy trình review):

1. **Creative gameplay content**:
   - Highlight video gameplay
   - Screenshot moment hay trong game
   - Build/setup tướng

2. **Fan art & cosplay**:
   - Vẽ nhân vật game
   - Cosplay tướng (theo skin gốc)
   - 3D model, figurine

3. **Story & testimonial**:
   - Kể kỷ niệm với game (text only, không upload ảnh đời thực)
   - Review trải nghiệm
   - Tag bạn cùng chơi

4. **Meme & humor**:
   - Meme về tướng/skill
   - Joke trong cộng đồng
   - Comic strip

**Lưu ý**: Mọi UGC có upload ảnh đời thực user vẫn cần check checklist 7 bước trong `GSX-OP-002` trước khi user submit.

### 3.3. Quy trình review chéo bắt buộc

**Quy định**: Mọi UGC contest (kể cả không liên quan giấy tờ) phải có vòng review chéo trong team Community trước go-live.

Workflow:
```
1. Người thiết kế → viết draft thể lệ
2. Self-check với UGC Compliance Checklist
3. Submit Lead review (mandatory)
4. Lead chỉ approve nếu: 
   - Pass checklist 100%
   - Có disclaimer rõ ràng
   - Có plan moderation 24h đầu
5. Lead approve → đăng
6. Moderate 24h đầu theo lịch
```

**Không bỏ bước review chéo dù lý do gì**: bài "nhỏ", "gấp", "đã làm tương tự trước".

### 3.4. Vị trí cảnh báo bắt buộc

**Quy định**: Mọi cảnh báo bảo vệ thông tin cá nhân phải xuất hiện trong:

1. **Caption chính** (dòng đầu tiên hoặc trong 3 dòng đầu)
2. **Hình ảnh thể lệ** (visual banner)

**Không được phép** đặt cảnh báo ở:
- ❌ Comment phụ
- ❌ Mô tả nhỏ dưới banner
- ❌ Link out đến trang khác
- ❌ Chỉ trong reply user (sau khi đã có người vi phạm)

**Lý do**: Bài học từ case 2025 - user bỏ qua cảnh báo nếu không thấy ngay khi đọc.

### 3.5. Plan moderation 24h đầu

**Quy định**: Mọi UGC contest phải có plan moderation cụ thể, không chờ "moderate bình thường".

Yêu cầu tối thiểu:
- **Random spot-check mỗi 4-6 tiếng** trong 24h đầu
- Có ít nhất 2 người được assign (chính + backup)
- Lịch moderation gửi Lead trước khi go-live
- Action plan rõ ràng khi phát hiện vi phạm:
  - Ai có quyền xóa post user?
  - Ai có quyền ban user vi phạm?
  - Khi nào escalate Lead?

### 3.6. Auto-scan keyword/visual

**Quy định**: Nếu có thể, set up auto-scan để monitor:
- Keyword nhạy cảm trong comment ("CCCD", "giấy tờ", "ảnh cá nhân")
- Visual có hình giấy tờ (qua tool nhận dạng nếu có)

Hiện tại Game Studio X có Content Scanner tool - dùng cho moderation hậu kỳ.

### 3.7. Quy định về phần thưởng

**Quy định**: Để giảm risk user lộ giấy tờ "vì giải thưởng hấp dẫn":

- Phần thưởng nên dạng **in-game items** (skin, RP, đồ trang trí) thay vì voucher đời thực
- Nếu là gift card/voucher → giá trị nhỏ, không yêu cầu xác minh danh tính
- Nếu phần thưởng > 500k → chuyển sang **Promotion Tool** để verify (xem `GSX-OP-001`)

---

## 4. Red Lines (Cấm tuyệt đối)

- ❌ UGC yêu cầu upload bất kỳ giấy tờ định danh nào (kể cả "có che thông tin")
- ❌ UGC yêu cầu upload ảnh CCCD/passport/bằng lái dưới bất kỳ hình thức nào
- ❌ Triển khai UGC contest mà không có review chéo trong team
- ❌ Cảnh báo bảo vệ data chỉ ở comment phụ (không có ở caption + visual)
- ❌ UGC không có plan moderation 24h đầu
- ❌ UGC có giải thưởng yêu cầu user gửi data nhạy cảm qua Google Form

---

## 5. Quy trình áp dụng

### Khi nào cần check rule này?

- Trước khi viết thể lệ bất kỳ UGC contest nào
- Khi review thể lệ contest từ Marketing/CTV
- Khi BTC bên thứ 3 đề xuất UGC contest có VNG hỗ trợ

### Checklist nhanh
Xem `GSX-TOOL-002: UGC Event Compliance Checklist` - đặc biệt section:

```
[ ] Event có yêu cầu user đăng tải hình ảnh chứa dữ liệu cá nhân không?
    → Nếu CÓ: dừng triển khai, redesign thể lệ
    → Nếu KHÔNG: tiếp tục checklist
[ ] Cảnh báo bảo vệ thông tin cá nhân có ở caption chính không?
[ ] Cảnh báo bảo vệ thông tin cá nhân có ở visual thể lệ không?
[ ] Có người trực moderate trong 24h đầu không?
```

### Khi không chắc - hỏi ai?

| Loại câu hỏi | Liên hệ |
|---|---|
| Concept UGC này có ổn không? | Community Lead |
| Có vi phạm NĐ13 không? | LCCA (xem CONTACTS_DIRECTORY) |
| Phần thưởng có cần xác minh? | Community Lead + Brand Manager |
| Phát hiện vi phạm trong contest đang chạy | Community Lead NGAY |

---

## 6. Chế tài khi vi phạm

| Cấp độ | Hành vi | Hình thức xử lý | Người quyết |
|---|---|---|---|
| Cấp 1 | UGC thiếu disclaimer ở visual nhưng có ở caption | Sửa ngay, ghi log | Community Lead |
| Cấp 2 | UGC không có review chéo, monitor 24h | Đào tạo lại CTV, cảnh cáo, review process | Community Lead + Manager |
| Cấp 3 | UGC vi phạm NĐ13 - user đã đăng giấy tờ định danh public | Gỡ contest ngay, gỡ toàn bộ post user vi phạm, incident report, có thể bị A05 tuýt còi, kỷ luật theo Nội quy lao động | Dept Head + LCCA |

---

## 7. Tham chiếu

### Pháp lý gốc
- `GSX-LEGAL-001`: Nghị định 13/2023/NĐ-CP - Điều 3 (nguyên tắc tối thiểu hóa dữ liệu, trách nhiệm bảo mật)
- `GSX-LEGAL-008`: Facebook Community Standards - cấm đăng giấy tờ chính phủ

### Case study liên quan
- `GSX-CASE-001`: UGC Contest 2025 - 22 case vi phạm trong 3 ngày, bài học gốc

### Tool/Checklist liên quan
- `GSX-TOOL-002`: UGC Event Compliance Checklist
- `GSX-TOOL-001`: Pre-Launch Checklist (universal)

### Rule liên quan
- `GSX-OP-001`: Data Collection Policy
- `GSX-OP-002`: Content Moderation Rules

---

## 8. Changelog

| Version | Date | Changed by | Notes |
|---|---|---|---|
| 1.0 | 2026-06-03 | Hub Owner | Initial - codify từ Case Study UGC ND13 2025 |
