<p align="center">
  <img src="docs/assets/tashan.svg" alt="他山 Logo" width="200" />
</p>

<p align="center">
  <strong>数字分身 0→1 初始构建系统</strong><br>
  <em>Digital Twin Bootstrap: Initial Construction (0→1)</em>
</p>

<p align="center">
  <a href="#项目简介">简介</a> •
  <a href="#核心内容">核心内容</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#生态位置">生态位置</a> •
  <a href="#贡献">贡献</a> •
  <a href="README.en.md">English</a>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![状态](https://img.shields.io/badge/状态-原型进行中-yellow)

> 🟡 **本仓库当前处于原型阶段**，从现有工作区剥离并规范化中。

---

## 项目简介

### 在大框架中的位置

「人—智能体混合数字世界」研究的第二大构造是**数字分身路径**——真人如何进入世界。本项目对应其**第一阶段：0→1**，即如何从极少的信息构造一个可工作的初始分身。

数字分身不是一次性快照，而是对真实个体的**持续逼近的动态表示**。0→1 阶段的关键不是追求一次性高保真，而是构造一个**结构明确、可更新、可被后续迭代接管的初始近似**，并为所有数据附加来源标记与置信度。

### 核心设计

**三条采集路径并行**，以降低测量成本并保留校准空间：

- **结构化对话**：通过 AI 引导的对话逐步提取多维画像
- **心理量表**：Mini-IPIP（大五人格）、AMS（学术动机）等提供可解释的测量基础
- **AI 推断**：对无法直接采集的维度进行推断，标注置信度，可被后续校准覆写

**七维画像**：身份 / 能力 / 当前需求 / 认知风格（RCSS）/ 学术动机（AMS）/ 人格（Mini-IPIP）/ 综合解读

**输出格式**：结构化 Profile（Markdown + JSON），供⑤迭代系统和上层应用使用。

### 目标读者

- AI 工程师：构建用户画像与个性化系统
- 产品开发者：设计用户接入数字世界的入口
- 研究者：研究人类数字孪生的初始构建方法

---

## 核心内容

- `采集系统/`：结构化对话引导流程
- `量表/`：Mini-IPIP、AMS 等标准量表施测逻辑
- `推断引擎/`：AI 推断模块（含置信度标注）
- `画像格式/`：Profile Schema 定义（JSON + Markdown）
- `当前工作区/`：原型系统（从 `profiles/` 目录迁移）

---

## 快速开始

> 📋 待正式版本发布后更新。原型阶段请参考工作区内的现有系统。

---

## 生态位置

| 层级 | 项目 | 仓库 | 类型 | 状态 |
|------|------|------|------|:----:|
| 世界底座 | ① 公理体系 | [world-axiom-framework](https://github.com/TashanGKD/world-axiom-framework) | 开源 | 🔲 |
| 世界底座 | ② 体系结构 | [world-three-particle-impl](https://github.com/TashanGKD/world-three-particle-impl) | 开源 | 🔲 |
| 世界底座 | ③ 沙盘验证 | [world-sandbox-validation](https://github.com/TashanGKD/world-sandbox-validation) | 开源 | 🔲 |
| 数字分身 | **④ 0→1构建** ← 本仓库 | [digital-twin-bootstrap](https://github.com/TashanGKD/digital-twin-bootstrap) | 开源 | 🟡 |
| 数字分身 | ⑤ 1→100迭代 | [digital-twin-iteration](https://github.com/TashanGKD/digital-twin-iteration) | 开源 | 🔲 |
| 核心应用 | 数字世界应用 | TashanGKD/tashan-world（私有） | 私有 | 🔲 |
| 商业化 | 数字分身平台 | TashanGKD/tashan-twin-platform（私有） | 私有 | 🔲 |
| 公益 | 他山论坛 | [tashan-forum](https://github.com/TashanGKD/tashan-forum) | 开源公益 | 🔲 |

**直接依赖关系**：
- 本仓库产出的 Profile 格式供 ⑤ 迭代系统消费
- 本仓库定义的 Agent State 结构必须符合 ① 公理中对 Bᵢ 粒子的定义（场景K）
- Profile Schema 变动会触发**场景L**（通知消费分身数据的上层应用适配）

---

## 贡献

欢迎贡献！详见 [CONTRIBUTING.md](CONTRIBUTING.md)（待建）。

---

## 更新日志

见 [CHANGELOG.md](CHANGELOG.md)（待建）。

---

## 许可证

MIT License. See [LICENSE](LICENSE) for details.
