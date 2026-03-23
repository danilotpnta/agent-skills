---
name: add-skill
description: "Guide for adding a new skill to this repo following the full workflow. Use when the user says: (1) add a new skill, (2) create a skill, (3) make a skill, (4) I have an idea for a skill, (5) let us add this skill, (6) I want to build a skill, (7) let us add another skill, (8) new skill for X, or any similar phrasing about creating or adding a skill to this project."
allowed-tools: Bash, Read, Write, Edit, Glob
---

# Add Skill

Follow this checklist every time a skill is added to this repo. Do not skip steps.

## Step 1 — Understand the skill

Before creating anything, ask:
- What does this skill do?
- What user phrases should trigger it automatically?
- Does it need scripts, references, or assets — or just a SKILL.md?

If unclear, ask the user for concrete examples before proceeding.

## Step 2 — Create a branch

```bash
git checkout master && git pull
git checkout -b skills/<skill-name>
```

Branch naming: `skills/<skill-name>` (hyphen-case, matches the skill directory name).

## Step 3 — Scaffold the skill

Run the init script to create the directory structure:

```bash
uv run python skills/add-skill/scripts/init_skill.py <skill-name>
```

This creates `skills/<skill-name>/` with `SKILL.md`, and optional `scripts/`, `references/`, `assets/` subdirectories. Delete any subdirectories you don't need.

Or create manually if the skill only needs a `SKILL.md`:

```bash
mkdir -p skills/<skill-name>
```

## Step 4 — Write SKILL.md

Key rules:
- `name` must match the directory name exactly
- `description` must say **when** to trigger the skill — this is what Claude reads to auto-invoke it. See references/design-guide.md for how to write an effective description.
- Keep SKILL.md body under 500 lines. Move detail to `references/` files.
- Add `allowed-tools` if the skill needs specific tools without prompting

For design principles (concise, progressive disclosure, degrees of freedom, when to use scripts/references/assets), read:
**[references/design-guide.md](references/design-guide.md)**

## Step 5 — Update README.md

Add a row to the skills table:

```markdown
| [skill-name](skills/skill-name/SKILL.md) | One-line description |
```

## Step 6 — Bump version and update CHANGELOG

In both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, increment the minor version (e.g. `1.1.0` → `1.2.0`). Keep them in sync.

In `CHANGELOG.md`, add a new entry at the top:

```markdown
## [X.Y.0] - YYYY-MM-DD

### Added
- `skill-name` skill: one-line description
```

## Step 7 — Run tests

```bash
uv run pytest
```

The new skill is auto-discovered — no test code needed unless the skill has scripts. All tests must pass before committing.

## Step 8 — Commit

Stage only the relevant files:

```bash
git add skills/<skill-name>/ README.md CHANGELOG.md .claude-plugin/plugin.json
git commit -m "Add <skill-name> skill (vX.Y.0)"
```

## Step 9 — PR and merge

```bash
git push -u origin skills/<skill-name>
gh pr create --title "Add <skill-name> skill (vX.Y.0)" --base master
```

Write the PR body based on what was actually built. A good PR body for this repo includes:

- **Summary** — what the skill does, why it was added, and any non-obvious design decisions (e.g. why uvx instead of pip, why a references/ file was split out, what inspired the skill)
- **Changes** — list of files modified (skill files, README, CHANGELOG, plugin.json) so reviewers know what to look at
- **Test plan** — pytest result with count, plus manual verification steps using the actual trigger phrases for this skill

Include any other context that would help someone understand the PR without reading every file — for example, if the skill was adapted from another repo, if it depends on another skill, or if there are known limitations.

After review, merge:

```bash
gh pr merge <number> --merge
git checkout master && git pull
```
