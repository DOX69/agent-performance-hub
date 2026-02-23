# 🚀 APH — Agent Performance Hub

![Tests](https://img.shields.io/badge/Tests-122%20passed-brightgreen)
![Token Efficiency](https://img.shields.io/badge/Token%20Efficiency-67.7%25-green)
![Skills](https://img.shields.io/badge/Skills-241-blue)
![Status](https://img.shields.io/badge/Status-Private-orange)
![Last Updated](https://img.shields.io/badge/Last%20Updated-2026--02--23-blue)
![Lastest version](https://img.shields.io/badge/Latest%20version-v0.1.4-blue)

**A CLI tool for managing curated AI agent skills across all your projects.**

Install 241 skills for Gemini, Claude, and other AI agents — selectively, only what you need.

---

## 📋 Table of Contents

- [⚡ Quick Start](#-quick-start-3-steps)
- [📖 Commands](#-commands)
- [📦 What Gets Created](#-what-gets-created)
- [🎯 Core Skills](#-core-skills-installed-by-default)
- [🗂️ Skill Categories](#-skill-categories)
- [🔄 Updating Skills](#-updating-skills)
- [🛠️ Requirements](#-requirements)
- [🧪 Development & Testing](#-development--testing)
- [🤖 Automated Maintenance](#-automated-maintenance)
- [📝 Adding New Skills](#-adding-new-skills)
- [📚 Documentation](#-documentation)
- [📊 Metrics](#-metrics)
- [🤝 Collaboration](#-collaboration)
- [⚖️ License](#-license)
- [📅 Changelog](CHANGELOG.md)

---

## ⚡ Quick Start (3 steps)

### 1. Install

**Note:** Since this is a private package, you must configure authentication first.
👉 **[Read the Setup Guide](docs/REGISTRY_SETUP.md)**

```bash
# Recommended: Modern setup using 'uv'
# 1. Install uv: https://docs.astral.sh/uv/
uv init
uv venv .venv
source .venv/bin/activate  # Windows: .venv/Scripts/activate

# 2. Install APH CLI
uv pip install aph-cli
```

### 2. Initialize your project

```bash
cd your-project/
aph init
```

This creates `.agent/` with **6 core skills**: brainstorming, git-pushing, expert-skill-creator, clean-code, systematic-debugging, verification-before-completion.

### 3. Add skills you need

```bash
aph list                      # Browse all 241 skills
aph search docker             # Search by keyword
aph add docker-expert         # Install a skill
```

---

## 📖 Commands

| Command | Description |
|---------|-------------|
| `aph init` | Initialize `.agent/` with core skills |
| `aph init --skills a,b,c` | Initialize with custom skill set |
| `aph list` | List all available skills (241) |
| `aph list --installed` | Show only installed skills |
| `aph list --category security` | Filter by category |
| `aph search <query>` | Search by name, description, or tags |
| `aph add <skill> [skill2...]` | Install one or more skills |
| `aph remove <skill>` | Remove a skill |
| `aph update` | Update all installed skills |
| `aph update <skill>` | Update a specific skill |
| `aph info <skill>` | Show detailed info about a skill |
| `aph uninstall` | Completely remove APH and `.agent/` from project |
| `aph version` | Show CLI version |

> [!TIP]
> **Agent-friendly help** — Every command supports `--help` (or `-h`) with structured output designed for both humans and AI agents. Each help page includes **PURPOSE**, **USAGE**, **EXIT_CODES**, **PRECONDITIONS**, and **EXAMPLES** sections, so an agent can programmatically understand what a command does, what it expects, and how to handle errors.
>
> ```bash
> aph add --help    # See structured help for any command
> aph -h            # Short flag works too
> ```

---

## 📦 What Gets Created

When you run `aph init`, the following structure is created in your project:

```
your-project/
└── .agent/
    ├── skills/              # Installed skills (SKILL.md per skill)
    ├── knowledge/           # Project context (architecture, tech stack)
    ├── methodology/         # How agents should reason
    ├── debug/               # Error patterns, benchmarks
    ├── sources/             # Weekly surveillance sources
    └── .aph-manifest.json   # Tracks installed skills
```

---

## 🎯 Core Skills (installed by default)

| Skill | Purpose |
|-------|---------|
| `brainstorming` | Explore ideas before implementation |
| `git-pushing` | Stage, commit, and push with conventional commits |
| `expert-skill-creator` | Create new skills with scaffolding |
| `clean-code` | Pragmatic coding standards |
| `systematic-debugging` | Debug methodology before proposing fixes |
| `verification-before-completion` | Quality gate before claiming done |

Override defaults: `aph init --skills brainstorming,docker-expert,nestjs-expert`

---

## 🗂️ Skill Categories

| Category | Count | Examples |
|----------|-------|---------|
| Security | 30+ | penetration testing, XSS, SQL injection, IDOR |
| AI Agents | 25+ | LangGraph, CrewAI, RAG, prompt engineering |
| Marketing | 20+ | SEO, content, copywriting, analytics |
| Frontend | 15+ | React, Tailwind, 3D web, scroll experiences |
| Integrations | 12+ | Stripe, Shopify, Slack, Telegram, HubSpot |
| DevOps | 8+ | Docker, AWS, GCP, Vercel, GitHub Actions |
| Backend | 8+ | NestJS, Node.js, GraphQL, Prisma |
| Methodology | 10+ | TDD, architecture, code review, planning |
| Data | 6+ | PostgreSQL, Firebase, ClickHouse, NoSQL |
| Tools | 10+ | PDF, DOCX, XLSX, Playwright, browser automation |

Browse all: `aph list` or `aph list --category <name>`

---

## 🔄 Updating Skills

```bash
# Update the aph-cli package itself
uv pip install --upgrade aph-cli

# Update all installed skills in your project to latest
aph update

# Update a specific skill
aph update docker-expert
```

## 🛠️ Requirements

- **Python 3.11+**
- **Git**
- **[uv](https://docs.astral.sh/uv/)** (Recommended for high performance)
- **Access to this private repository**

### Authentication (Private Repo)
Since this is a private repo, you'll need to authenticate.
- **HTTPS (Recommended)**: Use a GitHub Personal Access Token (PAT) or Git Credential Manager.
- **SSH (Alternative)**: Ensure your SSH key is added to GitHub.
- **HTTPS (Recommended)**: Use a GitHub Personal Access Token (PAT) or Git Credential Manager.
- **SSH (Alternative)**: Ensure your SSH key is added to GitHub.

### 💡 Troubleshooting: "command not found"
If `aph` is not recognized after installation:
1. **Try the fallback**: Use `python -m aph` instead of `aph`.
2. **Fix your PATH**: Ensure your Python Scripts directory is in your system's `PATH`.
   - On Windows, it usually looks like: `%AppData%\Local\Packages\Python...\LocalCache\local-packages\Python311\Scripts`

```bash
# Check if you have an SSH key
ls ~/.ssh/id_ed25519.pub

# If not, generate one
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
cat ~/.ssh/id_ed25519.pub
```

---

## 🧪 Development & Testing

```bash
# Clone the repo
git clone https://github.com/DOX69/agent-performance-hub.git
cd agent-performance-hub

# Install in editable mode
pip install -e .
pip install pytest

# Run tests (110 tests)
python -m pytest tests/ -v

# Regenerate skills registry after adding new skills
python scripts/generate_registry.py
```

### Test Coverage

| Module | Tests | What's tested |
|--------|-------|--------------|
| `test_config.py` | 9 | Paths, core skills, constants |
| `test_registry.py` | 17 | Loading, search, filtering, categories |
| `test_installer.py` | 22 | Init, install, remove, update, manifest |
| `test_cli.py` | 27 | All CLI commands via CliRunner |
| `test_generate_registry.py` | 16 | YAML parsing, category detection, scanning |

---

## 🤖 Automated Maintenance

This repo is maintained weekly by **Jules** (automated agent):

- **Every Thursday**: Scans AI research sources for updates
- **Registry regeneration**: `skills_registry.json` rebuilt automatically
- **Test validation**: All 110+ tests must pass before any change
- **CI/CD**: GitHub Actions runs tests on every push and PR

---

## 📝 Adding New Skills

1. Create a skill: `python .agent/skills/expert-skill-creator/scripts/init_skill.py my-skill --path .agent/skills`
2. Edit `SKILL.md` with your skill's content
3. Regenerate registry: `python scripts/generate_registry.py`
4. Run tests: `python -m pytest tests/ -v`
5. Push and create PR

---

## 📚 Documentation

For deeper insights into the project, consult the following guides:

| File | Description |
|------|-------------|
| [HOW_TO_USE.md](docs/HOW_TO_USE.md) | Practical guide to using `aph` across your projects |
| [EXAMPLES.md](docs/EXAMPLES.md) | Real-world examples of interactions using different skills |
| [SKILL_ANATOMY.md](docs/SKILL_ANATOMY.md) | Deep dive into the structure and elements of a standard skill |
| [VISUAL_GUIDE.md](docs/VISUAL_GUIDE.md) | Visual representation of the repository, workflows, and skills |
| [SETUP_SECRETS.md](docs/SETUP_SECRETS.md) | Guide to configuring API keys for workflows (e.g., Google Gemini) |
| [REGISTRY_SETUP.md](docs/REGISTRY_SETUP.md) | Quick guide on authentication and connection to the GitHub package registry |

---

## 📊 Metrics

- **241 skills** across 11 categories
- **110 tests** with 100% pass rate
- **Token Efficiency**: 67.7% reduction vs baseline
- **Agent Autonomy**: 84%

---

## 🤝 Collaboration

I'm open to collaboration on agentic workflows, skill development, and AI performance optimization.

To collaborate, discuss new features, or request access, feel free to reach out:
- **LinkedIn**: [Mickaël Rakotoarinivo](https://www.linkedin.com/in/mickael-rakotoarinivo)

---

## ⚖️ License

Private repository — access by invitation only.

---

**Last updated**: 2026-02-23 | See [CHANGELOG.md](CHANGELOG.md) for version history.
