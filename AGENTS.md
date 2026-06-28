# Skill 脚手架协作指南

本仓库用于开发、校验和评估符合 Agent Skills 规范的 skill。你是协助用户开发 skill 的 AI 编程代理。

## 1. 项目边界

- `skills/`：本仓库维护的 skill。
- `references/`：外部参考资料区，禁止读取内容。
- `.claude/`：Claude Code 项目配置与 skill 链接。
- `.codex/`：Codex 项目配置与 skill 链接。
- `tmp/skill-tests/`：CLI 实测目录，不提交版本库。

根目录 `references/` 只允许做路径和链接检查，不允许搜索、打开、摘录或依赖其内容。
`skills/<skill-name>/references/` 属于单个 skill 的资源目录，可按该 skill 指南读取。

## 2. 基本规则

1. 使用中文开发 skill，必要技术名词保留英文。
2. 只沉淀可复用能力，不写一次性对话背景。
3. skill 面向 AI agent，正文使用第二人称“你”。
4. 保持改动聚焦，不顺手重构无关文件。
5. 简洁优先，避免过度设计。
6. 新建、修改、评估 skill 时优先遵循 `skill-creator`。
7. skill 格式、frontmatter、资源目录和正文组织以 `skill-creator` 为准。
8. 本文件与 `skill-creator` 冲突时，以本文件为准。
9. 用户需求输入时，首先要停下来思考如何转成流程机制，而不是直接写到skill里。
10. 非必须不要探索项目内全文件

## 3. 启动检查

开始工作前检查：

```text
.claude/skills/skill-creator
.codex/skills/skill-creator
```

二者应指向：

```text
references/claude_skills/skills/skill-creator
```

只检查链接是否存在和目标是否正确，不读取 `references/` 内容。
目标已存在时不要覆盖；先确认是否为正确链接。

POSIX：

```bash
mkdir -p .claude/skills .codex/skills
ln -s ../../references/claude_skills/skills/skill-creator .claude/skills/skill-creator
ln -s ../../references/claude_skills/skills/skill-creator .codex/skills/skill-creator
```

PowerShell：

```powershell
New-Item -ItemType Directory -Force -Path .claude\skills, .codex\skills | Out-Null
New-Item -ItemType SymbolicLink -Path .claude\skills\skill-creator -Target ..\..\references\claude_skills\skills\skill-creator
New-Item -ItemType SymbolicLink -Path .codex\skills\skill-creator -Target ..\..\references\claude_skills\skills\skill-creator
```

Windows 无法创建 SymbolicLink 时，可使用 Junction，并在测试记录中说明。不要复制目录替代链接，除非用户明确要求。

## 4. 跨平台命令

执行命令前先判断平台和 shell。

- POSIX：使用 `sh` / `bash` 兼容命令。
- Windows：优先使用 PowerShell。
- 文档路径可用 `/`；实际命令按平台转义。
- 不要在 Windows 假设 `mkdir -p`、`ln -s`、`command -v`、`rm -rf` 可用。

检测 Claude Code CLI：

```bash
command -v claude
```

```powershell
Get-Command claude -ErrorAction SilentlyContinue
```

## 5. 工作流程

### Step 1: 判断任务类型

先判断用户是在：

1. 创建新 skill。
2. 修改或优化已有 skill。
3. 评估 skill。
4. 调整测试流程。
5. 修改脚手架项目。

需求不清楚时先澄清；需求明确时直接按最终目标推进，不要拆成不必要的阶段方案。

### Step 2: 判断是否应写入 skill

写入前检查：

- 是否对未来同类任务仍成立？
- 是否能指导 agent 做什么、何时做、如何判断完成？
- 是否避免了临时路径、临时背景和当前对话细节？
- 是否比原表达更简洁、歧义更少？

不满足则不要写入，或改写成通用规则。

### Step 3: 创建或修改 skill

新 skill 必须创建在：

```text
skills/<skill-name>/
```

禁止创建到：

```text
$CODEX_HOME/skills
~/.codex/skills
任何全局 skill 目录
```

如果运行 `skill-creator` 的 `init_skill.py`，必须显式指定输出目录为：

```text
./skills
```

修改已有 skill 时做结构化修复，优先调整流程、判断标准和资源路由，不做零散补丁式堆叠。

### Step 4: 应用本仓库补充约束

`skill-creator` 已覆盖通用格式和质量要求；本仓库只补充以下约束：

- 不创建到全局 skill 目录。
- 不复制 skill 目录替代链接。
- 不覆盖测试证据。
- 不汇报未实际执行的验证结果。

## 6. Forward-Testing

需要 subagent forward-testing 时，遵循 `skill-creator` 流程。

要求：

- 不把当前 agent 的诊断、预期答案或修复思路传给测试 agent。
- 测试 prompt 应模拟真实用户任务。
- 测试结果应能判断 skill 是否正确触发、执行和产出。
- 无法执行时记录为 `not run`，并说明原因。

## 7. Claude Code CLI 实测

CLI 实测只针对 Claude Code。

完成 skill 修改后，验证：

1. 平台发现。
2. 显式调用。
3. 隐式触发。
4. 真实 CLI 入口。

如果 `claude -p` 不支持、CLI 不存在、未授权或受权限限制，对应 case 记为 `not run`。

## 8. 测试目录规范

所有 CLI 实测必须放在：

```text
./tmp/skill-tests/
```

禁止使用系统临时目录、用户主目录、全局 skill 目录或仓库外目录。

每轮测试目录：

```text
./tmp/skill-tests/<YYYYMMDD-HHMMSS>-<skill-name>/
```

case 子目录：

```text
claude-explicit/
claude-implicit/
```

不要复用已有 case 目录；目录存在时换新时间戳，不覆盖旧证据。

## 9. 测试注册方式

每个 case 目录只注册本次待测 skill：

```text
.claude/skills/<skill-name> -> skills/<skill-name>
```

创建链接前检查：

1. 目标 skill 是否存在。
2. 链接路径是否已存在。
3. 已存在路径是否为本次需要的正确链接。

链接策略：

- POSIX：symlink。
- Windows：SymbolicLink；失败时可用 Junction，并记录。
- 不复制 skill 目录，除非用户明确要求。

## 10. 测试 Case

### 显式调用

prompt 可以点名 skill：

```text
Use $<skill-name> ...
```

用于验证平台能加载并执行该 skill。

### 隐式触发

prompt 不得点名 skill，也不得说“使用这个 skill”。
只给真实用户式任务，用于验证平台能否根据 `description` 主动选择 skill。

## 11. 测试证据

每个 case 至少保存：

```text
prompt.txt
command.txt
stdout.txt
stderr.txt
result.md
```

产物保存到 case 目录或：

```text
artifacts/
```

`result.md` 必须记录：

- 测试平台
- 测试类型
- 测试目录
- skill 注册方式
- prompt
- 执行命令
- 关键输出
- 失败信息
- 产物路径
- 结论：`passed`、`failed` 或 `not run`

多 case 汇总写入：

```text
summary.md
```

## 12. 汇报要求

完成后说明：

1. 改了什么。
2. 为什么这样改。
3. 如何验证。
4. 哪些 Claude Code case 通过。
5. 哪些 case 未运行及原因。
6. 剩余风险或待确认问题。

不要声称执行过未实际执行的测试。
不要在汇报前删除本轮测试证据。

## 13. 禁止事项

禁止：

1. 把新 skill 创建到全局目录。
2. 在 Windows 假设 POSIX 命令可用。
3. 复制 skill 目录替代链接。
4. 覆盖已有测试证据。
5. 把当前 agent 的诊断传给 forward-testing agent。
6. 把一次性需求写进 skill。
7. 汇报未执行过的验证结果。
