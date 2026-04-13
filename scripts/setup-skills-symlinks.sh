#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$ROOT_DIR/skills"

if [ ! -d "$SKILLS_DIR" ]; then
  echo "Error: skills/ directory not found at $SKILLS_DIR"
  exit 1
fi

# Create target directories
mkdir -p "$ROOT_DIR/.claude/skills" "$ROOT_DIR/.codex/skills"

# Symlink each skill folder into .claude/skills/ and .codex/skills/
for skill_dir in "$SKILLS_DIR"/*/; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"

  for target in "$ROOT_DIR/.claude/skills" "$ROOT_DIR/.codex/skills"; do
    link="$target/$skill_name"
    if [ -L "$link" ]; then
      rm "$link"
    elif [ -e "$link" ]; then
      echo "Warning: $link exists and is not a symlink, skipping"
      continue
    fi
    ln -s "$skill_dir" "$link"
    echo "Linked $skill_name -> $link"
  done
done

echo "Done."
