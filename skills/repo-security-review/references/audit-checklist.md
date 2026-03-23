# Audit Checklist

Structured checklists by audit type. Load this file when doing a deep-dive review
or when the user asks for a thorough audit of a specific ecosystem.

---

## General Repo Checklist

- [ ] Who maintains it? Check account age, activity history, and other repos
- [ ] When was it created? When was the last commit?
- [ ] Is there a `SECURITY.md` or vulnerability disclosure policy?
- [ ] Are there open issues or PRs mentioning "malicious", "backdoor", "suspicious"?
- [ ] Does the license match what the README claims?
- [ ] Is the repo a fork? If so, what changed from the upstream?

---

## Install Script Checklist (`install.sh`, `Makefile`, etc.)

- [ ] Read the full script before running — never pipe to shell blindly
- [ ] Does it download additional resources? From where?
- [ ] Does it verify checksums or signatures on downloaded files?
- [ ] Does it require `sudo`? Is there a stated reason?
- [ ] Does it modify shell profiles (`.bashrc`, `.zshrc`, `.profile`)?
- [ ] Does it add cron jobs or launch agents (`launchd`, `systemd`)?
- [ ] Does it send any data during install (registration, telemetry)?
- [ ] Does it clean up its own installer after running?

---

## npm / Node.js Checklist

- [ ] Check `package.json` for `scripts.postinstall`, `scripts.preinstall`, `scripts.install`
- [ ] Search for `child_process`, `exec`, `spawn`, `execSync` in the source
- [ ] Check `dependencies` and `devDependencies` for typosquats
- [ ] Verify the package on npmjs.com: maintainer history, download count, publish dates
- [ ] Look for `.npmrc` manipulation or registry overrides
- [ ] Check if the package uses `node-gyp` (compiles native code — higher risk surface)
- [ ] Search for `process.env` usage — what env vars does it read?
- [ ] Check for `require('fs')` with paths outside the package directory

---

## Python / PyPI Checklist

- [ ] Check `setup.py` for a custom `install` or `develop` command class
- [ ] Check `pyproject.toml` for build hooks (`[tool.hatch.build.hooks]`, etc.)
- [ ] Look for `subprocess`, `os.system`, `eval`, `exec` in the source
- [ ] Verify the package on pypi.org: maintainer, upload history, yanked versions
- [ ] Check `__init__.py` — is code executed on import?
- [ ] Look for `importlib` or dynamic imports of external modules
- [ ] Check `requirements.txt` for unpinned or suspicious packages
- [ ] Search for `os.environ` — what environment variables are accessed?

---

## GitHub Actions / CI Checklist

- [ ] List all workflow triggers: `push`, `pull_request`, `pull_request_target`, `workflow_dispatch`
- [ ] For `pull_request_target`: does the job check out PR code? Does it have secret access?
- [ ] Are third-party actions pinned to commit SHAs (safe) or branch names (unsafe)?
- [ ] Does any job publish to npm, PyPI, or a container registry? What triggers it?
- [ ] Are secrets scoped minimally (only jobs that need them)?
- [ ] Does the workflow use `${{ github.event.*.body }}` or other user-controlled inputs unsanitized?
- [ ] Are there `workflow_run` triggers that could inherit permissions from privileged workflows?

---

## Docker / Container Checklist

- [ ] What is the base image? Is it official or from an unknown user?
- [ ] Is the base image pinned to a digest (`image@sha256:...`) or a mutable tag (`latest`)?
- [ ] Does the `Dockerfile` download and execute scripts from URLs?
- [ ] Does it run as `root` inside the container?
- [ ] Does it expose unnecessary ports?
- [ ] Is there a `.dockerignore`? Could sensitive files be accidentally included in the image?
- [ ] Check `ENTRYPOINT` and `CMD` — what runs when the container starts?

---

## Browser Extension Checklist

- [ ] Check `manifest.json` for permissions — flag `<all_urls>`, `tabs`, `webRequest`, `cookies`, `storage`
- [ ] Does it request `host_permissions` for all sites?
- [ ] Is there a `background` service worker? What does it do?
- [ ] Does it inject content scripts into every page?
- [ ] Does it make external network requests? To where?
- [ ] Is the source minified/obfuscated? (Extensions should be readable)
- [ ] Check the Chrome Web Store / Firefox Add-ons listing: reviews mentioning data collection?
