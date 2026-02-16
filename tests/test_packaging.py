"""Tests for APH packaging and data inclusion."""

from pathlib import Path
from aph.config import SKILLS_REGISTRY_FILE
from aph.registry import load_registry

def test_skills_registry_file_exists():
    """Verify SKILLS_REGISTRY_FILE resolves to an existing file."""
    assert SKILLS_REGISTRY_FILE.exists(), f"Registry file not found at {SKILLS_REGISTRY_FILE}"
    assert SKILLS_REGISTRY_FILE.name == "skills_registry.json"

def test_load_registry_works():
    """Verify load_registry() can read and parse the file."""
    registry = load_registry()
    assert isinstance(registry, dict)
    assert "skills" in registry
