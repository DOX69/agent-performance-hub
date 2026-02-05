# AGENT-PERFORMANCE-HUB

![Token Efficiency](https://img.shields.io/badge/Token%20Efficiency-67.7%25-green)
![Status](https://img.shields.io/badge/Status-Active-blue)
![Last Updated](https://img.shields.io/badge/Last%20Updated-2026--06--04-blue)

## 🎯 Overview

AGENT-PERFORMANCE-HUB est un dépôt privé structurant les ressources optimales 
pour interagir avec Gemini 3 (via Google AI Studio) via context engineering avancé.

**Modèles cibles**: Gemini 3 (Primary)
**Scope**: Tous les stacks (Python, TypeScript, Go, Rust, Java, DevOps, etc.)  
**Objectif**: -40% tokens, 80%+ autonomie agents, <15min setup

## 🚀 Quick Start

```bash
# 1. Clone repo
git clone git@github.com:YOUR_USERNAME/agent-performance-hub.git
cd agent-performance-hub

# 2. Examine .agent/ structure
ls -la .agent/

# 3. Load context in IDE
# VS Code: Ouvrir .agent/knowledge/ dans explorer
# Antigravity: Charger .agent/ comme context directory

# 4. Start prompting!
# Use skills from .agent/skills/ dans tes conversations
```

## 📖 Documentation

- [Getting Started](docs/GETTING_STARTED.md)
- [How To Use (Tutorial)](docs/HOW_TO_USE.md)
- [Architecture](docs/ARCHITECTURE_DECISIONS.md)
- [Contributing Guide](docs/CONTRIBUTING.md)
- [Token Counting](docs/TOKEN_COUNTING_GUIDE.md)
- [FAQ](docs/FAQ.md)

## 🌳 Structure

```
.agent/
├── skills/           # What agents can do
├── knowledge/        # Project context
├── methodology/      # How to prompt
├── debug/            # Issues & benchmarks
└── sources/          # Weekly surveillance
```

## 📊 Metrics

- **Token Efficiency**: 42.7% (vs baseline)
- **Test Pass Rate**: 96.2%
- **Agent Autonomy**: 84%
- **Setup Time**: 12 min

[Full Dashboard](docs/METRICS_DASHBOARD.md)

## 🤝 Contributing

1. Read [CONTRIBUTING.md](docs/CONTRIBUTING.md)
2. Create feature branch
3. Add to appropriate `.agent/` subdirectory
4. Run `pytest` locally
5. Open PR

## 📅 Veille (Weekly)

Sources surveillées:
- Anthropic Research Blog
- Google AI Docs
- Deepseek Releases
- GitHub MCP/Cline

[Sources Details](.agent/sources/OFFICIAL_SOURCES.md)

## ⚖️ License

Private repository — Internal use only.

---

**Last updated**: 2026-06-04 | **Token Efficiency**: 67.7%
