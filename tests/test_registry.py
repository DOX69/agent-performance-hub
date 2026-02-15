"""Tests for aph.registry — Skills catalog loading and querying."""

import json
import pytest
from pathlib import Path

from aph.registry import (
    get_all_categories,
    get_all_skills,
    get_core_skills,
    get_skill_by_name,
    get_skills_by_category,
    load_registry,
    search_skills,
)


class TestLoadRegistry:
    """Verify registry loading from skills_registry.json."""

    def test_load_registry_returns_dict(self):
        """Registry should load as a valid dict."""
        registry = load_registry()
        assert isinstance(registry, dict)

    def test_registry_has_required_keys(self):
        """Registry must contain version, generated, and skills."""
        registry = load_registry()
        assert "version" in registry
        assert "generated" in registry
        assert "skills" in registry

    def test_registry_skills_is_list(self):
        """The skills field must be a list."""
        registry = load_registry()
        assert isinstance(registry["skills"], list)

    def test_registry_has_skills(self):
        """Registry must contain at least some skills."""
        registry = load_registry()
        assert len(registry["skills"]) > 0

    def test_registry_skill_has_required_fields(self):
        """Each skill in the registry must have name, description, category."""
        registry = load_registry()
        for skill in registry["skills"]:
            assert "name" in skill, f"Skill missing 'name': {skill}"
            assert "description" in skill, f"Skill {skill.get('name')} missing 'description'"
            assert "category" in skill, f"Skill {skill.get('name')} missing 'category'"


class TestGetAllSkills:
    """Verify get_all_skills returns the full catalog."""

    def test_returns_list(self):
        skills = get_all_skills()
        assert isinstance(skills, list)

    def test_returns_nonempty(self):
        skills = get_all_skills()
        assert len(skills) > 0

    def test_each_skill_is_dict(self):
        skills = get_all_skills()
        for skill in skills:
            assert isinstance(skill, dict)


class TestGetCoreSkills:
    """Verify core skills filtering."""

    def test_returns_only_core(self):
        """Every returned skill should have core=True."""
        core = get_core_skills()
        for skill in core:
            assert skill.get("core") is True, f"Skill '{skill['name']}' is not marked as core"

    def test_core_count_matches_config(self):
        """Number of core skills should match config."""
        from aph.config import CORE_SKILLS
        core = get_core_skills()
        assert len(core) == len(CORE_SKILLS)


class TestGetSkillByName:
    """Verify exact name lookup."""

    def test_find_existing_skill(self):
        """Should find a known core skill."""
        skill = get_skill_by_name("brainstorming")
        assert skill is not None
        assert skill["name"] == "brainstorming"

    def test_returns_none_for_nonexistent(self):
        """Should return None for a skill that doesn't exist."""
        skill = get_skill_by_name("this-skill-definitely-does-not-exist-xyz")
        assert skill is None


class TestSearchSkills:
    """Verify skill search functionality."""

    def test_search_by_name(self):
        """Searching for a skill name should find it."""
        results = search_skills("brainstorming")
        names = [s["name"] for s in results]
        assert "brainstorming" in names

    def test_search_by_partial_name(self):
        """Partial name match should work."""
        results = search_skills("docker")
        assert len(results) > 0
        # At least one result should contain 'docker' in the name
        assert any("docker" in s["name"] for s in results)

    def test_search_returns_empty_for_nonsense(self):
        """Searching for nonsense should return empty list."""
        results = search_skills("xyzzy-nonexistent-gibberish-12345")
        assert results == []

    def test_search_is_case_insensitive(self):
        """Search should be case-insensitive."""
        lower = search_skills("docker")
        upper = search_skills("DOCKER")
        assert len(lower) == len(upper)


class TestGetSkillsByCategory:
    """Verify category filtering."""

    def test_returns_list(self):
        results = get_skills_by_category("methodology")
        assert isinstance(results, list)

    def test_all_results_match_category(self):
        """Every result should be in the requested category."""
        results = get_skills_by_category("security")
        for skill in results:
            assert skill["category"] == "security"

    def test_empty_for_nonexistent_category(self):
        results = get_skills_by_category("nonexistent-category-xyz")
        assert results == []


class TestGetAllCategories:
    """Verify category listing."""

    def test_returns_sorted_list(self):
        categories = get_all_categories()
        assert isinstance(categories, list)
        assert categories == sorted(categories)

    def test_categories_are_strings(self):
        categories = get_all_categories()
        for cat in categories:
            assert isinstance(cat, str)

    def test_has_expected_categories(self):
        """Should contain at least some expected categories."""
        categories = get_all_categories()
        # These should definitely exist given 241 skills
        assert "security" in categories
        assert "methodology" in categories
