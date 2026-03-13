---
name: collect-basic-info
description: 采集科研数字分身的基础信息（研究阶段、学科领域、方法范式、技术能力、科研流程能力）。当用户开始建立科研数字分身、或基础信息尚未填写时使用。
---

# Phase 1：基础信息采集

## 重要交互规则

1. **每次严格只问一个问题**，等用户回答后再问下一个。
2. **优先使用 ask_choice**（选择题），只在必须自由输入时才用 ask_text。
3. **所有提问必须通过 UI 工具发出**（ask_choice / ask_text / ask_rating），不要用纯文本提问。
4. **问题数量和逻辑不得精简**，按下方流程完整执行每一步。

## 启动步骤

### 步骤一：询问是否使用 AI 记忆辅助建档

（仅在科研数字分身**新建**或基础信息**大量为空**时执行此步骤）

**不要先询问姓名或标识**。

调用 ask_choice：
- question: "在开始逐项填写之前，想问一下——你平时有没有使用过带记忆功能的 AI 工具？（比如 ChatGPT、Claude、Gemini 等，且已有一定时间的使用记录）\n\n如果有，我可以帮你生成一段提示词发给你的 AI，让它预填信息，节省不少时间。"
- options:
  - {id: "migrate", label: "有，我想先从 AI 记忆中提取信息", description: "可发给多个 AI，回复依次粘贴回来，我帮你整合"}
  - {id: "fresh", label: "没有，或者不需要，直接开始填写"}

- 选 **"从 AI 记忆"** → 调用 read_skill("generate-ai-memory-prompt")，**不询问姓名**；完成导入后回到此 Skill 补充剩余空白字段
- 选 **"直接填写"** → 继续步骤二

### 步骤二：收集角色名

（仅在用户选择了「直接开始填写」时执行；若用户选了 AI 记忆优先，姓名在 import-ai-memory 中采集）

调用 ask_text：
- question: "请为你的数字分身起一个名字（可以是真名、昵称或任何你喜欢的称呼）。"
- placeholder: "如：张三、Dr. DDL、量子猫... 随你喜欢"

收到后：
- 调用 read_profile 检查画像当前状态
- 若已存在同名画像 → 从断点续采（定位尚未填写的字段）
- 若不存在 → 基于模板创建新画像

### 步骤三：告知采集计划

用普通文字简要说明：「接下来分两批采集：**基础身份**和**能力自评**，共约 10 分钟。我会一个问题一个问题地问。」

## 第一批：基础身份（逐个提问，每次只问一个）

按顺序逐一提问：

**Q1** — 调用 ask_choice：
- question: "你目前处于哪个研究阶段？"
- options: [{id:"phd",label:"博士生"}, {id:"postdoc",label:"博士后"}, {id:"junior",label:"青年教师（助理教授/讲师）"}, {id:"pi",label:"独立PI"}, {id:"other",label:"其他"}]

**Q2** — 调用 ask_text：
- question: "你的主要研究领域是什么？"
- placeholder: "请说明一级学科（如认知科学、材料学）+ 具体方向（如计算神经科学）。如有交叉方向也请提及。"

**Q3** — 调用 ask_choice：
- question: "你主要采用哪种研究方法？（选最接近的一项）"
- options: [{id:"exp",label:"实验法"}, {id:"theory",label:"理论推导"}, {id:"compute",label:"计算建模"}, {id:"data",label:"数据驱动"}, {id:"qual",label:"质性研究"}, {id:"mixed",label:"混合方法"}]

**Q4** — 调用 ask_text：
- question: "你所在的机构是哪里？导师/所在团队的研究方向是？"
- placeholder: "不需要精确，大致描述即可。如：XX大学XX学院，导师做计算建模方向"

**Q5** — 调用 ask_choice：
- question: "你目前的学术合作圈大概是什么情况？"
- options: [{id:"internal",label:"主要在实验室内部合作"}, {id:"cross_inst",label:"有跨机构合作"}, {id:"cross_disc",label:"有跨学科合作"}, {id:"both",label:"跨机构 + 跨学科都有"}, {id:"solo",label:"主要独立工作"}]

## 第二批：能力自评

用普通文字说明：「接下来了解你的科研能力，请为以下各环节打分（1=非常薄弱，5=非常强）。」

依次对以下 6 个维度调用 ask_rating（**每次只问一个**）：

**维度1** — ask_rating:
- question: "问题定义能力（独立识别领域空白、提出有价值研究问题的能力）"
- min_val: 1, max_val: 5, min_label: "非常薄弱", max_label: "非常强"

评分后追问 — ask_choice:
- question: "关于问题定义，有没有你特别擅长或特别想提升的具体方面？"
- options: [{id:"has",label:"有，我来说明"}, {id:"skip",label:"跳过"}]
- 若选"有" → ask_text 收集

**维度2** — ask_rating:
- question: "文献整合能力（文献检索、综述撰写、跨领域文献联系）"
- （同上格式）

评分后同样追问是否有特别擅长或想提升的方面。

**维度3** — ask_rating:
- question: "方案设计能力（设计实验/计算方案、控制变量）"

**维度4** — ask_rating:
- question: "实验执行能力（实验/计算任务的执行规范性、时间管理）"

**维度5** — ask_rating:
- question: "论文写作能力（学术写作的流畅度、逻辑结构、英文表述）"

**维度6** — ask_rating:
- question: "项目管理能力（多任务管理、跨合作者协调、进度把控）"

每个维度评分后都追问「有没有特别擅长或想提升的方面」（可跳过）。

## 技术能力采集

调用 ask_text：
- question: "请列举你主要使用的编程语言和科研工具，并大致说明熟练程度。"
- placeholder: "如：Python（熟练）、MATLAB（入门）、fMRIPrep（日常使用）"

## 代表性产出（可选）

调用 ask_choice：
- question: "你是否有代表性的学术产出？（已发表论文、开源项目、工具包等）"
- options: [{id:"has",label:"有，我来简述"}, {id:"skip",label:"暂时跳过，之后补充"}]

若选"有" → 调用 ask_text：
- question: "请简述你的代表性学术产出。"
- placeholder: "如：一作论文发表于 Nature Communications，开源工具包 xxx（GitHub 星标 200+）"
- multiline: true

## 当前需求采集

用普通文字说明：「最后，我想了解一下你现在实际面对的情境——这将帮助科研数字分身系统给你更贴近现实的建议。」

**Q-需求1** — 调用 ask_text：
- question: "你现在每天/每周花费最多精力的事情是什么？可以列举 1–3 件，不限于科研，也包括杂事、沟通、行政等。"
- placeholder: "如：写毕业论文、带本科生实验、处理审稿意见"
- multiline: true

收到后追问 — ask_choice：
- question: "做这些事情时，你的整体感受是？"
- options: [{id:"fulfilled",label:"充实"}, {id:"tired",label:"疲惫"}, {id:"chaotic",label:"混乱"}, {id:"mixed",label:"混合（时而充实时而疲惫）"}, {id:"skip",label:"跳过"}]

**Q-需求2** — 调用 ask_text：
- question: "你目前遇到的最大卡点或困扰是什么？哪件事让你感觉「推不动」或者「不知道怎么办」？"
- placeholder: "如：实验数据不理想，不确定要不要换方向"

收到后追问 — ask_choice：
- question: "针对这个困难，你最希望获得哪方面的帮助？"
- options: [{id:"method",label:"方法和思路"}, {id:"resource",label:"资源和工具"}, {id:"emotional",label:"情绪支持和鼓励"}, {id:"all",label:"都需要"}, {id:"skip",label:"跳过"}]

**Q-需求3** — 调用 ask_text：
- question: "如果现在有一件事可以改变，让你接下来三个月更顺，你最想改变什么？"
- placeholder: "可以是一个技能、一个习惯、一段关系、一个系统，不必是宏大目标"

将三个问题的答案分别记录到画像的「三、当前需求」章节。

## 完成后操作

1. 将所有收集到的信息通过 write_profile 写入画像对应字段
2. 将 `采集阶段` 更新为 `basic_info_done`
3. 用普通文字简要告知：「基础信息已采集完毕，正在为你生成画像...」
4. **自动**调用 read_skill("infer-profile-dimensions")，直接进入推断环节，不需要用户额外操作
