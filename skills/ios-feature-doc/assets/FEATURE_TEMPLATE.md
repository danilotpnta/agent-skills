# Feature: [FEATURE NAME]

> **Template instructions:** Copy this file to `docs/features/FEATURE_<NAME>.md` and fill every section.
> Delete sections that are genuinely not applicable (rare). Do not leave placeholders unfilled.
> The goal: a new developer can read this doc and understand the feature end-to-end without asking anyone.

---

## Status

| Field | Value |
|-------|-------|
| Branch | `feature/...` |
| Status | Draft / In Review / Merged / Deprecated |
| Author | |
| Started | YYYY-MM-DD |
| Merged | YYYY-MM-DD (or pending) |

---

## 1. Problem Statement

> What user problem does this feature solve? Be specific — describe the pain point before jumping to the solution.

---

## 2. Feature Overview

> One paragraph describing what the feature does from the user's perspective. Avoid implementation details here.

**Feature name:** The visible name shown in the UI.
**Entry point:** Where the user finds it (tab, button, menu item, context menu, etc.).
**Icon / trigger:** Symbol or action that surfaces it, if any.
**Auto-triggers:** Does it fire automatically in any flow? If so, when.

---

## 3. User Scenarios

> Walk through the concrete scenarios a user might encounter. Use numbered steps.
> Cover: happy path, edge cases, and what happens when the feature partially fails.

### Scenario A — [Name]
1. Step one
2. Step two
3. Expected result

### Scenario B — [Name]
...

---

## 4. Architecture & Design Decisions

> This is the most important section for a new developer. Document *why* decisions were made, not just *what* was decided. Include alternatives considered and why they were rejected.

### Decision 1: [Title]
- **Chosen approach:**
- **Alternatives considered:**
- **Reason for choice:**

### Decision 2: [Title]
...

---

## 5. Data Model

> List every model property touched by this feature. For new properties, explain their purpose and invariants. For existing properties, explain how this feature uses or depends on them.

### [ModelName]
| Property | Type | Purpose | Notes |
|----------|------|---------|-------|
| `fieldName` | `Type?` | What it stores | Any invariants or gotchas |

---

## 6. Files Changed

> Every file modified or created. Include a short description of what changed and why.

| File | Type | Change Summary |
|------|------|---------------|
| `services/foo_service.py` | Modified | Added `bar()` method |
| `views/foo_view.swift` | Modified | Added toolbar button |

---

## 7. Backend / External Service Impact

> Precision matters here — API calls, DB reads/writes, and cache misses have real cost.

### Reads / Queries
| Trigger | Count | Source | Notes |
|---------|-------|--------|-------|
| Feature action | 1 | DB / cache / API | Note if from local cache |

### Writes / Mutations
| Trigger | Count | Fields written | Notes |
|---------|-------|---------------|-------|
| Feature action | 1 | List of fields | Batched? Transactional? |

### Net change vs. before this feature
> Example: "+1 write per import. Catalog reads: unchanged."

---

## 8. Algorithm / Core Logic

> Describe any non-trivial algorithm implemented. Pseudocode is fine. The goal is that someone can re-implement it from scratch if needed.

```
Step 1: ...
Step 2: ...
```

---

## 9. Critical Gotchas

> Things that are non-obvious and will cause bugs if a developer doesn't know them. These are the things you wish you knew before starting.

### Gotcha 1: [Title]
Explanation and how to avoid the mistake.

---

## 10. Debug Logging

> How to read the debug output for this feature. Include example log lines.
> Note whether debug wrappers are stripped from release/production builds.

| Log prefix | Meaning |
|------------|---------|
| `[FeatureName]` | ... |

---

## 11. Edge Cases & Known Limitations

| Scenario | Current behaviour | Ideal behaviour | Priority |
|----------|-----------------|-----------------|----------|
| Empty state | ... | ... | Low |

---

## 12. Multi-Device / Concurrency Behaviour

> What happens when two users are active on the same account simultaneously?
> Are there write conflicts? Is the feature safe under concurrent use?

---

## 13. Testing Checklist

> Manual steps to verify the feature works. Be specific enough that anyone can follow them without prior knowledge.

- [ ] Happy path: ...
- [ ] Edge case: ...
- [ ] Offline / error state: ...

---

## 14. Performance Considerations

> CPU, memory, or network cost of this feature. Note if any operation scales with data size.

---

## 15. Future Considerations / TODOs

> Things deliberately left out of scope, known improvements, and open questions.

| Item | Priority | Notes |
|------|----------|-------|
| ... | High / Medium / Low | ... |
