"""APH Installer — Core logic for installing/removing skills."""

import json
import shutil
from datetime import datetime
from pathlib import Path

from .config import (
    AGENT_DIR_NAME,
    BUNDLED_DEBUG_DIR,
    BUNDLED_KNOWLEDGE_DIR,
    BUNDLED_METHODOLOGY_DIR,
    BUNDLED_SKILLS_DIR,
    BUNDLED_SOURCES_DIR,
    CORE_SKILLS,
    DEBUG_SUBDIR,
    INIT_SUBDIRS,
    KNOWLEDGE_SUBDIR,
    MANIFEST_FILE,
    METHODOLOGY_SUBDIR,
    README_AGENT_FILE,
    SKILLS_SUBDIR,
    SOURCES_SUBDIR,
)

README_AGENT_CONTENT = """# 🤖 Agent Performance Hub (APH) — Agent Guide

Welcome, Agent. This project uses **APH** to manage your specialized skills and project context. You are fully autonomous to search, add, and use skills in this project using the `aph` CLI.

## 🚀 Core Capabilities
This project is equipped with **240+ skills** across categories like Security, AI Agents, Marketing, Frontend, DevOps, and more.

### 🔍 Explore & Search
- `aph list` — List all available skills in the registry.
- `aph list --category <name>` — Filter skills by category (e.g., `security`, `ai-agents`).
- `aph search <query>` — Search by name, description, or tags (e.g., `aph search stripe`).
- `aph info <skill>` — View purpose, usage, and examples for a specific skill.

### 📦 Installation & Management
- `aph add <skill>` — Install a skill into `.agent/skills/`.
- `aph remove <skill>` — Remove an unneeded skill.
- `aph update` — Update all installed skills to the latest version.
- `aph update <skill>` — Update a specific skill.

### 🛠️ Reference & Execution
- `aph --help` or `aph -h` — Global help.
- `aph <command> --help` — Detailed structured help for any command.

## 📁 Project Structure
The `.agent/` directory is your brain:
- `skills/` — Actionable instructions (`SKILL.md`) for specific tasks.
- `knowledge/` — Project context, architecture, and tech stack references.
- `methodology/` — Core reasoning and workflow patterns.
- `debug/` — Error patterns and benchmarks.

## 💡 How to Perform at your Best
1. **Be Proactive**: If you lack expertise for a task (e.g., "Set up a Stripe webhook"), `aph search stripe` and `aph add stripe-integration` immediately.
2. **Read the Docs**: After installing a skill, read its `SKILL.md`. It contains optimized instructions designed for agents.
3. **Use the Help**: Every `aph` command provides **PURPOSE**, **USAGE**, and **EXAMPLES** structured for AI agents. When in doubt, run `aph <command> --help`.
4. **Follow Methodology**: Check `.agent/methodology/` to understand the project's preferred reasoning style before making major changes.

---
*APH v0.1.0 — Empowering autonomous agents with the right skills at the right time.*
"""


def get_project_agent_dir(project_path: Path | None = None) -> Path:
    """Get the .agent/ directory path for the current/given project."""
    base = project_path or Path.cwd()
    return base / AGENT_DIR_NAME


def get_manifest_path(project_path: Path | None = None) -> Path:
    """Get the manifest file path."""
    return get_project_agent_dir(project_path) / MANIFEST_FILE


def load_manifest(project_path: Path | None = None) -> dict:
    """Load the APH manifest tracking installed skills.

    Returns:
        dict with 'installed_skills', 'initialized_at', 'updated_at'.
    """
    manifest_path = get_manifest_path(project_path)
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    return {
        "aph_version": "0.1.0",
        "initialized_at": None,
        "updated_at": None,
        "installed_skills": [],
    }


def save_manifest(manifest: dict, project_path: Path | None = None) -> None:
    """Save the APH manifest."""
    manifest["updated_at"] = datetime.now().isoformat()
    manifest_path = get_manifest_path(project_path)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def is_initialized(project_path: Path | None = None) -> bool:
    """Check if the current project has been initialized with aph."""
    return get_manifest_path(project_path).exists()


def get_installed_skills(project_path: Path | None = None) -> list[str]:
    """Return list of installed skill names."""
    manifest = load_manifest(project_path)
    return manifest.get("installed_skills", [])


def _copy_directory(src: Path, dst: Path) -> None:
    """Copy a directory tree, creating parents if needed."""
    if not src.exists():
        return
    if dst.exists():
        # Merge: copy new files, overwrite existing
        for item in src.rglob("*"):
            if item.is_file():
                relative = item.relative_to(src)
                target = dst / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
    else:
        shutil.copytree(src, dst)


def init_project(
    project_path: Path | None = None,
    skills: list[str] | None = None,
) -> tuple[bool, str]:
    """Initialize a project with .agent/ and core skills.

    Args:
        project_path: Target project root (defaults to cwd).
        skills: List of skill names to install. Defaults to CORE_SKILLS.

    Returns:
        (success: bool, message: str)
    """
    agent_dir = get_project_agent_dir(project_path)

    if is_initialized(project_path):
        return False, (
            f"Project already initialized! (.agent/ exists at {agent_dir})\n"
            "Use 'aph add <skill>' to install additional skills,\n"
            "or 'aph update' to update existing ones."
        )

    # Create .agent/ subdirectories
    for subdir in INIT_SUBDIRS:
        (agent_dir / subdir).mkdir(parents=True, exist_ok=True)

    # Create .gitignore to avoid pushing .agent/ content to git
    (agent_dir / ".gitignore").write_text("*\n", encoding="utf-8")

    # Create README_AGENT.md to guide agents
    (agent_dir / README_AGENT_FILE).write_text(README_AGENT_CONTENT, encoding="utf-8")

    # Copy knowledge, methodology, debug, sources from bundled package
    _copy_directory(BUNDLED_KNOWLEDGE_DIR, agent_dir / KNOWLEDGE_SUBDIR)
    _copy_directory(BUNDLED_METHODOLOGY_DIR, agent_dir / METHODOLOGY_SUBDIR)
    _copy_directory(BUNDLED_DEBUG_DIR, agent_dir / DEBUG_SUBDIR)
    _copy_directory(BUNDLED_SOURCES_DIR, agent_dir / SOURCES_SUBDIR)

    # Install skills
    skills_to_install = skills or CORE_SKILLS
    installed = []
    errors = []

    for skill_name in skills_to_install:
        success, msg = install_skill(skill_name, project_path)
        if success:
            installed.append(skill_name)
        else:
            errors.append(f"  ⚠ {skill_name}: {msg}")

    # Create manifest
    manifest = {
        "aph_version": "0.1.0",
        "initialized_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "installed_skills": installed,
    }
    save_manifest(manifest, project_path)

    # Build result message
    msg = f"✅ Initialized .agent/ at {agent_dir}\n"
    msg += f"   Installed {len(installed)} core skill(s): {', '.join(installed)}\n"
    if errors:
        msg += "\n⚠ Some skills could not be installed:\n" + "\n".join(errors)
    msg += "\n\n💡 Next steps:\n"
    msg += "   aph list          — Browse all available skills\n"
    msg += "   aph add <skill>   — Install additional skills\n"
    msg += "   aph search <term> — Search skills by keyword\n"

    return True, msg


def install_skill(
    skill_name: str, project_path: Path | None = None
) -> tuple[bool, str]:
    """Install a single skill into the project's .agent/skills/.

    Args:
        skill_name: Name of the skill to install.
        project_path: Target project root.

    Returns:
        (success: bool, message: str)
    """
    src = BUNDLED_SKILLS_DIR / skill_name
    if not src.exists():
        return False, f"Skill '{skill_name}' not found in the registry."

    agent_dir = get_project_agent_dir(project_path)
    dst = agent_dir / SKILLS_SUBDIR / skill_name

    # Copy skill directory
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    # Update manifest
    manifest = load_manifest(project_path)
    if skill_name not in manifest["installed_skills"]:
        manifest["installed_skills"].append(skill_name)
        manifest["installed_skills"].sort()
        save_manifest(manifest, project_path)

    return True, f"Installed '{skill_name}'"


def remove_skill(
    skill_name: str, project_path: Path | None = None
) -> tuple[bool, str]:
    """Remove a skill from the project's .agent/skills/.

    Args:
        skill_name: Name of the skill to remove.
        project_path: Target project root.

    Returns:
        (success: bool, message: str)
    """
    agent_dir = get_project_agent_dir(project_path)
    skill_dir = agent_dir / SKILLS_SUBDIR / skill_name

    if not skill_dir.exists():
        return False, f"Skill '{skill_name}' is not installed."

    shutil.rmtree(skill_dir)

    # Update manifest
    manifest = load_manifest(project_path)
    if skill_name in manifest["installed_skills"]:
        manifest["installed_skills"].remove(skill_name)
        save_manifest(manifest, project_path)

    return True, f"Removed '{skill_name}'"


def update_skill(
    skill_name: str, project_path: Path | None = None
) -> tuple[bool, str]:
    """Update a skill to the latest version from the package.

    Args:
        skill_name: Name of the skill to update.
        project_path: Target project root.

    Returns:
        (success: bool, message: str)
    """
    if skill_name not in get_installed_skills(project_path):
        return False, f"Skill '{skill_name}' is not installed. Use 'aph add {skill_name}' first."

    return install_skill(skill_name, project_path)


def update_all_skills(
    project_path: Path | None = None,
) -> tuple[int, int, list[str]]:
    """Update all installed skills.

    Returns:
        (updated_count, error_count, error_messages)
    """
    installed = get_installed_skills(project_path)
    updated = 0
    errors = []

    for skill_name in installed:
        success, msg = install_skill(skill_name, project_path)
        if success:
            updated += 1
        else:
            errors.append(f"  ⚠ {skill_name}: {msg}")

    return updated, len(errors), errors


def uninstall_aph(
    project_path: Path | None = None,
) -> tuple[bool, str]:
    """Uninstall APH from the system and remove .agent/ directory.

    Args:
        project_path: Target project root.

    Returns:
        (success: bool, message: str)
    """
    import subprocess
    import shutil
    import sys
    import site

    agent_dir = get_project_agent_dir(project_path)
    
    # Remove .agent directory
    if agent_dir.exists():
        shutil.rmtree(agent_dir)
        
    # Uninstall package
    success = False
    error_msg = ""

    commands = [
        [sys.executable, "-m", "pip", "uninstall", "aph-cli", "-y"],
        ["pip", "uninstall", "aph-cli", "-y"],
        ["uv", "pip", "uninstall", "aph-cli"],
    ]

    for cmd in commands:
        try:
            # DEVNULL hides output to keep the CLI clean
            subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            success = True
            break
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            error_msg = str(e)
            continue

    # Fallback to manual removal if pip commands fail
    # This ensures the aph folder in uv venv/site-packages and aph_cli-* are removed
    if not success:
        try:
            site_packages = site.getsitepackages()
            if hasattr(site, "getusersitepackages"):
                site_packages.append(site.getusersitepackages())

            removed_something = False
            for sp in site_packages:
                sp_path = Path(sp)
                if not sp_path.exists():
                    continue
                
                # Remove main module directory
                aph_dir = sp_path / "aph"
                if aph_dir.exists() and aph_dir.is_dir():
                    shutil.rmtree(aph_dir)
                    removed_something = True

                # Remove distribution info directories
                for meta_dir in sp_path.glob("aph_cli-*"):
                    if meta_dir.is_dir():
                        shutil.rmtree(meta_dir)
                        removed_something = True

            if removed_something:
                success = True
        except Exception as e:
            error_msg = f"Fallback manual removal also failed: {e}"

    if not success:
        return False, f"Failed to uninstall aph-cli package: {error_msg}"
        
    return True, "Uninstalled APH and removed .agent/ directory."
