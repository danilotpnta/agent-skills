"""
Integration tests for the plugin structure.

Validates that plugin.json is well-formed and all paths it references
actually exist on disk. These act as a structural smoke test — catch
broken references before users try to install the plugin.
"""

import json
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def manifest(repo_root: Path) -> dict:
    """Load and parse plugin.json once for all tests in this module."""
    manifest_path = repo_root / ".claude-plugin" / "plugin.json"
    assert manifest_path.exists(), f"plugin.json not found at {manifest_path}"
    return json.loads(manifest_path.read_text(encoding="utf-8"))


class TestPluginManifest:
    """Validates plugin.json structure and required fields."""

    def test_manifest_has_name(self, manifest: dict):
        assert "name" in manifest and manifest["name"], (
            "plugin.json is missing required 'name' field"
        )

    def test_manifest_has_version(self, manifest: dict):
        assert "version" in manifest and manifest["version"], (
            "plugin.json is missing 'version' field"
        )

    def test_manifest_has_description(self, manifest: dict):
        assert "description" in manifest and manifest["description"], (
            "plugin.json is missing 'description' field"
        )

    def test_version_format(self, manifest: dict):
        """Version should follow semver (MAJOR.MINOR.PATCH)."""
        version = manifest.get("version", "")
        parts = version.split(".")
        assert len(parts) == 3 and all(p.isdigit() for p in parts), (
            f"version '{version}' does not follow semver (MAJOR.MINOR.PATCH)"
        )


class TestPluginPaths:
    """Validates that all paths referenced in plugin.json exist on disk."""

    def test_skills_directory_exists(self, manifest: dict, repo_root: Path):
        skills_path = manifest.get("skills")
        if not skills_path:
            pytest.skip("No 'skills' path defined in plugin.json")
        resolved = (repo_root / skills_path).resolve()
        assert resolved.exists(), (
            f"skills directory '{skills_path}' referenced in plugin.json does not exist"
        )

    def test_commands_directory_exists_if_defined(self, manifest: dict, repo_root: Path):
        commands_path = manifest.get("commands")
        if not commands_path:
            pytest.skip("No 'commands' path defined in plugin.json")
        resolved = (repo_root / commands_path).resolve()
        assert resolved.exists(), (
            f"commands directory '{commands_path}' referenced in plugin.json does not exist"
        )

    def test_skills_directory_contains_at_least_one_skill(
        self, manifest: dict, repo_root: Path
    ):
        skills_path = manifest.get("skills")
        if not skills_path:
            pytest.skip("No 'skills' path defined in plugin.json")
        resolved = (repo_root / skills_path).resolve()
        skill_files = list(resolved.rglob("SKILL.md"))
        assert skill_files, (
            f"skills directory '{skills_path}' exists but contains no SKILL.md files"
        )
