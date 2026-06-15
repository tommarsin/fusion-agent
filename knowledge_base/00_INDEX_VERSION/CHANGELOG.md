# Changelog - GameLaw AI

Mọi thay đổi đáng kể trong Hub đều log ở đây.

Format: `[Date] - [Doc ID] - [Type] - [Description]`
Type: ADDED | UPDATED | DEPRECATED | REMOVED

---

## [2026-06-03] - Hub Initialization

- ADDED: Khởi tạo folder structure v1.0
- ADDED: Tạo 4 template chuẩn trong `99_TEMPLATES/`:
  - TEMPLATE_Operating_Rule.md
  - TEMPLATE_Legal_Source.md
  - TEMPLATE_Case_Study.md
  - TEMPLATE_Daily_Tool.md
- ADDED: README hướng dẫn cho từng folder

## [2026-06-03] - Wave 1 Content Complete - Operating Rules Critical

Hoàn thành Wave 1 - 4 rule critical đầu tiên:

- ADDED: `GSX-OP-001` Data Collection Policy (NĐ13 - Form vs Promotion Tool)
- ADDED: `GSX-OP-002` Content Moderation Rules (9 nhóm tiêu chí + checklist 7 bước)
- ADDED: `GSX-OP-007` UGC Event Rules (red lines + review chéo bắt buộc)
- ADDED: `GSX-OP-009` Third-Party Tournament Rules (4 tier + 7-step workflow + chế tài 3 cấp)

Source materials đã consolidate:
- gsx-scanner-guide.html → OP-002
- Case_Study_UGC_Contest_ND13_Violation.md → OP-007 + GSX-CASE-001
- Playbook_Tournament_Third party_v2_3_with_form_ND13.html → OP-009
- Memory data về NĐ13 → OP-001

Next steps:
- Hub Owner review Wave 1 trước khi triển khai Wave 2
- Wave 2 sẽ cover: OP-003 (KOL SOP), OP-008 (IP Rights), OP-010 (Crisis Comm), OP-011 (Info Classification)

## [2026-06-03] - Wave 2 Content Complete - Operating Rules High Priority

Hoàn thành Wave 2 - 4 rule high priority:

- ADDED: `GSX-OP-003` Partner SOP - KOL/Influencer (7 nguyên tắc + 3 giai đoạn + conflict of interest)
- ADDED: `GSX-OP-008` IP Rights Rules (music, KOL imagery, logo, watermark, fan art)
- ADDED: `GSX-OP-010` Crisis Communication Playbook (7-step + script chuẩn + 3 nhóm đối tượng)
- ADDED: `GSX-OP-011` Information Classification (4 cấp + NDA workflow + IPO compliance)

Source materials đã consolidate:
- Game Studio X SOP Ung Xu Doi Tac → OP-003, OP-010, OP-011
- VNG Communication Policy → OP-010, OP-011
- Email nhà sáng lập "Quyết định thôi việc Năm N" → OP-003 chế tài (Case-003)
- Email nhà sáng lập "Crisis thâu tóm Năm N+2" → OP-010 (Case-004)
- Email nhà sáng lập "IPO Nasdaq 2023" → OP-011 (Confidentiality marking standard)
- Scanner Guide nhóm 4G → OP-008
- Tournament Playbook logo rules → OP-008

Next steps:
- Hub Owner review Wave 2 trước khi triển khai Wave 3
- Wave 3 sẽ cover: OP-004 (Media SOP), OP-005 (Brand SOP), OP-006 (Community Engagement), OP-012 (Financial Integrity)

## [2026-06-03] - Wave 3 Content Complete - All 12 Operating Rules Done

Hoàn thành Wave 3 - 4 rule còn lại + đóng cấu trúc Layer 2:

- ADDED: `GSX-OP-004` Partner SOP - Media/Báo chí (quy trình chuyển CBC + script chuẩn)
- ADDED: `GSX-OP-005` Partner SOP - Brand/Sponsor (5-step verify + restricted categories + MOU clauses)
- ADDED: `GSX-OP-006` Community Engagement Rules (tone theo platform + mod action + drama handling)
- ADDED: `GSX-OP-012` Financial Integrity (test minh bạch nhà sáng lập + cross-check ≥2 + whistleblowing)

**Layer 2 Status: 12/12 Operating Rules COMPLETE (all draft, pending review)**

Source materials đã consolidate:
- VNG Communication Policy → OP-004
- Email nhà sáng lập "Một tờ báo lớn Năm N" → OP-004 (Case-007)
- Riot SEA Guidelines restricted categories → OP-005
- Game Studio X Scanner Guide platform differentiation → OP-006
- Email nhà sáng lập "Hóa đơn khống Năm N" → OP-012 (Case-003) - precedent gốc

Next steps:
- Hub Owner review toàn bộ 12 rules
- Bắt đầu Wave 4: viết 7 Case Studies với template chuẩn
- Sau đó Layer 1 (Legal Source) + Layer 3 (Daily Tools)
- Cuối cùng: build HTML render từ markdown source

## [2026-06-03] - Layer 1 Complete - All 9 Legal Sources Done

Hoàn thành toàn bộ Layer 1 - Legal Source:

- ADDED: `GSX-LEGAL-001` Nghị định 13/2023/NĐ-CP - Bảo vệ dữ liệu cá nhân (Điều 3, 25, 28, 38, 43)
- ADDED: `GSX-LEGAL-002` Bộ luật Hình sự - Điều 225, 226 (IP rights)
- ADDED: `GSX-LEGAL-003` Bộ luật Hình sự - Điều 174, 175 (Lừa đảo, lạm dụng tín nhiệm)
- ADDED: `GSX-LEGAL-004` Luật An ninh mạng (Điều 8, 16, 26)
- ADDED: `GSX-LEGAL-005` VNG Communication Policy (CS-CBC-001/01)
- ADDED: `GSX-LEGAL-006` VNG Social Media Guidelines
- ADDED: `GSX-LEGAL-007` Riot SEA 3rd Party Organized Play Guidelines v1.3
- ADDED: `GSX-LEGAL-008` Facebook Community Standards
- ADDED: `GSX-LEGAL-009` Nghị định 147/2024/NĐ-CP - Quản lý Internet & game online

**Layer 1 Status: 9/9 Legal Sources COMPLETE (all draft, pending LCCA review)**

Cross-reference đã hoàn thành 2 chiều:
- 12 Operating Rules link xuống 9 Legal Sources
- 9 Legal Sources link ngược lên Operating Rules tương ứng
- Compliance Hub đã có 2/5 layers complete

Next steps:
- Hub Owner review Layer 1 (especially LCCA verify legal accuracy)
- Build Layer 3 (Daily Tools - 12 file) hoặc Layer 4 (Case Studies - 7 file)
- Cuối: HTML render

## [2026-06-03] - Layer 3 Complete - All 12 Daily Tools Done

Hoàn thành Layer 3 - Daily Tools:

**Checklists (4 files)**:
- ADDED: `GSX-TOOL-001` Pre-Launch Checklist (universal) - 7 nhóm check
- ADDED: `GSX-TOOL-002` UGC Event Compliance Checklist - 4 stage + Red Line check
- ADDED: `GSX-TOOL-003` Form Compliance Checklist (NĐ13) - decision tree tool + 3 elements
- ADDED: `GSX-TOOL-004` Tournament Compliance Checklist - 33 hạng mục đầy đủ

**Reference Cards (3 files)**:
- ADDED: `GSX-TOOL-005` Content Scanner Guide - 9 nhóm tiêu chí + checklist 7 bước
- ADDED: `GSX-TOOL-011` Quick Reference 1-pager - cheatsheet treo bàn
- ADDED: `GSX-TOOL-012` Interactive Playbook HTML (placeholder - sẽ build sau khi xong markdown)

**Decision Tree (1 file)**:
- ADDED: `GSX-TOOL-006` Escalation Decision Tree - 8 câu hỏi quyết định escalate cấp nào

**Scripts & Templates (4 files)**:
- ADDED: `GSX-TOOL-007` Scripts Library - 20+ script chuẩn cho user/KOL/báo chí/BTC
- ADDED: `GSX-TOOL-008` Incident Report Template - 11 section đầy đủ
- ADDED: `GSX-TOOL-009` Consent Checkbox Templates - 5 template cho 5 loại form
- ADDED: `GSX-TOOL-010` NDA Request Template - form gửi LCCA

**Layer 3 Status: 11/12 Daily Tools COMPLETE + 1 placeholder cho HTML build**

Hub progress:
- Layer 1: 9/9 ✅
- Layer 2: 12/12 ✅
- Layer 3: 11/12 ✅ (TOOL-012 sẽ build sau)
- Layer 4: 0/7 ⏳
- Layer 5: 0/4 ⏳

Next steps:
- Hub Owner review Layer 3 - các tools này CTV/team sẽ dùng hàng ngày
- Build Layer 4 (Case Studies) - 7 case đã reference
- Build Layer 5 (Training) - onboarding + quiz
- Cuối: HTML render từ markdown

## [2026-06-03] - Layer 4 Complete - All 7 Case Studies Done

Hoàn thành Layer 4 - Case Studies:

- ADDED: `GSX-CASE-001` UGC Contest ND13 Violation (2025) - case gốc của Game Studio X, dẫn đến rule OP-007
- ADDED: `GSX-CASE-002` Bản đồ vi phạm content moderation - case nhân viên thôi việc, dẫn đến rule OP-002 + Content Scanner tool
- ADDED: `GSX-CASE-003` Hóa đơn khống + trục lợi (Năm N) - precedent quan trọng nhất cho financial integrity, dẫn đến rule OP-012
- ADDED: `GSX-CASE-004` Khủng hoảng truyền thông "bị thâu tóm" (Năm N+2) - case về crisis communication response
- ADDED: `GSX-CASE-005` Sexual harassment FV (Năm N+9) - "đóng góp ≠ miễn trừ vi phạm" principle
- ADDED: `GSX-CASE-006` cơ quan quản lý địa phương (Năm N) - Information Gate principle gốc
- ADDED: `GSX-CASE-007` Một tờ báo lớn tấn công ngành game (Năm N) - narrative leadership pattern

**Layer 4 Status: 7/7 Case Studies COMPLETE (all draft)**

Hub progress:
- Layer 1 (Legal Source): 9/9 ✅
- Layer 2 (Operating Rules): 12/12 ✅
- Layer 3 (Daily Tools): 11/12 + 1 placeholder ✅
- Layer 4 (Case Studies): 7/7 ✅
- Layer 5 (Training): 0/4 ⏳

Cross-reference đầy đủ giờ đã hoạt động:
- 7 case study link xuôi sang rules + tools
- 12 rule link ngược sang case study minh hoạ
- 9 legal source link xuôi sang rules áp dụng
- 11 tool link ngược sang rule gốc

Next steps:
- Layer 5 (Training): 4 file onboarding/quiz/refresh
- HTML build từ markdown source

## [2026-06-03] - Layer 5 Complete - All 4 Training Files Done

Hoàn thành Layer 5 - Training:

- ADDED: `GSX-TRAIN-001` Onboarding Day 1 - 7-block training 90 phút cho CTV mới
- ADDED: `GSX-TRAIN-002` Compliance Basic Quiz - 20 câu test 5 lĩnh vực, pass threshold 80%
- ADDED: `GSX-TRAIN-003` Annual Refresh Checklist - 7-part refresh 30-60 phút/năm
- ADDED: `GSX-TRAIN-004` Case Study Reading List - mapping 7 case theo role + situation

**Layer 5 Status: 4/4 Training Files COMPLETE**

🎉 **ALL MARKDOWN SOURCE COMPLETE** - Hub đã đầy đủ content:
- Layer 1: 9/9 ✅
- Layer 2: 12/12 ✅
- Layer 3: 11/12 + 1 placeholder ✅
- Layer 4: 7/7 ✅
- Layer 5: 4/4 ✅

Total: **43 content files** + 14 supporting files (README, templates, index)

Next steps:
- Hub Owner review tổng thể v1.7
- Build HTML Hub render từ markdown source (TOOL-012)
- Deploy nội bộ cho team Community Game Studio X

## [2026-06-08] - v2.0 RELEASE - HTML Hub Build Complete

🎉 **FINAL MILESTONE**: GameLaw AI v2.0 ready for deployment

- ADDED: `012_GSX_Compliance_Hub.html` (392 KB) - Interactive HTML Hub
- REMOVED: `012_Interactive_Playbook_Placeholder.md` (superseded by HTML)
- UPDATED: `TOOL-012` status from placeholder → active

**HTML Hub features**:
- Single-file standalone, 393 KB, mở offline trên mọi browser
- 45 documents embedded (60 markdown files, lọc README + templates)
- Sidebar navigation theo Layer
- Full-text search 200ms debounce
- Click cross-reference (GSX-OP-XXX, GSX-CASE-XXX...) navigate trực tiếp
- Tailwind CSS via CDN
- Markdown parsed bằng marked.js
- Print-friendly cho Quick Reference
- Layer badges với màu phân biệt
- Responsive mobile/desktop

**Hub final status**:
- Layer 1 (Legal Source): 9/9 ✅
- Layer 2 (Operating Rules): 12/12 ✅
- Layer 3 (Daily Tools): 11 markdown + 1 HTML Hub ✅
- Layer 4 (Case Studies): 7/7 ✅
- Layer 5 (Training): 4/4 ✅

**Deployment options**:
1. Open file trực tiếp: file:///path/to/012_GSX_Compliance_Hub.html
2. Upload Drive nội bộ - share link team
3. Host trên GitHub Pages (nếu cần URL public)
4. Tích hợp vào myVNG portal nội bộ

Total project deliverable: **60 markdown files + 1 HTML Hub + ~11,000 dòng compliance content**

## [2026-06-09] - v2.6 PATCH - Tách danh bạ + Việt hóa chọn lọc

🛠️ **Patch theo feedback Hub Owner**: Tách tên người khỏi các quy định, đưa vào file phụ lục danh bạ riêng để dễ cập nhật khi có thay đổi nhân sự.

**Files added (1)**:
- ADDED: `00_INDEX_VERSION/CONTACTS_DIRECTORY.md` - Danh bạ liên hệ Hub (tách riêng)

**Files updated (5)**:
- UPDATED: `GSX-OP-013` v1.1 - Bỏ tên PR Manager/LCCA contact khỏi workflow chính, chỉ giữ ở APPENDIX. Workflow nội bộ Game Studio X chỉ tới Brand Manager. LCCA/CBC chỉ là tham khảo khi cần. Việt hóa chọn lọc một số thuật ngữ. Thêm section "Định nghĩa quan trọng" cho thuật ngữ chuyên môn.
- UPDATED: `GSX-LEGAL-010` v1.1 - Bỏ "route qua PR Manager (CBC)", thay bằng "trình Brand Manager phụ trách sản phẩm"
- UPDATED: `GSX-OP-005` - Bỏ "PR Manager (CBC) review", thay bằng "Brand Manager phụ trách sản phẩm duyệt"
- UPDATED: `GSX-OP-009` - Bỏ "PR Manager (CBC) review", thay bằng "Brand Manager phụ trách sản phẩm duyệt"
- UPDATED: `GSX-TOOL-001` - Tương tự

**Phase 3 sweep (16 file)**: Sweep toàn bộ workflow context - thay tên người bằng vai trò/đơn vị + reference CONTACTS_DIRECTORY:
- OP-001 Data Collection (escalation table)
- OP-002 Content Moderation (advertising route)
- OP-004 Partner SOP Media (PR Manager refs - 2 chỗ)
- OP-007 UGC Event (escalation table)
- OP-011 Information Classification (NDA escalation)
- TOOL-005 Content Scanner Guide (advertising approval)
- TOOL-006 Escalation Decision Tree (PR Manager ref)
- TOOL-007 Scripts Library (PR Manager transfer)
- TOOL-010 NDA Request Template (4 references)
- TOOL-011 Quick Reference 1-pager (3 references including SOS contacts)
- TRAIN-001 Onboarding Day 1 (Legal Owner)
- TRAIN-002 Compliance Basic Quiz (answer C wording)
- README root (Legal owner)
- 01_LEGAL_SOURCE/README (merge approval)
- OWNERSHIP_MAP (Legal Owner section + Domain Owners table)

**Giữ nguyên có chủ ý**:
- `LEGAL-005 VNG Communication Policy`: tên tác giả/người ký policy gốc (metadata của văn bản nguồn)
- `LEGAL-005`: trích quy trình từ policy VNG gốc (mô tả lại policy, không phải workflow Game Studio X)
- `CHANGELOG.md`: text mô tả lịch sử thay đổi
- `CONTACTS_DIRECTORY.md`: file designed để chứa tên người

**Nguyên tắc mới được codify**:
- Các quy định trong Hub chỉ tham chiếu đến **vai trò/đơn vị** (vd: "Brand Manager", "LCCA", "CBC")
- Tên người cụ thể được tách riêng vào `CONTACTS_DIRECTORY.md`
- Khi có thay đổi nhân sự → chỉ cần update file danh bạ, không cần sửa tất cả các quy định

**Lý do thay đổi workflow**:
Trước đây Claude (Hub designer) đã tự suy luận workflow phải route qua PR Manager/CBC và LCCA. Hub Owner catch ra rằng đây là speculation không có cơ sở chính thức. Workflow thực tế: Brand Manager phụ trách sản phẩm duyệt nội bộ Game Studio X là đủ. LCCA/CBC chỉ tham khảo khi có tình huống đặc biệt (tài liệu phức tạp, rủi ro PR cao).



🆕 **Quy định mới**: TT12/2026/TT-BVHTTDL có hiệu lực 05/07/2026 - cấm dùng từ ngữ tuyệt đối ("nhất", "duy nhất"...) trong quảng cáo nếu không có tài liệu chứng minh. Mức phạt 20-40 triệu/lần (tổ chức).

**Files added (2)**:
- ADDED: `GSX-LEGAL-010` Luật Quảng cáo + NĐ87/2026 + TT12/2026 - Từ ngữ tuyệt đối
- ADDED: `GSX-OP-013` Advertising Standards - rule áp dụng cho toàn bộ Community Game Studio X

**Files updated (5)**:
- UPDATED: `GSX-OP-002` Content Moderation - thêm nhóm 4J "Từ ngữ tuyệt đối"
- UPDATED: `GSX-OP-005` Partner SOP Brand - section 3.5.1 cross-brand material có từ tuyệt đối
- UPDATED: `GSX-OP-009` Tournament Rules - section 3.10 BTC dùng từ tuyệt đối
- UPDATED: `GSX-TOOL-001` Pre-Launch Checklist - thêm 1 mục check, update Red Lines 6→7
- UPDATED: `GSX-TOOL-005` Content Scanner Guide - thêm nhóm 4J, update Red Lines 6→7
- UPDATED: `GSX-TOOL-011` Quick Reference - 7 Red Lines + 13 Operating Rules

**Naming convention update (51 files)**:
- CHANGED: "Tom" → "Hub Owner" (employee code chuẩn VNG) trong toàn bộ Hub
- 99 occurrences across 51 files replaced

**Hub status now**:
- Layer 1: 10/10 ✅ (was 9)
- Layer 2: 13/13 ✅ (was 12)
- Layer 3: 11 + 1 HTML Hub ✅
- Layer 4: 7/7 ✅
- Layer 5: 4/4 ✅

**Scope notice**: Hub design áp dụng cho **toàn bộ Game Studio X Community**, không chỉ Wild Rift/LMHT. Wording trong rule mới đã được generic hóa.

**Action items cho team trước 05/07/2026**:
- [ ] Hub Owner rà template caption/banner đang dùng - xóa từ tuyệt đối không có chứng minh
- [ ] Hub Owner brief CTV về danh sách từ cấm
- [ ] Xác nhận workflow approval với LCCA contact + PR Manager (CBC)
- [ ] Audit landing page event đang active

## [2026-06-09] - v2.7 ADD - GLOSSARY + Định nghĩa thuật ngữ inline

🛠️ **Patch theo feedback Hub Owner**: Trước đây Hub dùng viết tắt (LCCA, CBC, PII, A05...) mà không có chỗ giải thích tập trung. CTV mới sẽ confused. Sửa bằng cách:

**Files added (1)**:
- ADDED: `00_INDEX_VERSION/GLOSSARY.md` - Bảng từ điển toàn Hub
  - 8 nhóm thuật ngữ: VNG/đơn vị, Cơ quan chức năng, Đối tác, Tài liệu, Pháp lý, Game/Esport, Nội dung/Truyền thông, Cấu trúc Hub
  - 5 khái niệm pháp lý quan trọng có mô tả chi tiết

**Files updated (7)**:
- UPDATED: `GSX-OP-001` Data Collection - thêm mục 1.4 "Viết tắt & Thuật ngữ trong tài liệu này"
- UPDATED: `GSX-OP-002` Content Moderation - tương tự (focus: scanner, whitelist, red line)
- UPDATED: `GSX-OP-007` UGC Event - tương tự (focus: UGC, worst-case design, 2nd-eye review)
- UPDATED: `GSX-OP-010` Crisis Communication - tương tự (focus: cooling rule, information gate, escalation chain)
- UPDATED: `GSX-CASE-001` UGC Contest ND13 - thêm mục 0 "Viết tắt & Thuật ngữ trong case study này"
- UPDATED: `GSX-CASE-003` Hóa đơn khống nhà sáng lập - tương tự (focus: test minh bạch, proportionality, whistleblowing)
- UPDATED: `README.md` root - thêm reference đến GLOSSARY

**Approach (Option 1.5)**:
- GLOSSARY tổng làm điểm tra cứu chung
- Inline definitions chỉ ở 7 file critical mà CTV onboarding phải đọc (theo TRAIN-001)
- Các file khác: reader tự tra GLOSSARY khi cần

**Lý do thay đổi**:
Trước đây Claude (Hub designer) đã viết tắt LCCA, CBC, A05... khắp Hub như thể ai cũng biết. CTV mới đọc lần đầu sẽ không hiểu. Hub Owner catch ra rằng "search trong tài liệu không thấy LCCA là gì" → đúng - chỉ có 1 chỗ giải thích duy nhất trong OP-013. Fix bằng cách tạo điểm tra cứu trung tâm + thêm inline cho file critical.

---

## [Template entry cho lần update sau]

## [YYYY-MM-DD] - [Doc ID nếu có] - [Tên thay đổi ngắn]

- TYPE: [Mô tả thay đổi]
- Lý do: [Tại sao]
- Tác giả: [Tên]
- Files ảnh hưởng: [Liệt kê]
