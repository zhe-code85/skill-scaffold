# Skill 脚手架协作指南

本文件为在本仓库中工作的 AI 编码代理提供协作约定。你是协助用户开发skill的AI 编程助手。

## 项目定位

本仓库用于开发、校验和评估符合 [Agent Skills 规范](https://agentskills.io/specification) 的 skill。

## 目录结构

- `skills/`：本仓库开发和维护的 skill。
- `references/`：外部参考资料，包含 Claude Skills 参考仓库。
- `.claude/`：Claude Code 项目级配置与 skill 链接。
- `.codex/`：Codex 项目级配置与 skill 链接。
- `tmp/skill-tests/`：仓库内 CLI 实测运行目录，用于隔离注册待测 skill、保存测试输入输出和产物；该目录属于临时验证区，不提交到版本库。

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

1. 明确任务类型：判断用户是在创建或修改 skill、优化或评估现有 skill、调整评估流程，还是修改脚手架本身。
2. 创建、修改、优化或评估 skill 时要使用 `skill-creator`，并优先遵循其中已经定义的创建、编辑、静态校验和 subagent forward-testing 流程；如果 `skill-creator` 的默认建议与本文件冲突，以本文件为准。
3. 本仓库覆盖 `skill-creator` 的默认 skill 落盘位置：新 skill 必须创建在项目根目录的 `skills/<skill-name>` 下。运行 `skill-creator` 的 `init_skill.py` 时，将输出目录显式设为本仓库的 `./skills`；不要采用 `skill-creator` 默认的 `$CODEX_HOME/skills`、`~/.codex/skills` 或任何全局技能目录。
4. 编写或修改 skill 前，先分析用户真实意图，确认要沉淀的是可复用能力，而不是某一次对话中的一次性需求；需求不清楚时先向用户澄清。
5. 需要执行 subagent forward-testing 时，按 `skill-creator` 的 forward-testing 流程执行；不得把当前 agent 的诊断、预期答案或修复思路传给测试 agent。
6. 完成 skill 修改后，按本仓库的 CLI 实测流程验证 Codex 或 Claude Code 的平台发现、隐式触发或真实 CLI 入口；如果当前系统不支持对应 CLI、命令不可用、未授权或受权限限制，就跳过该平台或 case，并标记为 `not run`，说明未测试原因。
7. CLI 实测必须区分目标平台，并按“CLI 测试目录管理”在仓库内隔离测试目录中枚举待测 skill，避免污染全局技能目录：
   - 测 Codex 平台时，在测试目录创建 `.codex/skills/<skill-name>`，并让它指向仓库内 `skills/<skill-name>`；如果系统支持 `codex exec`，就从该测试目录运行；否则跳过并记录 Codex CLI 未测试。
   - 测 Claude Code 平台时，在测试目录创建 `.claude/skills/<skill-name>`，并让它指向仓库内 `skills/<skill-name>`；如果系统支持 `claude -p`，就从该测试目录运行；否则跳过并记录 Claude Code CLI 未测试。
   - 使用 symlink 时，先检查目标路径和已有链接，避免覆盖无关文件。
8. CLI 实测至少区分两类 case：
   - 显式调用测试：prompt 可以写 `Use $<skill-name> ...`，用于验证目标平台能加载并执行该 skill。
   - 隐式触发测试：prompt 不得点名 skill，也不得说“使用这个 skill”，只给真实用户式任务，用于验证目标平台是否会根据 frontmatter `description` 主动选择该 skill。
9. 每次 CLI 实测都应记录可复查证据：测试平台、测试类型、测试目录、skill 注册方式、输入 prompt、关键输出、产物路径、执行命令、失败信息，以及结论 `passed`、`failed` 或 `not run`；`not run` 必须说明原因。
10. 汇报结果时说明改了什么、如何验证、哪些平台和 case 已通过、哪些未运行，以及仍有哪些风险或待用户确认的问题。

## CLI 测试目录管理

- 所有 Codex 和 Claude Code CLI 实测都必须在仓库根目录下的 `./tmp/skill-tests/` 中进行；不要使用系统 `/tmp`、用户主目录、全局 skill 目录或仓库外的任意目录作为测试工作区。
- 每轮测试创建独立运行目录，命名为 `./tmp/skill-tests/<YYYYMMDD-HHMMSS>-<skill-name>/`。同一轮内按平台和 case 创建子目录，例如 `codex-explicit/`、`codex-implicit/`、`claude-explicit/`、`claude-implicit/`；从对应 case 子目录执行 CLI 命令。
- 不要复用已有 case 子目录。若目标运行目录或 case 子目录已存在，先换用新的时间戳目录；不要覆盖其中的 prompt、输出、产物或 symlink。
- 在每个 case 子目录内只注册本次要测的 skill：Codex case 创建 `.codex/skills/<skill-name>`，Claude Code case 创建 `.claude/skills/<skill-name>`，并让它指向仓库内 `skills/<skill-name>`。创建 symlink 前必须检查目标路径和已有路径；若已有路径不是本次需要的正确链接，停止并换用新的 case 子目录。
- 每个 case 子目录至少保存 `prompt.txt`、`command.txt`、`stdout.txt`、`stderr.txt` 和 `result.md`；如测试产生文件，将产物保存在该 case 子目录或其 `artifacts/` 下，并在 `result.md` 中记录相对路径。
- `result.md` 应记录平台、测试类型、测试目录、skill 注册方式、输入 prompt、执行命令、关键输出、失败信息、产物路径和结论 `passed`、`failed` 或 `not run`。多个 case 的汇总可以写入运行目录根部的 `summary.md`。
- `tmp/skill-tests/` 是可清理的本地测试区，但不要在汇报前删除本轮测试证据。清理旧目录时，只删除符合本规范命名且确认不再需要复查的运行目录。

## 协作注意事项

- 编写前先问自己用户需求是否想清楚了，不清楚的和用户澄清。
- 编写时简洁优先，不要过度设计，要化繁为简。
- 写入任何规则前，先做抽象化检查：
  1. 这条内容是否对未来同类任务仍然成立？
  2. 它是否直接告诉 agent 应该做什么、何时做、如何判断完成？
  3. 是否包含“用户要求/刚才讨论/某工具没定义/我认为”等一次性背景？
- 保持改动聚焦，不顺手重构无关文件。
- 你编写的 skill 是给 AI 智能体使用的操作指南。使用第二人称“你”来写，直接告诉智能体在什么情况下做什么、为什么这样做、如何判断完成。
- 你需要先分析用户真实意图，再写成可复用的 skill 指令。不要把某一次对话中的用户需求硬编码进 skill，除非它们本身就是通用约束，skill 不要写成说明文。
- 优化修复skill时不要补丁式修复，要做结构化修复。
- 你应让每个 skill 尽量具备可检查的成功标准。适合自动评估的任务应准备 eval 提示和断言；偏主观的任务也要提供人工评审的关注点。
- 使用中文开发skill，必要的技术名词保留英文原名。
