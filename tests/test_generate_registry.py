"""Tests for scripts/generate_registry.py — Registry generation."""

import json
import pytest
from pathlib import Path
import importlib.util
import sys

# Load generate_registry as a module from scripts/
SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "generate_registry.py"
spec = importlib.util.spec_from_file_location("generate_registry", SCRIPT_PATH)
generate_registry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_registry)


class TestParseYamlFrontmatter:
    """Verify YAML frontmatter parsing from SKILL.md files."""

    def test_parse_simple_frontmatter(self):
        content = "---\nname: test-skill\ndescription: A test skill\n---\n# Content"
        result = generate_registry.parse_yaml_frontmatter(content)
        assert result["name"] == "test-skill"
        assert result["description"] == "A test skill"

    def test_parse_frontmatter_with_quotes(self):
        content = '---\nname: "test-skill"\ndescription: \'A test skill\'\n---\n# Content'
        result = generate_registry.parse_yaml_frontmatter(content)
        assert result["name"] == "test-skill"
        assert result["description"] == "A test skill"

    def test_parse_frontmatter_with_tags_list(self):
        content = "---\nname: test\ntags:\n  - tag1\n  - tag2\n---\n# Content"
        result = generate_registry.parse_yaml_frontmatter(content)
        assert result["tags"] == ["tag1", "tag2"]

    def test_parse_empty_frontmatter(self):
        content = "# No frontmatter here"
        result = generate_registry.parse_yaml_frontmatter(content)
        assert result == {}

    def test_parse_frontmatter_with_comments(self):
        content = "---\nname: test\n# This is a comment\ndescription: desc\n---\n"
        result = generate_registry.parse_yaml_frontmatter(content)
        assert result["name"] == "test"
        assert result["description"] == "desc"


class TestDetectCategory:
    """Verify skill category detection."""

    def test_security_skills(self):
        assert generate_registry.detect_category("sql-injection-testing", []) == "security"
        assert generate_registry.detect_category("burp-suite-testing", []) == "security"

    def test_frontend_skills(self):
        assert generate_registry.detect_category("react-patterns", []) == "frontend"
        assert generate_registry.detect_category("tailwind-patterns", []) == "frontend"

    def test_devops_skills(self):
        assert generate_registry.detect_category("docker-expert", []) == "devops"

    def test_methodology_skills(self):
        assert generate_registry.detect_category("brainstorming", []) == "methodology"

    def test_unknown_defaults_to_other(self):
        assert generate_registry.detect_category("completely-unknown-xyz", []) == "other"

    def test_tags_influence_category(self):
        result = generate_registry.detect_category("my-custom-skill", ["docker", "containers"])
        assert result == "devops"


class TestScanSkills:
    """Verify full skill scanning."""

    def test_scan_returns_list(self):
        skills = generate_registry.scan_skills()
        assert isinstance(skills, list)

    def test_scan_finds_skills(self):
        skills = generate_registry.scan_skills()
        assert len(skills) > 0

    def test_scanned_skills_have_required_fields(self):
        skills = generate_registry.scan_skills()
        for skill in skills:
            assert "name" in skill
            assert "description" in skill
            assert "category" in skill
            assert "tags" in skill
            assert "core" in skill
            assert "size_kb" in skill

    def test_core_skills_are_marked(self):
        """Core skills should be flagged in scan results."""
        skills = generate_registry.scan_skills()
        core_names = {s["name"] for s in skills if s["core"]}
        from aph.config import CORE_SKILLS
        for skill in CORE_SKILLS:
            assert skill in core_names, f"Core skill '{skill}' not marked as core in scan"


class TestRegistryOutput:
    """Verify the generated registry file."""

    def test_registry_file_exists(self):
        """After running generate_registry, the file should exist."""
        output = generate_registry.OUTPUT_FILE
        assert output.exists()

    def test_registry_is_valid_json(self):
        content = generate_registry.OUTPUT_FILE.read_text(encoding="utf-8")
        data = json.loads(content)
        assert isinstance(data, dict)

    def test_registry_has_metadata(self):
        content = json.loads(generate_registry.OUTPUT_FILE.read_text(encoding="utf-8"))
        assert "version" in content
        assert "generated" in content
        assert "total_skills" in content
        assert "categories" in content
        assert "skills" in content

    def test_registry_skill_count_matches(self):
        content = json.loads(generate_registry.OUTPUT_FILE.read_text(encoding="utf-8"))
        assert content["total_skills"] == len(content["skills"])
