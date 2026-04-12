# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a scaffold project for developing, validating, and evaluating skills. Skills are created following Claude Code and Codex standards but must not be constrained to any single platform — they should be portable across both.

## Workflow

- Use the **Skill-Creator** skill (`superpowers:writing-skills` or `skill-creator:skill-creator`) to create, validate, and evaluate skills
- Skills are developed inside `skills/` which is its own independent git repository
- To test skills in Claude Code: symlink `skills/` into `.claude/skills/`
- To test skills in Codex: symlink `skills/` into `.codex/skills/`
- **Auto-symlink**: whenever the `skills/` directory is detected to exist, automatically create symlinks `.claude/skills → ../skills` and `.codex/skills → ../skills` if they don't already exist. Do this before any skill development or testing work

## Directory Layout

- `skills/` — skill repository (separate git repo, gitignored here); contains all skill definitions
- `.claude/` — Claude Code project-level config; symlink skills here for live testing
- `.codex/` — Codex project-level config; symlink skills here for live testing
