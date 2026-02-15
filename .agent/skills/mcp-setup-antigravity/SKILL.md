---
name: mcp-setup-antigravity
description: Use this skill to learn how to add new MCP servers to the Antigravity configuration.
---

# MCP Setup for Antigravity

This skill documents the process of adding new Model Context Protocol (MCP) servers to the Antigravity configuration.

## Configuration File Location

The main configuration file is located at:
`c:\Users\ggrft\.gemini\antigravity\mcp_config.json`

## Adding a New Server

To add a new MCP server, you need to modify the `mcpServers` object in the JSON file. Each server entry requires a unique key (the server name) and a configuration object.

### Configuration Object Structure

```json
"server-name": {
  "command": "executable-command",
  "args": ["arg1", "arg2"],
  "env": {
    "ENV_VAR_NAME": "value"
  }
}
```

- **command**: The executable to run (e.g., `node`, `npx`, `docker`, `python`).
- **args**: An array of arguments to pass to the command.
- **env**: (Optional) An object containing environment variables required by the server.

### Example: NotebookLM

Here is an example of the NotebookLM configuration:

```json
"notebooklm": {
  "command": "npx",
  "args": [
    "-y",
    "notebooklm-mcp-server"
  ],
  "env": {
    "SHOW_BROWSER": "true",
    "HEADLESS": "false",
    "NOTEBOOKLM_PROFILE": "full"
  }
}
```

## Restarting

After modifying `mcp_config.json`, you must restart the Antigravity application (or reloading the window) for the changes to take effect.

## Troubleshooting

- Ensure the JSON syntax is valid.
- Verify that the `command` is available in your system's PATH.
- Check the server's documentation for required environment variables.
