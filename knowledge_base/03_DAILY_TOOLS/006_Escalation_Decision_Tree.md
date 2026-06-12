---
doc_id: GSX-TOOL-006
title: "Escalation Decision Tree - Cây quyết định escalate"
tool_type: decision-tree
audience: all
use_when: Khi gặp tình huống bất thường/sự cố và không biết đi đâu
estimated_time: 1-2 phút để xác định cấp
version: 1.0
last_updated: 2026-06-03
maintained_by: Community Lead
related_operating_rules:
  - GSX-OP-010
---

# Escalation Decision Tree

## 🎯 Khi nào dùng tool này?

Khi gặp bất kỳ tình huống nào sau:
- User/KOL/đối tác đe doạ bóc phốt, drama lan rộng
- Phát hiện vi phạm pháp lý (NĐ13, bản quyền, bản đồ)
- Cơ quan chức năng / báo chí liên hệ
- Đồng nghiệp có dấu hiệu vi phạm tài chính
- Sự cố platform (account bị warning, page bị restrict)
- Mất phương hướng - không biết quyết định gì

## ⚡ Cách dùng nhanh

1. **Đi từ trên xuống** trong decision tree
2. **Dừng ở câu đầu tiên có YES**
3. **Action đúng cấp tương ứng**
4. **Trong 30 phút sau action**: xác nhận lại với Lead/Manager

---

## 🌳 DECISION TREE

```
╔═══════════════════════════════════════════════════╗
║  CÓ DẤU HIỆU NGUY HIỂM TÍNH MẠNG ?                ║
║  (user threat self-harm/suicide, đe doạ violence) ║
╚═══════════════════════════════════════════════════╝
                    │
        ┌───────────┴──────────┐
       YES                     NO
        │                       │
        ▼                       ▼
  ⚠️ L5 NGAY              Câu hỏi 2
  - Community Lead 
    NGAY (phone/Zalo)
  - Lead → HR + 
    Support chuyên môn
  - KHÔNG để case wait
```

```
╔═══════════════════════════════════════════════════╗
║  CƠ QUAN CHỨC NĂNG LIÊN HỆ ?                      ║
║  (cơ quan quản lý, A05, Công an, Cục PTTH...)             ║
╚═══════════════════════════════════════════════════╝
                    │
        ┌───────────┴──────────┐
       YES                     NO
        │                       │
        ▼                       ▼
  ⚠️ L5 NGAY              Câu hỏi 3
  - Manager Community 
    + LCCA + Dept Head
  - KHÔNG trả lời 
    trực tiếp
  - Lưu mọi bằng chứng
```

```
╔═══════════════════════════════════════════════════╗
║  BÁO CHÍ LIÊN HỆ ?                                ║
║  (Phóng viên, blogger lớn, podcast PR)            ║
╚═══════════════════════════════════════════════════╝
                    │
        ┌───────────┴──────────┐
       YES                     NO
        │                       │
        ▼                       ▼
  ⚠️ L4-L5                 Câu hỏi 4
  - Dùng câu chuẩn 
    chuyển CBC
  - PR Manager (CBC - xem CONTACTS_DIRECTORY) 
    NGAY
  - KHÔNG trả lời 
    "off the record"
```

```
╔═══════════════════════════════════════════════════╗
║  PHÁT HIỆN VI PHẠM RED LINE ?                     ║
║  - Bản đồ vi phạm đã đăng                         ║
║  - Form lộ CCCD/giấy tờ                           ║
║  - Vi phạm bản quyền nghiêm trọng                 ║
║  - Trục lợi/hoá đơn khống nội bộ                  ║
╚═══════════════════════════════════════════════════╝
                    │
        ┌───────────┴──────────┐
       YES                     NO
        │                       │
        ▼                       ▼
  ⚠️ L4-L5                 Câu hỏi 5
  - Dept Head + LCCA 
    NGAY
  - GỠ content vi phạm 
    NGAY (nếu là 
    content public)
  - Incident report 
    trong 24h
  - Whistleblowing: 
    HR/AF nếu nội bộ
```

```
╔═══════════════════════════════════════════════════╗
║  CRISIS LAN RỘNG ?                                ║
║  - >50 share/comment đồng tình                    ║
║  - Influencer comment vào                         ║
║  - Có khả năng viral cấp ngành                    ║
╚═══════════════════════════════════════════════════╝
                    │
        ┌───────────┴──────────┐
       YES                     NO
        │                       │
        ▼                       ▼
  ⚠️ L3-L4                 Câu hỏi 6
  - Marketing Lead +
    PR Manager
  - Cooling Rule (không 
    phản ứng tức thời)
  - Plan response 
    có data
```

```
╔═══════════════════════════════════════════════════╗
║  DRAMA BẮT ĐẦU LAN ?                              ║
║  (>5 share/comment đồng tình, nhiều user join)    ║
╚═══════════════════════════════════════════════════╝
                    │
        ┌───────────┴──────────┐
       YES                     NO
        │                       │
        ▼                       ▼
  ⚠️ L2-L3                Câu hỏi 7
  - Marketing Lead 
    vào cuộc
  - Đánh giá có 
    chuyển L3 không
```

```
╔═══════════════════════════════════════════════════╗
║  CÒN CHẤT LƯỢNG NHỎ - 1 USER, CHƯA LAN ?         ║
║  (Drama cá nhân, comment tiêu cực 1 user)         ║
╚═══════════════════════════════════════════════════╝
                    │
        ┌───────────┴──────────┐
       YES                     NO
        │                       │
        ▼                       ▼
  ✅ L1-L2              Câu hỏi 8
  - Tự xử (CTV + 
    Community Lead)
  - Áp dụng Scripts 
    Library
  - Lưu log 
    nhưng KHÔNG 
    cần escalate
```

```
╔═══════════════════════════════════════════════════╗
║  KOL/PARTNER ĐÒI THÊM QUYỀN LỢI / VI PHẠM MOU ?  ║
╚═══════════════════════════════════════════════════╝
                    │
        ┌───────────┴──────────┐
       YES                     NO
        │                       │
        ▼                       ▼
  ⚠️ L2-L3                Câu hỏi 9
  - Line Manager + 
    Marketing Lead
  - Dùng câu chuẩn 
    "ghi nhận, không 
    cam kết thêm"
  - Confirm sau qua 
    văn bản
```

```
╔═══════════════════════════════════════════════════╗
║  BÁO CÁO MEDIA / KOL có scandal LIÊN ĐỚI VNG ?    ║
╚═══════════════════════════════════════════════════╝
                    │
        ┌───────────┴──────────┐
       YES                     NO
        │                       │
        ▼                       ▼
  ⚠️ L3                   ✅ Tự đánh giá
  - Marketing Lead + 
    PR Manager
  - Plan distance khỏi 
    KOL/partner
```

---

## 📊 BẢNG CẤP ESCALATION TÓM TẮT

| Cấp | Người xử lý | Loại tình huống | SLA |
|---|---|---|---|
| **L1** | CTV / Nhân viên Community | Drama 1 user, comment tiêu cực không lan | Tự xử trong giờ |
| **L2** | Community Lead / Line Manager | Drama bắt đầu lan, KOL/partner đòi thêm | 30 phút |
| **L3** | Marketing Lead + PR Manager | Lan rộng, KOL scandal, drama có influencer | 1-2h |
| **L4** | Manager Community + Dept Head | Viral, red line vi phạm, báo chí | 1h |
| **L5** | BLĐ VNGGames + LCCA + CBC + HR | Cơ quan chức năng, threat tính mạng, vi phạm pháp luật nghiêm trọng | NGAY (< 30 phút) |

---

## 📞 KÊNH LIÊN HỆ ESCALATION

**Trong giờ hành chính**:
- Email + Zalo/Slack thường

**Ngoài giờ + cuối tuần** (cho tình huống urgent):
- Zalo/phone Line Manager NGAY
- Nếu không reach được Line Manager: phone Manager Community
- Nếu vẫn không reach: phone Dept Head

**Tình huống nghiêm trọng nhất (L5)**:
- Phone đồng thời cả Lead/Manager/Dept Head
- KHÔNG chờ ai reply trước - đảm bảo ít nhất 1 người tiếp nhận trong 5 phút

---

## ✅ Sau khi escalate

```
[ ] Đã lưu screenshot/URL/bằng chứng?
[ ] Đã gửi báo cáo template cho Manager?
   (AI - CHUYỆN GÌ - KÊNH NÀO - BẰNG CHỨNG - CẦN GÌ)
[ ] Đã ngừng phản hồi public (dùng câu chuẩn 1 lần)?
[ ] Đợi chỉ đạo, KHÔNG tự ý action thêm?
[ ] Trong 24h sau khi giải quyết: viết Incident Report (GSX-TOOL-008)?
```

---

## 🔗 Tham chiếu

- **Rule gốc**: GSX-OP-010 (Crisis Communication Playbook)
- **Tools liên quan**: 
  - GSX-TOOL-007 (Scripts Library - các câu chuẩn)
  - GSX-TOOL-008 (Incident Report Template)
- **Ownership**: `00_INDEX_VERSION/OWNERSHIP_MAP.md`

---

## Changelog

| Version | Date | Changed by | Notes |
|---|---|---|---|
| 1.0 | 2026-06-03 | Hub Owner | Initial - codify từ GSX-OP-010 escalation chain |
