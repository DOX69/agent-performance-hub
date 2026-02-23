import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from aph.installer import uninstall_aph

def test_uninstall_aph_removes_agent_dir_and_calls_pip():
    # Setup mocks
    mock_project_path = MagicMock(spec=Path)
    mock_agent_dir = MagicMock(spec=Path)
    
    with patch("aph.installer.get_project_agent_dir", return_value=mock_agent_dir) as mock_get_dir, \
         patch("shutil.rmtree") as mock_rmtree, \
         patch("subprocess.check_call") as mock_subprocess:
        
        # Setup the mock agent dir to exist
        mock_agent_dir.exists.return_value = True
        
        # Execute
        success, message = uninstall_aph(mock_project_path)
        
        # Verify
        assert success is True
        assert "Uninstalled" in message
        mock_rmtree.assert_called_once_with(mock_agent_dir)
        import sys
        mock_subprocess.assert_called_once_with([sys.executable, "-m", "pip", "uninstall", "aph-cli", "-y"], stdout=-3, stderr=-3)

def test_uninstall_aph_handles_missing_agent_dir():
    # Setup mocks
    mock_project_path = MagicMock(spec=Path)
    mock_agent_dir = MagicMock(spec=Path)
    
    with patch("aph.installer.get_project_agent_dir", return_value=mock_agent_dir) as mock_get_dir, \
         patch("shutil.rmtree") as mock_rmtree, \
         patch("subprocess.check_call") as mock_subprocess:
        
        # Setup the mock agent dir to NOT exist
        mock_agent_dir.exists.return_value = False
        
        # Execute
        success, message = uninstall_aph(mock_project_path)
        
        # Verify
        assert success is True
        mock_rmtree.assert_not_called()
        import sys
        mock_subprocess.assert_called_once_with([sys.executable, "-m", "pip", "uninstall", "aph-cli", "-y"], stdout=-3, stderr=-3)

def test_uninstall_cli_command():
    from click.testing import CliRunner
    from aph.cli import main
    
    runner = CliRunner()
    
    # Mock uninstall_aph to return success
    with patch("aph.installer.uninstall_aph", return_value=(True, "Uninstalled APH")) as mock_uninstall:
        # Test with confirmation (input "y")
        result = runner.invoke(main, ["uninstall"], input="y\n")
        assert result.exit_code == 0
        assert "This will remove the .agent/ directory and uninstall the 'aph' package." in result.output
        mock_uninstall.assert_called_once()
        
    # Mock uninstall_aph again
    with patch("aph.installer.uninstall_aph", return_value=(True, "Uninstalled APH")) as mock_uninstall:
        # Test with --force
        result = runner.invoke(main, ["uninstall", "--force"])
        assert result.exit_code == 0
        mock_uninstall.assert_called_once()
        
    # Mock uninstall_aph again
    with patch("aph.installer.uninstall_aph", return_value=(True, "Uninstalled APH")) as mock_uninstall:
        # Test abort (input "n")
        result = runner.invoke(main, ["uninstall"], input="n\n")
        assert result.exit_code == 0
        assert "Cancelled" in result.output
        mock_uninstall.assert_not_called()
