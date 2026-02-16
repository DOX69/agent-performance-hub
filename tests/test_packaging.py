
import pytest
from pathlib import Path
import sys
import importlib

# Try to use tomllib (Python 3.11+) or fallback to basic string checking
try:
    import tomllib
except ImportError:
    tomllib = None

from aph.config import SKILLS_REGISTRY_FILE, PACKAGE_ROOT, BUNDLED_SKILLS_DIR

def test_registry_location_is_inside_package():
    """Ensure the registry file is expected to be inside the package directory."""
    # Verify it is relative to the aph package
    assert "aph" in SKILLS_REGISTRY_FILE.parts[-2], "Registry file should be in the 'aph' subdirectory"
    assert SKILLS_REGISTRY_FILE.name == "skills_registry.json"

def test_bundled_assets_resolution():
    """Verify that we can resolve the bundled assets path."""
    # In this test environment (repo root), import aph.bundled should fail 
    # unless we manipulate sys.path or if editable install is active.
    # But assertions should verify that FALLBACK logic works or IMPORT works.
    
    assert BUNDLED_SKILLS_DIR.exists(), f"Bundled skills dir should exist at {BUNDLED_SKILLS_DIR}"
    assert (BUNDLED_SKILLS_DIR / "expert-skill-creator").exists(), "Core skill should be present"

def test_package_configuration():
    """Verify pyproject.toml defines the package structure correctly."""
    pyproject_path = PACKAGE_ROOT / "pyproject.toml"
    assert pyproject_path.exists()
    
    content = pyproject_path.read_text(encoding="utf-8")
    
    # Check for mapping
    assert '"aph.bundled" = ".agent"' in content or "'aph.bundled' = '.agent'" in content, \
        "pyproject.toml must map aph.bundled to .agent"
        
    # Check for package inclusion
    assert 'include = ["aph*"]' in content, "Should include aph*"
    
    # Check for package data
    assert '"aph.bundled" = ["**/*"]' in content or "'aph.bundled' = ['**/*']" in content, \
        "pyproject.toml must include data for aph.bundled"
