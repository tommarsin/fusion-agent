# 00 - Index & Version Control

## Mục đích folder
Quản lý version, ownership và lịch sử thay đổi của toàn Hub.

## Files trong folder này

| File | Mô tả | Update khi |
|---|---|---|
| `CHANGELOG.md` | Lịch sử mọi thay đổi của Hub | Mỗi lần có update |
| `OWNERSHIP_MAP.md` | Ai phụ trách cái gì | Khi có thay đổi nhân sự |
| `MASTER_INDEX.md` | Index tất cả file trong Hub với doc_id | Khi thêm file mới |
| `REVIEW_SCHEDULE.md` | Lịch review định kỳ 6 tháng/lần | Sau mỗi lần review |

## Naming convention cho doc_id

```
Game Studio X-{LAYER}-{NUMBER}

LAYER:
  LEGAL    → Layer 1 (Legal Source)
  OP       → Layer 2 (Operating Rules)
  TOOL     → Layer 3 (Daily Tools)
  CASE     → Layer 4 (Case Studies)
  TRAIN    → Layer 5 (Training)

NUMBER: 3-digit, bắt đầu từ 001

Ví dụ:
  GSX-LEGAL-001: NĐ13/2023
  GSX-OP-001: Data Collection Policy
  GSX-TOOL-001: Pre-Launch Checklist
  GSX-CASE-001: UGC Contest ND13 Violation
```
