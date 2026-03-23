---
name: gitingest
description: Convert any Git repository into a text file optimized for LLM consumption using GitIngest. Use when the user wants to ingest a repo, create a text digest of a codebase, prepare a repository for LLM analysis, or needs to convert a GitHub URL to a readable text file.
allowed-tools: Bash, Read
---

# GitIngest

Convert any Git repository into a prompt-friendly text file for LLM consumption. GitIngest extracts the structure and contents of a repository into a single text file that can be easily processed by language models.

## When to Use

- User wants to analyze an entire codebase with an LLM
- User needs a text representation of a repository
- User mentions "ingest", "digest", or converting a repo to text
- User wants to prepare code for LLM context

## Workflow

### 1. Run with uvx (no install needed)

The preferred approach — `uvx` runs gitingest in an isolated environment without any setup:

```bash
uvx gitingest <target> -o output.txt
```

This always works as long as `uv` is installed. No venv, no pip, no prior installation needed.

### 2. Identify the Target

Determine what the user wants to ingest:
- **Local directory:** A path on the filesystem
- **GitHub URL:** `https://github.com/owner/repo`
- **Current directory:** If unspecified, confirm with user before proceeding

### 3. Run GitIngest

**For a local directory:**
```bash
uvx gitingest /path/to/repository -o output.txt
```

**For a GitHub repository:**
```bash
uvx gitingest https://github.com/owner/repo -o output.txt
```

**For the current directory:**
```bash
uvx gitingest . -o output.txt
```

### 4. Common Options

| Option | Description |
|--------|-------------|
| `-o <file>` | Output to specified file (use `-` for stdout) |
| `-t <token>` | GitHub token for private repos |
| `--include-gitignored` | Include files normally ignored by .gitignore |
| `--include-submodules` | Process git submodules |

**Private repositories:**
```bash
uvx gitingest https://github.com/owner/private-repo -t $GITHUB_TOKEN -o output.txt
```

### 5. Permanent Install (optional)

If the user runs gitingest frequently and wants it available as a regular command:

```bash
uv tool install gitingest
gitingest <target> -o output.txt
```

### 6. Output

After running, confirm:
- Output file location
- Approximate size and token count if reported
- Any warnings or skipped files

Warn the user if the output is large — token counts help gauge whether it will fit in an LLM context window.

## Tips

- For very large repos, suggest focusing on a specific subdirectory: `uvx gitingest /repo/src/`
- The web interface works too: replace "hub" with "ingest" in any GitHub URL → `gitingest.com/owner/repo`
- Output is human-readable as well as LLM-optimized

## Reference

- **GitHub:** https://github.com/coderamp-labs/gitingest
