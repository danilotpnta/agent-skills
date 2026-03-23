"""
Pytest configuration and shared fixtures for agent-skills tests.
"""

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Absolute path to the repository root."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def skills_dir(repo_root: Path) -> Path:
    """Absolute path to the skills/ directory."""
    return repo_root / "skills"


@pytest.fixture(scope="session")
def plugin_manifest(repo_root: Path) -> Path:
    """Absolute path to .claude-plugin/plugin.json."""
    return repo_root / ".claude-plugin" / "plugin.json"
