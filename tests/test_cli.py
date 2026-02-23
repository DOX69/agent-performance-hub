"""Tests for aph.cli — CLI commands via click CliRunner."""

import re
import json
import pytest
from pathlib import Path
from click.testing import CliRunner

from aph.cli import main


@pytest.fixture
def runner():
    """Create a Click test runner."""
    return CliRunner()


@pytest.fixture
def isolated_runner(tmp_path):
    """Create a Click test runner that changes to a temp directory."""
    runner = CliRunner()
    return runner, tmp_path


class TestVersion:
    """Verify aph version command."""

    def test_shows_version(self, runner):
        result = runner.invoke(main, ["version"])
        assert result.exit_code == 0
        assert "aph" in result.output
        # Check for dynamic version format:
        # Matches: 0.1.2, 0.1.3.dev1, 0.1.dev1+g...
        # The key is at least "digit.digit" at the start.
        assert re.search(r"\d+\.\d+", result.output)

    def test_version_dev_fallback_format(self, runner, monkeypatch):
        """Verify version command handles setuptools_scm dev fallback gracefully."""
        # Mock aph.__version__ to a dev version
        from aph import cli
        monkeypatch.setattr(cli, "__version__", "0.1.dev38+gf54a9888e.d20260223")
        result = runner.invoke(main, ["version"])
        assert result.exit_code == 0
        assert "aph v0.1.dev38+gf54a9888e.d20260223" in result.output
        assert re.search(r"dev\d+\+g[a-f0-9]+", result.output)


class TestHelp:
    """Verify aph --help  output."""

    def test_main_help(self, runner):
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "APH" in result.output
        assert "Agent Performance Hub" in result.output
        assert "PURPOSE:" in result.output
        assert "USAGE:" in result.output
        assert "EXIT_CODES:" in result.output
        assert "EXAMPLES:" in result.output

    def test_main_help_short_flag(self, runner):
        """Verify -h works as alias for --help."""
        result = runner.invoke(main, ["-h"])
        assert result.exit_code == 0
        assert "Agent Performance Hub" in result.output

    def test_init_help(self, runner):
        result = runner.invoke(main, ["init", "--help"])
        assert result.exit_code == 0
        assert "PURPOSE:" in result.output
        assert "PRECONDITIONS:" in result.output
        assert "--skills" in result.output

    def test_list_help(self, runner):
        result = runner.invoke(main, ["list", "--help"])
        assert result.exit_code == 0
        assert "PURPOSE:" in result.output
        assert "--installed" in result.output
        assert "--category" in result.output

    def test_add_help(self, runner):
        result = runner.invoke(main, ["add", "--help"])
        assert result.exit_code == 0
        assert "PURPOSE:" in result.output
        assert "ARGUMENTS:" in result.output
        assert "PRECONDITIONS:" in result.output

    def test_search_help(self, runner):
        result = runner.invoke(main, ["search", "--help"])
        assert result.exit_code == 0
        assert "PURPOSE:" in result.output
        assert "ARGUMENTS:" in result.output

    def test_remove_help(self, runner):
        result = runner.invoke(main, ["remove", "--help"])
        assert result.exit_code == 0
        assert "PURPOSE:" in result.output
        assert "--force" in result.output

    def test_update_help(self, runner):
        result = runner.invoke(main, ["update", "--help"])
        assert result.exit_code == 0
        assert "PURPOSE:" in result.output
        assert "ARGUMENTS:" in result.output

    def test_info_help(self, runner):
        result = runner.invoke(main, ["info", "--help"])
        assert result.exit_code == 0
        assert "PURPOSE:" in result.output
        assert "OUTPUT:" in result.output


class TestInit:
    """Verify aph init command."""

    def test_init_creates_agent_dir(self, isolated_runner, monkeypatch):
        runner, tmp_path = isolated_runner
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(main, ["init"])
        assert result.exit_code == 0
        assert (tmp_path / ".agent").exists()
        assert "Initialized" in result.output or "✅" in result.output

    def test_init_with_custom_skills(self, isolated_runner, monkeypatch):
        runner, tmp_path = isolated_runner
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(main, ["init", "--skills", "brainstorming,clean-code"])
        assert result.exit_code == 0
        assert (tmp_path / ".agent" / "skills" / "brainstorming").exists()
        assert (tmp_path / ".agent" / "skills" / "clean-code").exists()

    def test_init_fails_twice(self, isolated_runner, monkeypatch):
        runner, tmp_path = isolated_runner
        monkeypatch.chdir(tmp_path)
        runner.invoke(main, ["init"])
        result = runner.invoke(main, ["init"])
        assert result.exit_code != 0

    def test_init_matches_bundled_subdirs(self, isolated_runner, monkeypatch):
        """Verify that aph init creates all subdirectories present in the bundled .agent repo."""
        from aph.config import BUNDLED_AGENT_ROOT, INIT_SUBDIRS, AGENT_DIR_NAME
        
        runner, tmp_path = isolated_runner
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(main, ["init"])
        assert result.exit_code == 0
        
        # Get actual directories in the bundled .agent directory
        bundled_dirs = [d.name for d in BUNDLED_AGENT_ROOT.iterdir() if d.is_dir() and not d.name.startswith("__")]
        
        # Ensure that ALL directories found in the bundled .agent are configured in INIT_SUBDIRS
        # and are successfully created by `aph init`
        created_agent_dir = tmp_path / AGENT_DIR_NAME
        for bundled_dir in bundled_dirs:
            assert bundled_dir in INIT_SUBDIRS, f"Bundled directory '{bundled_dir}' is missing from INIT_SUBDIRS in config.py"
            created_subdir = created_agent_dir / bundled_dir
            assert created_subdir.exists(), f"Directory '{bundled_dir}' was not created by aph init"
            assert len(list(created_subdir.iterdir())) > 0, f"Directory '{bundled_dir}' is empty, it should be populated."


class TestList:
    """Verify aph list command."""

    def test_list_all_skills(self, runner):
        result = runner.invoke(main, ["list"])
        assert result.exit_code == 0
        assert "brainstorming" in result.output

    def test_list_by_category(self, runner):
        result = runner.invoke(main, ["list", "--category", "security"])
        assert result.exit_code == 0

    def test_list_installed_requires_init(self, isolated_runner, monkeypatch):
        runner, tmp_path = isolated_runner
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(main, ["list", "--installed"])
        assert result.exit_code != 0
        assert "not initialized" in result.output.lower()

    def test_list_installed_after_init(self, isolated_runner, monkeypatch):
        runner, tmp_path = isolated_runner
        monkeypatch.chdir(tmp_path)
        runner.invoke(main, ["init"])
        result = runner.invoke(main, ["list", "--installed"])
        assert result.exit_code == 0
        assert "brainstorming" in result.output


class TestSearch:
    """Verify aph search command."""

    def test_search_existing(self, runner):
        result = runner.invoke(main, ["search", "docker"])
        assert result.exit_code == 0
        assert "docker" in result.output.lower()

    def test_search_nonexistent(self, runner):
        result = runner.invoke(main, ["search", "xyzzy-nonexistent-gibberish"])
        assert result.exit_code == 0
        assert "No skills matching" in result.output


class TestAdd:
    """Verify aph add command."""

    def test_add_requires_init(self, isolated_runner, monkeypatch):
        runner, tmp_path = isolated_runner
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(main, ["add", "docker-expert"])
        assert result.exit_code != 0
        assert "not initialized" in result.output.lower()

    def test_add_skill(self, isolated_runner, monkeypatch):
        runner, tmp_path = isolated_runner
        monkeypatch.chdir(tmp_path)
        runner.invoke(main, ["init"])
        result = runner.invoke(main, ["add", "docker-expert"])
        assert result.exit_code == 0
        assert (tmp_path / ".agent" / "skills" / "docker-expert").exists()

    def test_add_multiple_skills(self, isolated_runner, monkeypatch):
        runner, tmp_path = isolated_runner
        monkeypatch.chdir(tmp_path)
        runner.invoke(main, ["init"])
        result = runner.invoke(main, ["add", "docker-expert", "nestjs-expert"])
        assert result.exit_code == 0
        assert (tmp_path / ".agent" / "skills" / "docker-expert").exists()
        assert (tmp_path / ".agent" / "skills" / "nestjs-expert").exists()

    def test_add_nonexistent_skill(self, isolated_runner, monkeypatch):
        runner, tmp_path = isolated_runner
        monkeypatch.chdir(tmp_path)
        runner.invoke(main, ["init"])
        result = runner.invoke(main, ["add", "nonexistent-xyz"])
        assert "not found" in result.output.lower() or "❌" in result.output


class TestRemove:
    """Verify aph remove command."""

    def test_remove_requires_init(self, isolated_runner, monkeypatch):
        runner, tmp_path = isolated_runner
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(main, ["remove", "brainstorming"])
        assert result.exit_code != 0

    def test_remove_skill(self, isolated_runner, monkeypatch):
        runner, tmp_path = isolated_runner
        monkeypatch.chdir(tmp_path)
        runner.invoke(main, ["init"])
        result = runner.invoke(main, ["remove", "brainstorming", "--force"])
        assert result.exit_code == 0
        assert not (tmp_path / ".agent" / "skills" / "brainstorming").exists()


class TestUpdate:
    """Verify aph update command."""

    def test_update_requires_init(self, isolated_runner, monkeypatch):
        runner, tmp_path = isolated_runner
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(main, ["update"])
        assert result.exit_code != 0

    def test_update_all(self, isolated_runner, monkeypatch):
        runner, tmp_path = isolated_runner
        monkeypatch.chdir(tmp_path)
        runner.invoke(main, ["init"])
        result = runner.invoke(main, ["update"])
        assert result.exit_code == 0
        assert "Updated" in result.output

    def test_update_single(self, isolated_runner, monkeypatch):
        runner, tmp_path = isolated_runner
        monkeypatch.chdir(tmp_path)
        runner.invoke(main, ["init"])
        result = runner.invoke(main, ["update", "brainstorming"])
        assert result.exit_code == 0


class TestInfo:
    """Verify aph info command."""

    def test_info_existing_skill(self, runner):
        result = runner.invoke(main, ["info", "brainstorming"])
        assert result.exit_code == 0
        assert "brainstorming" in result.output

    def test_info_nonexistent_skill(self, runner):
        result = runner.invoke(main, ["info", "nonexistent-xyz"])
        assert result.exit_code != 0
        assert "not found" in result.output.lower()
