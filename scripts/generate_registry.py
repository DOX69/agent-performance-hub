#!/usr/bin/env python3
"""Generate skills_registry.json by scanning .agent/skills/*/SKILL.md.

Reads YAML frontmatter from each skill's SKILL.md to extract:
- name, description, tags, version

Then categorizes skills based on directory patterns and tags,
and writes the full registry to skills_registry.json.

Usage:
    python scripts/generate_registry.py

This script is run:
- By Jules as part of weekly maintenance
- By the update-registry.yml GitHub workflow
- Manually when adding new skills
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

# ─── Config ───────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent.resolve()
SKILLS_DIR = REPO_ROOT / ".agent" / "skills"
OUTPUT_FILE = REPO_ROOT / "aph" / "skills_registry.json"

# Core skills — installed by default with `aph init`
CORE_SKILLS = [
    "brainstorming",
    "git-pushing",
    "expert-skill-creator",
    "clean-code",
    "systematic-debugging",
    "verification-before-completion",
    "test-driven-development",
]

# Category detection based on skill name patterns and common tags
CATEGORY_PATTERNS = {
    "security": [
        "pentest", "penetration", "vulnerability", "exploit", "hacking",
        "privilege-escalation", "injection", "xss", "sql-injection",
        "burp", "metasploit", "wireshark", "nmap", "red-team",
        "idor", "smtp-penetration", "ssh-penetration", "wordpress-penetration",
        "api-fuzzing", "broken-authentication", "active-directory",
        "aws-penetration", "cloud-penetration", "security",
    ],
    "frontend": [
        "react", "frontend", "tailwind", "css", "ui-ux", "scroll",
        "3d-web", "canvas", "d3", "web-design", "core-components",
        "interactive-portfolio", "web-artifacts",
    ],
    "backend": [
        "backend", "nestjs", "nodejs", "express", "graphql",
        "api-patterns", "prisma", "bullmq",
    ],
    "devops": [
        "docker", "deployment", "vercel", "gcp", "aws-serverless",
        "azure", "server-management", "github-workflow",
    ],
    "ai-agents": [
        "agent", "llm", "rag", "prompt", "crewai", "langgraph",
        "langfuse", "mcp", "voice-ai", "computer-use",
        "context-window", "conversation-memory", "prompt-caching",
    ],
    "methodology": [
        "brainstorming", "planning", "debugging", "tdd", "test",
        "code-review", "architecture", "clean-code", "verification",
        "kaizen", "lint", "performance-profiling",
    ],
    "data": [
        "database", "clickhouse", "nosql", "neon-postgres",
        "supabase", "firebase",
    ],
    "marketing": [
        "seo", "content", "copywriting", "email", "analytics",
        "paid-ads", "social", "popup", "pricing", "referral",
        "launch", "competitor", "brand", "marketing",
    ],
    "integrations": [
        "stripe", "plaid", "twilio", "hubspot", "segment",
        "shopify", "salesforce", "slack", "discord", "telegram",
        "algolia", "clerk",
    ],
    "tools": [
        "pdf", "docx", "pptx", "xlsx", "file", "git",
        "bash", "powershell", "browser", "playwright",
        "skill-developer", "skill-creator", "workflow",
    ],
}


def parse_yaml_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from a SKILL.md file.

    Handles the --- delimited YAML block at the top of the file.
    Does a simple key-value parse without requiring the yaml library
    to keep dependencies minimal.
    """
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    yaml_text = match.group(1)

    current_key = None
    list_values = []

    for line in yaml_text.split("\n"):
        line = line.rstrip()

        # Skip empty lines and comments
        if not line or line.strip().startswith("#"):
            continue

        # List item (indented with -)
        if re.match(r"^\s+-\s+", line):
            value = re.sub(r"^\s+-\s+", "", line).strip()
            # Remove quotes
            value = value.strip("'\"")
            list_values.append(value)
            if current_key:
                frontmatter[current_key] = list_values
            continue

        # Key-value pair
        kv_match = re.match(r"^(\w[\w_-]*)\s*:\s*(.*)", line)
        if kv_match:
            current_key = kv_match.group(1)
            value = kv_match.group(2).strip().strip("'\"")
            list_values = []

            if value:
                frontmatter[current_key] = value
            continue

    return frontmatter


def detect_category(skill_name: str, tags: list[str]) -> str:
    """Detect the category of a skill based on its name and tags."""
    combined = skill_name.lower() + " " + " ".join(t.lower() for t in tags)

    for category, patterns in CATEGORY_PATTERNS.items():
        for pattern in patterns:
            if pattern in combined:
                return category

    return "other"


def get_skill_size_kb(skill_dir: Path) -> int:
    """Calculate total size of a skill directory in KB."""
    total = 0
    for f in skill_dir.rglob("*"):
        if f.is_file():
            total += f.stat().st_size
    return max(1, total // 1024)


def scan_skills() -> list[dict]:
    """Scan all skills and extract metadata."""
    skills = []

    if not SKILLS_DIR.exists():
        print(f"⚠ Skills directory not found: {SKILLS_DIR}")
        return skills

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        skill_name = skill_dir.name
        content = skill_md.read_text(encoding="utf-8", errors="replace")

        # Parse frontmatter
        metadata = parse_yaml_frontmatter(content)

        name = metadata.get("name", skill_name)
        description = metadata.get("description", "")

        # Clean description — remove brackets and quotes
        description = description.strip("[]'\"")
        # Truncate very long descriptions
        if len(description) > 200:
            description = description[:197] + "..."

        tags = metadata.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]

        category = detect_category(skill_name, tags)
        is_core = skill_name in CORE_SKILLS
        size_kb = get_skill_size_kb(skill_dir)

        skills.append({
            "name": skill_name,
            "description": description,
            "category": category,
            "tags": tags if isinstance(tags, list) else [tags],
            "core": is_core,
            "size_kb": size_kb,
        })

    return skills


def main():
    print("🔍 Scanning skills directory...")
    skills = scan_skills()
    print(f"   Found {len(skills)} skills")

    # Count by category
    categories = {}
    for s in skills:
        cat = s["category"]
        categories[cat] = categories.get(cat, 0) + 1

    print("\n📊 Categories:")
    for cat, count in sorted(categories.items()):
        print(f"   {cat}: {count}")

    # Build registry
    registry = {
        "version": "0.1.0",
        "generated": datetime.now().strftime("%Y-%m-%d"),
        "total_skills": len(skills),
        "core_skills": [s["name"] for s in skills if s["core"]],
        "categories": dict(sorted(categories.items())),
        "skills": skills,
    }

    # Write output
    OUTPUT_FILE.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\n✅ Registry written to {OUTPUT_FILE}")
    print(f"   Total: {len(skills)} skills, {len(categories)} categories")


if __name__ == "__main__":
    main()
