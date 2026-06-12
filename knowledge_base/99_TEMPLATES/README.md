# 99 - Templates

## Mục đích folder

Boilerplate templates dùng khi tạo file mới trong Hub. **Đừng tạo file mới mà không bắt đầu từ template.**

---

## 4 templates chính

| Template | Dùng cho | Layer áp dụng |
|---|---|---|
| `TEMPLATE_Legal_Source.md` | Tóm tắt 1 luật/nghị định/chính sách | Layer 1 |
| `TEMPLATE_Operating_Rule.md` | Viết 1 rule áp dụng cho team | Layer 2 |
| `TEMPLATE_Daily_Tool.md` | Tạo checklist/decision tree/script library | Layer 3 |
| `TEMPLATE_Case_Study.md` | Document 1 case study | Layer 4 |

---

## Cách dùng template

### Bước 1: Copy template ra folder đích
```bash
cp 99_TEMPLATES/TEMPLATE_Operating_Rule.md 02_GSX_OPERATING_RULES/013_Ten_Rule_Moi.md
```

### Bước 2: Fill frontmatter trước
Frontmatter (phần `---` đầu file) là **bắt buộc**, không skip.
- doc_id: format `Game Studio X-{LAYER}-{NUMBER}`, NUMBER lấy số kế tiếp trong MASTER_INDEX
- title: tên file dễ hiểu
- version: 1.0 cho file mới
- status: bắt đầu với `draft`
- last_updated, last_reviewed_by: ngày + tên Hub Owner
- related_*: link với các file Hub khác

### Bước 3: Fill content theo structure có sẵn
Đừng tự đổi structure - giữ nguyên các heading H2 trong template.
Section nào không áp dụng → ghi "N/A - lý do".

### Bước 4: Cập nhật MASTER_INDEX
Thêm entry mới vào `00_INDEX_VERSION/MASTER_INDEX.md` với status `placeholder` hoặc `draft`.

### Bước 5: Log changelog
Thêm entry vào `00_INDEX_VERSION/CHANGELOG.md`.

---

## Khi nào tạo template mới?

Không tự ý tạo template mới. Nếu thấy cần template mới:
1. Discuss với Hub Owner (Hub Owner)
2. Lý do template hiện có không đáp ứng được
3. Approval → tạo template + log changelog

Nguyên tắc: **càng ít template càng tốt**. Nhiều template = confusing.
