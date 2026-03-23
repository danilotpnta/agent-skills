# Skill Design Guide

Reference this file when writing a new SKILL.md. These principles are adapted from
the deepagents skill-creator and apply directly to Claude Code skills.

---

## Core Principles

### Concise is key

The context window is shared with everything else: conversation history, other skills'
metadata, tool results, system prompt. Every token counts.

**Default assumption: Claude is already capable.** Only add context it doesn't already
have. Challenge each section: "Does Claude really need this?" and "Does this paragraph
justify its token cost?"

Prefer concrete examples over verbose explanations.

### The description field is everything

The `description` field is the **only** thing Claude reads to decide whether to invoke
the skill. The body is loaded only after the skill triggers.

Rules:
- Say **when** to use it, not what it does: "Use when the user asks to X" not "This skill does X"
- List concrete trigger phrases (users say "ingest a repo", "convert to text", etc.)
- Max 1024 characters
- No angle brackets
- Never summarize the workflow in the description — Claude will follow the summary and skip the full body

### Degrees of freedom

Match instruction specificity to how fragile the task is:

| Task type | Style | Example |
|---|---|---|
| Multiple valid approaches | High-level text | "Explain the code clearly" |
| Preferred pattern, some variation ok | Pseudocode or structured steps | "Follow these phases: 1. Investigate 2. Fix" |
| Fragile, must be exact | Specific commands, few parameters | `uvx gitingest <url> -o output.txt` |

Think of it as guardrails on a path: a narrow bridge with cliffs needs specific rails,
an open field needs none.

---

## Progressive Disclosure

Skills use a three-level loading system:

1. **description** — always in context (~100 words). Used for triggering.
2. **SKILL.md body** — loaded when skill triggers. Keep under 500 lines.
3. **references/ files** — loaded by Claude only when needed. Unlimited.

### When to split content into references/

- The SKILL.md body exceeds ~150 lines
- A section is only relevant for specific sub-cases
- You have detailed API docs, schemas, or examples
- Multiple variants exist (e.g., `references/aws.md`, `references/gcp.md`)

When you split, always link from SKILL.md and say exactly when to load the file:

```markdown
For advanced configuration options, read [references/advanced.md](references/advanced.md).
```

---

## Anatomy of a Skill

```
skill-name/
├── SKILL.md           (required)
├── scripts/           (optional) — executable code Claude runs
├── references/        (optional) — docs loaded into context as needed
└── assets/            (optional) — files used in output, not loaded into context
```

### scripts/

Use when: the same code is written repeatedly, or deterministic reliability is needed.

Examples:
- `scripts/init_skill.py` — scaffolds a new skill directory
- `scripts/analyze.py` — parses data and returns JSON

Scripts can be executed without being read into context — token efficient. Claude can
also read and patch them for environment-specific adjustments.

**In this repo:** scripts must work with `uv run python scripts/<name>.py`. Add
dependencies to the skill's own section in pyproject.toml if needed.

### references/

Use when: the agent needs to read documentation, schemas, or guides while working.

Examples:
- `references/api-docs.md` — external API reference
- `references/schema.md` — database table definitions
- `references/design-guide.md` — this file

Keep individual reference files under ~300 lines. For longer files, add a table of
contents at the top.

### assets/

Use when: the skill produces output that includes files (templates, boilerplate, images).

Examples:
- `assets/template.html` — starter HTML for a frontend skill
- `assets/cloudformation.yaml` — infrastructure template

Assets are **not** loaded into context. Claude uses them as source files to copy or modify.

---

## SKILL.md body structure

No single required structure, but common patterns:

**Workflow-based** (sequential process):
```
## Overview
## Step 1 — ...
## Step 2 — ...
## Step 3 — ...
```

**Task-based** (tool collection):
```
## Overview
## Task: Do X
## Task: Do Y
## Task: Do Z
```

**Reference/guidelines** (standards or specs):
```
## Overview
## Guidelines
## Specifications
```

Always end with references to any bundled files and say when to use them.

---

## What NOT to include in a skill

- README.md, INSTALLATION.md, QUICK_REFERENCE.md — not for users, adds clutter
- Changelog or version history — belongs at the repo level
- Information Claude already knows (basic Python syntax, standard git commands)
- Warnings about things that can't happen in practice
