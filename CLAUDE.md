# CLAUDE.md

This file provides repository-level guidance when working in this project.

## Project Focus

- This project is a scaffold for developing, validating, and evolving an RTL phased skill system.
- Focus on phase boundaries, routing logic, artifact contracts, fallback paths, and re-entry rules.
- Deliverables should remain portable across Claude Code and Codex unless the user explicitly asks for a platform-specific result.
- Default to Chinese unless the user asks for another language.

## Current Repository Layout

- Use the `writing-skills` skill when creating, updating, validating, or evaluating skill definitions.
- `skills/` is the source repository for in-development skills and is maintained as an independent git repository.
- Root `.claude/` and `.codex/` are for the scaffold project's own agents, not for skill testing.
- Use `claude -p` for live skill evaluation.
- `workspace/` is the shared, general-purpose root for skill testing workspaces. Use it as the standard replacement for legacy skill-specific workspace directories such as `using-rtl-powers-workspace/`.
- Inside `workspace/`, keep shared Claude runtime assets under `workspace/.claude/`, and place each evaluation case directly under `workspace/` with a clear, stable case directory name.
- Do not expose `workspace/.claude/` to a case via a whole-directory `.claude` symlink. This setup has produced unstable `claude -p` behavior in local evaluation.
- Each `workspace/<case_name>/` must contain a real local `.claude/` directory.
- Inside each case-local `.claude/`, copy `settings.json` from `workspace/.claude/settings.json` unless the case needs an explicit override, and expose shared skills via a `skills -> ../../.claude/skills` symlink.
- Create `workspace/` if it does not already exist. The directory structure is:

```text
workspace/
    .claude/                    # Shared Claude runtime assets
        settings.json           # Shared settings template for case-local .claude directories
        skills/                 # Shared Claude Code skills directory
            skill_name1         # Symlink 1 to a skill from the `skills/` source repository
            skill_name2         # Symlink 2 to a skill from the `skills/` source repository
    case_name/                  # One isolated workspace per evaluation case
        .claude/                # Real case-local Claude configuration directory
            settings.json       # Case-local copy of workspace/.claude/settings.json
            skills -> ../../.claude/skills
```

- Before live skill testing, ensure the latest skills from the `skills/` source repository are symlinked into `workspace/.claude/skills/`.
- Manage case directories through naming rather than extra nesting. Prefer stable names such as `eval-1-ambiguous-entry`, `eval-2-module-first`, or `case-uart-subsystem-entry`.

## Role Separation

| Location | Primary role | Should contain | Should not contain |
|----------|--------------|----------------|--------------------|
| `CLAUDE.md` | Scaffold-agent guidance | Repository conventions, authoring policy, and testing environment rules | Per-skill runtime instructions or copied user intent |
| User conversation | Intent source | Requirements, corrections, approvals, and missing context | Reusable process rules |
| `skills/` | Skill source repository | In-development skill definitions | Scaffold-agent policy or test-only setup |
| `skills/<skill-name>/SKILL.md` | Runtime guide for the AI executing that skill | Control flow, boundaries, checks, outputs, and direct "you should..." instructions | Repository policy, rationale, or copied user wording |
| `workspace/` | Isolated `claude -p` test workspace | Shared runtime assets under `workspace/.claude/`, real case-local `.claude/` directories, and flat case directories directly under `workspace/` | Source-of-truth skill content or scaffold-agent configuration |

## Skill Authoring Rules

- Optimize for the RTL phased skill system first. Local design choices should strengthen phase separation, routing clarity, and cross-skill consistency rather than only improving one isolated skill.
- Treat user requirements as input to transform, not text to transcribe. Do not copy phrases like "this skill should..." into `SKILL.md`.
- Write `SKILL.md` as an execution script for another AI: what to inspect, what to do, what to check, when to stop, and what to output.
- In `SKILL.md`, second-person instructions such as "you should..." address the AI executing that skill, not the scaffold project user.
- Keep control flow in `SKILL.md`; keep heavy reference material in `references/` and load it only when needed.
- Do not overfit `SKILL.md` to one prompt or pressure scenario. Fix the abstract rule, boundary, go/no-go condition, or artifact contract instead.
- Make the executing AI's role, decisions, human-confirmation points, boundaries, and handoffs explicit.
- Treat upstream artifacts such as specs, plans, and checklists as inputs to review critically, not instructions to follow blindly.
- Make completion concrete. The output should have an explicit path, format, and required content so the executing AI does not have to guess.

## Skill Evaluation Rules

- For agent behavior validation, prefer `claude -p` pressure scenarios. Use this when the expected result depends on whether an agent correctly reads a skill, routes a task, refuses unsafe progression, handles fallback paths, or follows artifact contracts.
- Before running `claude -p`, confirm the Claude environment is free of unrelated skills or MCP integrations that could contaminate the result.
- Behavioral validation with `claude -p` should run in an isolated environment that loads only the in-development skills under test and the minimum required local configuration.
- Describe the intended testing workspace and setup rules directly in this file; do not infer the contract from the repository's current checked-in environment state.
- Do not depend on `scripts/link-skills` as part of the documented skill-testing environment setup.
- For mechanical structure validation, scripts, `rg`, and other deterministic checks are sufficient. Use these for frontmatter shape, file existence, link targets, path consistency, word counts, and other checks that do not depend on agent judgment.
- Treat a pressure scenario as the behavioral contract unless it is defective, contradictory, or built on an invalid fixture.
- After changing a skill for a failed pressure scenario, rerun the failing scenario and at least one adjacent non-failing scenario.

## Avoid Redundant Guidance

- Do not restate generic workflow that is already owned by shared skills such as `writing-skills`, `brainstorming`, or `writing-plans` unless this repository needs a deliberate local override.
- Keep this file focused on stable repository policy and repo-specific constraints; put reusable execution detail in the relevant skill instead.
