---
doc_id: GSX-TOOL-009
title: "Consent Checkbox Templates - Mẫu consent cho form"
tool_type: template-form
audience: community-team
use_when: Khi setup form thu data user (Google Form, Promotion Tool, landing page)
estimated_time: 5 phút copy + adapt
version: 1.0
last_updated: 2026-06-03
maintained_by: Community Lead + LCCA
related_operating_rules:
  - GSX-OP-001
related_legal_sources:
  - GSX-LEGAL-001
---

# Consent Checkbox Templates

## 🎯 Khi nào dùng tool này?

Khi setup form thu data user - cần có consent checkbox + statement of purpose + retention timeline theo NĐ13/2023.

## ⚡ Cách dùng nhanh

1. Identify loại form đang setup
2. Copy template phù hợp
3. **Adapt placeholders [tên hoạt động], [retention], v.v.**
4. **KHÔNG xóa các yếu tố cốt lõi**
5. Submit Lead review trước khi go-live

---

## 📋 3 ELEMENT BẮT BUỘC TRONG MỌI FORM

Mọi template dưới đây đều có 3 element bắt buộc theo NĐ13:

1. **Statement of Purpose** (mục đích cụ thể)
2. **Retention timeline** (lưu bao lâu)
3. **Consent checkbox** (không default-checked, đặt ở đầu form)

---

## 📝 TEMPLATE 1: Form đăng ký event/contest đơn giản

**Phù hợp với**: Đăng ký event nhỏ, mini-game, vote, không có quà giá trị cao.

```markdown
═══════════════════════════════════════════
ĐĂNG KÝ THAM GIA [TÊN HOẠT ĐỘNG]
═══════════════════════════════════════════

THÔNG TIN THU THẬP & SỬ DỤNG DỮ LIỆU

Khi điền form này, bạn cung cấp các thông tin sau cho VNGGames:
- IGN (In-game name)
- Server / Rank (nếu có)
- Discord username (nếu cần)

Thông tin của bạn sẽ được dùng để:
(1) Xác nhận bạn đủ điều kiện tham gia [TÊN HOẠT ĐỘNG]
(2) Liên hệ thông báo kết quả qua kênh in-game/Discord
(3) Thống kê tổng kết hoạt động (dạng anonymized)

Thông tin sẽ được lưu trữ trong [30 NGÀY] kể từ khi kết thúc [TÊN HOẠT ĐỘNG], 
sau đó sẽ được xóa hoàn toàn.

Bạn có quyền yêu cầu truy cập / sửa / xóa thông tin của mình bất cứ lúc nào 
qua email: [support@vnggames.vn]

─────────────────────────────────────────
☐ Tôi đã đọc và đồng ý với các thông tin trên * [bắt buộc]
─────────────────────────────────────────

[Các trường form khác...]
```

---

## 📝 TEMPLATE 2: Form đăng ký nhận quà có giá trị

**Phù hợp với**: Hoạt động có quà giá trị < 500k, cần thông tin nhận quà nhưng không cần CCCD.

```markdown
═══════════════════════════════════════════
ĐĂNG KÝ NHẬN QUÀ - [TÊN HOẠT ĐỘNG]
═══════════════════════════════════════════

THÔNG TIN THU THẬP & SỬ DỤNG DỮ LIỆU

Để trao quà, VNGGames cần các thông tin sau từ bạn:
- IGN (In-game name)
- Email liên hệ
- [Trường khác: Server / Discord / địa chỉ nhận quà nếu có]

Thông tin của bạn sẽ được sử dụng cho mục đích:
(1) Xác nhận bạn là người chiến thắng hợp lệ của [TÊN HOẠT ĐỘNG]
(2) Liên hệ qua email để gửi quà (mã code/voucher in-game/quà vật lý)
(3) Lưu hồ sơ trao thưởng theo quy định nội bộ

Thông tin sẽ được lưu trữ:
- Trong thời gian xử lý trao quà: tối đa [30 NGÀY] kể từ thông báo trúng giải
- Sau đó: dữ liệu sẽ được xóa, chỉ lưu mã code trao thưởng (không có PII)

Bạn có quyền yêu cầu truy cập / sửa / xóa thông tin của mình bất cứ lúc nào 
qua email: [support@vnggames.vn]

VNGGames cam kết:
- Không chia sẻ thông tin của bạn cho bên thứ 3 nào khác
- Không dùng thông tin cho mục đích khác ngoài đã nêu
- Tuân thủ Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân

─────────────────────────────────────────
☐ Tôi đã đọc và đồng ý với các thông tin trên * [bắt buộc]
─────────────────────────────────────────
☐ (Tùy chọn) Tôi đồng ý nhận thông tin về các hoạt động khác từ VNGGames 
   qua email này
─────────────────────────────────────────

[Các trường form khác...]
```

---

## 📝 TEMPLATE 3: Form đăng ký giải đấu (BTC bên thứ 3)

**Phù hợp với**: Form BTC dùng cho giải đấu cộng đồng. VNG review trước approve.

```markdown
═══════════════════════════════════════════
ĐĂNG KÝ THAM GIA GIẢI ĐẤU [TÊN GIẢI]
═══════════════════════════════════════════

ĐƠN VỊ TỔ CHỨC

Giải đấu [TÊN GIẢI] được tổ chức bởi [TÊN BTC]. 
[TÊN BTC] là đơn vị tổ chức và chịu trách nhiệm pháp lý đối với việc thu thập, 
sử dụng dữ liệu của người tham gia.

VNGGames hỗ trợ truyền thông cho giải đấu, không phải đơn vị tổ chức và không 
thu thập trực tiếp dữ liệu qua form này.

THÔNG TIN THU THẬP & SỬ DỤNG DỮ LIỆU

Khi điền form này, bạn cung cấp các thông tin sau cho [TÊN BTC]:
- IGN của Captain + các thành viên đội
- Tên đội tham gia
- Server / Rank (verify đủ điều kiện)
- Discord/Liên hệ Captain

Thông tin của bạn được [TÊN BTC] sử dụng để:
(1) Xác nhận đội đăng ký hợp lệ
(2) Liên hệ thông báo lịch thi đấu
(3) Tổ chức và điều hành giải đấu

Thời gian lưu trữ thông tin: tối đa [60 NGÀY] kể từ khi giải đấu kết thúc.

[TÊN BTC] cam kết:
- Tuân thủ Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân
- Không chia sẻ thông tin của bạn cho bên thứ 3 không liên quan đến giải đấu
- Bảo mật thông tin trong quá trình tổ chức

Bạn có quyền yêu cầu [TÊN BTC] truy cập / sửa / xóa thông tin của mình 
qua email: [email BTC]

─────────────────────────────────────────
☐ Tôi đã đọc và đồng ý với các thông tin trên * [bắt buộc]

☐ Tôi xác nhận đủ 18 tuổi (HOẶC có sự đồng ý của phụ huynh nếu dưới 18 tuổi) * 
  [bắt buộc]
─────────────────────────────────────────

[Các trường form khác...]
```

---

## 📝 TEMPLATE 4: Form survey/feedback (anonymized)

**Phù hợp với**: Khảo sát opinion, không thu PII.

```markdown
═══════════════════════════════════════════
KHẢO SÁT - [TÊN CHỦ ĐỀ]
═══════════════════════════════════════════

VỀ KHẢO SÁT NÀY

Cảm ơn bạn dành thời gian tham gia khảo sát. Phản hồi của bạn giúp VNGGames 
cải thiện trải nghiệm cộng đồng tốt hơn.

Khảo sát này KHÔNG yêu cầu thông tin định danh cá nhân (họ tên thật, SĐT, 
email, CCCD). Bạn có thể trả lời ẩn danh.

Các thông tin tùy chọn (nếu bạn muốn cung cấp) sẽ giúp chúng tôi phân tích 
chi tiết hơn:
- IGN (để contact bạn nếu cần làm rõ phản hồi)
- Discord (để mời tham gia interview deep-dive)
- Khoảng độ tuổi
- Khoảng thời gian chơi game

Phản hồi của bạn sẽ được:
(1) Tổng hợp ở dạng anonymized
(2) Dùng để improve sản phẩm và community programs
(3) Chia sẻ với team nội bộ VNGGames (KHÔNG chia sẻ ra ngoài)

Dữ liệu sẽ được lưu trong [90 NGÀY] để phân tích sâu, sau đó chỉ giữ lại 
phân tích aggregated, không có thông tin cá nhân.

─────────────────────────────────────────
☐ Tôi hiểu khảo sát này không bắt buộc và tôi tự nguyện tham gia
─────────────────────────────────────────

[Câu hỏi khảo sát...]
```

---

## 📝 TEMPLATE 5: Form thu data nhạy cảm (Promotion Tool)

**Phù hợp với**: Trao thưởng > 500k cần CCCD verify. CHỈ DÙNG TRONG PROMOTION TOOL.

> ⚠️ **KHÔNG dùng template này trong Google Form**. Promotion Tool có UI riêng - dưới đây là text clause để embed.

```markdown
═══════════════════════════════════════════
XÁC MINH NGƯỜI NHẬN GIẢI - [TÊN HOẠT ĐỘNG]
═══════════════════════════════════════════

THÔNG BÁO QUAN TRỌNG VỀ DỮ LIỆU CÁ NHÂN

Để xác minh và trao giải có giá trị cao theo quy định pháp luật Việt Nam, 
VNGGames cần thu thập một số thông tin định danh của bạn:
- Họ tên đầy đủ (theo CCCD/CMND)
- Số CCCD/CMND
- Ảnh CCCD/CMND (mặt trước, có thể che 6 số cuối nếu muốn)
- SĐT liên lạc
- Địa chỉ nhận quà (nếu quà vật lý)

Đây là dữ liệu cá nhân NHẠY CẢM. VNGGames bảo vệ thông tin của bạn theo 
Nghị định 13/2023/NĐ-CP với các biện pháp sau:

1. **Lưu trữ tại Việt Nam**: Dữ liệu được lưu trong hệ thống nội bộ tại VN, 
   không chuyển ra nước ngoài.
   
2. **Truy cập giới hạn**: Chỉ nhân sự được ủy quyền của VNGGames mới có thể 
   truy cập, mọi truy cập đều được log.
   
3. **Xóa sau xử lý**: Dữ liệu sẽ được xóa hoàn toàn sau [30 NGÀY] kể từ khi 
   bạn nhận quà thành công.
   
4. **Không chia sẻ**: VNGGames không chia sẻ dữ liệu này với bất kỳ bên thứ 3 
   nào khác ngoài đơn vị vận chuyển (chỉ thông tin cần thiết để giao hàng).

Bạn có quyền:
- Truy cập / sửa / xóa thông tin của mình bất cứ lúc nào
- Rút lại đồng ý (sẽ ảnh hưởng đến việc trao thưởng)
- Khiếu nại nếu VNGGames không tuân thủ cam kết

Liên hệ thực thi quyền: [legal@vnggames.vn] hoặc [hotline]

─────────────────────────────────────────
☐ Tôi đã đọc và đồng ý cho VNGGames thu thập, sử dụng các thông tin nêu trên 
   theo Nghị định 13/2023/NĐ-CP * [bắt buộc]

☐ Tôi xác nhận thông tin tôi cung cấp là chính xác và là của chính tôi 
   (không dùng thông tin người khác) * [bắt buộc]

☐ Tôi xác nhận đủ 18 tuổi để tự thực thi quyền và nghĩa vụ liên quan 
   * [bắt buộc nếu không có giám hộ]
─────────────────────────────────────────
```

---

## ⚠️ NHỮNG ĐIỀU CẤM TRONG CONSENT CLAUSE

```
❌ Default-checked checkbox - vi phạm Điều 11 NĐ13
❌ Consent gộp "tôi đồng ý mọi điều khoản và chính sách"
   → Phải tách thành từng item rõ ràng
❌ Buộc consent marketing trong form thu data chức năng
   → Phải optional + checkbox riêng
❌ Ngôn ngữ mơ hồ: "phục vụ cộng đồng", "phục vụ user", "phục vụ marketing"
   → Phải cụ thể activity và mục đích
❌ Hết hạn vô tận "lưu trữ vĩnh viễn" hoặc không nói về retention
   → BẮT BUỘC có timeline cụ thể
❌ Ẩn cảnh báo ở cuối form sau khi đã điền hết
   → Phải đặt ở đầu form, trước khi user nhập thông tin
```

---

## 🔗 Tham chiếu

- **Rule gốc**: GSX-OP-001 (Data Collection Policy)
- **Legal source**: GSX-LEGAL-001 (NĐ13/2023)
- **Checklist verify form**: GSX-TOOL-003 (Form Compliance Checklist)
- **Case study minh hoạ**: GSX-CASE-001 (UGC ND13 - thiếu cảnh báo dẫn đến vi phạm)

---

## Changelog

| Version | Date | Changed by | Notes |
|---|---|---|---|
| 1.0 | 2026-06-03 | Hub Owner | Initial - 5 template từ thực tiễn Community |
