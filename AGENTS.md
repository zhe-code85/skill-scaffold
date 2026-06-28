# Skill 脚手架协作指南

本文件为在本仓库中工作的 AI 编码代理提供协作约定。

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

PowerShell：

```powershell
New-Item -ItemType Directory -Force -Path .claude\skills, .codex\skills | Out-Null
New-Item -ItemType SymbolicLink -Path .claude\skills\skill-creator -Target ..\..\references\claude_skills\skills\skill-creator
New-Item -ItemType SymbolicLink -Path .codex\skills\skill-creator -Target ..\..\references\claude_skills\skills\skill-creator
```

Windows 无法创建 SymbolicLink 时，可使用 Junction，并在测试记录中说明。不要复制目录替代链接，除非用户明确要求。

如果目标路径已存在，不要覆盖；先检查它是否已经正确指向参考仓库。

## 跨平台命令

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

## Skill 编写与评估硬门禁

- 明确任务类型：判断用户是在创建或修改 skill、优化或评估现有 skill、调整评估流程，还是修改脚手架本身。
- 创建、修改、优化或评估 skill 时要使用 `skill-creator`。
- 本仓库覆盖 `skill-creator` 的默认 skill 落盘位置：新 skill 必须创建在项目根目录的 `skills/<skill-name>` 下。运行 `skill-creator` 的 `init_skill.py` 时，将输出目录显式设为本仓库的 `./skills`；
- 收到用户输入时，不要只理解用户字面意思，要分析用户真实意图，确认要沉淀的是可复用能力，不要把用户字面意思直接当成skill内容;
- 编辑skill前先问自己用户需求是否想清楚了，不清楚的要和用户澄清。
- 编辑skill时不要过度设计，50字能描述清楚事情不要用200字来描述，不要把skill写成说明文。
- 优化修复skill时不要补丁式修复，要做结构化修复。
- skill设计完成后，建立评估手段，确保：
   - skill能稳定触发
   - 门禁都能守住
   - skill流程运转正常
   - 端到端能完成
- 保持改动聚焦，不顺手重构无关文件。
- 使用中文开发skill，skill的Metadata Fields、子标题、专业技术名词保留英文原名。

---

## Anti-Patterns to Avoid

### 1. Windows-Style Paths
- ✅ Use: `scripts/helper.py`
- ❌ Avoid: `scripts\helper.py`

### 2. Too Many Options
```markdown
# Bad - confusing
"You can use pypdf, or pdfplumber, or PyMuPDF, or..."

# Good - provide a default with escape hatch
"Use pdfplumber for text extraction.
For scanned PDFs requiring OCR, use pdf2image with pytesseract instead."
```

### 3. Time-Sensitive Information
```markdown
# Bad - will become outdated
"If you're doing this before August 2025, use the old API."

# Good - use an "old patterns" section
## Current method
Use the v2 API endpoint.

## Old patterns (deprecated)
<details>
<summary>Legacy v1 API</summary>
...
</details>
```

### 4. Inconsistent Terminology
Choose one term and use it throughout:
- ✅ Always "API endpoint" (not mixing "URL", "route", "path")
- ✅ Always "field" (not mixing "box", "element", "control")

### 5. Vague Skill Names
- ✅ Good: `processing-pdfs`, `analyzing-spreadsheets`
- ❌ Avoid: `helper`, `utils`, `tools`
