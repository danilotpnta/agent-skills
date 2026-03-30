---
name: ios-feature-doc
description: "Generate comprehensive iOS feature documentation from code and git history. Use when the user says: (1) document this feature, (2) create feature doc, (3) write feature docs, (4) doc this feature, (5) generate feature documentation, (6) add feature docs, (7) write up what we built, or any similar phrasing about documenting a completed or in-progress iOS feature."
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# iOS Feature Doc

Generates a filled-out `docs/features/FEATURE_<NAME>.md` for an iOS project by reading git history, changed files, and conversation context. Follows the exact format defined in `assets/FEATURE_TEMPLATE.md`. Also bootstraps `docs/FEATURE_TEMPLATE.md` in the project if it does not exist yet.

---

## Step 1 — Determine the feature name

Derive the feature name from the current git branch (strip `feature/` prefix, convert hyphens to underscores, uppercase). If the branch name is ambiguous or not a feature branch, ask the user.

```bash
git rev-parse --abbrev-ref HEAD
```

Example: branch `feature/smart-sort` → document name `FEATURE_SMART_SORT.md`.

---

## Step 2 — Bootstrap docs structure (if needed)

Check whether `docs/features/` exists. If not, create it:

```bash
mkdir -p docs/features
```

Check whether `docs/FEATURE_TEMPLATE.md` exists in the project. If it does not, read [assets/FEATURE_TEMPLATE.md](assets/FEATURE_TEMPLATE.md) and write it to `docs/FEATURE_TEMPLATE.md` in the project root.

---

## Step 3 — Read the template

Read [assets/FEATURE_TEMPLATE.md](assets/FEATURE_TEMPLATE.md) now. Use it as the exact format guide for the output document — match every table structure, column name, and section heading exactly. Do not invent a different layout.

---

## Step 4 — Gather context

Run all of the following. Read the output carefully — it is the primary source of truth for the documentation.

```bash
# Branch and commits ahead of main
git rev-parse --abbrev-ref HEAD
git log --oneline main..HEAD          # or master..HEAD if main does not exist

# Files changed in this feature
git diff --name-status main..HEAD

# Full diff for implementation details
git diff main..HEAD
```

Then read the key changed files identified in the diff. Focus on:
- New methods / functions added
- Data model changes (new fields, modified structs/classes)
- Service layer changes (Firebase, network, persistence)
- UI entry points — where the user accesses the feature (SwiftUI views, toolbar buttons, menus)
- Any algorithm or non-trivial logic

Also read any existing conversation context the user has shared — it often contains decisions, gotchas, and rationale that are not visible in the diff.

---

## Step 5 — Fill out the documentation

Write `docs/features/FEATURE_<NAME>.md` following the template structure exactly. Every section must be filled — do not leave placeholders. Delete a section only if it is genuinely not applicable.

**The goal:** a new iOS developer reads this doc and understands the feature end-to-end without asking anyone.

Key things to capture that are often missed:
- **Why** each architecture decision was made, not just what was chosen — include alternatives considered and why they were rejected
- Any non-obvious data model invariants (e.g. a field that is only set on header items, not regular items)
- Firebase reads/writes per user action with precise counts
- Debug log prefixes and what each means
- Things that caused bugs during development — these become Critical Gotchas

---

## Step 6 — Write the file

Save to `docs/features/FEATURE_<NAME>.md`. Do not create any other files unless Step 2 triggered the bootstrap.

Confirm the output path to the user when done.
