# Agentic Coding Updates (2026-05)

## 🎯 Overview
Integration of new capabilities from Gemini 3 and Claude Sonnet 4.5 to enhance code generation and agentic behavior.

## 💎 Gemini 3: Auto Browse & Side Panel
**Capability**: Native "Auto Browse" allows the model to interact with web pages directly via Chrome.
**Usage**:
- **Research**: "Go to react.dev and find the latest hook patterns."
- **Testing**: "Open localhost:3000 and verify the login flow."
- **Integration**: Use `google-chrome-ai` connector (mock) to drive the browser.

## 🧠 Claude Sonnet 4.5: Agent SDK
**Capability**: Enhanced reasoning and native computer use.
**Usage**:
- **Visual Validation**: "Look at this screenshot of the UI. Is the button centered?"
- **Complex Refactoring**: Use the Agent SDK to map out dependency graphs before touching code.
- **Token Efficiency**: Sonnet 4.5 is optimized for long-context coding sessions.

## 📦 MCP Integration (Model Context Protocol)
**Update**: Use `mcp-use` for connecting custom tools.
- **Pattern**: Expose local dev tools (database, logs) as MCP servers so the agent can query them directly.
- **Reference**: See `.agent/sources/archive/sources-2026-01.json`.

## 🛠️ Recommended Workflow
1. **Plan** with Claude Sonnet 4.5 (reasoning).
2. **Execute** browsing/research with Gemini 3 (speed + integration).
3. **Verify** with MCP-connected tools.
