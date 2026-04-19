# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a scaffold project for developing, validating, and evaluating skills. Skills are created following Claude Code and Codex standards but must not be constrained to any single platform — they should be portable across both. 默认用中文回复.

## Workflow

- Use the **writing-skills** skill (`writing-skills`) to create, validate, and evaluate skills
- Skills are developed inside `skills/` which is its own independent git repository
- To test skills in Claude Code: expose each skill directory under `skills/` as its own entry inside `.claude/skills/`
- To test skills in Codex: expose each skill directory under `skills/` as its own entry inside `.codex/skills/`
- **Check before linking**: whenever the `skills/` directory is detected to exist, first inspect whether `.claude/skills/` and `.codex/skills/` already contain working per-skill links into `skills/`. If an entry is already working, leave it unchanged.
- **Repair only when needed**: if `.claude/skills/` or `.codex/skills/` is missing, create the directory. If specific skill links are missing or clearly broken, create or repair only those links. Do not replace `.claude/skills/` or `.codex/skills/` with a single symlink to `skills/`, and do not blindly recreate links at the start of every task.
- When manual linking is needed, keep `.claude/skills/` and `.codex/skills/` as directories and link each child of `skills/` individually (for example, `.claude/skills/<skill-name> → ../../skills/<skill-name>`), or use `scripts/link-skills skills/`

## Directory Layout

- `skills/` — skill repository (separate git repo, gitignored here); contains all skill definitions
- `.claude/` — Claude Code project-level config; `.claude/skills/` should contain per-skill links for live testing
- `.codex/` — Codex project-level config; `.codex/skills/` should contain per-skill links for live testing

## Skill Authoring Principles

This section defines how to turn user requirements into well-structured skills. These are meta-rules for the AI, not content to be copied into skills.

### File roles and operational roles

| File | Reader | What to write | What NOT to write |
|------|--------|---------------|-------------------|
| `CLAUDE.md` | AI that builds skills | Skill authoring methodology | Specific skill content or requirements |
| `SKILL.md` | AI that executes the skill | Execution instructions | User's original requirements, design intent, or justification |
| User conversation | You and the user | Requirements and feedback | — |

When writing a skill, keep both levels of role separation clear:

- **File-level role separation.** `CLAUDE.md` defines how to author skills; `SKILL.md` instructs another AI how to execute a skill; user conversation carries requirements and feedback.
- **Operational role separation inside `SKILL.md`.** A strong skill must also tell the executing AI what it is responsible for, what the human is responsible for, and when work must be handed to another skill or paused for clarification.
- **Write for the executing AI, not for the end user.** `SKILL.md` should read like instructions to another AI agent that is currently doing the work, not like documentation or sales copy for a human reader.
- **Make the AI's role explicit.** State whether the executing AI is expected to review, critique, implement, verify, coordinate, or only route. Do not leave its posture implicit.
- **Separate roles cleanly.** Distinguish among: the human partner (provides intent, missing context, approvals, corrections), the executing AI (performs the current stage's work), and adjacent skills (own upstream or downstream stages). Avoid skills that silently absorb responsibilities belonging to other roles.
- **Define boundaries and handoffs.** Say what this skill should not do, when it must stop, when it should ask the human, and when it should hand work to another skill instead of improvising across stage boundaries.
- **Treat upstream artifacts as inputs to be examined, not obeyed blindly.** If a skill consumes a plan, spec, checklist, or prior document, instruct the AI to load it, review it critically, and surface problems before execution continues.
- **Encode pause conditions explicitly.** Ambiguity, missing dependencies, contradictory instructions, failed validation, and broken upstream assumptions should have explicit stop-and-escalate behavior in the skill body.
- **Encode re-entry conditions explicitly.** If the human updates an input artifact or resolves a blocker, say which earlier step the AI should return to rather than letting it continue from stale assumptions.

### Core rules

1. **Digest requirements, don't transcribe them.** User requirements are input to the skill creation process. Transform them into executable instructions for the AI. Never copy user statements like "this skill should do X" or "I want Y" directly into SKILL.md.

2. **SKILL.md is an execution script, not a spec.** Structure it as control flow — "when condition X is detected, do Y, then check Z, output in format W." Avoid sentences that describe intent ("this skill exists to help users..."). Instead, write what the AI should actually do step by step.

3. **Control flow first, knowledge as support.** The primary structure of SKILL.md should be imperative steps and conditional branches. Knowledge blocks (coding standards, templates, domain rules) serve as supporting material — embed small ones inline, put large ones in `references/` and load on demand.

4. **Handle failure paths.** Every branch should cover: what to do when preconditions aren't met, when tools are unavailable, when upstream artifacts are missing. Don't only describe the happy path.

5. **Output must be explicit.** Always specify what the final deliverable looks like: file path, format, required sections, naming conventions. The executing AI should never have to guess what to produce.

### Responsibility checklist for skill authors

Before finalizing a `SKILL.md`, ensure it answers these questions directly:

- Who is executing this skill?
- What is that AI allowed and expected to decide on its own?
- What must be confirmed with the human instead of guessed?
- What belongs to upstream or downstream skills rather than this one?
- What artifacts must be reviewed before action starts?
- Under what conditions must execution stop and ask for help?
- What concrete output marks this skill as complete?
