# 🚀 APH — Agent Performance Hub

![Tests](https://img.shields.io/badge/Tests-110%20passed-brightgreen)
![Token Efficiency](https://img.shields.io/badge/Token%20Efficiency-67.7%25-green)
![Skills](https://img.shields.io/badge/Skills-241-blue)
![Status](https://img.shields.io/badge/Status-Private-orange)

**A CLI tool for managing curated AI agent skills across all your projects.**

Install 241 skills for Gemini, Claude, and other AI agents — selectively, only what you need.

---

## ⚡ Quick Start (3 steps)

### 1. Install

```bash
# Requires SSH access to this private repo
pip install git+ssh://git@github.com/DOX69/agent-performance-hub.git
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
| `aph version` | Show CLI version |

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
# Update the aph package itself (get latest skills from repo)
pip install --upgrade git+ssh://git@github.com/DOX69/agent-performance-hub.git

# Update all installed skills in your project to latest
aph update

# Update a specific skill
aph update docker-expert
```

---

## 🛠️ Requirements

- **Python 3.11+**
- **Git** with SSH key configured for GitHub
- **SSH access** to this private repository

### Setting up SSH access

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
git clone git@github.com:DOX69/agent-performance-hub.git
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

## 📊 Metrics

- **241 skills** across 11 categories
- **110 tests** with 100% pass rate
- **Token Efficiency**: 67.7% reduction vs baseline
- **Agent Autonomy**: 84%

---

## ⚖️ License

Private repository — access by invitation only.

To request access, contact the repository owner.

---

**Last updated**: 2026-02-14 | **aph** v0.1.0

## 🤝 Collaborate

To collaborate on this project, please contact:

- **Email**: mickael.rakotoa@gmail.com
- **LinkedIn**: [https://www.linkedin.com/in/mickael-rakotoarinivo](https://www.linkedin.com/in/mickael-rakotoarinivo)
