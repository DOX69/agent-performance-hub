---
name: n8n-automation
description: "Expert in n8n workflow automation, covering self-hosted setup, node configuration, webhook handling, and AI agent integration."
---

# Skill: n8n Automation & Integration

## Objectifs
- Create complex, reliable automation workflows without heavy coding.
- Integrate various APIs and services (Google Sheets, Slack, GitHub, OpenAI).
- Deploy and manage self-hosted n8n instances.

## Setup & Hosting
- **Docker**: The recommended way to run n8n.
  ```bash
  docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8n/n8n
  ```
- **Environment Variables**:
  - `N8N_BASIC_AUTH_ACTIVE=true`
  - `N8N_BASIC_AUTH_USER=admin`
  - `N8N_BASIC_AUTH_PASSWORD=securepassword`
  - `WEBHOOK_URL=https://your-domain.com/`

## Key Concepts
- **Nodes**: The building blocks (Trigger, Action, Logic).
- **Function Item Node**: Use JavaScript for complex logic not covered by standard nodes.
- **Workflows**: JSON representation of the automation logic.

## AI Integration with MCP
- **Method**: Use n8n's "LangChain" nodes or standard HTTP Request nodes to call AI agents.
- **Agent Handoff**: Trigger an n8n workflow from an agent (via Webhook) to perform side-effects (sending emails, updating DBs).

## Best Practices
- **Error Handling**: Always use "Error Trigger" workflows or "Continue On Fail" settings.
- **Pin Data**: Use pinned data for easier debugging during development.
- **Credentials**: Never hardcode keys; use n8n Credential Manager.

## Exemples de Prompts Recommandés
- "Create an n8n workflow that watches for new GitHub issues and posts a summary to Slack."
- "Explain how to loop through a JSON array in n8n using the Split In Batches node."
- "Write a JavaScript function for the n8n Function node to parse this specific date format."
