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
