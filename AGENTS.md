# Skill 脚手架协作指南

本文件为在本仓库中工作的 AI 编码代理提供协作约定。开始任务前先阅读本文件，并让后续操作与这里的项目目标、目录约定和验证要求保持一致。

## 项目定位

本仓库用于开发、校验和评估符合 [Agent Skills 规范](https://agentskills.io/specification) 的 skill。

开发 skill 时，不要把用户的原始请求直接写进 skill；你需要先理解用户想让 AI 智能体反复完成什么任务，再把它提炼成可复用、可验证、面向智能体执行的指导。

## 目录结构

- `skills/`：本仓库开发和维护的 skill。
- `references/`：外部参考资料，包含 Claude Skills 参考仓库。
- `.claude/`：Claude Code 项目级配置与 skill 链接。
- `.codex/`：Codex 项目级配置与 skill 链接。

## 开始前检查

确认 `.claude/skills/skill-creator` 和 `.codex/skills/skill-creator` 都存在，并指向 `references/claude_skills/skills/skill-creator`。

如果缺失，执行：

```bash
mkdir -p .claude/skills .codex/skills

ln -s ../../references/claude_skills/skills/skill-creator .claude/skills/skill-creator
ln -s ../../references/claude_skills/skills/skill-creator .codex/skills/skill-creator
```

如果目标路径已存在，不要覆盖；先检查它是否已经正确指向参考仓库。

## 工作流程

1. 明确任务类型：判断用户是在创建新 skill、优化现有 skill、调整评估流程，还是修改脚手架本身。
2. 涉及 skill 创建、修改、优化或评估时，使用 `skill-creator` skill，并优先参考其中的流程、目录和评估建议。
3. 修改 skill 前，先提炼意图：明确触发场景、目标用户、输入输出、成功标准、依赖工具和边界条件。
4. 编写或修改后进行阶段性验证。根据改动范围选择合适的检查方式，例如 Markdown 结构检查、链接检查、示例任务试跑、eval 数据校验或脚本测试。
5. 汇报结果时说明改了什么、如何验证、仍有哪些风险或待用户确认的问题。

## Skill 编写原则

- **面向 AI 智能体**
  skill 是给 AI 智能体使用的操作指南。使用第二人称“你”来写，直接告诉智能体在什么情况下做什么、为什么这样做、如何判断完成。

- **提炼用户需求**
  先分析用户真实意图，再写成可复用的 skill 指令。不要把某一次对话中的个人背景、临时文件名或一次性偏好硬编码进 skill，除非它们本身就是通用约束。

- **让触发条件清晰**
  `SKILL.md` 的 frontmatter 必须包含 `name` 和 `description`。`description` 应说明这个 skill 何时触发、解决什么问题，以及哪些相近场景也应该使用它。

- **保持渐进披露**
  `SKILL.md` 应聚焦核心流程。较长的说明、示例、模板、脚本和参考资料应放入 `references/`、`scripts/` 或 `assets/`，并在主文档中说明何时读取或使用。

- **写成可执行流程**
  优先使用清晰步骤、检查点和示例。能用脚本稳定完成的重复工作，尽量放入 `scripts/`，并在 skill 中说明调用方式。

- **重视验证**
  每个 skill 都应尽量具备可检查的成功标准。适合自动评估的任务应准备 eval 提示和断言；偏主观的任务也要提供人工评审的关注点。

## 协作注意事项

- 保持改动聚焦，不顺手重构无关文件。
- 工作区可能已有用户改动；不要回滚或覆盖未确认的变更。
- 新增说明时优先使用简洁中文，必要的技术名词保留英文原名。
- 修改完成后，检查文档是否存在错别字、断链、命令不可执行或前后矛盾。
