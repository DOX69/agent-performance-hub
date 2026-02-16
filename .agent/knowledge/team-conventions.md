# Team Conventions

## Code Style
- Follow PEP 8 for Python.
- Follow Airbnb Style Guide for JavaScript/TypeScript.
- Use `pre-commit` hooks for automatic checks.

## Git Workflow
- **Branching**: Feature branches from `main` (`feat/`, `fix/`, `chore/`).
- **Commit Messages**: Conventional Commits (`feat: add login`, `fix: resolve crash`).
- **PRs**: Require 1 review, CI passing.

## Naming
- **Files**: `snake_case.py`, `kebab-case.ts`, `PascalCase.tsx`.
- **Variables**: `snake_case` (Python), `camelCase` (JS/TS).
- **Classes**: `PascalCase`.

## File Organization
- Colocate tests with code or in `tests/` folder.
- Group by feature rather than type where possible.

## Global Rules
### Test-Driven Development (TDD) using test-driven-development skill
> [!IMPORTANT]
> When implementing a new feature or fixing a bug, you **MUST** follow this workflow:
> 1. **Create a failing test first** (Red) - Prove the feature is missing or the bug exists.
> 2. **Implement the code** (Green) - Write the minimal code to make the test pass.
> 3. **Verify locally** - Run the specific test case.
> 4. **Verify suite** - Run all tests (`pytest tests/`) to ensure no regressions.

### Test Preservation
> [!CAUTION]
> **NEVER** modify or remove a failing test that is already in the suite to make the suite pass.
> - If a test fails, the **implementation** is wrong, not the test.
> - You must **ALWAYS** ask for user validation before modifying any existing test logic.
> - Tests are the source of truth.
