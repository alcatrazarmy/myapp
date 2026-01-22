# Bronze CI Bot System

This directory contains the Bronze-level CI bot orchestrator and related tooling.

## Overview

The Bronze CI system provides fast, deterministic checks for code quality:

- **Format checks**: Ensures consistent code formatting across languages
- **Linting**: Fast static analysis to catch common issues
- **Smoke tests**: Quick sanity checks to verify basic functionality
- **Pre-commit hooks**: Catches issues before they're committed

## Components

### 1. GitHub Actions Workflow (`../.github/workflows/bronze-ci.yml`)

Automated CI pipeline that runs on:
- Pull request events (opened, reopened, synchronize)
- Pushes to main branch
- Manual workflow dispatch

The workflow automatically detects project languages and runs appropriate checks.

### 2. Regular Bot (`regular_bot.py`)

A Python-based orchestrator for Bronze-level checks. Can be run locally or in CI.

**Usage:**
```bash
# Run all checks
python .github/bots/regular_bot.py --all

# Run specific checks
python .github/bots/regular_bot.py --check-format
python .github/bots/regular_bot.py --lint
python .github/bots/regular_bot.py --smoke-test
```

**Features:**
- Automatic language detection (Python, C/C++, Dart/Flutter)
- Detailed output and summary
- Exit codes for CI integration

### 3. Pre-commit Hooks (`../.pre-commit-config.yaml`)

Local hooks that run before each commit.

**Setup:**
```bash
pip install pre-commit
pre-commit install
```

**Manual run:**
```bash
pre-commit run --all-files
```

## Supported Languages

### Python
- **Formatter**: black
- **Linter**: ruff
- **Tests**: pytest (smoke tests)

### C/C++
- **Formatter**: clang-format
- **Linter**: (future: clang-tidy)

### Dart/Flutter
- **Formatter**: dart format
- **Analyzer**: flutter analyze
- **Tests**: flutter test

## Design Principles

1. **Fast**: Bronze checks should complete in under 2 minutes
2. **Deterministic**: Same input always produces same output
3. **Lightweight**: Minimal dependencies and resource usage
4. **Progressive**: Bronze is the first tier; Silver/Gold add deeper checks

## Future Enhancements

- Add more language support (JavaScript, Go, Rust)
- Integrate with Silver-level checks (deeper analysis, security scans)
- Add automatic fix mode for some checks
- Bot integration with GitHub PR comments
