# Global Rules

These are the core global rules that all AI agents must strictly adhere to when functioning within this repository.

## 1. Test-Driven Development (TDD) Workflow
> [!IMPORTANT]
> When implementing a new feature or fixing a bug, you **MUST** follow this workflow:
> 1. **Red (Fail):** Create a failing test first. This proves the feature is missing or verifies the bug exists.
> 2. **Green (Pass):** Implement the minimal code required to make the test pass. Do not over-engineer.
> 3. **Refactor:** Improve the code without changing its behavior, ensuring the tests remain green.
> 4. **Verify Locally:** Run the specific test case using the appropriate test runner.
> 5. **Verify Suite:** Run all tests (e.g., `pytest tests/`) to ensure no regressions were introduced.

## 2. Test Preservation rules
> [!CAUTION]
> **NEVER** modify, comment out, or remove a failing test that is already in the suite simply to make the suite pass.
> - If a test fails, assume the **implementation** is wrong, not the test.
> - You must **ALWAYS** ask for explicit user validation before modifying any existing test logic.
> - Tests act as the ultimate source of truth for features and behavior in this repository.

## 3. Agent Usage & Skill Management
> [!IMPORTANT]
> **Always prioritize `aph` for skills.**
> - Use `aph list` and `aph search <term>` to dynamically find the best skills needed for your tasks.
> - Use `aph --help` to understand command usage and capabilities.
> - **Always activate the virtual environment** (`source .venv/bin/activate` or `.\.venv\Scripts\activate` on Windows) before using `aph`.

> [!NOTE]
> **Handling Missing Skills**
> If an `aph search` fails to find an essential skill for your task:
> 1. Do not manually create a new skill in the `.agent/skills/` directory unless you are explicitly acting as the maintainer for that task.
> 2. Add the missing skill to the **TODO list** in `prompts/jules_weekly_watch.md` under the "Requested Skills" section.
> 3. Provide a brief, descriptive reason about what is needed and why.
> 4. Jules will create it during the next weekly maintenance cycle using the `expert-skill-creator` tool to ensure quality and avoid duplication.
