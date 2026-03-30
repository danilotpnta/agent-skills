---
name: feature-doc
description: "Generate comprehensive feature documentation from code and git history. Use when the user says: (1) document this feature, (2) create feature doc, (3) write feature docs, (4) doc this feature, (5) generate feature documentation, (6) add feature docs, (7) create a feature document, (8) write up what we built, or any similar phrasing about documenting a completed or in-progress feature."
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Feature Doc

Generates a filled-out `docs/features/FEATURE_<NAME>.md` by reading git history, changed files, and conversation context. Also bootstraps `docs/FEATURE_TEMPLATE.md` in the project if it does not exist yet.

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

Check whether `docs/FEATURE_TEMPLATE.md` exists. If it does not, read the bundled asset and write it to `docs/FEATURE_TEMPLATE.md` in the project root.

> See [assets/FEATURE_TEMPLATE.md](assets/FEATURE_TEMPLATE.md) — copy this file to the project when `docs/FEATURE_TEMPLATE.md` is absent.

---

## Step 3 — Gather context

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
- Data model changes (new fields, modified structs)
- Service layer changes (network, database, persistence)
- UI entry points (where the user accesses the feature)
- Any algorithm or non-trivial logic

Also read any existing conversation context the user has shared — it often contains decisions, gotchas, and rationale that are not visible in the diff.

---

## Step 4 — Fill out the documentation

Write `docs/features/FEATURE_<NAME>.md` using the 15-section structure. Every section must be filled — do not leave placeholders. Delete a section only if it is genuinely not applicable.

**The goal:** a new developer reads this doc and understands the feature end-to-end without asking anyone.

### Sections

**Status table** — branch, status (Draft / In Review / Merged / Deprecated), author (from git log), start date (first commit on branch), merge date if known.

**1. Problem Statement** — What user pain does this solve? Describe the state before this feature existed. Be concrete, not abstract.

**2. Feature Overview** — One paragraph from the user's perspective. Include: feature name as shown in UI, entry point, icon/symbol name, whether it auto-triggers anywhere.

**3. User Scenarios** — Every scenario: happy path, edge cases, partial failure. Numbered steps. Include backend cost (reads/writes, API calls) per scenario where relevant.

**4. Architecture & Design Decisions** — Most important section for new devs. For each non-obvious decision: chosen approach, alternatives considered, reason for choice. If a simpler approach was tried first and failed, document why it failed.

**5. Data Model** — Every model property touched. For new fields: purpose and invariants. For existing fields: how this feature uses or depends on them.

**6. Files Changed** — Every file modified or created with a one-line summary of what changed and why.

**7. Backend / External Service Impact** — Precise cost per user action (DB reads/writes, API calls, cache hits). Include a "net change vs. before" summary. Note whether reads are cached or network.

**8. Algorithm / Core Logic** — Pseudocode for any non-trivial logic. Goal: someone can re-implement from scratch using only this section.

**9. Critical Gotchas** — Non-obvious things that will cause bugs if unknown. Things you wish you knew before starting.

**10. Debug Logging** — What each log prefix means, how to read debug output. Note whether debug wrappers are stripped from release builds.

**11. Edge Cases & Known Limitations** — Table: scenario | current behaviour | ideal behaviour | priority.

**12. Multi-Device / Concurrency Behaviour** — What happens under simultaneous use? Idempotent? Last-write-wins? Conflicts possible?

**13. Testing Checklist** — Manual steps specific enough for anyone to follow without prior knowledge. Include negative cases (no data, offline, empty state).

**14. Performance Considerations** — CPU, memory, network cost. Note anything that scales with data size.

**15. Future Considerations / TODOs** — Table: item | priority | notes. Capture things deliberately left out of scope and open questions.

---

## Step 5 — Write the file

Save to `docs/features/FEATURE_<NAME>.md`. Do not create any other files unless Step 2 triggered the bootstrap.

Confirm the output path to the user when done.
