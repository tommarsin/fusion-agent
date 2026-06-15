# GameLaw AI Agent — Game Content Compliance AI System

An AI compliance agent for game marketing & operations teams.
Consolidates Vietnamese law, platform policies (Meta/TikTok/Google), and internal rules into a single source of truth.
Provides Q&A with citations, a 4-step content scanner (detect → explain → rewrite → checklist), rule authoring from links, and a Notion webhook connector.

Built for GreenNode Claw-a-thon 2026 by Team Fusion.

## Quick start

```bash
cp .env.example .env   # fill in LLM + DB credentials
python -m venv venv && venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py         # → http://localhost:8080
curl http://localhost:8080/health
```

Full setup, architecture, and API docs: see `ARCHITECTURE.md` (coming in release v1.0).
