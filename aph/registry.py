"""APH Skills Registry — Load and query the skills catalog."""

import json
from pathlib import Path
from typing import Optional

from .config import SKILLS_REGISTRY_FILE


def load_registry() -> dict:
    """Load the skills registry from skills_registry.json.

    Returns:
        dict with 'version', 'generated', and 'skills' list.

    Raises:
        FileNotFoundError: If skills_registry.json doesn't exist.
        json.JSONDecodeError: If the file is malformed.
    """
    if not SKILLS_REGISTRY_FILE.exists():
        raise FileNotFoundError(
            f"Skills registry not found at {SKILLS_REGISTRY_FILE}.\n"
            "Run 'python scripts/generate_registry.py' to generate it."
        )
    return json.loads(SKILLS_REGISTRY_FILE.read_text(encoding="utf-8"))


def get_all_skills() -> list[dict]:
    """Return all skills from the registry."""
    registry = load_registry()
    return registry.get("skills", [])


def get_core_skills() -> list[dict]:
    """Return only core skills (installed by default with `aph init`)."""
    return [s for s in get_all_skills() if s.get("core", False)]


def get_skill_by_name(name: str) -> Optional[dict]:
    """Find a skill by exact name.

    Args:
        name: Skill name (e.g., 'docker-expert').

    Returns:
        Skill dict or None if not found.
    """
    for skill in get_all_skills():
        if skill["name"] == name:
            return skill
    return None


def search_skills(query: str) -> list[dict]:
    """Search skills by name, description, or tags.

    Args:
        query: Search query (case-insensitive).

    Returns:
        List of matching skill dicts.
    """
    query_lower = query.lower()
    results = []
    for skill in get_all_skills():
        name = skill.get("name", "").lower()
        desc = skill.get("description", "").lower()
        tags = [t.lower() for t in skill.get("tags", [])]
        category = skill.get("category", "").lower()

        if (
            query_lower in name
            or query_lower in desc
            or any(query_lower in tag for tag in tags)
            or query_lower in category
        ):
            results.append(skill)
    return results


def get_skills_by_category(category: str) -> list[dict]:
    """Return all skills in a given category.

    Args:
        category: Category name (e.g., 'devops', 'frontend').

    Returns:
        List of matching skill dicts.
    """
    cat_lower = category.lower()
    return [
        s for s in get_all_skills()
        if s.get("category", "").lower() == cat_lower
    ]


def get_all_categories() -> list[str]:
    """Return a sorted list of unique categories."""
    categories = set()
    for skill in get_all_skills():
        cat = skill.get("category", "uncategorized")
        categories.add(cat)
    return sorted(categories)
