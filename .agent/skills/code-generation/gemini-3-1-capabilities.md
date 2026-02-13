# Gemini 3.1 Capabilities (2026-02)

## 🎯 Overview
Gemini 3.1 introduces native infinite context and multi-modal reasoning, significantly altering how we approach large-scale refactoring and architecture analysis.

## ♾️ Infinite Context
**Capability**: The model can now ingest entire codebases without token limits or RAG retrieval steps.
**Usage**:
- **Repo-Wide Analysis**: "Read the entire `src/` directory and map the dependency graph."
- **Legacy Refactoring**: "Identify all deprecated API usages across 500 files and propose a migration plan."
- **Prompt**: `@codebase (full) explain the authentication flow` (No longer needs chunking).

## 👁️ Multi-modal Reasoning
**Capability**: Native understanding of UI screenshots alongside code.
**Usage**:
- **Visual Debugging**: Upload a screenshot of a UI bug + the React component. Gemini 3.1 correlates the visual artifact with the CSS/JSX line.
- **Design Implementation**: "Implement this Figma design pixel-perfectly."

## 🚀 Recommended Workflow
1. **Context Loading**: Use the `infinity-loader` tool to dump the repo into context.
2. **Analysis**: Ask high-level architectural questions.
3. **Execution**: Use standard code generation for specific files.
