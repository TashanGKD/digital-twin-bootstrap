# web/skills

本目录为项目根目录下 `.cursor/skills/` 的**独立副本**，供 web 后端使用，使 web 部分不直接依赖 `.cursor` 文件夹。

- **用途**：`backend/tools.py` 的 `read_skill()` 从这里读取 SKILL 内容。
- **同步**：若在 `.cursor/skills/` 中增删或修改了 Skill，请同步更新本目录（复制对应 `SKILL.md` 或整子目录），以保持 web 与 Cursor 行为一致。
