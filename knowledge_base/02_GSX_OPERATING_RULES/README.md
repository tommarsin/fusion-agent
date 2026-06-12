# 02 - Game Studio X Operating Rules

## Mục đích folder

Quy tắc đã được team Game Studio X **diễn giải** từ luật + chính sách + bài học case study, thành hướng dẫn cụ thể áp dụng được cho công việc hàng ngày.

Đây là **tầng quan trọng nhất** - team Community đọc folder này nhiều nhất.

---

## Nguyên tắc thiết kế rule

1. **Mỗi rule có doc_id duy nhất** (GSX-OP-XXX)
2. **Mỗi rule phải link ngược về Layer 1** - nguồn pháp lý gốc
3. **Mỗi rule phải có ví dụ thực tế** - không viết chung chung
4. **Mỗi rule phải có Red Lines** - điều cấm tuyệt đối, không exception
5. **Mỗi rule phải có chế tài cụ thể** khi vi phạm

Template chuẩn: `99_TEMPLATES/TEMPLATE_Operating_Rule.md`

---

## 12 Rule modules dự kiến

### Nhóm A: Data & Privacy
- `001_Data_Collection_Policy.md` - GSX-OP-001
  - NĐ13: Form vs Promotion Tool decision
  - Consent checkbox templates
  - Data retention policy

### Nhóm B: Content
- `002_Content_Moderation_Rules.md` - GSX-OP-002
  - 9 nhóm tiêu chí (4A-4I)
  - SAFE/WARNING/BLOCKED verdict
  - Platform-specific (Website, Fanpage, Group, Discord)

### Nhóm C: Partners
- `003_Partner_SOP_KOL.md` - GSX-OP-003
  - 7 nguyên tắc cốt lõi
  - Pre-Outreach / During / Post-Campaign
- `004_Partner_SOP_Media.md` - GSX-OP-004
  - Quy trình phỏng vấn báo chí (theo VNG Communication Policy)
- `005_Partner_SOP_Brand.md` - GSX-OP-005
  - NDA, sponsorship, key visual approval

### Nhóm D: Community
- `006_Community_Engagement_Rules.md` - GSX-OP-006
  - Facebook Group, Discord, Fanpage moderation
  - User interaction guidelines
- `007_UGC_Event_Rules.md` - GSX-OP-007
  - Red Lines từ Case Study #1 (UGC NĐ13)
  - Review chéo bắt buộc
  - Monitoring SOP

### Nhóm E: IP & Brand
- `008_IP_Rights_Rules.md` - GSX-OP-008
  - Music licensing
  - KOL imagery rights
  - Brand logo usage
  - Third-party watermark

### Nhóm F: Tournament
- `009_Third_Party_Tournament_Rules.md` - GSX-OP-009
  - 4 tier (Community/Esports Team/Branded/Collegiate)
  - 7-step approval workflow
  - Banned activities (cá độ, thu phí, hoạt động ngoài giờ)
  - Logo usage rules

### Nhóm G: Crisis & Security
- `010_Crisis_Communication_Playbook.md` - GSX-OP-010
  - 7-step escalation
  - Script library
  - Cooling rule + data response (bài học từ Case Năm N+2)
- `011_Information_Classification.md` - GSX-OP-011
  - 4 cấp: Confidential / Internal / Restricted / Public
  - Cấm tuyệt đối
- `012_Financial_Integrity.md` - GSX-OP-012
  - Quy trình duyệt hoá đơn/vendor (bài học từ Case Năm N)
  - Cross-check ≥ 2 người
  - Disclosure obligation

---

## Khi nào update folder này?

- Có case study mới → review rule liên quan
- Layer 1 (Legal) update → cập nhật rule áp dụng
- Có hoạt động mới phát sinh chưa có rule → tạo rule mới
- Team feedback rule không rõ ràng/khó áp dụng → revise

Mọi update cần qua **Domain Owner** tương ứng (xem `00_INDEX_VERSION/OWNERSHIP_MAP.md`).
