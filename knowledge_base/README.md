# GameLaw AI — Knowledge Base

> **Bộ tài liệu compliance tổng hợp cho team Community - VNGGames Game Studio X.**
> Single source of truth cho mọi quy định pháp lý, chính sách nội bộ, và case study liên quan đến công việc community.

---

## 📖 Cách dùng Hub này

Hub được tổ chức theo **3 layer + 4 module hỗ trợ**:

| Folder | Vai trò | Đối tượng đọc | Tần suất update |
|---|---|---|---|
| `01_LEGAL_SOURCE/` | Nguồn pháp lý gốc (luật, nghị định, chính sách VNG) | Reference | Khi có thay đổi từ Nhà nước/VNG |
| `02_GSX_OPERATING_RULES/` | Quy tắc Game Studio X đã diễn giải từ luật | Daily | Khi có case study mới |
| `03_DAILY_TOOLS/` | Playbook, checklist, script - dùng hàng ngày | Daily | Thường xuyên |
| `04_CASE_STUDIES/` | Bài học từ sự cố thực tế | Reference | Append-only khi có sự cố |
| `05_TRAINING/` | Onboarding + refresh hàng năm | CTV mới | 1 lần/năm |
| `99_TEMPLATES/` | Boilerplate cho tài liệu mới | Internal | Khi thêm rule/case mới |
| `00_INDEX_VERSION/` | Index, changelog, ownership | Internal | Mỗi lần update |

> 💡 **Gặp viết tắt lạ?** Tra `00_INDEX_VERSION/GLOSSARY.md` - bảng từ điển thuật ngữ và viết tắt dùng trong Hub.

---

## 🎯 3 entry point chính theo audience

### Cho CTV mới (Day 1)
1. Đọc `05_TRAINING/Onboarding_Day1.md`
2. Đọc `03_DAILY_TOOLS/Quick_Reference_1pager.pdf`
3. Làm quiz `05_TRAINING/Quiz_Compliance_Basic.md`

### Cho team Community hàng ngày
1. Bookmark `03_DAILY_TOOLS/` - mở mỗi khi cần tra cứu
2. Khi go-live hoạt động mới: chạy qua `03_DAILY_TOOLS/Pre_Launch_Checklist.md`
3. Khi có sự cố: mở `03_DAILY_TOOLS/Escalation_Decision_Tree.md`

### Cho cross-team (LCCA, Marketing, Leadership)
1. Đọc `02_GSX_OPERATING_RULES/` - rule layer chính thức, đầy đủ
2. Reference link xuống `01_LEGAL_SOURCE/` để verify nguồn pháp lý
3. Reference link sang `04_CASE_STUDIES/` để hiểu context thực tế

---

## 🔗 Compliance Trigger Map

Tôi đang làm hoạt động X → cần check rule nào?

| Hoạt động | Rules áp dụng | Tool kiểm tra | Approval cần |
|---|---|---|---|
| Đăng bài Fanpage/Website | Content Moderation (9 nhóm) | Game Studio X Scanner | Self-check, Lead duyệt nếu chứa KOL |
| Đăng bài Group/Discord | Content Moderation (casual tier) | Game Studio X Scanner | Self-check |
| Tổ chức UGC contest | NĐ13 + Content Moderation + IP | Pre-Launch Checklist | Marketing Lead |
| Thu data user (form đăng ký, event) | NĐ13 - Data Collection Policy | Form Compliance Checklist | LCCA nếu có data nhạy cảm |
| Mời/làm việc KOL | Partner SOP (KOL section) + IP Rights | KOL approval form | Dept Head |
| Duyệt giải đấu bên thứ 3 | Tournament Rules + Riot Guidelines + ND13 | Tournament Compliance Checklist | Community Lead → Manager → Riot SEA (tùy tier) |
| Phát ngôn với báo chí | VNG Communication Policy + Partner SOP | Script Library | PR Manager / CBC |
| Xử lý khủng hoảng truyền thông | Escalation Decision Tree | Incident Report Template | Theo cấp escalation |

---

## ⚙️ Cập nhật & Maintenance

- **Owner chính**: Hub Owner - Game Studio X Community Team
- **Legal owner**: LCCA (xem `00_INDEX_VERSION/CONTACTS_DIRECTORY.md` để biết người phụ trách hiện tại)
- **Review cycle**: 6 tháng/lần hoặc ngay sau khi có sự cố nghiêm trọng
- **Changelog**: xem `00_INDEX_VERSION/CHANGELOG.md`

---

## 📋 Status hiện tại

- **Version**: v2.0 - RELEASE (all layers + HTML Hub complete)
- **Last updated**: 2026-06-08
- **Total files**: 60 markdown + 1 HTML Hub
- **Hub progress**:
  - Layer 1 (Legal Source): 9/9 ✅
  - Layer 2 (Operating Rules): 12/12 ✅
  - Layer 3 (Daily Tools): 11 markdown + 1 HTML Hub ✅
  - Layer 4 (Case Studies): 7/7 ✅
  - Layer 5 (Training): 4/4 ✅
- **Deployment ready**: Open `03_DAILY_TOOLS/012_GSX_Compliance_Hub.html` trong browser bất kỳ
