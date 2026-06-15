"""
Integrations layer — adapters cho hệ thống ngoài (Item 9.5+).

Adapter đầu tiên: Notion (Content Calendar). Thiết kế theo adapter pattern
(brainstorm #013 ý 1) — interface đọc/ghi tách khỏi flow scan để không lock-in
một nhà cung cấp checklist/calendar cụ thể.
"""
