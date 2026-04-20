# CLAUDE.md

This file provides repository-level guidance when working in this project.

## Project Focus

- This project is for designing, validating, and evolving an RTL phased skill system.
- The core concern is the system itself: phase boundaries, routing logic, artifact contracts, fallback paths, and re-entry rules.
- Deliverables should remain portable across Claude Code and Codex unless the user explicitly asks for a platform-specific result.
- Default to Chinese unless the user asks for another language.

## Current Repository Layout

- Use the `writing-skills` skill when creating, updating, validating, or evaluating skill definitions in this project.
- The current repository stores skill definitions under `skills/`, which is an independent git repository.
- For live testing, expose each child of `skills/` as its own entry under `.claude/skills/` and `.codex/skills/`.
- Before creating or repairing links, inspect existing entries first. If a link already works, leave it unchanged.
- Repair only what is missing or clearly broken. Do not replace `.claude/skills/` or `.codex/skills/` with a single symlink to `skills/`, and do not recreate every link at the start of each task.
- If manual linking is needed, keep `.claude/skills/` and `.codex/skills/` as directories and link each skill individually, or use `scripts/link-skills skills/`.

## Role Separation

| Location | Primary role | Should contain | Should not contain |
|----------|--------------|----------------|--------------------|
| `CLAUDE.md` | Repository-level policy for skill authoring | Stable methodology and repo-specific rules | Per-skill requirements or copied user intent |
| `SKILL.md` | Runtime instructions for the executing AI | Executable control flow for that skill | User wording, design rationale, or generic repo policy |
| User conversation | Source of intent and corrections | Requirements, feedback, approvals, missing context | Long-term reusable process rules |

## Skill Authoring Rules

- Optimize for the RTL phased skill system first. Local design choices should strengthen phase separation, routing clarity, and cross-skill consistency rather than only improving one isolated skill.
- Treat user requirements as input to transform, not text to transcribe. Do not copy phrases like "this skill should..." into `SKILL.md`.
- Write `SKILL.md` as an execution script for another AI: what to inspect, what to do, what to check, when to stop, and what to output.
- Keep control flow in `SKILL.md`; keep heavy reference material in `references/` and load it only when needed.
- Make the executing AI's role explicit: what it may decide on its own, what must be confirmed with the human, and what belongs to adjacent skills instead.
- Define boundaries and handoffs explicitly. State when the skill must pause, escalate, or route to another skill instead of improvising.
- Treat upstream artifacts such as specs, plans, and checklists as inputs to review critically, not instructions to follow blindly.
- Make completion concrete. The output should have an explicit path, format, and required content so the executing AI does not have to guess.

## Avoid Redundant Guidance

- Do not restate generic workflow that is already owned by shared skills such as `writing-skills`, `brainstorming`, or `writing-plans` unless this repository needs a deliberate local override.
- Keep this file focused on stable repository policy and repo-specific constraints; put reusable execution detail in the relevant skill instead.
- Do not make the project definition depend on the current `skills/` directory layout. Mention repository layout only when it affects the concrete work to be done.
