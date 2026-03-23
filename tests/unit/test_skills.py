"""
Unit tests for SKILL.md files.

Validates that every skill in the skills/ directory has valid structure
and required frontmatter fields. These tests run against the raw markdown
files — no Claude invocation needed.
"""

from pathlib import Path

import pytest

# Max description length enforced by Claude Code (skills system)
MAX_DESCRIPTION_LENGTH = 1024


def _parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from a markdown file. Returns empty dict if absent."""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    block = content[3:end].strip()
    result = {}
    for line in block.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def _skill_paths(skills_dir: Path) -> list[Path]:
    """Return all SKILL.md files found under skills/."""
    return sorted(skills_dir.rglob("SKILL.md"))


def pytest_generate_tests(metafunc):
    """Parametrize skill-level tests over every SKILL.md in the repo."""
    if "skill_path" in metafunc.fixturenames:
        skills_dir = Path(__file__).parent.parent.parent / "skills"
        paths = _skill_paths(skills_dir)
        ids = [p.parent.name for p in paths]
        metafunc.parametrize("skill_path", paths, ids=ids)


class TestSkillStructure:
    """Validates every SKILL.md has the required structure."""

    def test_skill_file_is_not_empty(self, skill_path: Path):
        content = skill_path.read_text(encoding="utf-8")
        assert content.strip(), f"{skill_path} is empty"

    def test_skill_has_frontmatter(self, skill_path: Path):
        content = skill_path.read_text(encoding="utf-8")
        assert content.startswith("---"), (
            f"{skill_path} is missing YAML frontmatter (must start with ---)"
        )

    def test_skill_has_name(self, skill_path: Path):
        content = skill_path.read_text(encoding="utf-8")
        fm = _parse_frontmatter(content)
        assert "name" in fm and fm["name"], (
            f"{skill_path} frontmatter is missing a 'name' field"
        )

    def test_skill_has_description(self, skill_path: Path):
        content = skill_path.read_text(encoding="utf-8")
        fm = _parse_frontmatter(content)
        assert "description" in fm and fm["description"], (
            f"{skill_path} frontmatter is missing a 'description' field"
        )

    def test_description_within_length_limit(self, skill_path: Path):
        content = skill_path.read_text(encoding="utf-8")
        fm = _parse_frontmatter(content)
        desc = fm.get("description", "")
        assert len(desc) <= MAX_DESCRIPTION_LENGTH, (
            f"{skill_path} description is {len(desc)} chars "
            f"(max {MAX_DESCRIPTION_LENGTH})"
        )

    def test_skill_name_matches_directory(self, skill_path: Path):
        content = skill_path.read_text(encoding="utf-8")
        fm = _parse_frontmatter(content)
        skill_name = fm.get("name", "")
        dir_name = skill_path.parent.name
        assert skill_name == dir_name, (
            f"{skill_path}: 'name' field '{skill_name}' "
            f"does not match directory name '{dir_name}'"
        )

    def test_skill_has_body_content(self, skill_path: Path):
        content = skill_path.read_text(encoding="utf-8")
        # Body is everything after the closing ---
        end = content.find("---", 3)
        body = content[end + 3:].strip() if end != -1 else ""
        assert body, f"{skill_path} has no content after frontmatter"
