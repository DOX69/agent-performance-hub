"""Tests for aph.cli — CLI commands via click CliRunner."""

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
    """Verify `aph version` command."""

    def test_shows_version(self, runner):
        result = runner.invoke(main, ["version"])
        assert result.exit_code == 0
        assert "aph" in result.output
        assert "0.1.0" in result.output


class TestHelp:
    """Verify `aph --help` output."""

    def test_main_help(self, runner):
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "APH" in result.output
        assert "Agent Performance Hub" in result.output

    def test_init_help(self, runner):
        result = runner.invoke(main, ["init", "--help"])
        assert result.exit_code == 0
        assert "--skills" in result.output

    def test_list_help(self, runner):
        result = runner.invoke(main, ["list", "--help"])
        assert result.exit_code == 0
        assert "--installed" in result.output
        assert "--category" in result.output

    def test_add_help(self, runner):
        result = runner.invoke(main, ["add", "--help"])
        assert result.exit_code == 0

    def test_search_help(self, runner):
        result = runner.invoke(main, ["search", "--help"])
        assert result.exit_code == 0

    def test_remove_help(self, runner):
        result = runner.invoke(main, ["remove", "--help"])
        assert result.exit_code == 0

    def test_update_help(self, runner):
        result = runner.invoke(main, ["update", "--help"])
        assert result.exit_code == 0

    def test_info_help(self, runner):
        result = runner.invoke(main, ["info", "--help"])
        assert result.exit_code == 0


class TestInit:
    """Verify `aph init` command."""

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


class TestList:
    """Verify `aph list` command."""

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
    """Verify `aph search` command."""

    def test_search_existing(self, runner):
        result = runner.invoke(main, ["search", "docker"])
        assert result.exit_code == 0
        assert "docker" in result.output.lower()

    def test_search_nonexistent(self, runner):
        result = runner.invoke(main, ["search", "xyzzy-nonexistent-gibberish"])
        assert result.exit_code == 0
        assert "No skills matching" in result.output


class TestAdd:
    """Verify `aph add` command."""

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
    """Verify `aph remove` command."""

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
    """Verify `aph update` command."""

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
    """Verify `aph info` command."""

    def test_info_existing_skill(self, runner):
        result = runner.invoke(main, ["info", "brainstorming"])
        assert result.exit_code == 0
        assert "brainstorming" in result.output

    def test_info_nonexistent_skill(self, runner):
        result = runner.invoke(main, ["info", "nonexistent-xyz"])
        assert result.exit_code != 0
        assert "not found" in result.output.lower()
