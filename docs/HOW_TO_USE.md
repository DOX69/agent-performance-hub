# How To Use `agent-performance-hub`

This guide explains how to leverage the skills, knowledge, and methodology from this repository in your other projects.

The **recommended and most efficient way** to use these skills is via the `aph` CLI.

## Installation using `uv` (Recommended)

To set up the skills in a new or existing project, use `uv` for a fast installation:

1. **Install uv** (if you haven't): [Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)
2. **Initialize and Install**:
    ```bash
    # Ensure you are in your project directory
    uv init  # If it's a new Python project
    uv venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    
    # Install the CLI tool
    uv pip install "git+https://github.com/DOX69/agent-performance-hub.git@main"
    
    # Initialize the basic skills framework
    aph init
    ```

When you run `aph init`, this creates an `.agent/` folder containing core skills like `@brainstorming` and `@clean-code`.

## Adding Specific Skills

Once initialized, use the CLI to add the specialized skills you need for your task:

1. **Search for a skill**:
    ```bash
    aph list
    aph search data-pipelines
    ```

2. **Install the skill**:
    ```bash
    aph add data-pipelines
    ```

3. **Use the skill**:
   In your AI Assistant (like Antigravity or Claude Code), you can simply mention the installed skill.
   
   > "I want to implement a new feature. Please refer to `@data-pipelines` (or `.agent/skills/data-pipelines/SKILL.md`) for the patterns."

The agent will read the local file and adapt its behavior instantly.

## ⚠️ Troubleshooting `uv pip install` Version Issues

If you notice `aph version` reports a `.dev` version (e.g., `0.1.dev38...`) instead of the official release tag from GitHub:
This happens because `uv` skips downloading Git tags during installation to ensure blazing-fast speed. `aph-cli` uses `setuptools_scm` to deduce the version from Git tags, so without them, it defaults to counting commits.

**How to resolve this:**
Force `uv` to resolve the literal tag by bypassing the cache:
```bash
uv cache clean
uv pip install "git+https://github.com/DOX69/agent-performance-hub.git@v0.1.4"
```

## Why use the CLI instead of Copy-Pasting?
- **Updates**: Run `aph update` at any time to pull the latest improvements from the centralized hub.
- **Consistency**: The `aph` CLI guarantees you get the complete structure for a skill, including example scripts, templates, and constraints.
- **Cleanliness**: Avoids adding hundreds of skills to your project by cherry-picking only what you need.
