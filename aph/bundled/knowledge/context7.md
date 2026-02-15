# Context7

## Overview
Context7 is an advanced context retrieval and management system designed to optimize the information provided to AI agents. It acts as a bridge between your knowledge base and the LLM's context window.

## Key Features
- **Semantic Search**: Retrieval of relevant code snippets and documentation.
- **Context Optimization**: Filtering and compression of context to save tokens.
- **MCP Integration**: Works seamlessly with Model Context Protocol.

## Usage in this Project
- **API Key**: `ctx7sk-...` (Managed via Environment Variables).
- **Integration**: Used by `mcp-server-context7` to fetch realtime documentation.

## Best Practices
- Always prefer Context7 retrieval over dumping full files into context.
- Use specific queries vs broad topics.
