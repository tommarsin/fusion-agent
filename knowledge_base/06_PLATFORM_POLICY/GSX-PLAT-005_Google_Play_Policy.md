---
doc_id: GSX-PLAT-005
title: "Google Play Developer Policy — Quy định store listing & nội dung game"
type: platform_policy
issuing_authority: Google LLC
issued_date: 2024-01-01
effective_date: 2024-01-01
status: active
last_summarized: 2026-06-12
summarized_by: Hub Owner
official_link: https://play.google.com/about/developer-content-policy/
applies_to_gsx: yes
priority: high
platforms:
  - store
related_operating_rules:
  - GSX-OP-013: Advertising Standards
  - GSX-OP-002: Content Moderation Rules
  - GSX-OP-001: Data Collection Policy
tags: [google-play, android, store-guidelines, loot-box, gacha, metadata, rating, platform-policy, game, data-safety]
---

# Google Play Developer Policy — Quy định store listing & nội dung game

## 1. Thông tin cơ bản

- **Nền tảng**: Google Play Store (Android)
- **Cơ quan ban hành**: Google LLC
- **Link gốc**: https://play.google.com/about/developer-content-policy/
- **Link phụ (Store Listing)**: https://support.google.com/googleplay/android-developer/answer/9876820
- **Phạm vi**: Nội dung app được chấp thuận, yêu cầu Store Listing (title, description, screenshot), Data Safety section, và quy định về in-app purchase — đặc biệt cho game mobile.
- **Lưu ý**: Google Play policy bao gồm cả Families Policy (game dành cho trẻ em), nghiêm ngặt hơn policy thông thường.

---

## 2. Tóm tắt nội dung quan trọng cho Game Studio X

> ⚠️ Đây là **tóm tắt diễn giải**, KHÔNG phải bản dịch toàn văn. Xem link gốc để biết quy định đầy đủ.

### 2.1. Nhóm bị CẤM tuyệt đối

| Nhóm | Mô tả tóm tắt |
|---|---|
| Nội dung gây hại cho trẻ em | Bất kỳ nội dung nào gây hại hoặc khai thác trẻ em — bị xóa ngay và tài khoản bị terminate. |
| Cờ bạc thực tiền không phép | Tương tự App Store; cần giấy phép quốc gia cụ thể; cấm hoàn toàn tại VN. |
| Phần mềm độc hại / Malware | Không được thu thập data bí mật, không cài backdoor. |
| Thông tin sai lệch / Deceptive | App giả mạo thương hiệu khác, description sai tính năng, screenshot không thực tế. |
| Vi phạm quyền riêng tư | Thu thập data cá nhân vượt phạm vi khai báo trong Data Safety section. |

### 2.2. Nhóm hạn chế — cần điều kiện

| Nhóm | Điều kiện |
|---|---|
| Simulated gambling / Loot box | Được phép nếu không dùng tiền thật. **Kể từ 2024:** Google Play yêu cầu khai báo "paid loot boxes" trong questionnaire khi submit. |
| Nội dung 18+ / Mature | Game có bạo lực cao, nội dung người lớn → cần đặt rating "Mature 17+" và bật bảo vệ content phù hợp. |
| Monetization trong game | In-app purchase qua hệ thống Google Play Billing; subscription cần rõ điều khoản; không lock content đã mua nếu xóa-cài lại. |
| Quảng cáo trong game (3rd party ads) | Không hiển thị quảng cáo người lớn trong game có rating thấp. SDK quảng cáo phải tuân thủ Play's Ads Policy. |
| Data collection | Phải khai báo đầy đủ trong **Data Safety section** — loại data thu thập, mục đích, sharing với bên thứ ba. |

### 2.3. Data Safety Section — Yêu cầu bắt buộc từ 2022

Kể từ 5/2022, mọi app trên Google Play phải khai báo:
- **Loại dữ liệu thu thập**: vị trí, contact, tài chính, tin nhắn, app activity (gameplay data)…
- **Mục đích sử dụng**: analytics, quảng cáo, cải thiện app, tính năng cốt lõi.
- **Chia sẻ với bên thứ ba**: analytics SDK, ads SDK, bên thứ ba.
- **Bảo mật**: mã hóa khi truyền, người dùng có thể xóa data.

Game không khai báo đúng → bị từ chối update; khai báo sai → bị gỡ.

### 2.4. Store Listing — Yêu cầu metadata

1. **Title (30 ký tự):** Không keyword stuffing, không dùng tên đối thủ.
2. **Short description (80 ký tự):** Tóm tắt giá trị cốt lõi, không misleading.
3. **Full description:** Chính xác với tính năng thực; không copy-paste từ web không liên quan; không dùng từ "free" nếu có IAP ẩn.
4. **Screenshots/Videos:** Phải là actual gameplay, không là render/cinematic. Google ngày càng kiểm chặt điều này sau nhiều khiếu nại từ user.
5. **Content Rating (IARC):** Phải điền questionnaire IARC; rating được cấp tự động; khai báo sai có thể bị gỡ.

### 2.5. Loot box / Gacha — Yêu cầu cụ thể

Google Play (từ 2024) yêu cầu:
- Khai báo trong Store Listing questionnaire rằng game có "paid randomized items".
- Khuyến nghị mạnh (nhiều thị trường bắt buộc): hiển thị tỷ lệ trước khi mua.
- Tại Nhật và một số thị trường: bắt buộc pity system disclosure.

---

## 3. Ý nghĩa thực tế với team Community

### 3.1. Việc gì BẮT BUỘC?
- Điền Data Safety section chính xác và đồng bộ với privacy policy thực tế.
- Khai báo "paid loot boxes" trong questionnaire nếu game có gacha.
- Rating IARC phải khớp nội dung thực — đặc biệt nếu game có chat, violence, gambling elements.
- Screenshot/video phản ánh gameplay thực tế.

### 3.2. Việc gì BỊ CẤM?
- Thu thập data vượt phạm vi đã khai báo trong Data Safety section.
- Description hứa hẹn tính năng chưa có trong phiên bản hiện tại.
- Hiển thị quảng cáo người lớn trong game có rating thấp hơn 17+.
- Dùng billing system ngoài Google Play cho IAP (trừ trường hợp được approved).

### 3.3. Hậu quả vi phạm
- App update bị từ chối.
- App bị gỡ khỏi Play Store.
- Developer account bị terminate.
- Kết hợp với NĐ147 (GSX-LEGAL-009): game tại VN có thể đối diện vi phạm kép.

---

## 4. Liên hệ với Operating Rules

- **GSX-OP-001**: Data Safety section là biểu hiện công khai của nghĩa vụ NĐ13 — phải nhất quán.
- **GSX-OP-013**: Từ tuyệt đối trong title/description vi phạm cả Google Play policy và Luật QC VN.
- **GSX-OP-002**: Nội dung chat/UGC trong game cần có moderation system (Play yêu cầu).

---

## 5. Tài liệu tham khảo

- Google Play Developer Policy Center: https://play.google.com/about/developer-content-policy/
- Data Safety section help: https://support.google.com/googleplay/android-developer/answer/10787469
- Store listing best practices: https://support.google.com/googleplay/android-developer/answer/9876820
- IARC content rating: https://support.google.com/googleplay/android-developer/answer/188189
- Payments policy: https://support.google.com/googleplay/android-developer/answer/9858738

---

## 6. Lịch sử cập nhật

| Version | Date | Updated by | Notes |
|---|---|---|---|
| 1.0 | 2026-06-12 | Hub Owner | Initial summary — tóm tắt cho Game Studio X |
