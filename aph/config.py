"""APH configuration constants and defaults."""

from pathlib import Path

# ─── Package Paths ────────────────────────────────────────────────────────────
# The directory where this file resides (the aph package directory)
PACKAGE_DIR = Path(__file__).parent.resolve()
REPO_ROOT = PACKAGE_DIR.parent

# Determine where the bundled resources are located
# 1. Check for 'bundled' directory inside the package (installed mode)
if (PACKAGE_DIR / "bundled").exists():
    BUNDLED_DIR = PACKAGE_DIR / "bundled"
    SKILLS_REGISTRY_FILE = BUNDLED_DIR / "skills_registry.json"
# 2. Fallback to repo root .agent (development/test mode)
elif (REPO_ROOT / ".agent").exists():
    BUNDLED_DIR = REPO_ROOT / ".agent"
    SKILLS_REGISTRY_FILE = REPO_ROOT / "skills_registry.json"
else:
    # Fallback to allow import but commands might fail
    BUNDLED_DIR = PACKAGE_DIR / "bundled"
    SKILLS_REGISTRY_FILE = BUNDLED_DIR / "skills_registry.json"

# The bundled skills directory inside the package
BUNDLED_SKILLS_DIR = BUNDLED_DIR / "skills"

# The bundled knowledge/methodology/debug/sources directories
BUNDLED_KNOWLEDGE_DIR = BUNDLED_DIR / "knowledge"
BUNDLED_METHODOLOGY_DIR = BUNDLED_DIR / "methodology"
BUNDLED_DEBUG_DIR = BUNDLED_DIR / "debug"
BUNDLED_SOURCES_DIR = BUNDLED_DIR / "sources"


# ─── Target Project Paths ─────────────────────────────────────────────────────
AGENT_DIR_NAME = ".agent"
SKILLS_SUBDIR = "skills"
KNOWLEDGE_SUBDIR = "knowledge"
METHODOLOGY_SUBDIR = "methodology"
DEBUG_SUBDIR = "debug"
SOURCES_SUBDIR = "sources"

# Manifest file tracking installed skills
MANIFEST_FILE = ".aph-manifest.json"

# ─── Core Skills ──────────────────────────────────────────────────────────────
# These are installed by default with `aph init`
CORE_SKILLS = [
    "brainstorming",
    "git-pushing",
    "expert-skill-creator",
    "clean-code",
    "systematic-debugging",
    "verification-before-completion",
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
GITHUB_SSH_URL = f"git@github.com:{GITHUB_REPO}.git"
GITHUB_HTTPS_URL = f"https://github.com/{GITHUB_REPO}"
