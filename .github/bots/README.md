# Bronze Bot Orchestrator

This directory contains the Bronze-level CI bot scaffolding and orchestration tools.

## Overview

The Bronze bot provides:
- **Fast checks**: Deterministic formatting and linting
- **Smoke tests**: Quick validation of core functionality
- **Multi-language support**: Python, Dart/Flutter, C/C++
- **Orchestration**: Coordinated execution of all checks

## Files

- `bronze_orchestrator.py` - Main orchestrator bot (PoC)
- `README.md` - This file

## Usage

### Running the orchestrator directly

```bash
# Install dependencies first
pip install black ruff pytest

# Run the orchestrator
python .github/bots/bronze_orchestrator.py
```

### Running via GitHub Actions

The Bronze CI workflow (`.github/workflows/bronze-ci.yml`) automatically runs these checks on:
- Pull requests (opened, reopened, synchronized)
- Pushes to main branch
- Manual workflow dispatch

## Check Types

### Python
- **Black**: Code formatting verification
- **Ruff**: Fast Python linter
- **Pytest**: Smoke test execution (if tests exist)

### Dart/Flutter
- **dart format**: Code formatting verification
- **flutter analyze**: Static analysis

### C/C++
- **clang-format**: Code formatting verification (if available)

## Pre-commit Hooks

Install pre-commit hooks to run checks locally before committing:

```bash
pip install pre-commit
pre-commit install
```

This will automatically run formatting and linting checks on changed files.

## Extending

To add new checks:
1. Add check methods to `BronzeOrchestrator` class
2. Update `run_all_checks()` to call new methods
3. Update workflow to install required tools

## Philosophy

Bronze-level checks are:
- **Fast**: Complete in under 2 minutes
- **Deterministic**: Same input = same output
- **Focused**: Format, lint, smoke only
- **Fail-fast**: Quick feedback to developers
