# Antigravity IDE Agent Rules

This document outlines the standard operating procedures and specific rules for agents operating within the Google Antigravity IDE environment.

## 1. Review-Driven Development
> [!IMPORTANT]
> - By default, adopt a **Review-Driven Development** approach.
> - When generating significant changes, designing architecture, or modifying sensitive functionality, explicitly request user review.
> - Ensure changes are segmented into verifiable, reviewable chunks rather than monolithic pull requests.

## 2. Agent Interaction Modes
> [!NOTE]
> - **Planning Mode:** Use this mode for complex, multi-step tasks. Create task plans (`task.md`), implementation guides, and walkthroughs. Allow user intervention and feedback at each crucial conceptual step before proceeding with execution.
> - **Fast/Execution Mode:** Use this mode for predictable, well-defined tasks (e.g., executing terminal commands during a standard setup), where immediate execution accelerates development without risking system stability.

## 3. Security and Execution Policies
> [!CAUTION]
> - **Secure Mode:** Always respect the IDE's secure mode constraints. Do not actively attempt to bypass network restrictions or file level sandboxes.
> - **JavaScript Execution:** When utilizing browser automation tools, adhere to the active JavaScript execution policy. If disabled or set to 'request review', do not blindly execute untrusted JS.
> - **Command Execution:** Do not auto-execute potentially destructive bash/terminal commands. Ensure `SafeToAutoRun` is strictly `false` for actions like deleting files, mutating external state, or modifying core infrastructure unless it is part of a verified workflow.

## 4. Workspaces and Multi-Agent Orchestration
- Rely on the active workspaces provided in the context metadata (`[URI] -> [CorpusName]`).
- Write project files solely within these designated absolute paths. Avoid writing inside temporary directories, the `.gemini` dir, or Desktop unless explicitly stated by the user.
