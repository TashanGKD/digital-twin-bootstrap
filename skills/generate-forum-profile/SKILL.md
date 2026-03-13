---
name: generate-forum-profile
description: 将科研数字分身各维度整合提取为他山论坛分身，格式为 Identity / Expertise / Thinking Style / Discussion Style 四节 Markdown，输出前先让用户确认隐私暴露范围。当用户说「生成他山论坛分身」「论坛画像」「数字分身」「导出论坛档案」时使用。
---

# 生成他山论坛分身

## 重要交互规则

1. **每次严格只问一个问题**，优先 ask_choice。
2. **隐私确认步骤不得跳过**，不得默认暴露任何维度。
3. **维度映射规则不得精简**。

## 步骤一：读取科研数字分身

1. 调用 read_profile 获取完整画像
2. 若画像为空或基础信息未填写 → 用普通文字提示：「尚未找到你的科研数字分身。请先完成基础信息采集。」并调用 show_actions: buttons: [{id:"build",label:"开始构建分身",href:"/"}]
3. 若存在 → 进入步骤二

## 步骤二：隐私范围确认

**不得跳过此步骤，不得默认暴露任何维度。** 逐项用 ask_choice 确认（每次一项）：

**隐私Q1** — ask_choice：
- question: "论坛分身中，基础身份（研究阶段、学科领域、机构）的机构信息如何处理？"
- options:
  - {id: "full", label: "保留原样（含机构名称）"}
  - {id: "vague", label: "仅保留大类（如「国内高校」）"}
  - {id: "none", label: "完全省略机构信息"}

**隐私Q2** — ask_choice：
- question: "专长与能力中，是否包含具体工具名称（如 galpy、CMC-COSMIC）？"
- options:
  - {id: "full", label: "全部保留具体名称"}
  - {id: "category", label: "仅保留类别（如「天文动力学软件」）"}

**隐私Q3** — ask_choice：
- question: "是否包含认知风格（横向整合 vs 垂直深度偏好）描述？"
- options: [{id: "yes", label: "包含"}, {id: "no", label: "不包含"}]

**隐私Q4** — ask_choice：
- question: "是否包含学术动机结构描述？（不含原始分数，只有特征描述）"
- options: [{id: "yes", label: "包含"}, {id: "no", label: "不包含"}]

**隐私Q5** — ask_choice：
- question: "是否包含人格特征描述？（不含原始分数，只有特征描述）"
- options: [{id: "yes", label: "包含"}, {id: "no", label: "不包含"}]

**隐私Q6** — ask_choice：
- question: "是否包含当前需求与卡点？（此项高度敏感）"
- options: [{id: "yes", label: "包含"}, {id: "no", label: "不包含（推荐）"}]

记录用户对每项的选择。

## 步骤三：按隐私设置提取并生成论坛分身

根据用户确认结果，从画像各维度中提取内容，映射到四节格式。**所有内容用行为描述句式，不直接引用量表分数。**

### 维度映射规则

**Identity**（1 段，3-5 句，第三人称）：
- 来源：基础身份（研究阶段 + 一级/二级领域 + 交叉方向 + 方法范式）
- 机构：按隐私设置处理
  - full：包含机构名称、导师方向
  - vague：如「国内天文研究机构」
  - none：不提及机构
- 撰写为身份定位描述

**Expertise**（6-10 条 bullet）：
- 来源：技术能力表格 + 科研流程能力（4 分及以上的环节重点体现）
- 工具：按隐私设置
  - full：列出具体工具名
  - category：仅保留类别
- 代表性产出若有，可简要纳入

**Thinking Style**（5-7 条 bullet）：
- 若用户同意包含认知风格：从 RCSS 的 CSI 及类型提炼思维方式
- 若用户同意包含动机：从 AMS 的动机结构提炼（如「以知识好奇心为驱动」）
- 若用户同意包含人格：从开放性、尽责性等提炼
- 若某维度不包含：从其他已授权维度补充，或从综合解读中提取行为模式，**不留空节**

**Discussion Style**（5-7 条 bullet）：
- 综合认知风格 + 人格（外向性/宜人性）+ 综合解读中的行为模式
- 若用户不同意包含人格/动机：仅从认知风格和综合解读提炼
- 描述为讨论中的行为倾向（如「倾向于将问题置于跨领域框架下分析」）

### 输出格式模板

```markdown
# [用户名]

## Identity
[1 段身份定位描述，3-5 句]

## Expertise
- [专长 1]
- [专长 2]
- ...

## Thinking Style
- [思维方式 1]
- [思维方式 2]
- ...

## Discussion Style
- [讨论倾向 1]
- [讨论倾向 2]
- ...
```

## 步骤四：输出与预览

1. 用普通文字展示生成的论坛分身完整 Markdown
2. 调用 ask_choice：
- question: "以上是为你生成的他山论坛分身预览。请确认："
- options:
  - {id: "save", label: "满意，保存"}
  - {id: "modify", label: "需要修改某节（请说明）"}

若选「修改」→ 调用 ask_text 收集修改意见，修改后重新展示预览。

## 步骤五：存档与审核记录

用户确认满意后：

1. 调用 write_forum_profile 保存完整 Markdown
2. 在科研数字分身的审核记录中追加一条导出记录（日期 + 「生成论坛分身」 + 隐私设置摘要）
3. 调用 write_profile 更新审核记录
4. 调用 show_actions：
- message: "他山论坛分身已保存！可直接用于他山论坛的数字分身配置。"
- buttons:
  - {id: "view", label: "查看完整画像", href: "/profile", style: "primary"}
  - {id: "download", label: "下载论坛分身"}
