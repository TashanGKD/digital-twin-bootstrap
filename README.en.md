<p align="center">
  <img src="docs/assets/tashan.svg" alt="Tashan Logo" width="200" />
</p>

<p align="center">
  <strong>Digital Twin Bootstrap: Initial Construction (0→1)</strong><br>
  <em>数字分身 0→1 初始构建系统</em>
</p>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#core-design">Design</a> •
  <a href="#ecosystem">Ecosystem</a> •
  <a href="#contributing">Contributing</a> •
  <a href="README.md">中文</a>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Status](https://img.shields.io/badge/status-prototype-yellow)

> 🟡 **Prototype in progress.** Being extracted from the working workspace into a standalone repository.

---

## Overview

The first phase of the **digital twin pathway**: constructing a viable initial twin from sparse, partial information (0→1).

The goal is not immediate high fidelity, but to produce a structured, updateable initial approximation with explicit provenance, confidence levels, and calibratability. Three acquisition paths run in parallel to balance cost and accuracy:

- **Structured dialogue** — AI-guided conversation to extract multidimensional profiles
- **Psychometric instruments** — Mini-IPIP (Big Five), AMS (Academic Motivation Scale) provide interpretable measurement backbone
- **AI inference** — Inferred dimensions are labeled with confidence and remain overwritable

**Output**: A structured Profile (Markdown + JSON) consumed by the ⑤ iteration system and upstream applications.

---

## Core Design

**Seven profile dimensions**: Identity / Capability / Current Needs / Cognitive Style (RCSS) / Academic Motivation (AMS) / Personality (Mini-IPIP) / Integrated Interpretation

---

## Ecosystem

| Layer | Project | Repository | Type | Status |
|-------|---------|-----------|------|:------:|
| World Substrate | ① Axiom Framework | [world-axiom-framework](https://github.com/TashanGKD/world-axiom-framework) | Open Source | 🔲 |
| World Substrate | ② Architecture | [world-three-particle-impl](https://github.com/TashanGKD/world-three-particle-impl) | Open Source | 🔲 |
| World Substrate | ③ Sandbox Validation | [world-sandbox-validation](https://github.com/TashanGKD/world-sandbox-validation) | Open Source | 🔲 |
| Digital Twin | **④ Bootstrap (0→1)** ← this repo | [digital-twin-bootstrap](https://github.com/TashanGKD/digital-twin-bootstrap) | Open Source | 🟡 |
| Digital Twin | ⑤ Iteration (1→100) | [digital-twin-iteration](https://github.com/TashanGKD/digital-twin-iteration) | Open Source | 🔲 |
| Core App | Digital World | TashanGKD/tashan-world (private) | Private | 🔲 |
| Commercial | Twin Platform | TashanGKD/tashan-twin-platform (private) | Private | 🔲 |
| Public Interest | Tashan Forum | [tashan-forum](https://github.com/TashanGKD/tashan-forum) | Open Source | 🔲 |

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon).

---

## License

MIT License. See [LICENSE](LICENSE) for details.
