---
doc_id: GSX-PLAT-004
title: "Apple App Store Review Guidelines — Quy định marketing & metadata game"
type: platform_policy
issuing_authority: Apple Inc.
issued_date: 2024-09-01
effective_date: 2024-09-01
status: active
last_summarized: 2026-06-12
summarized_by: Hub Owner
official_link: https://developer.apple.com/app-store/review/guidelines/
applies_to_gsx: yes
priority: high
platforms:
  - store
related_operating_rules:
  - GSX-OP-013: Advertising Standards
  - GSX-OP-002: Content Moderation Rules
  - GSX-OP-001: Data Collection Policy
tags: [app-store, apple, ios, store-guidelines, loot-box, gacha, metadata, rating, platform-policy, game]
---

# Apple App Store Review Guidelines — Quy định marketing & metadata game

## 1. Thông tin cơ bản

- **Nền tảng**: Apple App Store (iOS, iPadOS, macOS, tvOS)
- **Cơ quan ban hành**: Apple Inc.
- **Link gốc**: https://developer.apple.com/app-store/review/guidelines/
- **Phạm vi**: Quy định nội dung app được chấp thuận, yêu cầu metadata (tên, mô tả, screenshot), và các điều kiện về in-app purchase — đặc biệt liên quan game.
- **Lưu ý**: App Store Guidelines cập nhật theo chu kỳ; phần 3 (Business) và phần 5 (Legal) là quan trọng nhất với game mobile.

---

## 2. Tóm tắt nội dung quan trọng cho Game Studio X

> ⚠️ Đây là **tóm tắt diễn giải**, KHÔNG phải bản dịch toàn văn. Xem link gốc để biết quy định đầy đủ.

### 2.1. Nhóm bị CẤM tuyệt đối (liên quan game/marketing)

| Nhóm | Mô tả tóm tắt |
|---|---|
| Loot box không công bố tỷ lệ | Kể từ 2017, Apple yêu cầu app có randomized virtual items phải **công bố odds** trước khi mua. Không công bố = vi phạm. |
| Screenshot/metadata gây hiểu lầm | Screenshot không phản ánh gameplay thực tế, tên app dùng từ của đối thủ (keyword stuffing), mô tả sai tính năng. |
| Nội dung người lớn không có rating 17+ | Game có content bạo lực, khỏa thân hoặc ngôn ngữ 18+ mà khai rating thấp hơn thực tế. |
| Cờ bạc không được cấp phép | Real-money gambling, cá cược, casino thực tiền — chỉ cho phép tại thị trường có giấy phép cụ thể. |
| Bắt chước giao diện Apple | Dùng giao diện/icon giống UI hệ thống Apple để đánh lừa user. |

### 2.2. Nhóm hạn chế — cần điều kiện

| Nhóm | Điều kiện |
|---|---|
| In-App Purchase & Loot box | Phải dùng hệ thống IAP của Apple (30% phí); phải hiển thị tỷ lệ cho randomized items; không khóa nội dung đã mua nếu user xóa-cài lại. |
| Subscription trong game | Phải rõ về điều khoản gia hạn, dễ hủy; không được ẩn mức phí. |
| Quảng cáo trong game (monetization) | Không được hiển thị quảng cáo người lớn trong game xếp hạng thấp hơn 17+. |
| VoIP/Social features | Nếu game có chat/voice → phải có cơ chế report content xấu, moderation. |
| Dữ liệu người dùng | App phải có Privacy Nutrition Label (khai báo data usage); nếu thu thập data cho marketing → phải xin phép App Tracking Transparency (ATT). |

### 2.3. Yêu cầu metadata đặc biệt cho game

1. **Tên app (App Name):** Không vượt quá 30 ký tự. Không nhồi keyword ("Best RPG Game 2024 Free Action"), không dùng tên thương hiệu của bên khác.
2. **Mô tả (Description):** Phải chính xác với tính năng thực tế. Không hứa hẹn tính năng chưa có. Không dùng ngôn ngữ quảng cáo thái quá như "revolutionary", "world-class" nếu không có căn cứ.
3. **Screenshots & Preview Video:** Phải phản ánh gameplay thực tế trong device được chọn. Overlay text trên screenshot được phép nhưng không được che toàn bộ gameplay.
4. **Keywords:** 100 ký tự giới hạn; không được trùng tên app; không nhồi tên đối thủ.
5. **Age Rating:** Khai báo phải chính xác — Apple kiểm tra và có thể forced-update rating nếu phát hiện sai.

### 2.4. Loot box / Gacha — Yêu cầu cụ thể

Apple yêu cầu (guideline 3.1.1):
- Hiển thị **odds của từng item** trước khi user mua loot box/gacha roll.
- Không được che giấu tỷ lệ sau nhiều lớp click.
- Khuyến nghị: hiển thị tỷ lệ trong popup ngay trước khi confirm payment.

---

## 3. Ý nghĩa thực tế với team Community

### 3.1. Việc gì BẮT BUỘC?
- Công bố tỷ lệ gacha/loot box rõ ràng (in-game screen + có thể trong App Store description).
- Khai báo Privacy Nutrition Label chính xác; xin ATT nếu track user cho ads.
- Screenshot/video preview phản ánh đúng gameplay thực.
- Rating đúng với nội dung — đặc biệt nếu game có chat user-generated.

### 3.2. Việc gì BỊ CẤM?
- Ẩn tỷ lệ gacha hoặc gây hiểu nhầm về tỷ lệ.
- Dùng tên/brand của đối thủ trong metadata để tối ưu search.
- Bán IAP bằng hệ thống thanh toán ngoài mà không thông báo đúng cách.
- Rating thấp cho game có nội dung 17+.

### 3.3. Hậu quả vi phạm
- App bị từ chối (Rejection) khi submit/update.
- App bị gỡ khỏi store (Removal) nếu phát hiện sau khi publish.
- Developer account bị terminate cho vi phạm nghiêm trọng.
- Tại Việt Nam: vi phạm công bố tỷ lệ loot box có thể thêm vi phạm NĐ147 (GSX-LEGAL-009).

---

## 4. Liên hệ với Operating Rules

- **GSX-OP-013**: Từ tuyệt đối trong App Name/Description vi phạm cả App Store guidelines và Luật QC VN.
- **GSX-OP-001**: ATT + Privacy Nutrition Label là thể hiện của nghĩa vụ consent theo NĐ13.
- **GSX-OP-002**: Game có chat/voice phải có moderation (UGC content rules).

---

## 5. Tài liệu tham khảo

- App Store Review Guidelines: https://developer.apple.com/app-store/review/guidelines/
- App Store Connect Help — App Information: https://developer.apple.com/help/app-store-connect/
- In-App Purchase & Loot box disclosure (guideline 3.1.1): https://developer.apple.com/app-store/review/guidelines/#in-app-purchase
- App Tracking Transparency: https://developer.apple.com/documentation/apptrackingtransparency

---

## 6. Lịch sử cập nhật

| Version | Date | Updated by | Notes |
|---|---|---|---|
| 1.0 | 2026-06-12 | Hub Owner | Initial summary — tóm tắt cho Game Studio X |
