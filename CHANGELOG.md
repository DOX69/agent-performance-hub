# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.3] - 2026-06-12 (Planned)
### Added
- **Private Registry Support**: Configured package for distribution via private GitHub Packages registry (`aph-cli`).
- **Dynamic Versioning**: Integrated `setuptools-scm` to manage versions via Git tags automatically.
- **CI/CD Workflows**:
  - `publish-beta.yml`: Automatically publishes to registry on push to `staging` branch.
  - `publish-prod.yml`: Automatically publishes release to registry on new tags (`v*`).
- **Documentation**: Added `docs/REGISTRY_SETUP.md` with detailed installation and authentication instructions.
- **Team Conventions**: Updated `team-conventions.md` with rules for skill searching and requesting missing skills.

### Changed
- **Package Rename**: Renamed package from `aph` to `aph-cli` in `pyproject.toml`.
- **Tests**: Updated CLI version test to support dynamic version strings.

## [0.1.2] - 2026-06-11
### Added
- Initial release of Agent Performance Hub (APH).
- Core skills: `brainstorming`, `git-pushing`, `expert-skill-creator`, `clean-code`, `systematic-debugging`, `verification-before-completion`.
- CLI commands: `init`, `list`, `search`, `add`, `remove`, `update`, `info`, `version`.
- Automated weekly maintenance agent (Jules).
