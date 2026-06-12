---
doc_id: GSX-TOOL-008
title: "Incident Report Template - Mẫu báo cáo sự cố"
tool_type: template-form
audience: all
use_when: Trong 24h sau khi sự cố compliance/crisis được giải quyết xong
estimated_time: 30-60 phút để viết
version: 1.0
last_updated: 2026-06-03
maintained_by: Community Lead + LCCA
related_operating_rules:
  - GSX-OP-010
---

# Incident Report Template

## 🎯 Khi nào dùng tool này?

Trong **24h sau khi sự cố được giải quyết** (không phải lúc đang xảy ra):
- Mọi sự cố cấp 2 trở lên trong escalation chain
- Vi phạm compliance phát hiện và xử lý
- Crisis truyền thông đã được handle
- Vi phạm nội bộ phát hiện qua whistleblowing
- Yêu cầu của cơ quan chức năng đã response

## ⚡ Cách dùng nhanh

1. Copy template dưới đây
2. Fill từng section - bám sát facts, không cảm xúc
3. Submit Lead/Manager + lưu Drive nội bộ
4. Recommendation section có thể trigger update rule/case study

---

## 📝 TEMPLATE INCIDENT REPORT

```markdown
# Incident Report: [Tên ngắn gọn sự cố]

**Doc ID**: INC-[YYYY-MM-DD]-[short-code]
**Reported by**: [Tên - role]
**Date of incident**: [YYYY-MM-DD HH:MM]
**Date of resolution**: [YYYY-MM-DD HH:MM]
**Date of report**: [YYYY-MM-DD]
**Classification**: [data-privacy / content-moderation / partner / tournament / financial / workplace / crisis-comm]
**Severity**: [Critical / High / Medium / Low]
**Status**: [Resolved / Ongoing / Escalated]

---

## 1. EXECUTIVE SUMMARY (TL;DR)

[3-5 câu tóm tắt: chuyện gì xảy ra, ai liên quan, hậu quả, đã xử lý ra sao]

---

## 2. TIMELINE

| Time | Event | Action taken |
|---|---|---|
| [HH:MM] | [Sự việc cụ thể] | [Action] |
| [HH:MM] | [Sự việc cụ thể] | [Action] |
| [HH:MM] | [Sự việc cụ thể] | [Action] |

[Tiếp tục tới khi resolved]

---

## 3. CONTEXT

### 3.1. Bối cảnh trước sự cố
[Thông tin về hoạt động/campaign/tình huống đang diễn ra trước khi sự cố xảy ra]

### 3.2. Đối tượng liên quan
- **Internal**: [Liệt kê role/team liên quan - không nhất thiết tên]
- **External**: [User/KOL/partner/báo chí/cơ quan chức năng nếu có]

### 3.3. Kênh/Platform xảy ra
- [Facebook Fanpage / Group / Discord / Email / Phone / Sự kiện offline / khác]

---

## 4. ROOT CAUSE ANALYSIS

### 4.1. Nguyên nhân trực tiếp (proximate cause)
[Tại sao sự cố xảy ra ở thời điểm đó]

### 4.2. Nguyên nhân hệ thống (systemic cause)
[Tại sao process/rule hiện tại không phòng ngừa được sự cố này]

### 4.3. Yếu tố con người (human factors)
[Yếu tố con người - lỗi cá nhân, thiếu training, áp lực thời gian, v.v.]

### 4.4. Yếu tố quy trình (process factors)
[Quy trình hiện tại có gap gì]

---

## 5. IMPACT ASSESSMENT

### 5.1. Hậu quả pháp lý
- [ ] Có vi phạm pháp luật? [Cụ thể luật/điều nào]
- [ ] Có vi phạm chính sách VNG? [Policy nào]
- [ ] Có vi phạm tiêu chuẩn nền tảng? [Facebook/YouTube/Riot]

### 5.2. Hậu quả uy tín
- [ ] User số lượng bao nhiêu bị ảnh hưởng?
- [ ] Có viral trên MXH không? Reach ước tính?
- [ ] Có báo chí đưa tin không?
- [ ] Cộng đồng phản ứng thế nào?

### 5.3. Hậu quả tài chính
- [ ] Phạt tiền có thể (nếu có)?
- [ ] Thiệt hại thực tế (refund, replacement, makeup campaign)?
- [ ] Cost xử lý nội bộ?

### 5.4. Hậu quả với đối tác
- [ ] Riot Games có quan ngại không?
- [ ] KOL/Brand partner có rút khỏi hợp tác?
- [ ] Cộng đồng partner (other Cyber, BTC) có dao động?

---

## 6. ACTION TAKEN

### 6.1. Immediate actions (trong vài giờ đầu)
1. [Action 1] - by [role]
2. [Action 2] - by [role]
3. [Action 3] - by [role]

### 6.2. Short-term actions (trong 24-48h)
1. [Action 1]
2. [Action 2]

### 6.3. Communication
- [ ] Internal communication: [Ai được inform - khi nào]
- [ ] External communication: [Statement public nếu có]
- [ ] User communication: [DM/email/post]

### 6.4. Escalation chain followed
- [ ] L1 → L2: [time, by whom]
- [ ] L2 → L3: [time, by whom]
- [ ] L3 → L4: [time, by whom]
- [ ] L4 → L5: [time, by whom]

---

## 7. EVIDENCE & DOCUMENTATION

### 7.1. Bằng chứng
- [ ] Screenshot: [link Drive]
- [ ] URL/Link: [danh sách]
- [ ] Email/Chat log: [link]
- [ ] Recording: [link nếu có]

### 7.2. Documents liên quan
- [ ] Brief/Plan original: [link]
- [ ] Compliance checklist trước go-live: [link]
- [ ] Approval emails: [link]

---

## 8. LESSONS LEARNED

### 8.1. Cái gì đã hoạt động tốt?
[Process/người/quyết định nào đã giúp xử lý sự cố hiệu quả]

### 8.2. Cái gì cần cải thiện?
[Process/quyết định nào lẽ ra nên khác]

### 8.3. Cảnh báo sớm bị bỏ qua?
[Có dấu hiệu sớm nào mà team đã không nhận diện kịp]

---

## 9. RECOMMENDATIONS

### 9.1. Rule/Policy cần update
- [ ] Rule [GSX-OP-XXX]: cần sửa [cụ thể]
- [ ] Cần tạo rule mới: [domain]
- [ ] Tool/Checklist [GSX-TOOL-XXX]: cần thêm item [cụ thể]

### 9.2. Training cần bổ sung
- [ ] Toàn team Community
- [ ] CTV mới
- [ ] Lead/Manager
- [ ] Cross-team (Brand, PR, KOL Mgmt)

### 9.3. Technical/Tool cần triển khai
- [ ] Auto-monitor [cụ thể]
- [ ] Approval workflow [cụ thể]
- [ ] Documentation system [cụ thể]

### 9.4. Người đề xuất follow-up
| Recommendation | Owner | Deadline | Status |
|---|---|---|---|
| [Item] | [Name] | [Date] | [ ] |
| [Item] | [Name] | [Date] | [ ] |

---

## 10. CASE STUDY CONVERSION

Sự cố này có cần convert thành Case Study trong Hub không?

- [ ] CÓ → Tạo `GSX-CASE-XXX` từ template (`99_TEMPLATES/TEMPLATE_Case_Study.md`)
- [ ] KHÔNG (sự cố nhẹ, không có bài học systemic)

Nếu CÓ:
- **Doc ID dự kiến**: GSX-CASE-XXX
- **Share scope**: [gsx-internal / community-only / all-vng / public-ok]
- **Owner viết case**: [Tên]
- **Deadline complete case study**: [Date]

---

## 11. SIGN-OFF

| Role | Name | Signature/Confirm | Date |
|---|---|---|---|
| Reporter | | | |
| Line Manager | | | |
| Marketing Lead (nếu liên quan) | | | |
| Dept Head | | | |
| LCCA (nếu vi phạm pháp lý) | | | |

---

**End of report**

## File location: 
`Drive/Compliance/Incidents/[YYYY]/INC-[YYYY-MM-DD]-[short-code]/report.md`
```

---

## ⚠️ Lưu ý khi viết report

- **Facts > feelings**: Stick to what happened, not how you felt
- **Anonymize nếu nhạy cảm**: Dùng role thay tên cá nhân nếu cần
- **Don't blame, do learn**: Mục đích là phòng ngừa tương lai, không tìm scapegoat
- **Specific > vague**: "User threat bóc phốt qua DM Facebook" tốt hơn "có vấn đề với user"
- **Honest về what went wrong**: Sai lầm phải document để học, không che giấu

---

## 🔗 Tham chiếu

- **Rule gốc**: GSX-OP-010 (Crisis Communication) - mục quy trình 7 bước
- **Tool liên quan**: GSX-TOOL-006 (Escalation Decision Tree)
- **Conversion sang Case Study**: 99_TEMPLATES/TEMPLATE_Case_Study.md

---

## Changelog

| Version | Date | Changed by | Notes |
|---|---|---|---|
| 1.0 | 2026-06-03 | Hub Owner | Initial - codify quy trình incident từ GSX-OP-010 |
