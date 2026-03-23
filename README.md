# agent-skills

A collection of [Claude Code](https://claude.ai/claude-code) skills for modern Python development and agentic workflows.

## Installation

### Install via Claude Code plugin system

From within a Claude Code session:

```
/plugin marketplace add danilotpnta/agent-skills
/plugin install agent-skills@danilotpnta-skills
/reload-plugins
```

### Install manually (local development)

Clone the repo and add it as a local plugin:

```bash
git clone https://github.com/danilotpnta/agent-skills.git
```

Then in Claude Code settings, add the path to the cloned directory under `plugins`.

---

## Skills

| Skill | Description |
|-------|-------------|
| [uv-manager](skills/uv-manager/SKILL.md) | Manage Python projects and dependencies using uv — the authoritative convention for all Python work |
| [gitingest](skills/gitingest/SKILL.md) | Convert any Git repository into a text file optimized for LLM consumption using `uvx gitingest` |
| [add-skill](skills/add-skill/SKILL.md) | Step-by-step checklist for adding a new skill to this repo — auto-triggered when you say "add a skill" or similar |
| [repo-security-review](skills/repo-security-review/SKILL.md) | Audit a GitHub repo, install script, or package for malicious code, data collection, and supply chain risks before installation |

---

## Usage

Skills load automatically when Claude detects a relevant task, or you can invoke them directly:

```
/uv-manager
/agent-skills:uv-manager     # namespaced form when installed as plugin
```

---

## Contributing

Contributions welcome. Please open an issue before submitting a PR for significant changes.

1. Fork the repo
2. Create a branch: `git checkout -b skills/your-skill-name`
3. Add your skill under `skills/your-skill-name/SKILL.md`
4. Open a pull request

See [skills/uv-manager/SKILL.md](skills/uv-manager/SKILL.md) for an example of skill structure.

---

## License

[MIT](LICENSE) License - see LICENSE file for details
