#!/usr/bin/env python3
"""Scaffold a new skill directory for agent-skills.

Creates the skill directory under skills/ with a SKILL.md template and
optional subdirectories. Delete any subdirectories you don't need.

Usage:
    uv run python skills/add-skill/scripts/init_skill.py <skill-name>
    uv run python skills/add-skill/scripts/init_skill.py <skill-name> --with-scripts
    uv run python skills/add-skill/scripts/init_skill.py <skill-name> --with-references
    uv run python skills/add-skill/scripts/init_skill.py <skill-name> --with-assets
    uv run python skills/add-skill/scripts/init_skill.py <skill-name> --all

Examples:
    uv run python skills/add-skill/scripts/init_skill.py my-skill
    uv run python skills/add-skill/scripts/init_skill.py cost-tracker --with-scripts
    uv run python skills/add-skill/scripts/init_skill.py api-docs --with-references
"""

import argparse
import re
import sys
from pathlib import Path

SKILL_MD_TEMPLATE = """\
---
name: {skill_name}
description: "[TODO: Describe what this skill does and WHEN to invoke it. List trigger phrases. Example: Use when the user asks to X, Y, or Z, or says phrases like 'do X' or 'help me with Y'.]"
allowed-tools: Bash, Read
---

# {skill_title}

[TODO: 1-2 sentences explaining what this skill does.]

## When to Use

[TODO: List concrete scenarios and trigger phrases. Move this to the description field
and delete this section — the body is only loaded after triggering, so 'When to Use'
sections in the body don't help Claude decide to invoke the skill.]

## Workflow

[TODO: Step-by-step instructions. Use concrete commands, not abstract descriptions.
Match specificity to how fragile the task is — see references/design-guide.md.]

## Reference

[TODO: Link to any bundled files and say exactly when to load them. Delete if none.]
"""

EXAMPLE_SCRIPT = """\
#!/usr/bin/env python3
\"\"\"
Helper script for {skill_name}.

Usage:
    uv run python skills/{skill_name}/scripts/example.py

Replace with actual implementation or delete if not needed.
\"\"\"


def main():
    print("Helper script for {skill_name}")
    # TODO: implement


if __name__ == "__main__":
    main()
"""

EXAMPLE_REFERENCE = """\
# Reference: {skill_title}

[TODO: Add detailed reference documentation here — API docs, schemas, guides.
This file is loaded into context only when Claude needs it, keeping SKILL.md lean.]

## Table of Contents

1. [Section 1](#section-1)
2. [Section 2](#section-2)

---

## Section 1

[TODO: Add content]

## Section 2

[TODO: Add content]
"""

EXAMPLE_ASSET = """\
# Assets: {skill_title}

[TODO: Replace this file with actual assets (templates, boilerplate, images, fonts).
Assets are NOT loaded into context — they are files Claude uses in its output.

Examples:
- template.html — HTML boilerplate to copy into new projects
- cloudformation.yaml — infrastructure template
- starter/ — directory with scaffold files

Delete this placeholder and add real asset files.]
"""


def to_title_case(skill_name: str) -> str:
    return " ".join(word.capitalize() for word in skill_name.split("-"))


def validate_skill_name(name: str) -> str | None:
    """Return error message if name is invalid, else None."""
    if not re.match(r"^[a-z0-9-]+$", name):
        return "Name must be hyphen-case: lowercase letters, digits, and hyphens only"
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return "Name cannot start/end with a hyphen or contain consecutive hyphens"
    if len(name) > 64:
        return f"Name is too long ({len(name)} chars, max 64)"
    return None


def init_skill(
    skill_name: str,
    with_scripts: bool = False,
    with_references: bool = False,
    with_assets: bool = False,
) -> int:
    repo_root = Path(__file__).parent.parent.parent.parent
    skill_dir = repo_root / "skills" / skill_name

    if skill_dir.exists():
        print(f"Error: {skill_dir} already exists")
        return 1

    skill_title = to_title_case(skill_name)
    skill_dir.mkdir(parents=True)
    print(f"Created {skill_dir.relative_to(repo_root)}/")

    (skill_dir / "SKILL.md").write_text(
        SKILL_MD_TEMPLATE.format(skill_name=skill_name, skill_title=skill_title)
    )
    print(f"  Created SKILL.md")

    if with_scripts:
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir()
        script = scripts_dir / "example.py"
        script.write_text(
            EXAMPLE_SCRIPT.format(skill_name=skill_name, skill_title=skill_title)
        )
        script.chmod(0o755)
        print(f"  Created scripts/example.py")

    if with_references:
        references_dir = skill_dir / "references"
        references_dir.mkdir()
        (references_dir / "reference.md").write_text(
            EXAMPLE_REFERENCE.format(skill_name=skill_name, skill_title=skill_title)
        )
        print(f"  Created references/reference.md")

    if with_assets:
        assets_dir = skill_dir / "assets"
        assets_dir.mkdir()
        (assets_dir / "README.md").write_text(
            EXAMPLE_ASSET.format(skill_name=skill_name, skill_title=skill_title)
        )
        print(f"  Created assets/README.md")

    print(f"\nSkill '{skill_name}' created. Next steps:")
    print(f"  1. Edit skills/{skill_name}/SKILL.md — complete the TODO items")
    print(f"  2. Delete any unused subdirectories")
    print(f"  3. Run: uv run pytest tests/unit/test_skills.py")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold a new skill directory for agent-skills"
    )
    parser.add_argument("skill_name", help="Skill name in hyphen-case (e.g. my-skill)")
    parser.add_argument("--with-scripts", action="store_true", help="Create scripts/ directory")
    parser.add_argument("--with-references", action="store_true", help="Create references/ directory")
    parser.add_argument("--with-assets", action="store_true", help="Create assets/ directory")
    parser.add_argument("--all", dest="all_dirs", action="store_true", help="Create all subdirectories")
    args = parser.parse_args()

    error = validate_skill_name(args.skill_name)
    if error:
        print(f"Error: {error}")
        return 1

    return init_skill(
        skill_name=args.skill_name,
        with_scripts=args.with_scripts or args.all_dirs,
        with_references=args.with_references or args.all_dirs,
        with_assets=args.with_assets or args.all_dirs,
    )


if __name__ == "__main__":
    sys.exit(main())
