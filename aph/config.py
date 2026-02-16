"""APH configuration constants and defaults."""

from pathlib import Path

# ─── Package Paths ────────────────────────────────────────────────────────────
# The root of the installed aph package (where .agent/skills/ lives)
PACKAGE_ROOT = Path(__file__).parent.parent.resolve()

# The bundled skills directory inside the package
BUNDLED_SKILLS_DIR = PACKAGE_ROOT / ".agent" / "skills"

# The bundled knowledge/methodology/debug/sources directories
BUNDLED_KNOWLEDGE_DIR = PACKAGE_ROOT / ".agent" / "knowledge"
BUNDLED_METHODOLOGY_DIR = PACKAGE_ROOT / ".agent" / "methodology"
BUNDLED_DEBUG_DIR = PACKAGE_ROOT / ".agent" / "debug"
BUNDLED_SOURCES_DIR = PACKAGE_ROOT / ".agent" / "sources"

# Skills registry file
SKILLS_REGISTRY_FILE = PACKAGE_ROOT / "skills_registry.json"

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
GITHUB_HTTPS_URL = f"https://github.com/{GITHUB_REPO}.git"
GITHUB_SSH_URL = f"git@github.com:{GITHUB_REPO}.git"
