"""Integration tests for APH CLI help output using subprocess."""

import subprocess
import sys
import os
import pytest


def run_aph_cmd(args):
    """Run aph command via subprocess and return output."""
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    env["PYTHONIOENCODING"] = "utf-8"
    cmd = [sys.executable, "-m", "aph.cli"] + args
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env
    )
    return result


class TestCliHelpIntegration:
    """Verify CLI help works in real execution context."""

    def test_main_help_output(self):
        """Test `python -m aph --help`."""
        result = run_aph_cmd(["--help"])
        if result.returncode != 0:
            print(f"\nSTDERR:\n{result.stderr}")
        assert result.returncode == 0
        output = result.stdout
        
        # Verify structured sections
        assert "Agent Performance Hub" in output
        assert "PURPOSE:" in output
        assert "USAGE:" in output
        assert "COMMANDS:" in output
        assert "EXIT_CODES:" in output
        assert "EXAMPLES:" in output
        
        # Verify core commands list
        assert "init" in output
        assert "list" in output
        assert "search" in output
        assert "add" in output
        
    def test_main_help_short_flag(self):
        """Test `python -m aph -h`."""
        result = run_aph_cmd(["-h"])
        if result.returncode != 0:
            print(f"\nSTDERR:\n{result.stderr}")
        assert result.returncode == 0
        assert "Agent Performance Hub" in result.stdout
        
    def test_subcommand_help_structured(self):
        """Test `python -m aph add --help` has structure."""
        result = run_aph_cmd(["add", "--help"])
        if result.returncode != 0:
            print(f"\nSTDERR:\n{result.stderr}")
        assert result.returncode == 0
        output = result.stdout
        
        assert "PURPOSE:" in output
        assert "Add new skills" in output
        assert "ARGUMENTS:" in output
        assert "PRECONDITIONS:" in output
        
    def test_invalid_command_help_suggestion(self):
        """Test running invalid command shows help/error."""
        result = run_aph_cmd(["invalid-cmd"])
        assert result.returncode != 0
        assert "No such command" in result.stderr
