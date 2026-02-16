"""APH configuration constants and defaults."""

from pathlib import Path

# ─── Package Paths ────────────────────────────────────────────────────────────
# The root of the installed aph package (where .agent/skills/ lives)
PACKAGE_ROOT = Path(__file__).parent.parent.resolve()

# Helper: Try to find bundled resources
try:
    import aph.bundled
    # If installed as a package with the mapping
    if hasattr(aph.bundled, "__file__") and aph.bundled.__file__:
        BUNDLED_AGENT_ROOT = Path(aph.bundled.__file__).parent
    else:
        # Namespace package (no __init__.py, so no __file__)
        BUNDLED_AGENT_ROOT = Path(list(aph.bundled.__path__)[0])
except ImportError:
    # If running from source/repo without mapping
    BUNDLED_AGENT_ROOT = PACKAGE_ROOT / ".agent"

# The bundled skills directory inside the package (or repo)
BUNDLED_SKILLS_DIR = BUNDLED_AGENT_ROOT / "skills"

# The bundled knowledge/methodology/debug/sources directories
BUNDLED_KNOWLEDGE_DIR = BUNDLED_AGENT_ROOT / "knowledge"
BUNDLED_METHODOLOGY_DIR = BUNDLED_AGENT_ROOT / "methodology"
BUNDLED_DEBUG_DIR = BUNDLED_AGENT_ROOT / "debug"
BUNDLED_SOURCES_DIR = BUNDLED_AGENT_ROOT / "sources"

# Skills registry file
SKILLS_REGISTRY_FILE = PACKAGE_ROOT / "aph" / "skills_registry.json"

# ─── Target Project Paths ─────────────────────────────────────────────────────
AGENT_DIR_NAME = ".agent"
SKILLS_SUBDIR = "skills"
KNOWLEDGE_SUBDIR = "knowledge"
METHODOLOGY_SUBDIR = "methodology"
DEBUG_SUBDIR = "debug"
SOURCES_SUBDIR = "sources"

# Manifest file tracking installed skills
MANIFEST_FILE = ".aph-manifest.json"

# Agent-facing README explaining how to use APH
README_AGENT_FILE = "README_AGENT.md"

# ─── Core Skills ──────────────────────────────────────────────────────────────
# These are installed by default with `aph init`
CORE_SKILLS = [
    "brainstorming",
    "git-pushing",
    "expert-skill-creator",
    "clean-code",
    "systematic-debugging",
    "verification-before-completion",
    "test-driven-development",
]

# ─── Directories created on `aph init` ────────────────────────────────────────
INIT_SUBDIRS = [
    SKILLS_SUBDIR,
    KNOWLEDGE_SUBDIR,
    METHODOLOGY_SUBDIR,
    DEBUG_SUBDIR,
    SOURCES_SUBDIR,
]

# ─── GitHub Repo ──────────────────────────────────────────────────────────────
GITHUB_REPO = "DOX69/agent-performance-hub"
GITHUB_HTTPS_URL = f"https://github.com/{GITHUB_REPO}.git"
GITHUB_SSH_URL = f"git@github.com:{GITHUB_REPO}.git"
