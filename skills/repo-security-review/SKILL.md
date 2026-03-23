---
name: repo-security-review
description: "Security audit for GitHub repositories, install scripts, and open source packages before installation. Use when the user wants to check if a repo or app is safe to install, review install scripts for malicious code, verify an open source project isn't collecting data, or audit dependencies for suspicious packages. Triggers on phrases like 'is this safe to install', 'check this repo', 'review this script', 'audit this code', 'is this sketchy', 'can I trust this', 'should I install this'."
allowed-tools: Bash, Read, WebFetch, WebSearch, Agent
---

# Repo Security Review

Audits a GitHub repository, install script, or package for malicious code, data collection, suspicious dependencies, and supply chain risks before installation.

## Step 1 — Identify the target

Determine what to audit:
- **GitHub URL** → use the `gitingest` skill to fetch a text digest of the repo
- **Raw install script** (e.g. `curl | bash` URL) → fetch it with `WebFetch`
- **Package name** (npm, PyPI, etc.) → search for the package page and fetch metadata
- **Local script/file** → read it directly with `Read`

If the user only provides a name (no URL), search for the official repo first.

## Step 2 — Fetch the content

For GitHub repos, invoke the `gitingest` skill to get a full text digest. Focus on:
- `README.md`, `install.sh`, `Makefile`, `setup.py`, `package.json`, `requirements.txt`
- CI/CD configs: `.github/workflows/`, `.travis.yml`, `Dockerfile`
- Any script that runs on install or post-install hooks

For install scripts, fetch the raw URL and read the full content.

## Step 3 — Audit against red flags

Work through the checklist systematically. Load [references/red-flags.md](references/red-flags.md) for the full catalog of patterns to look for.

High-priority checks (always run):
1. **Install script behavior** — does it pipe to shell? Does it download and execute binaries?
2. **Network calls** — does code phone home, send telemetry, or exfiltrate data?
3. **Obfuscated code** — base64-encoded payloads, eval/exec on dynamic strings
4. **Dependency confusion** — private package names that could be hijacked
5. **Post-install hooks** — npm `postinstall`, pip `setup.py install`, etc.
6. **CI/CD pipeline** — does it have access to secrets? Does it push to package registries?

## Step 4 — Assess repo reputation

Quick signals (not conclusive, but useful context):
- Age of repo and last commit
- Number of contributors and stars
- Whether the maintainer account is new or has history
- Open issues mentioning security concerns
- Whether it's a fork of a well-known project with suspicious changes

## Step 5 — Report findings

Structure the report as:

```
## Security Review: <repo/package name>

**Verdict:** Safe / Caution / Do Not Install

### Summary
1-3 sentences on the overall risk level.

### Findings
- [CRITICAL] ...
- [HIGH] ...
- [MEDIUM] ...
- [LOW/INFO] ...

### What it does (data & network)
What data the code accesses and where it sends it.

### Recommendation
What the user should do: install as-is, install with caveats, audit further, or avoid.
```

Use severity levels: CRITICAL (active malice), HIGH (strong red flag), MEDIUM (suspicious but explainable), LOW/INFO (worth noting).

If no issues are found, say so clearly — a clean bill of health is a valid outcome.

## References

- Load [references/red-flags.md](references/red-flags.md) during Step 3 for the full pattern catalog.
- Load [references/audit-checklist.md](references/audit-checklist.md) for deep-dive checklists by audit type (scripts, npm, PyPI, CI/CD).
