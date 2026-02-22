import os
import glob
import pytest

def test_no_pypi_pkg_github_com():
    """
    Ensure no GitHub workflows attempt to publish to pypi.pkg.github.com,
    as GitHub Packages does not natively support the PyPI protocol.
    """
    workflows_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".github", "workflows")
    
    # Check if the directory exists - if not, skip test or fail
    if not os.path.exists(workflows_dir):
        pytest.skip(f"Workflows directory not found: {workflows_dir}")
        
    workflow_files = glob.glob(os.path.join(workflows_dir, "*.yml"))
    workflow_files += glob.glob(os.path.join(workflows_dir, "*.yaml"))
    
    assert len(workflow_files) > 0, "No workflow files found to test."

    for workflow_file in workflow_files:
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Assert that the problematic URL is not in the workflow file.
            assert "https://pypi.pkg.github.com" not in content, (
                f"Workflow file {os.path.basename(workflow_file)} contains unsupported "
                f"'https://pypi.pkg.github.com' PyPI registry URL."
            )
