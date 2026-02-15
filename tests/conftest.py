"""Test configuration and fixtures."""

import sys
import pytest
from pathlib import Path

# Add repo root to sys.path so we can import 'aph' and 'scripts'
REPO_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT))

@pytest.fixture(scope="session", autouse=True)
def setup_bundled_environment():
    """Ensure the environment is set up for testing.

    This handles:
    1. Ensuring skills_registry.json exists (by running generation script if needed).
    """
    registry_file = REPO_ROOT / "skills_registry.json"

    if not registry_file.exists():
        print("Generating skills registry for tests...")
        from scripts.generate_registry import main as generate_registry
        generate_registry()
