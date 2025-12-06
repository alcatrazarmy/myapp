# Bronze CI Pipeline Documentation

This document describes the Bronze-level CI pipeline and bot scaffolding for the Bauliver repository.

## Overview

The Bronze CI pipeline provides fast, deterministic checks that run on every pull request and push to main. These checks are designed to fail fast and provide quick feedback to developers.

## Components

### 1. GitHub Actions Workflow (`.github/workflows/bronze-ci.yml`)

The main CI workflow that runs on:
- Pull request events (opened, reopened, synchronized)
- Pushes to `main` branch
- Manual workflow dispatch

**Features:**
- Multi-language support (Python, Dart/Flutter, C/C++)
- Automatic language detection
- Fast execution (< 2 minutes target)
- Clear, actionable feedback

### 2. Pre-commit Hooks (`.pre-commit-config.yaml`)

Local development hooks that run before commits are created.

**Installation:**
```bash
pip install pre-commit
pre-commit install
```

**Included hooks:**
- Generic file checks (trailing whitespace, line endings, etc.)
- Python: Black formatter, Ruff linter
- Dart: Format checker
- Security: Secret detection
- YAML/JSON validation

### 3. Bot Orchestrator (`.github/bots/bronze_orchestrator.py`)

A Python-based orchestrator that coordinates all Bronze-level checks.

**Features:**
- Language detection
- Coordinated check execution
- JSON report generation
- Detailed error reporting

**Usage:**
```bash
python .github/bots/bronze_orchestrator.py
```

### 4. Python Configuration (`pyproject.toml`)

Centralized configuration for Python tools:
- Black: Line length 100, Python 3.11 target
- Ruff: Fast linting with common rules
- Pytest: Test discovery and markers

### 5. Security Baseline (`.secrets.baseline`)

Baseline for detect-secrets to avoid false positives.

## Check Types

### Python Checks
- **Black**: Deterministic code formatting
- **Ruff**: Fast Python linter (replaces flake8, isort, etc.)
- **Pytest**: Smoke test execution

### Dart/Flutter Checks
- **dart format**: Code formatting verification
- **flutter analyze**: Static analysis

### C/C++ Checks
- **clang-format**: Code formatting verification

## Running Checks Locally

### Via Pre-commit (Recommended)
```bash
pre-commit run --all-files
```

### Via Orchestrator
```bash
python .github/bots/bronze_orchestrator.py
```

### Individual Tools
```bash
# Python
black --check .
ruff check .
pytest -k smoke

# Dart/Flutter
flutter format --dry-run .
flutter analyze
```

## Adding New Checks

1. **Update the orchestrator** (`bronze_orchestrator.py`):
   - Add a new check method
   - Update `run_all_checks()` to call it

2. **Update the workflow** (`bronze-ci.yml`):
   - Add tool installation if needed
   - Add check execution in the script

3. **Update pre-commit** (`.pre-commit-config.yaml`):
   - Add new hook for local development

## Philosophy

Bronze-level checks follow these principles:

- **Fast**: Complete in under 2 minutes
- **Deterministic**: Same input always produces same output
- **Focused**: Only format, lint, and smoke tests
- **Fail-fast**: Provide immediate feedback
- **Multi-language**: Support project's tech stack
- **Developer-friendly**: Clear error messages

## Troubleshooting

### Workflow fails on language not installed
Some checks skip gracefully if tools aren't available. This is by design for multi-language support.

### Pre-commit hooks slow
Pre-commit only runs on changed files by default. Use `--all-files` flag sparingly.

### False positive in secret detection
Update `.secrets.baseline`:
```bash
detect-secrets scan --baseline .secrets.baseline
```

## Future Enhancements

- Add TypeScript/JavaScript support
- Integrate with GitHub status checks
- Add check timing metrics
- Create GitHub bot integration
- Add automatic fix suggestions

## Related Files

- `.github/workflows/bronze-ci.yml` - Main CI workflow
- `.pre-commit-config.yaml` - Pre-commit hooks configuration
- `.github/bots/bronze_orchestrator.py` - Bot orchestrator
- `.github/bots/README.md` - Bot documentation
- `pyproject.toml` - Python tool configuration
- `.secrets.baseline` - Secret detection baseline
