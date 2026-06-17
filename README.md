# GameLaw AI Agent

> **Làm game mà không rõ luật? Để đó có GameLaw AI Agent lo.**
> *Building games without knowing the law? Let GameLaw AI Agent handle it.*

AI Compliance Agent cho marketing & vận hành ngành game — gom luật Việt Nam, policy nền tảng (Meta/TikTok/Google Ads) và rule nội bộ thành **một playbook tuân thủ duy nhất**, kèm AI quét nội dung trước khi đăng.

Built for **GreenNode Claw-a-thon 2026** · **Team Fusion** (Group 8).

---

## 🔗 Trải nghiệm / Live demo

| | Link |
|---|---|
| 🌐 **Agent UI** (mở bằng Incognito) | https://endpoint-39d10191-f65d-4917-8de1-1424bf162743.agentbase-runtime.aiplatform.vngcloud.vn/ui |
| ❤️ **Health check** | https://endpoint-39d10191-f65d-4917-8de1-1424bf162743.agentbase-runtime.aiplatform.vngcloud.vn/health |
| 📹 **Video demo** (< 3 phút) | https://youtu.be/JDCbFH_-llY |

---

## 📝 Giới thiệu / About

### 🇻🇳 Tiếng Việt

**A. Vấn đề**
Team marketing/vận hành game phải tuân thủ cùng lúc 3 lớp luật: luật nhà nước (quảng cáo, dữ liệu, nội dung số) + policy nền tảng (Meta, TikTok, Google Ads) + rule nội bộ. Hậu quả khi sai:
- Tri thức phân mảnh ở hàng chục file/chat → không có nguồn chuẩn duy nhất
- Review thủ công → chậm, dễ sai, không scale khi nhiều game/campaign
- Vi phạm thật: ads bị reject, page bị khoá, rủi ro pháp lý

**B. Người dùng**
Nhân viên marketing game, content creator, social media operator, compliance lead, quản lý vận hành tại studio game.

**C. Cách hoạt động**
1. **Playbook tuân thủ** — biến hàng chục văn bản luật rời rạc thành 1 cẩm nang trọng tâm: custom rule vận hành + daily-tool checklist + case study răn đe → hiểu giá trị thực tế của luật, không chỉ trích luật khô khan
2. **Content Scanner 4 bước** — nhập text/ảnh → (1) phát hiện vi phạm, (2) giải thích kèm trích dẫn luật, (3) viết lại an toàn, (4) tạo checklist pre-publish
3. **Chatbot** hỏi đáp pháp lý có trích dẫn nguồn
4. **Tùy chỉnh** — mỗi Game Studio chỉnh playbook theo nhu cầu riêng
5. **Public API** (`POST /scan`, `/ask`) — tích hợp vào bất kỳ tool nào; demo nối Notion quét Content Calendar tự động

**D. Giá trị**
- Giảm 80%+ thời gian review thủ công
- Chuẩn hoá kiến thức pháp lý cho cả team, hết phụ thuộc 1-2 người
- Bắt lỗi trước khi publish, không phải sau khi bị phạt
- Onboarding nhân sự mới nhanh hơn nhờ case study + chatbot

### 🇬🇧 English

**A. The Problem**
Game marketing/operations teams must comply with 3 layers of rules at once: national law (advertising, data, digital content) + platform policies (Meta, TikTok, Google Ads) + internal rules. When it goes wrong:
- Knowledge scattered across dozens of files/chats → no single source of truth
- Manual review → slow, error-prone, doesn't scale across many games/campaigns
- Real consequences: ads rejected, pages banned, legal risk

**B. Target Users**
Game marketers, content creators, social media operators, compliance leads, operations managers at game studios.

**C. How It Works**
1. **Compliance Playbook** — turns dozens of scattered legal documents into one focused handbook: custom operating rules + daily-tool checklists + cautionary case studies → grasp the real-world value of the law, not just dry citations
2. **4-step Content Scanner** — input text/image → (1) detect violations, (2) explain with legal citations, (3) rewrite safely, (4) generate pre-publish checklist
3. **Chatbot** — legal Q&A with cited sources
4. **Customizable** — each Game Studio tailors the playbook to its own needs
5. **Public API** (`POST /scan`, `/ask`) — integrate into any tool; demo connects to Notion to scan the Content Calendar automatically

**D. Value**
- Cuts 80%+ of manual review time
- Standardizes legal knowledge across the team — no more dependence on 1–2 people
- Catches violations before publishing, not after a penalty
- Faster onboarding for new hires via case studies + chatbot

---

## 🏗️ Kiến trúc / Architecture

```
[HTML Hub: chat / scan / ingest / duyệt / audit / role-switch]   [Notion automation → webhook]
                 │ HTTPS                                                  │ HTTPS
                 ▼                                                        ▼
   ┌──────────────────────────────────────────────────────────────────────────┐
   │   GameLaw AI Agent — AgentBase Custom Agent (Python · FastAPI)            │
   │   0.0.0.0:8080 · GET /health · POST /ask /scan /checklist /ingest /approve│
   │     ├─ RAG Retriever (BM25 over knowledge base + rules in DB)             │
   │     ├─ Content Scanner (detect → explain → rewrite → checklist)           │
   │     ├─ Authoring Engine (+ Web Fetch khi input là link)                   │
   │     ├─ Role gate (X-Role: Admin/Mod/User) + Audit log                     │
   │     └─ LLM client → MaaS (OpenAI-compatible)                              │
   └──────────────┬───────────────────────────────────┬───────────────────────┘
                  ▼                                   ▼
        [VNG Cloud vDB — Postgres]            [MaaS LLM: Minimax 2.5 · Gemma 4 31B vision]
```

**Tech stack:** Python · FastAPI · Jinja2 · BM25 RAG · VNG Cloud vDB (Postgres) · GreenNode MaaS LLM · Docker · GreenNode AgentBase.

---

## 🔌 API Endpoints

Base URL = endpoint ở trên. Header: `X-Role: User | Mod | Admin`.

| Method | Endpoint | Role | Mô tả |
|--------|----------|------|-------|
| GET | `/health` | — | Health check |
| GET | `/ui` | — | Web Hub (chat + scanner + knowledge base) |
| POST | `/ask` | All | Chatbot Q&A có trích dẫn |
| POST | `/scan` | All | Content Scanner 4 bước (text + ảnh base64) |
| POST | `/checklist` | All | Sinh checklist pre-publish |
| POST | `/notion-scan` | Mod+ | Quét Notion Content Calendar |
| POST | `/ingest` · `/draft` | Mod+ | Nạp / soạn rule từ link/text |
| GET · PUT · DELETE | `/rules` · `/rules/{id}` | Mod+ | Quản lý rule + lịch sử |
| POST | `/approve` · GET `/submissions` · GET `/audit` | Admin | Duyệt luật, audit log |

Ví dụ:

```bash
curl -X POST "$BASE/scan" -H "X-Role: User" -H "Content-Type: application/json" \
  -d '{"content":"Tải game ngay - thắng 100% mọi ván! Rút tiền thật!","platforms":["meta","tiktok"]}'
```

---

## 🚀 Quick start (local)

```bash
cp .env.example .env       # điền LLM + DB credentials
python -m venv venv
# Windows:    venv\Scripts\Activate.ps1
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python main.py             # → http://localhost:8080
curl http://localhost:8080/health
```

---

## 👥 Team Fusion

| Thành viên | Vai trò |
|-----------|---------|
| Phucndt | Concept · knowledge base · backend |
| Vilph | Co-builder · user experience (tài liệu & quay/chụp video submit) |

GreenNode Claw-a-thon 2026 — Group 8.
