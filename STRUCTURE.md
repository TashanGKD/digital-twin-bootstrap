# 他山科研数字分身系统 — 完整目录结构

> 版本：新版（Block Protocol 交互式画像采集）
> 日期：2026-03-13

## 目录树

```
digital-twin-bootstrap/
│
├── start.py                        # 一键启动脚本（Python，跨平台）
├── start.sh                        # 一键启动脚本（Shell）
├── README.md                       # 项目说明
├── STRUCTURE.md                    # 本文件（目录结构说明）
│
├── backend/                        # Python FastAPI 后端（端口 8000）
│   ├── .env                        # ★ 实际配置（LLM_API_KEY 等）
│   ├── .env.example                # 配置模板
│   ├── requirements.txt            # Python 依赖
│   ├── main.py                     # FastAPI 入口，13个 API 端点
│   ├── agent.py                    # Agent 核心循环（Block Protocol + 11个工具）
│   ├── config.py                   # 环境变量读取
│   ├── llm_client.py               # LLM 客户端（OpenAI SDK → DashScope）
│   ├── sessions.py                 # 会话管理（内存 + profiles/ 落盘）
│   ├── tools.py                    # 工具实现（read_skill/read_doc/read_profile/write_profile）
│   ├── prompts.py                  # 系统提示词（META_SYSTEM_PROMPT）
│   ├── profile_parser.py           # Markdown 画像解析（纯正则）
│   ├── scientist_match.py          # 科学家匹配（几何 + LLM）
│   ├── scientists_db.py            # 30位知名科学家数据库
│   └── pdf_export.py               # PDF 导出（xhtml2pdf）
│
├── frontend/                       # React 19 + Vite 前端（端口 5173）
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.ts              # 代理配置：/api/* → localhost:8000
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── tsconfig.json / tsconfig.app.json / tsconfig.node.json
│   ├── eslint.config.js
│   ├── index.html
│   ├── public/
│   │   └── vite.svg
│   └── src/
│       ├── main.tsx                # 入口
│       ├── App.tsx                 # 路由（4页面）
│       ├── App.css                 # 全局样式（1348行，黑白极简主义）
│       ├── index.css               # Tailwind base + 字体 + 打印优化
│       ├── api.ts                  # 全部 API 调用（fetch SSE）
│       ├── types.ts                # 全局类型
│       ├── pages/
│       │   ├── ChatPage.tsx        # 对话采集主页（/）
│       │   ├── ProfilePage.tsx     # 画像展示（/profile）
│       │   ├── ScalesPage.tsx      # 量表列表（/scales）
│       │   └── ScaleTestPage.tsx   # 量表测试（/scales/:scaleId）
│       ├── components/
│       │   ├── blocks/
│       │   │   ├── BlockRenderer.tsx   # Block 分发路由器
│       │   │   ├── ChoiceBlock.tsx     # 可点击单选按钮
│       │   │   ├── TextInputBlock.tsx  # 文本输入框
│       │   │   ├── RatingBlock.tsx     # 数字评分按钮
│       │   │   ├── ChartBlock.tsx      # SVG 图表（radar/bar）
│       │   │   ├── ActionsBlock.tsx    # 操作按钮组
│       │   │   └── CopyableBlock.tsx   # 一键复制框
│       │   ├── profile/
│       │   │   ├── ProfileHeader.tsx
│       │   │   ├── CapabilitySection.tsx
│       │   │   ├── NeedsSection.tsx
│       │   │   ├── CognitiveStyleSection.tsx
│       │   │   ├── MotivationSection.tsx
│       │   │   ├── PersonalitySection.tsx
│       │   │   ├── InterpretationSection.tsx
│       │   │   ├── ScientistMatchSection.tsx
│       │   │   ├── ScientistCard.tsx
│       │   │   ├── ScientistScatter.tsx
│       │   │   └── DataSourceBadge.tsx
│       │   ├── ChatWindow.tsx
│       │   ├── DownloadButton.tsx
│       │   ├── LoadingDots.tsx
│       │   ├── MessageBubble.tsx
│       │   └── ProfilePanel.tsx
│       ├── data/
│       │   └── scales.ts           # 三套量表完整题库（前端内置）
│       └── utils/
│           └── scoring.ts          # 量表计分逻辑（含反向计分）
│
├── skills/                         # Agent 可读取的技能文件（11套）
│   ├── collect-basic-info/SKILL.md
│   ├── administer-ams/SKILL.md
│   ├── administer-rcss/SKILL.md
│   ├── administer-mini-ipip/SKILL.md
│   ├── infer-profile-dimensions/SKILL.md
│   ├── review-profile/SKILL.md
│   ├── update-profile/SKILL.md
│   ├── generate-forum-profile/SKILL.md
│   ├── generate-ai-memory-prompt/SKILL.md
│   ├── import-ai-memory/SKILL.md
│   └── modify-profile-schema/SKILL.md
│
├── doc/                            # Agent 可读取的参考文档（7份）
│   ├── academic-motivation-scale.md
│   ├── mini-ipip-scale.md
│   ├── researcher-cognitive-style.md
│   ├── tashan-profile-outline.md
│   ├── tashan-profile-examples.md
│   ├── multidimensional-work-motivation-scale.md
│   └── implementation-guide.md
│
└── profiles/                       # 用户画像落盘目录（运行时自动创建）
    └── _template.md                # 画像模板（sessions.py 初始化用）
```

## 路径说明（已修复）

`backend/sessions.py` 和 `backend/tools.py` 中的路径均以 `backend/` 为起点：
- `REPO_ROOT = Path(__file__).resolve().parent.parent`  → `digital-twin-bootstrap/`
- `profiles/` 目录在 `digital-twin-bootstrap/profiles/`
- `skills/` 目录在 `digital-twin-bootstrap/skills/`
- `doc/` 目录在 `digital-twin-bootstrap/doc/`

## 启动方式

```bash
cd digital-twin-bootstrap
python start.py
# 后端: http://localhost:8000
# 前端: http://localhost:5173  ← 浏览器打开
```

## 依赖

- Python 3.11+（后端）
- Node.js 18+（前端）
- `.env` 中填写 `LLM_API_KEY`（已预填）
