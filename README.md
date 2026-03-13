<p align="center">
  <img src="docs/assets/tashan.svg" alt="他山 Logo" width="200" />
</p>

<p align="center">
  <strong>他山科研数字分身系统</strong><br>
  <em>Tashan Research Digital Twin · 0→1 Bootstrap</em>
</p>

<p align="center">
  <a href="#项目简介">简介</a> •
  <a href="#功能特性">功能</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#api-配置">API 配置</a> •
  <a href="#代码结构">代码结构</a> •
  <a href="#生态位置">生态位置</a> •
  <a href="#贡献">贡献</a> •
  <a href="README.en.md">English</a>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![React](https://img.shields.io/badge/React-19-61dafb)
![状态](https://img.shields.io/badge/状态-原型可用-yellow)

> 通过结构化 AI 对话，采集科研人员的多维画像，构建可复用、可协作、可演化的数字化自我表示。

---

## 项目简介

### 在大框架中的位置

「人—智能体混合数字世界」研究的第二大构造是**数字分身路径**——真人如何进入世界。本项目是该路径的**第一阶段（0→1）**：如何从极少的信息构造一个可工作的初始分身。

数字分身不是一次性的静态画像，而是对真实个体的**持续逼近的动态表示**（Agent State 层的工程实化）。0→1 阶段的核心目标不是追求一次性高保真，而是构造一个**结构明确、来源可追溯、置信度标注、可被后续迭代接管**的初始近似。

### 核心设计

**三条并行采集路径**：

| 路径 | 方式 | 优势 |
|------|------|------|
| 结构化对话 | AI 引导的多轮访谈（Block 协议 SSE）| 低门槛，自然语言，自适应 |
| 标准量表 | Mini-IPIP / AMS / RCSS（前端内置完整题库）| 有测量学基础，可解释 |
| AI 推断 | 对无法直接采集的维度进行推断 | 覆盖死角，标注置信度，可覆写 |

**七维画像结构**（符合公理体系 Bᵢ 粒子 Agent State 定义）：

```
身份（研究阶段·学科·方法范式）→ 能力（技术栈·科研流程）
→ 当前需求 → 认知风格（RCSS）→ 学术动机（AMS）
→ 人格（Mini-IPIP）→ 综合解读
```

### 适合以下场景

- 科研人员快速构建自己的数字分身（5-15分钟完成初始画像）
- 研究者作为进入他山数字世界的入口
- 数字孪生研究中"0→1 构建"阶段的工程参考实现

---

## 功能特性

- **对话式采集**：AI 主导的分阶段访谈，Block 协议（choice/rating/text-input）让交互结构化
- **11 套技能文件**：Agent 可按需调用，覆盖基础信息采集、量表施测、AI推断、画像生成、论坛分身等
- **三套标准量表**（前端内置完整题库，含反向计分）：
  - **Mini-IPIP**（20题）：大五人格
  - **AMS-GSR 28**：学术动机（内在/外在/无动机）
  - **RCSS**：科研认知风格（横向整合 vs 垂直深度）
- **画像可视化**：雷达图 + 柱状图直观展示各维度得分
- **科学家匹配**：几何距离 + LLM 语义，匹配30位知名科学家作为认知参考
- **他山论坛分身**：一键生成可发布到他山论坛的 Identity/Expertise/Thinking/Discussion 四节格式
- **AI 记忆导入**：支持从 ChatGPT/Claude 记忆导入，智能与已有画像合并
- **多格式导出**：Markdown 下载 / PDF 导出 / 一键复制论坛分身
- **多模型支持**：前端可切换 Qwen3.5/Kimi/GLM/MiniMax 等

---

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- 任意兼容 OpenAI API 的 LLM 服务商账号（见 [API 配置](#api-配置)）

### 一键启动

```bash
# 克隆仓库
git clone https://github.com/TashanGKD/digital-twin-bootstrap.git
cd digital-twin-bootstrap

# 配置 API（必须，见下方说明）
cp backend/.env.example backend/.env
# 编辑 backend/.env，填入你的 API Key

# 一键启动（自动安装依赖、启动前后端）
python start.py
```

启动后：
- 后端：`http://localhost:8000`
- **前端：`http://localhost:5173` ← 浏览器打开这个**

按 `Ctrl+C` 停止。

### 手动启动（可选）

```bash
# 后端
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 前端（另开终端）
cd frontend
npm install
npm run dev
```

---

## API 配置

### 第一步：复制配置模板

```bash
cp backend/.env.example backend/.env
```

### 第二步：编辑 `backend/.env`

```bash
# 选择 AI 提供商（支持：zhipuai | kimi | qwen | deepseek | minimax）
LLM_PROVIDER=qwen

# 填入对应的 API Key（只需填当前使用的提供商）
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# （可选）覆盖默认模型
# LLM_MODEL=qwen-plus
```

### 支持的 AI 提供商

| 提供商 | 环境变量 | 获取 Key 地址 | 推荐模型 |
|--------|---------|-------------|---------|
| 通义千问（阿里云）| `QWEN_API_KEY` | [dashscope.aliyun.com](https://dashscope.aliyun.com) | `qwen-plus` |
| 智谱 AI（GLM）| `ZHIPUAI_API_KEY` | [zhipuai.cn](https://open.zhipuai.cn) | `glm-4-plus` |
| Kimi / Moonshot | `KIMI_API_KEY` | [platform.moonshot.cn](https://platform.moonshot.cn) | `moonshot-v1-8k` |
| DeepSeek | `DEEPSEEK_API_KEY` | [platform.deepseek.com](https://platform.deepseek.com) | `deepseek-chat` |

### 高级配置（自定义 Base URL）

如果你使用的是代理地址、私有部署或其他兼容 OpenAI API 的服务，可以覆盖 Base URL：

```bash
# backend/.env
LLM_PROVIDER=qwen
QWEN_API_KEY=sk-xxxxxxxx
LLM_BASE_URL=https://your-proxy.example.com/v1
LLM_MODEL=your-model-name
```

系统使用 OpenAI Python SDK，任何兼容 OpenAI API 格式的服务商均可接入。

### 验证配置

启动后访问 `http://localhost:8000/models`，可查看当前可用模型列表，确认连接正常。

---

## 代码结构

```
digital-twin-bootstrap/
│
├── start.py                        # 一键启动脚本（跨平台）
├── start.sh                        # Shell 启动脚本
│
├── backend/                        # Python FastAPI 后端（端口 8000）
│   ├── .env.example                # 配置模板（复制为 .env 后填入 Key）
│   ├── requirements.txt            # Python 依赖
│   ├── main.py                     # FastAPI 入口，13 个 API 端点
│   ├── agent.py                    # Agent 核心循环（Block Protocol + 工具调用）
│   ├── config.py                   # 环境变量读取
│   ├── llm_client.py               # LLM 客户端（OpenAI SDK 兼容接口）
│   ├── sessions.py                 # 会话管理（内存 + profiles/ 落盘）
│   ├── tools.py                    # 工具实现（read_skill/read_doc/read_profile/write_profile）
│   ├── prompts.py                  # 系统提示词
│   ├── profile_parser.py           # Markdown 画像解析
│   ├── scientist_match.py          # 科学家匹配（几何 + LLM）
│   ├── scientists_db.py            # 30 位知名科学家数据库
│   └── pdf_export.py               # PDF 导出
│
├── frontend/                       # React 19 + TypeScript + Vite（端口 5173）
│   └── src/
│       ├── pages/                  # 4个页面（对话/画像/量表列表/量表测试）
│       ├── components/             # UI 组件（Block 渲染器/画像展示/聊天窗口）
│       ├── data/scales.ts          # 三套量表完整题库（前端内置）
│       └── utils/scoring.ts        # 量表计分逻辑（含反向计分）
│
├── skills/                         # Agent 可读取的技能文件（11 套）
│   ├── collect-basic-info/SKILL.md
│   ├── administer-ams/SKILL.md
│   ├── administer-rcss/SKILL.md
│   ├── administer-mini-ipip/SKILL.md
│   └── ...（共 11 套）
│
├── doc/                            # Agent 可读取的参考文档（量表原题等，7 份）
│
└── profiles/                       # 用户画像落盘目录（运行时自动创建，.gitignore 排除）
    └── _template.md                # 画像模板
```

### 关键 API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/chat` | Block 协议 SSE 对话（流式返回） |
| `GET` | `/profile/{session_id}` | 获取当前画像 |
| `GET` | `/models` | 获取可用模型列表 |
| `POST` | `/scales/submit` | 提交量表作答结果 |
| `GET` | `/profile/{session_id}/download` | Markdown 下载 |
| `GET` | `/profile/{session_id}/pdf` | PDF 导出 |
| `POST` | `/reset/{session_id}` | 重置会话 |

---

## 生态位置

本项目是「人—智能体混合数字世界」体系的**数字分身第一阶段（0→1 初始构建）**：

| 层级 | 项目 | 仓库 | 类型 | 状态 |
|------|------|------|------|:----:|
| 世界底座 | ① 公理体系 | [world-axiom-framework](https://github.com/TashanGKD/world-axiom-framework) | 开源 | 🟡 |
| 世界底座 | ② 体系结构 | [world-three-particle-impl](https://github.com/TashanGKD/world-three-particle-impl) | 开源 | 🟡 |
| 世界底座 | ③ 沙盘验证 | [world-sandbox-validation](https://github.com/TashanGKD/world-sandbox-validation) | 开源 | 🔲 |
| 数字分身 | **④ 0→1构建** ← 本仓库 | [digital-twin-bootstrap](https://github.com/TashanGKD/digital-twin-bootstrap) | 开源 | 🟡 |
| 数字分身 | ⑤ 1→100迭代 | [digital-twin-iteration](https://github.com/TashanGKD/digital-twin-iteration) | 开源 | 🔲 |
| 核心应用 | 数字世界应用 | TashanGKD/tashan-world | 私有 | 🔲 |
| 商业化 | 数字分身平台 | TashanGKD/tashan-twin-platform | 私有 | 🔲 |
| 公益 | 他山论坛 | [tashan-forum](https://github.com/TashanGKD/tashan-forum) | 开源公益 | 🔲 |

**直接依赖关系**：
- 本项目输出的 Profile（7维 Markdown + JSON）是 ⑤ 迭代系统的输入
- 本项目定义的 Agent State 结构对应 ② 体系结构中 Bᵢ 粒子的状态定义
- Profile Schema 变动需触发联动规则**场景L**（通知消费分身数据的上层应用）

---

## 贡献

欢迎贡献！详见 [CONTRIBUTING.md](CONTRIBUTING.md)（待建）。

**Skill 贡献**（无需改代码）：在 `skills/` 目录下添加新的 `技能名/SKILL.md` 即可扩展 Agent 能力。

---

## 更新日志

见 [CHANGELOG.md](CHANGELOG.md)（待建）。

---

## 许可证

MIT License. See [LICENSE](LICENSE) for details.
