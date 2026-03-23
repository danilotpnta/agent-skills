---
name: uv-manager
description: Manage Python projects and dependencies using uv. Use when setting up a Python project, adding/removing packages, running scripts in a uv-managed environment, creating virtual environments, or when any skill needs Python packages installed.
allowed-tools: Bash, Read, Glob
---

## uv Project Management

This skill defines the authoritative conventions for managing Python environments and dependencies with [uv](https://docs.astral.sh/uv/). All other skills that require Python should follow these conventions.

### Core Philosophy

uv handles environments automatically. Prefer `uv run` over manually activating venvs. Prefer `uv add` over `pip install`. Let uv manage the lockfile (`uv.lock`) — never edit it by hand.

---

### Project Setup

**New project:**
```bash
uv init my-project        # creates pyproject.toml, .python-version, main.py
cd my-project
```

**Existing project (first time):**
```bash
uv sync                   # creates .venv and installs all dependencies from uv.lock
```

**Pin Python version:**
```bash
uv python pin 3.12        # writes .python-version — commit this file
```

---

### Dependency Management

**Add a dependency:**
```bash
uv add requests
uv add "fastapi>=0.100"
uv add --dev pytest ruff   # dev-only dependencies
uv add --optional docs sphinx  # optional group
```

**Remove a dependency:**
```bash
uv remove requests
```

**Upgrade dependencies:**
```bash
uv lock --upgrade-package requests   # upgrade one
uv lock --upgrade                    # upgrade all
uv sync                              # apply changes
```

**Check what's installed:**
```bash
uv pip list
uv tree                   # show dependency tree
```

---

### Running Code

Always prefer `uv run` — it ensures the correct environment without activation:

```bash
uv run python script.py
uv run pytest
uv run ruff check .
uv run python -c "import sys; print(sys.version)"
```

**Run a tool without installing it globally:**
```bash
uvx ruff check .           # runs ruff in an isolated env, no install needed
uvx httpie GET example.com
```

---

### Virtual Environments

uv creates `.venv` in the project root automatically. Avoid manual activation when possible. When direct path access is needed:

```bash
.venv/bin/python           # direct invocation (scripts, CI)
.venv/bin/pytest
```

**Explicit venv creation (rarely needed):**
```bash
uv venv                    # creates .venv in current directory
uv venv --python 3.11      # specific Python version
```

---

### Files to Commit

| File | Commit? | Notes |
|------|---------|-------|
| `pyproject.toml` | Yes | dependency declarations |
| `uv.lock` | Yes | reproducible installs |
| `.python-version` | Yes | pins Python version |
| `.venv/` | No | always in .gitignore |

---

### Common Patterns for Other Skills

When a skill needs to run Python with packages:

```bash
# Check if project is already synced
uv sync --frozen            # fast check — fails if lockfile is stale

# Install and run in one step
uv run --with requests python -c "import requests; ..."

# Run a script that needs specific packages
uv run --with pandas --with matplotlib python analyze.py
```

See [uv documentation](https://docs.astral.sh/uv/) for full reference.
