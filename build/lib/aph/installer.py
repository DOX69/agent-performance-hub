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
    SKILLS_SUBDIR,
    SOURCES_SUBDIR,
)


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
