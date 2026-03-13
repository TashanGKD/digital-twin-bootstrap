<p align="center">
  <a href="https://tashan.ac.cn/homepage/" target="_blank" rel="noopener noreferrer">
    <img src="docs/assets/tashan.svg" alt="Tashan Logo" width="200" />
  </a>
</p>

<p align="center">
  <strong>Tashan Research Digital Twin · 0→1 Bootstrap</strong><br>
  <em>他山科研数字分身系统</em>
</p>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#api-configuration">API Config</a> •
  <a href="#project-structure">Structure</a> •
  <a href="#ecosystem">Ecosystem</a> •
  <a href="#contributing">Contributing</a> •
  <a href="README.md">中文</a>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![React](https://img.shields.io/badge/React-19-61dafb)

> Build a structured, traceable, multi-dimensional digital twin of a researcher through AI-guided conversation — the 0→1 initial construction phase.

---

## Overview

### Role in the Research Program

The "Human-Agent Hybrid Digital World" research program consists of two major constructions. The second is the **digital twin pathway**: how real humans enter the world. This project implements the **first phase (0→1)**: constructing a viable initial twin from sparse information.

A digital twin is not a one-time snapshot but a **dynamically updated approximation of the real individual** (the engineering realization of the Bᵢ particle Agent State layer). The 0→1 phase focuses on producing a structured, source-labeled, confidence-annotated initial approximation that can be refined by downstream iteration systems.

### Three Acquisition Paths

| Path | Method | Strength |
|------|--------|----------|
| Structured conversation | AI-guided multi-turn interview (Block Protocol SSE) | Low barrier, natural language, adaptive |
| Standard psychometrics | Mini-IPIP / AMS / RCSS (full item banks built into frontend) | Interpretable, measurement-grounded |
| AI inference | Inference for dimensions that cannot be directly elicited | Fills gaps, labeled with confidence, overwritable |

### Seven-Dimension Profile

```
Identity (stage · field · paradigm) → Capability (tech stack · research workflow)
→ Current Needs → Cognitive Style (RCSS) → Academic Motivation (AMS)
→ Personality (Mini-IPIP) → Integrated Interpretation
```

---

## Features

- **Conversational collection**: AI-driven phased interview with Block Protocol (choice/rating/text-input) for structured interaction
- **11 skill files**: Agent calls skills on demand for profile collection, scale administration, AI inference, forum profile generation, and more
- **Three standard scales** (complete item banks with reverse scoring):
  - **Mini-IPIP** (20 items): Big Five personality
  - **AMS-GSR 28**: Academic motivation (intrinsic/extrinsic/amotivation)
  - **RCSS**: Research cognitive style (horizontal integration vs. vertical depth)
- **Profile visualization**: Radar charts and bar charts for dimension scores
- **Scientist matching**: Geometric distance + LLM semantics against 30 notable scientists
- **Forum profile generation**: One-click Identity/Expertise/Thinking/Discussion format for Tashan Forum
- **AI memory import**: Import from ChatGPT/Claude memory and intelligently merge with existing profile
- **Multi-format export**: Markdown download / PDF export / copy forum profile
- **Multi-model support**: Switch between Qwen3.5/Kimi/GLM/MiniMax from the frontend

---

## Quick Start

### Requirements

- Python 3.11+
- Node.js 18+
- An API key from any OpenAI-compatible LLM provider (see [API Configuration](#api-configuration))

### One-Command Launch

```bash
# Clone
git clone https://github.com/TashanGKD/digital-twin-bootstrap.git
cd digital-twin-bootstrap

# Configure API (required — see below)
cp backend/.env.example backend/.env
# Edit backend/.env and fill in your API key

# Launch (auto-installs dependencies, starts both frontend and backend)
python start.py
```

After launch:
- Backend: `http://localhost:8000`
- **Frontend: `http://localhost:5173` ← open this in your browser**

Press `Ctrl+C` to stop.

### Manual Launch (optional)

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

---

## API Configuration

### Step 1: Copy the template

```bash
cp backend/.env.example backend/.env
```

### Step 2: Edit `backend/.env`

```bash
# Choose your AI provider: zhipuai | kimi | qwen | deepseek | minimax
LLM_PROVIDER=qwen

# Fill in the API key for your chosen provider
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# (Optional) Override the default model
# LLM_MODEL=qwen-plus
```

### Supported Providers

| Provider | Environment Variable | Get Key | Recommended Model |
|----------|---------------------|---------|-------------------|
| Qwen (Alibaba Cloud) | `QWEN_API_KEY` | [dashscope.aliyun.com](https://dashscope.aliyun.com) | `qwen-plus` |
| ZhipuAI (GLM) | `ZHIPUAI_API_KEY` | [zhipuai.cn](https://open.zhipuai.cn) | `glm-4-plus` |
| Kimi / Moonshot | `KIMI_API_KEY` | [platform.moonshot.cn](https://platform.moonshot.cn) | `moonshot-v1-8k` |
| DeepSeek | `DEEPSEEK_API_KEY` | [platform.deepseek.com](https://platform.deepseek.com) | `deepseek-chat` |

### Advanced: Custom Base URL

For proxy servers, private deployments, or other OpenAI-compatible services:

```bash
# backend/.env
LLM_PROVIDER=qwen
QWEN_API_KEY=sk-xxxxxxxx
LLM_BASE_URL=https://your-proxy.example.com/v1
LLM_MODEL=your-model-name
```

The system uses the OpenAI Python SDK, so any OpenAI-compatible API endpoint works.

### Verify Configuration

After starting, visit `http://localhost:8000/models` to see the available model list and confirm the connection is working.

---

## Project Structure

```
digital-twin-bootstrap/
│
├── start.py                        # One-command launcher (cross-platform)
├── start.sh                        # Shell launcher
│
├── backend/                        # Python FastAPI backend (port 8000)
│   ├── .env.example                # Configuration template (copy to .env)
│   ├── requirements.txt
│   ├── main.py                     # FastAPI entry, 13 API endpoints
│   ├── agent.py                    # Agent loop (Block Protocol + tool calls)
│   ├── config.py                   # Environment variable loading
│   ├── llm_client.py               # LLM client (OpenAI SDK compatible)
│   ├── sessions.py                 # Session management (memory + disk)
│   ├── tools.py                    # Tool implementations
│   ├── prompts.py                  # System prompt
│   ├── profile_parser.py           # Markdown profile parser
│   ├── scientist_match.py          # Scientist matching
│   ├── scientists_db.py            # 30 notable scientists database
│   └── pdf_export.py               # PDF export
│
├── frontend/                       # React 19 + TypeScript + Vite (port 5173)
│   └── src/
│       ├── pages/                  # 4 pages: Chat / Profile / Scale List / Scale Test
│       ├── components/             # UI: Block renderer / profile display / chat window
│       ├── data/scales.ts          # Full item banks for 3 scales
│       └── utils/scoring.ts        # Scale scoring (with reverse scoring)
│
├── skills/                         # 11 skill files readable by the Agent
├── doc/                            # 7 reference documents (scale items, etc.)
└── profiles/                       # User profiles (runtime, gitignored)
    └── _template.md
```

---

## Ecosystem

| Layer | Project | Repository | Type | Status |
|-------|---------|-----------|------|:------:|
| World Substrate | ① Axiom Framework | [world-axiom-framework](https://github.com/TashanGKD/world-axiom-framework) | Open Source | 🟡 |
| World Substrate | ② Architecture | [world-three-particle-impl](https://github.com/TashanGKD/world-three-particle-impl) | Open Source | 🟡 |
| World Substrate | ③ Sandbox Validation | [world-sandbox-validation](https://github.com/TashanGKD/world-sandbox-validation) | Open Source | 🔲 |
| Digital Twin | **④ Bootstrap (0→1)** ← this repo | [digital-twin-bootstrap](https://github.com/TashanGKD/digital-twin-bootstrap) | Open Source | 🟡 |
| Digital Twin | ⑤ Iteration (1→100) | [digital-twin-iteration](https://github.com/TashanGKD/digital-twin-iteration) | Open Source | 🔲 |
| Core App | Digital World | TashanGKD/tashan-world | Private | 🔲 |
| Commercial | Twin Platform | TashanGKD/tashan-twin-platform | Private | 🔲 |
| Public Interest | Tashan Forum | [tashan-forum](https://github.com/TashanGKD/tashan-forum) | Open Source | 🔲 |

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon).

**Skill contributions** (no code changes needed): Add a new `skill-name/SKILL.md` in the `skills/` directory to extend the Agent's capabilities.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
