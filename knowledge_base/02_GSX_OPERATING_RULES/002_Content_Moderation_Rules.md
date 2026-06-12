---
doc_id: GSX-OP-002
title: "Content Moderation Rules - Kiểm duyệt nội dung"
version: 1.0
status: draft
created: 2026-06-03
last_updated: 2026-06-03
last_reviewed_by: Hub Owner
legal_owner: LCCA
next_review_date: 2026-12-03
applies_to: Community Team, CTV làm content/moderation, người duyệt bài
related_legal_sources:
  - GSX-LEGAL-002: Bộ luật Hình sự - Điều 225, 226 (IP)
  - GSX-LEGAL-004: Luật An ninh mạng
  - GSX-LEGAL-006: VNG Social Media Guidelines
  - GSX-LEGAL-008: Facebook Community Standards
related_case_studies:
  - GSX-CASE-002: Bản đồ vi phạm trong content moderation
related_tools:
  - GSX-TOOL-005: Content Scanner Guide
  - GSX-TOOL-001: Pre-Launch Checklist
tags: [content-moderation, scanner, ban-do, ip-rights, platform-rules]
---

# GSX-OP-002: Content Moderation Rules

## 1. Mục đích & Phạm vi

### 1.1. Tại sao có rule này?

Mọi nội dung đăng trên kênh chính thức VNGGames (Website, Fanpage, Facebook Group, Discord) đại diện cho thương hiệu. Một bài đăng sai có thể dẫn đến:
- Bị cơ quan quản lý/Cục An ninh mạng tuýt còi (vi phạm chính trị, bản đồ)
- Bị nền tảng gỡ post, warning fanpage, bóp tương tác
- Bị bên thứ 3 claim bản quyền
- **Nhân viên duyệt bài có thể bị thôi việc** (xem `GSX-CASE-002`)

Rule này codify 9 nhóm tiêu chí + checklist 7 bước cho hình ảnh + tiêu chuẩn theo nền tảng.

### 1.2. Áp dụng cho ai?

- Mọi nhân viên/CTV duyệt bài trước khi đăng
- Mọi người tạo content (bài viết, banner, video, livestream overlay)
- Mọi người chia sẻ lại content từ partner/community

### 1.3. Không áp dụng cho?

- Bình luận của user (có rule moderation riêng trong `GSX-OP-006: Community Engagement Rules`)
- Content nội bộ team không public ra ngoài

### 1.4. Viết tắt & Thuật ngữ trong tài liệu này

| Viết tắt/Thuật ngữ | Giải thích |
|---|---|
| **Game Studio X Scanner** | Tool nội bộ Game Studio X để moderation content trước khi đăng (xem `GSX-TOOL-005`) |
| **Whitelist** | Danh sách từ khóa game Game Studio X được benefit-of-the-doubt khi gặp ambiguous case |
| **Red Line** | Hành vi tuyệt đối cấm - không có ngoại lệ, gặp = STOP NOW |
| **UGC** (User-Generated Content) | Nội dung do user tạo (fan art, cosplay, video gameplay...) |
| **MXH** | Mạng xã hội (Facebook, Instagram, TikTok, Discord...) |
| **OOH** | Out-Of-Home - quảng cáo ngoài trời |
| **Bản đồ fiction** | Bản đồ trong game (Summoner's Rift, Runeterra) - không phải bản đồ địa lý thực, không vi phạm |
| **CBC** | Bộ phận Truyền thông Doanh nghiệp của VNG |
| **LCCA** | Bộ phận Pháp chế của VNG |

> 📖 Tra cứu thêm: `00_INDEX_VERSION/GLOSSARY.md`

---

## 2. Nguyên tắc cốt lõi

1. **Mọi bài đăng đều phải đi qua scanner** trước khi go-live - không có exception "bài nhỏ", "bài gấp", "bài routine"

2. **Bản đồ = BLOCKED tuyệt đối** - bất kỳ hình dạng lãnh thổ nào (VN hay quốc tế), không có ngoại lệ ngoài bản đồ fiction game thuần túy

3. **Khi nhiều ảnh → ảnh xấu nhất quyết định verdict** - 1 ảnh BLOCKED = cả bài BLOCKED

4. **Whitelist gaming Game Studio X → benefit of the doubt** nhưng KHÔNG bao gồm bản đồ

5. **Platform tier khác nhau, tiêu chí giống nhau** - chỉ khác tone/format

---

## 3. Quy định chi tiết

### 3.1. 9 nhóm tiêu chí kiểm duyệt (4A-4I)

**Quy định**: Mọi content phải pass 9 nhóm này. 1 nhóm FAIL critical = BLOCKED.

#### 4A. Chính trị & Pháp lý VN
- ❌ BLOCKED: Bản đồ bất kỳ có hình dạng lãnh thổ (VN/quốc tế) - điểm 0, không ngoại lệ
- ❌ BLOCKED: Chống Nhà nước, kêu gọi biểu tình
- ❌ BLOCKED: Cờ Nhà nước Việt Nam (chỉ được dùng theo hướng dẫn riêng)
- ✅ SAFE: Bản đồ fiction game thuần túy (Summoner's Rift, Runeterra)

#### 4B. Tôn giáo & Dân tộc
- ❌ BLOCKED: Chế giễu, bôi nhọ tôn giáo; kỳ thị dân tộc
- ✅ SAFE: Nhân vật game có yếu tố tôn giáo trong lore (vd: Karma, Yi)

#### 4C. Bạo lực & Gore
- ✅ SAFE: Stylized (game animation, anime style)
- ❌ BLOCKED: Realistic (người thật, máu thật, vết thương thật)

#### 4D. Sexual content
- ❌ BLOCKED: Nude, sexually suggestive, fetish
- ⚠️ WARNING: Trang phục hở hơn skin gốc của tướng
- ✅ SAFE: Trung thành skin gốc, cosplay tướng theo bản gốc

#### 4E. Thông tin cá nhân
- ❌ BLOCKED: SĐT, link cá nhân trong ảnh
- ❌ BLOCKED: CCCD, giấy tờ tùy thân (xem `GSX-OP-001`)
- ⚠️ WARNING: Ảnh người thật chưa che mặt (cần đồng ý)

#### 4F. Cờ bạc, cá độ, trục lợi
- ❌ BLOCKED: Quảng bá cá độ, kèo nhà cái
- ❌ BLOCKED: Cày thuê, boost rank, mua bán tài khoản

#### 4G. Bản quyền
- ❌ BLOCKED: Nhạc bản quyền không phép
- ❌ BLOCKED: Watermark bên thứ 3 không phép
- ❌ BLOCKED: Repost nguyên content đối thủ
- ⚠️ WARNING: Fan art nhân vật ngoài Riot/VNGGames không credit

#### 4H. Thương mại trái phép
- ❌ BLOCKED: Hack/cheat, mua bán tài khoản
- ⚠️ WARNING: So sánh game đối thủ mang tính công kích

#### 4I. Ngôn ngữ
- ❌ BLOCKED: Chửi tục nặng, kể cả viết tắt cách quãng (C.Ú.T, đ.m, v~l = ngang viết đầy đủ)
- ⚠️ WARNING: Xúc phạm trí tuệ ("có não không", "não cá vàng", "IQ âm", "óc lợn") - mọi nền tảng
- ✅ SAFE (Group/Discord): Slang gameplay (noob, feed, int, gank, bánh, ăn hành)
- ✅ SAFE: Whitelist Game Studio X (Wild Rift, Tốc Chiến, LMHT, LOL, TFT, Valorant, PUBG Mobile, tướng, skin, rank, meta...)

#### 4J. Từ ngữ tuyệt đối trong quảng cáo 🛑
**Áp dụng từ 05/07/2026** theo TT12/2026/TT-BVHTTDL + NĐ87/2026/NĐ-CP.
- ❌ BLOCKED: Dùng "nhất", "duy nhất", "tốt nhất", "số một", "hàng đầu", "đỉnh nhất" hoặc tương tự (cả tiếng Việt + tiếng Anh: "best", "top", "#1", "leading") trong **content thương mại** mà KHÔNG có tài liệu chứng minh hợp pháp
- ⚠️ WARNING: Dùng trong mô tả gameplay/character guide official
- ✅ SAFE: Diễn đạt định tính ("một trong những giải lớn", "cộng đồng sôi động", "phần thưởng hấp dẫn")
- ✅ SAFE: User comment / KOL review trên kênh KOL (không phải kênh VNG)

**Khi BẮT BUỘC dùng**: trình Brand Manager phụ trách sản phẩm duyệt + đính kèm tài liệu chứng minh + ghi rõ nguồn trên ấn phẩm. Xem `GSX-OP-013` chi tiết.

### 3.2. 4 verdict & 4 severity

**Verdict**:
- ✅ **SAFE**: Đăng được ngay
- ⚠️ **WARNING**: Cần chỉnh sửa nhỏ trước khi đăng, hoặc cần Lead duyệt thêm
- 🛑 **BLOCKED**: Không được đăng - phải redesign hoặc bỏ
- ❓ **NEEDS_REVIEW**: Edge case - escalate Lead

**Severity của findings**:
- **CRITICAL**: Vi phạm ngay lập tức → kéo verdict về BLOCKED (vd: bản đồ, chửi tục, chính trị)
- **HIGH**: Rủi ro cao → thường kéo về WARNING hoặc BLOCKED tuỳ ngữ cảnh
- **MED**: Cần chỉnh sửa nhỏ → thường ở mức WARNING
- **LOW**: Lưu ý nhỏ, không ảnh hưởng verdict nếu không kết hợp với lỗi khác

### 3.3. Checklist 7 bước cho hình ảnh

**Quy định**: Mọi bài có ảnh phải đi qua checklist 7 bước theo thứ tự. Dừng ngay khi phát hiện vi phạm BLOCKED.

```
1. Có bản đồ không?
   → CÓ → BLOCKED điểm 0, không check tiếp
   → KHÔNG → bước 2

2. Trang phục hở?
   → So sánh với skin gốc tướng
   → Hở hơn skin gốc → WARNING
   → Trung thành skin gốc → SAFE

3. Văn bản trong ảnh
   → Có SĐT, link, thông tin cá nhân không?
   → Có từ khóa cấm không?

4. Watermark bên thứ 3
   → Logo/watermark đơn vị khác không được cấp phép → cần xoá hoặc credit

5. Bạo lực
   → Stylized (game animation) → SAFE
   → Realistic (người thật, máu thật) → BLOCKED

6. Background & ngữ cảnh
   → Background có yếu tố nhạy cảm không?
   → Người thật trong ảnh có đồng ý không?

7. (Website/Fanpage thêm) - Chất lượng ảnh
   → Resolution đạt chuẩn đăng không?
```

**Lưu ý quan trọng**: Khi bài đăng có **nhiều ảnh** - nếu BẤT KỲ ảnh nào BLOCKED → verdict toàn bài = BLOCKED.

### 3.4. Tiêu chuẩn theo nền tảng

**Quy định**: Tiêu chí 9 nhóm áp dụng đồng đều, chỉ khác về tone & format yêu cầu.

| Nền tảng | Tier | Check thêm |
|---|---|---|
| **Website** | Formal | Chính tả, ngữ pháp, độ chính xác thông tin, chất lượng ảnh (đủ resolution), tone văn phong phù hợp thương hiệu |
| **Fanpage** | Formal | Chính tả, ngữ pháp, tone văn phong |
| **Facebook Group** | Casual | Slang game, meme cộng đồng, ngôn ngữ informal là bình thường. Chỉ kiểm 9 nhóm vi phạm cốt lõi |
| **Discord** | Casual | Tương tự Facebook Group - cộng đồng gaming, slang & meme là văn hóa bình thường |

**Default rule**: Nếu không rõ nền tảng → mặc định áp dụng tiêu chuẩn **Facebook Group**.

### 3.5. Whitelist gaming Game Studio X

**Quy định**: Nội dung có từ khóa whitelist Game Studio X rõ ràng được **benefit of the doubt** trong các trường hợp ambiguous.

**Whitelist**: Wild Rift, Tốc Chiến, Liên Minh Huyền Thoại, LOL, TFT, Đấu Trường Chân Lý, Valorant, PUBG Mobile, tướng, skin, rank, meta, buff, nerf, patch, gank, jungler, carry, support, cosplay tướng, fan art, esport, VCS, Wild Rounds, Quân Đoàn Tốc Chiến, Cắm Mắt Bắt View

**Ngoại lệ duy nhất**: **Bản đồ KHÔNG có benefit of the doubt** dù có từ khóa whitelist. Bản đồ luôn = BLOCKED.

---

## 4. Red Lines (Cấm tuyệt đối)

- ❌ Đăng bài có bản đồ hình dạng lãnh thổ (VN/quốc tế) - kể cả vô tình background
- ❌ Bypass quy trình scanner ("bài gấp", "bài routine", "bài cấp trên giao")
- ❌ Tự ý đăng mà không có 2nd-eye review nếu là bài lớn (banner main, video chính, bài announce sản phẩm)
- ❌ Đăng content có chửi tục, kể cả viết tắt cách quãng
- ❌ Đăng nhạc bản quyền không có license
- ❌ Đăng watermark/logo bên thứ 3 không được cấp phép
- ❌ Sửa content sau khi Lead đã approve mà không re-review

---

## 5. Quy trình áp dụng

### Khi nào cần check rule này?

- **Trước mọi bài đăng** trên Website, Fanpage, Group, Discord
- Khi share lại content từ partner/community/KOL
- Khi duyệt creative từ designer/CTV trước khi gửi đi in
- Khi review livestream overlay/banner trước khi go-live

### Workflow chuẩn

```
1. Người tạo content → self-check với scanner
2. Nếu SAFE → submit Lead/Senior review
3. Nếu WARNING → fix theo finding → re-scan
4. Nếu BLOCKED → redesign hoặc bỏ
5. Lead approve → đăng
6. Sau đăng: monitor 24h cho bài lớn
```

### Checklist nhanh
Xem `GSX-TOOL-005: Content Scanner Guide`

### Khi không chắc - hỏi ai?

| Loại câu hỏi | Liên hệ |
|---|---|
| Ảnh này có vi phạm nhóm 4A-4I không? | Community Lead |
| Edge case - không có rule rõ ràng | Community Lead → Hub Owner |
| Bản quyền nhạc/hình | Brand Manager game + LCCA |
| Vi phạm pháp luật (chính trị, bản đồ) | LCCA + Dept Head NGAY |

---

## 6. Chế tài khi vi phạm

| Cấp độ | Hành vi | Hình thức xử lý | Người quyết |
|---|---|---|---|
| Cấp 1 | Bỏ qua check scanner, bài có lỗi WARNING nhỏ | Gỡ/sửa bài trong 1h, ghi log | Community Lead |
| Cấp 2 | Đăng bài BLOCKED nhưng không phải bản đồ (vd: chửi tục, watermark sai) | Gỡ ngay, đào tạo lại, cảnh cáo | Community Lead + Manager |
| Cấp 3 | **Đăng bài có bản đồ** hoặc nội dung vi phạm pháp luật (chính trị, an ninh) | **Có thể bị thôi việc ngay** + team bị xử lý hành chính, incident report, báo cáo cơ quan chức năng nếu cần | Dept Head + BLĐ + LCCA |

> **Đặc biệt nghiêm trọng**: Bản đồ là RED LINE TUYỆT ĐỐI. Xem `GSX-CASE-002` để hiểu hậu quả thực tế từng xảy ra trong Game Studio X.

---

## 7. Tham chiếu

### Pháp lý gốc
- `GSX-LEGAL-002`: Bộ luật Hình sự - Điều 225, 226 (xâm phạm quyền tác giả/SHCN)
- `GSX-LEGAL-004`: Luật An ninh mạng (nội dung chống Nhà nước, bản đồ)
- `GSX-LEGAL-006`: VNG Social Media Guidelines
- `GSX-LEGAL-008`: Facebook Community Standards
- `GSX-LEGAL-010`: Luật Quảng cáo + NĐ87/2026 + TT12/2026 - Từ ngữ tuyệt đối (HL 05/07/2026)

### Case study liên quan
- `GSX-CASE-002`: Nhân viên duyệt bài có bản đồ vi phạm → bị thôi việc, team xử lý hành chính

### Tool/Checklist liên quan
- `GSX-TOOL-005`: Content Scanner Guide (hướng dẫn dùng tool)
- `GSX-TOOL-001`: Pre-Launch Checklist (universal)

### Tài liệu nội bộ VNG
- VNG Communication Policy (CS-CBC-001/01)
- VNG Social Media Guidelines

---

## 8. Changelog

| Version | Date | Changed by | Notes |
|---|---|---|---|
| 1.0 | 2026-06-03 | Hub Owner | Initial - ghép từ gsx-scanner-guide.html + Case Study bản đồ |
