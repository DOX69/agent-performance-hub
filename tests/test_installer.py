"""Tests for aph.installer — Skill installation, removal, and project init."""

import json
import pytest
import shutil
from pathlib import Path

from aph.installer import (
    get_installed_skills,
    get_manifest_path,
    get_project_agent_dir,
    init_project,
    install_skill,
    is_initialized,
    load_manifest,
    remove_skill,
    save_manifest,
    update_all_skills,
    update_skill,
)
from aph.config import AGENT_DIR_NAME, CORE_SKILLS


@pytest.fixture
def tmp_project(tmp_path):
    """Create a temporary project directory for testing."""
    project = tmp_path / "test-project"
    project.mkdir()
    return project


@pytest.fixture
def initialized_project(tmp_project):
    """Create and initialize a temporary project."""
    success, msg = init_project(project_path=tmp_project)
    assert success, f"Init failed: {msg}"
    return tmp_project


class TestGetProjectAgentDir:
    """Verify .agent/ path resolution."""

    def test_returns_path(self, tmp_project):
        result = get_project_agent_dir(tmp_project)
        assert isinstance(result, Path)

    def test_path_ends_with_agent(self, tmp_project):
        result = get_project_agent_dir(tmp_project)
        assert result.name == AGENT_DIR_NAME

    def test_path_is_under_project(self, tmp_project):
        result = get_project_agent_dir(tmp_project)
        assert str(result).startswith(str(tmp_project))


class TestManifest:
    """Verify manifest load/save operations."""

    def test_load_manifest_returns_default_when_missing(self, tmp_project):
        """Loading from a dir without manifest should return defaults."""
        manifest = load_manifest(tmp_project)
        assert isinstance(manifest, dict)
        assert manifest["installed_skills"] == []
        assert manifest["initialized_at"] is None

    def test_save_and_load_roundtrip(self, initialized_project):
        """Saving and loading a manifest should preserve data."""
        manifest = load_manifest(initialized_project)
        manifest["installed_skills"].append("test-skill")
        save_manifest(manifest, initialized_project)

        reloaded = load_manifest(initialized_project)
        assert "test-skill" in reloaded["installed_skills"]
        assert reloaded["updated_at"] is not None

    def test_save_sets_updated_at(self, initialized_project):
        """save_manifest should automatically set updated_at."""
        manifest = load_manifest(initialized_project)
        original_updated = manifest.get("updated_at")
        save_manifest(manifest, initialized_project)
        reloaded = load_manifest(initialized_project)
        assert reloaded["updated_at"] is not None


class TestIsInitialized:
    """Verify initialization detection."""

    def test_not_initialized_empty_dir(self, tmp_project):
        assert is_initialized(tmp_project) is False

    def test_initialized_after_init(self, initialized_project):
        assert is_initialized(initialized_project) is True


class TestInitProject:
    """Verify project initialization."""

    def test_init_creates_agent_dir(self, tmp_project):
        success, msg = init_project(project_path=tmp_project)
        assert success
        assert (tmp_project / ".agent").exists()

    def test_init_creates_subdirs(self, tmp_project):
        init_project(project_path=tmp_project)
        for subdir in ["skills", "knowledge", "methodology", "debug", "sources"]:
            assert (tmp_project / ".agent" / subdir).exists(), f"Missing: .agent/{subdir}"

    def test_init_creates_manifest(self, tmp_project):
        init_project(project_path=tmp_project)
        manifest_path = tmp_project / ".agent" / ".aph-manifest.json"
        assert manifest_path.exists()
        manifest = json.loads(manifest_path.read_text())
        assert "installed_skills" in manifest
        assert "initialized_at" in manifest

    def test_init_creates_agent_readme(self, tmp_project):
        init_project(project_path=tmp_project)
        readme_path = tmp_project / ".agent" / "README_AGENT.md"
        assert readme_path.exists()
        content = readme_path.read_text(encoding="utf-8")
        assert "APH" in content
        assert "Agent Guide" in content
        assert "aph search" in content

    def test_init_installs_core_skills(self, tmp_project):
        init_project(project_path=tmp_project)
        installed = get_installed_skills(tmp_project)
        for skill in CORE_SKILLS:
            assert skill in installed, f"Core skill '{skill}' not installed"

    def test_init_core_skill_dirs_exist(self, tmp_project):
        init_project(project_path=tmp_project)
        for skill in CORE_SKILLS:
            skill_dir = tmp_project / ".agent" / "skills" / skill
            assert skill_dir.exists(), f"Core skill dir missing: {skill}"
            assert (skill_dir / "SKILL.md").exists(), f"SKILL.md missing for: {skill}"

    def test_init_fails_if_already_initialized(self, initialized_project):
        """Double init should fail gracefully."""
        success, msg = init_project(project_path=initialized_project)
        assert not success
        assert "already initialized" in msg.lower()

    def test_init_with_custom_skills(self, tmp_project):
        """Init with custom skill list should install only those."""
        custom = ["brainstorming", "clean-code"]
        success, msg = init_project(project_path=tmp_project, skills=custom)
        assert success
        installed = get_installed_skills(tmp_project)
        assert set(installed) == set(custom)

    def test_init_returns_helpful_message(self, tmp_project):
        """Init message should include next steps."""
        success, msg = init_project(project_path=tmp_project)
        assert "aph list" in msg
        assert "aph add" in msg


class TestInstallSkill:
    """Verify individual skill installation."""

    def test_install_existing_skill(self, initialized_project):
        success, msg = install_skill("docker-expert", initialized_project)
        assert success
        assert (initialized_project / ".agent" / "skills" / "docker-expert").exists()

    def test_install_adds_to_manifest(self, initialized_project):
        install_skill("docker-expert", initialized_project)
        installed = get_installed_skills(initialized_project)
        assert "docker-expert" in installed

    def test_install_nonexistent_skill_fails(self, initialized_project):
        success, msg = install_skill("this-skill-does-not-exist-xyz", initialized_project)
        assert not success
        assert "not found" in msg.lower()

    def test_install_creates_skill_md(self, initialized_project):
        """Installed skill should have SKILL.md."""
        install_skill("docker-expert", initialized_project)
        assert (initialized_project / ".agent" / "skills" / "docker-expert" / "SKILL.md").exists()

    def test_reinstall_overwrites(self, initialized_project):
        """Reinstalling should not error — it overwrites."""
        install_skill("docker-expert", initialized_project)
        success, msg = install_skill("docker-expert", initialized_project)
        assert success

    def test_install_keeps_manifest_sorted(self, initialized_project):
        """Installed skills list should be alphabetically sorted."""
        install_skill("docker-expert", initialized_project)
        install_skill("algolia-search", initialized_project)
        installed = get_installed_skills(initialized_project)
        assert installed == sorted(installed)


class TestRemoveSkill:
    """Verify skill removal."""

    def test_remove_installed_skill(self, initialized_project):
        install_skill("docker-expert", initialized_project)
        success, msg = remove_skill("docker-expert", initialized_project)
        assert success
        assert not (initialized_project / ".agent" / "skills" / "docker-expert").exists()

    def test_remove_updates_manifest(self, initialized_project):
        install_skill("docker-expert", initialized_project)
        remove_skill("docker-expert", initialized_project)
        installed = get_installed_skills(initialized_project)
        assert "docker-expert" not in installed

    def test_remove_noninstalled_fails(self, initialized_project):
        success, msg = remove_skill("not-installed-xyz", initialized_project)
        assert not success
        assert "not installed" in msg.lower()


class TestUpdateSkill:
    """Verify skill update."""

    def test_update_installed_skill(self, initialized_project):
        """Updating an installed core skill should succeed."""
        success, msg = update_skill("brainstorming", initialized_project)
        assert success

    def test_update_noninstalled_fails(self, initialized_project):
        success, msg = update_skill("not-installed-xyz", initialized_project)
        assert not success


class TestUpdateAllSkills:
    """Verify bulk update."""

    def test_update_all_returns_counts(self, initialized_project):
        updated, errors, error_msgs = update_all_skills(initialized_project)
        assert updated == len(CORE_SKILLS)
        assert errors == 0
        assert error_msgs == []

    def test_update_all_preserves_manifest(self, initialized_project):
        """After update_all, installed skills should remain the same."""
        before = set(get_installed_skills(initialized_project))
        update_all_skills(initialized_project)
        after = set(get_installed_skills(initialized_project))
        assert before == after
