# CLAUDE.md

This file provides repository-level guidance when working in this project.

## Project Focus

- This project is a skill development scaffold for authoring, validating, and evolving runtime AI skills.
- Focus on skill boundaries, routing logic, artifact contracts, fallback paths, re-entry rules, and eval evidence.
- Deliverables should remain portable across Claude Code and Codex unless the user explicitly asks for a platform-specific result.
- Default to Chinese unless the user asks for another language.

## Repository Contract

- Use the `writing-skills` skill when creating, updating, validating, or evaluating skill definitions.
- `skills/` is the source repository for in-development runtime skills. A directory under `skills/` is a runtime skill only if it contains `SKILL.md`.
- `evals/` is the source repository for skill evaluation metadata, including pressure scenarios and the cross-suite evidence registry.
- `workspace/evals/<YYYYMMDD>/` is the standard root for new live eval runs and their evidence.
- Root `.claude/` and `.codex/` belong to scaffold agents, not skill evals.
- Historical evidence under `work/results/evals/<date>/` remains valid. Do not bulk-migrate legacy evidence unless the user explicitly asks.
- Do not place non-skill eval metadata under `skills/`, and do not maintain a manual runtime skill allowlist.

## Eval Workspace Contract

- Each eval case must run from an isolated case directory under the dated eval root.
- Each case must have a real local `.claude/` directory with an isolation `settings.json` and a generated `skills` symlink to the project `skills/` source tree.
- Case-local `settings.json` is required to reduce contamination from user-level plugins, MCP, project MCP, and ambient Claude configuration.
- Do not expose the scaffold root `.claude/` or a dated root `.claude/` to a case via whole-directory symlink.
- Keep case names stable and descriptive; do not create unnecessary nesting.
- The standard eval layout is:

```text
workspace/
    evals/
        YYYYMMDD/
            claude_settings.json        # Required isolation settings template for case-local .claude directories
            manifest.md                 # Daily eval execution table
            regression_summary.md       # Daily regression summary when applicable
            CASE_result_file.md         # One result-file per scenario when evidence is available
            case_name/                  # One isolated workspace per evaluation case
                .claude/                # Real case-local Claude configuration directory
                    settings.json       # Case-local isolation settings copied from claude_settings.json
                    skills -> <relative path to project skills/>
                docs/
                logs/
```

## Role Separation

| Location | Primary role | Should contain | Should not contain |
|----------|--------------|----------------|--------------------|
| `CLAUDE.md` | Scaffold-agent guidance | Repository conventions, authoring policy, and testing environment rules | Per-skill runtime instructions or copied user intent |
| User conversation | Intent source | Requirements, corrections, approvals, and missing context | Reusable process rules |
| `skills/` | Skill source repository | In-development skill definitions | Scaffold-agent policy, test-only setup, or eval metadata |
| `evals/` | Skill eval metadata | Pressure scenario definitions and cross-suite evidence registry | Runtime skill instructions or symlinks into `.claude/skills/` |
| `skills/<skill-name>/SKILL.md` | Runtime guide for the AI executing that skill | Control flow, boundaries, checks, outputs, and direct "you should..." instructions | Repository policy, rationale, or copied user wording |
| `workspace/evals/<YYYYMMDD>/` | Isolated eval run root | Case workspaces, isolation settings, result files, dated manifest, and regression summary | Source-of-truth skill content, scaffold-agent configuration, or unrelated development workspaces |

## Skill Folder Contract

- A skill is a self-contained folder rooted at `skills/<skill-name>/`.
- Every skill must contain `SKILL.md`.
- Optional bundled resources belong under `scripts/`, `references/`, and `assets/`.
- Use `scripts/` for deterministic or repeatedly rewritten logic, `references/` for load-as-needed documentation, and `assets/` for files consumed in outputs rather than context.
- Keep skill folders lean. Do not add auxiliary process documents such as `README.md`, installation guides, quick references, or changelogs unless the user explicitly asks for them.
- Use progressive disclosure: keep core workflow and decision logic in `SKILL.md`, move detailed reference material into `references/`, and avoid duplicating the same information in both places.
- Keep references shallow and discoverable. Reference files should be linked directly from `SKILL.md`; long reference files should include a table of contents.

## Skill Authoring Rules

- Optimize for the skill system as a whole. Local design choices should strengthen phase separation, routing clarity, and cross-skill consistency rather than only improving one isolated skill.
- Treat user requirements as input to transform, not text to transcribe.
- Write `SKILL.md` as an execution contract for another AI: what to inspect, what to decide, when to stop, and what to output.
- `SKILL.md` frontmatter must contain `name` and `description`. Treat `description` as the primary trigger surface.
- Write `description` in third person, start it with `Use when...`, and describe triggering conditions rather than workflow.
- Do not summarize the skill's step-by-step process in `description`; keep workflow detail in the body.
- Do not overfit `SKILL.md` to one prompt, run, or pressure scenario. Fix the abstract rule, boundary, go/no-go condition, or artifact contract.
- Make the executing AI's role, decisions, human-confirmation points, phase boundaries, and handoffs explicit.
- Treat upstream artifacts such as specs, plans, and checklists as inputs to review critically, not instructions to follow blindly.

## Skill Evaluation Rules

- Align skill evals with `superpowers:writing-skills` `RED -> GREEN -> REFACTOR`. `RED` is a failing baseline without the new or fixed skill behavior, `GREEN` is the same scenario passing after the skill change, and `REFACTOR` is closing newly exposed loopholes and rerunning.
- No new skill or skill edit is methodologically valid without a failing baseline first.
- Before changing a skill, document the agent's exact baseline behavior, explicit rationalizations, and triggering pressures in the scenario evidence. Fix the skill against those observed failures, not hypothetical ones.
- For agent behavior validation, prefer `claude -p` pressure scenarios. Use deterministic checks for mechanical structure validation.
- Run behavioral evals in an isolated case workspace that loads only the project skills and the minimum required local configuration. Case-local `settings.json` is part of this isolation boundary.
- For non-interactive `claude -p` automation that may create or edit files, use an explicit non-interactive permission policy. A run blocked by write approval is setup noise, not valid behavior evidence.
- Do not interpret empty default `stdout`/`stderr` as proof that nothing happened. Use verbose or structured output when runtime visibility is part of the evidence.
- Keep current working directory and runtime setup consistent when comparing interactive and non-interactive Claude runs.
- Treat a pressure scenario as the behavioral contract unless it is defective, contradictory, or built on an invalid fixture.
- After changing a skill for a failed pressure scenario, rerun the failing scenario and at least one adjacent non-failing scenario.
- When an eval is run, write a result-file under `workspace/evals/<YYYYMMDD>/` and update the dated `manifest.md` with scenario ID, suite, result file, status, workspace, and notes.
- Keep `evals/manifest.md` aligned with current evidence status. Use `result-file` for independent result files, `indirect-result` for evidence covered by another suite, `inline-evidence` for evidence recorded only in a scenario file, and `missing` when no traceable evidence exists.
- Record both pre-fix failures and post-fix reruns in the same result-file when a scenario drives a skill change; do not overwrite the failure history.
- Keep `regression_summary.md` for date-level rollups, not as the only evidence for a scenario.

## Avoid Redundant Guidance

- Do not restate generic workflow that is already owned by shared skills such as `writing-skills`, `brainstorming`, or `writing-plans` unless this repository needs a deliberate local override.
- Keep this file focused on stable repository policy and repo-specific constraints; put reusable execution detail in the relevant skill instead.
