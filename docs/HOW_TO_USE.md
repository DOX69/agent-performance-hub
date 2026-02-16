# How To Use `agent-performance-hub`

This guide explains how to leverage the skills, knowledge, and methodology from this repository in your other projects (e.g., specific web apps, data pipelines).  

**I recommend using strategy 4 for new projects using uv**.

## Strategy 1: The "Reference" Approach (Recommended for Antigravity)

In Google Antigravity or your IDE, simple keep this repository cloned in a known location (e.g., `~/code/agent-performance-hub`).

When working on another project, you can instruct your agent:

> "I want to implement a new feature. Please refer to `~/code/agent-performance-hub/.agent/skills/code-generation/web-app-vibe-coding.md` for the coding style."

**Pros:**
- Single source of truth.
- Updates to the hub are immediately available.
- No file duplication.

## Strategy 2: Git Submodules (For Strict Versioning)

If you want to enforce that a project uses a specific version of your agent skills:

1.  **Add submodule**:
    ```bash
    cd my-new-project
    git submodule add https://github.com/DOX69/agent-performance-hub.git .agent-hub
    ```

2.  **Symlink relevant skills**:
    ```bash
    mkdir -p .agent/skills
    ln -s ../.agent-hub/.agent/skills/code-generation/web-app-vibe-coding.md .agent/skills/vibe-coding.md
    ```

**Pros:**
- Project A can use v1.0 skills while Project B uses v2.0.
- reproducible builds.

**Cons:**
- More complex git workflow.

## Strategy 3: Copy-Paste (Simple & Custom)

Simply copy the relevant `.agent` folder or specific Markdown files into your new project.

```bash
cp -r ~/code/agent-performance-hub/.agent/skills/code-generation/web-app-vibe-coding.md ./docs/guidelines.md
```

**Pros:**
- Simple.
- Allows project-specific customization without affecting the hub.

**Cons:**
- Drift from the main hub updates.

## Strategy 4: Start from Scratch with `uv` (Fastest)

If you are starting a completely new project and want a managed virtual environment:

1. **Install uv** (if you haven't): [Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)
2. **Initialize and Install**:
    ```bash
    mkdir my-new-agent-project
    cd my-new-agent-project
    uv init
    uv venv .venv
    source .venv/Scripts/activate  # On Windows: .venv\Scripts\activate
    
    uv pip install git+https://github.com/DOX69/agent-performance-hub.git
    aph init
    ```

---

## Retrieving Specific Skills on Demand

If you are in an IDE and want to "install" a skill:

1.  **List available skills**:
    Run `ls ~/code/agent-performance-hub/.agent/skills/**/*.md`

2.  **Read/Apply**:
    Ask your agent: "Load the 'data-pipelines' skill from the agent-performance-hub."

The agent will read the file and adapt its behavior instantly.
