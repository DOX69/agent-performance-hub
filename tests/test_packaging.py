
import pytest
from pathlib import Path
import sys

# Try to use tomllib (Python 3.11+) or fallback to basic string checking
try:
    import tomllib
except ImportError:
    tomllib = None

from aph.config import SKILLS_REGISTRY_FILE, PACKAGE_ROOT

def test_registry_location_is_inside_package():
    """Ensure the registry file is expected to be inside the package directory."""
    # Verify it is relative to the aph package
    # SKILLS_REGISTRY_FILE should have 'aph' as parent folder name or part of path
    # On windows it might be ...\aph\skills_registry.json
    assert "aph" in SKILLS_REGISTRY_FILE.parts[-2], "Registry file should be in the 'aph' subdirectory"
    assert SKILLS_REGISTRY_FILE.name == "skills_registry.json"

def test_registry_file_exists_after_generation():
    """Verify that the registry file actually exists at the configured location."""
    # This assumes generate_registry.py has been run
    assert SKILLS_REGISTRY_FILE.exists(), f"Registry file not found at {SKILLS_REGISTRY_FILE}"
    
def test_package_data_includes_registry():
    """Verify pyproject.toml includes the registry in package data."""
    pyproject_path = PACKAGE_ROOT / "pyproject.toml"
    assert pyproject_path.exists()
    
    if tomllib:
        with open(pyproject_path, "rb") as f:
            config = tomllib.load(f)
        
        # Check [tool.setuptools.package-data]
        tool_config = config.get("tool", {}).get("setuptools", {}).get("package-data", {})
        aph_data = tool_config.get("aph", [])
        
        # Either explicit inclusion or wildcard that covers it
        assert "**/*" in aph_data or "skills_registry.json" in aph_data, \
            "pyproject.toml must include the registry file in package-data"
    else:
        # Fallback: simple text parsing to ensure the configuration exists
        content = pyproject_path.read_text(encoding="utf-8")
        assert '[tool.setuptools.package-data]' in content
        # Check for aph = ["**/*"] or similar. Whitespace might vary.
        # We look for 'aph' assignment in that section.
        # This is less robust but sufficient if tomllib is missing.
        assert 'aph = ["**/*"]' in content or "skills_registry.json" in content, \
            "pyproject.toml should include 'aph = [\"**/*\"]' or explicit registry file"
