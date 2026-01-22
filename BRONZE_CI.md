# Bronze CI System Documentation

## Overview

The Bronze CI system provides fast, deterministic quality checks for the Bauliver repository. It's designed as the first tier in a progressive CI/CD pipeline, focusing on:

- **Speed**: Complete in under 2 minutes
- **Determinism**: Same input = same output
- **Lightweight**: Minimal dependencies
- **Multi-language**: Supports Python, C/C++, Dart/Flutter

## Components

### 1. GitHub Actions Workflow (`.github/workflows/bronze-ci.yml`)

Automatically runs on:
- Pull requests (opened, reopened, synchronized)
- Pushes to `main` branch
- Manual trigger via workflow_dispatch

**What it checks:**
- **Python**: black formatting, ruff linting, pytest smoke tests
- **C/C++**: clang-format checks
- **Dart/Flutter**: dart format, flutter analyze

### 2. Pre-commit Hooks (`.pre-commit-config.yaml`)

Local hooks that run before each commit to catch issues early.

**Installation:**
```bash
pip install pre-commit
pre-commit install
```

**Manual run:**
```bash
# Run on all files
pre-commit run --all-files

# Run on staged files only (automatic on commit)
pre-commit run
```

### 3. Bronze Bot (`.github/bots/regular_bot.py`)

A Python orchestrator for Bronze-level checks that can run locally or in CI.

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
- Automatic language detection
- Detailed output with summaries
- Exit codes for CI integration
- Graceful degradation (skips unavailable tools)

## Setting Up Locally

### Prerequisites

```bash
# Install Python dependencies
pip install black ruff pytest pre-commit

# Install pre-commit hooks
pre-commit install
```

### Running Checks Locally

**Option 1: Use the bot**
```bash
python .github/bots/regular_bot.py --all
```

**Option 2: Use pre-commit**
```bash
pre-commit run --all-files
```

**Option 3: Run tools individually**
```bash
# Format check
black --check .

# Lint
ruff check .

# Tests
pytest -m smoke
```

## For Developers

### Adding New Python Code

1. Write your code following PEP 8 guidelines
2. Add tests (mark quick tests with `@pytest.mark.smoke`)
3. Run `black .` to format
4. Run `ruff check . --fix` to lint
5. Run tests with `pytest`
6. Commit (pre-commit hooks will run automatically)

### Adding New C/C++ Code

1. Ensure code follows project style
2. Format with `clang-format -i <file>`
3. Commit (pre-commit hooks will check formatting)

### Adding Tests

Bronze CI looks for:
- Files named `test_*.py` or `*_test.py`
- Tests marked with `@pytest.mark.smoke` for quick checks
- Test files in the `tests/` directory

Example smoke test:
```python
import pytest

@pytest.mark.smoke
def test_basic_functionality():
    """Quick smoke test."""
    assert True
```

## Configuration

### Python Tools (pyproject.toml)

- **black**: Line length 88, Python 3.11+
- **ruff**: Selected rules for code quality
- **pytest**: Configured to find tests and smoke tests

### Pre-commit Hooks

All hooks auto-update to latest compatible versions. To update:
```bash
pre-commit autoupdate
```

## Troubleshooting

### Pre-commit hooks fail

```bash
# See what failed
pre-commit run --all-files

# Auto-fix issues where possible
pre-commit run --all-files --hook-stage manual
```

### Bot can't find tools

The bot gracefully skips unavailable tools. To use all features:
```bash
# Install all Python tools
pip install black ruff pytest

# For C/C++ (Ubuntu/Debian)
sudo apt-get install clang-format

# For Flutter
# Follow Flutter installation guide
```

### CI workflow fails

1. Check the Actions tab on GitHub
2. Look at the Bronze CI workflow run
3. Review the specific step that failed
4. Run the same check locally to reproduce
5. Fix the issue and push again

## What Bronze CI Does NOT Do

Bronze CI is fast and lightweight, so it intentionally skips:

- Deep static analysis (save for Silver tier)
- Security scanning (save for Silver/Gold tier)
- Full test suite (only smoke tests)
- Performance testing
- Integration tests
- Deployment

These checks belong in higher tiers (Silver/Gold) of the CI pipeline.

## Next Steps

After Bronze CI passes, code proceeds to:
- **Silver CI**: Deeper analysis, more tests, security scans
- **Gold CI**: Full integration tests, performance tests, deployment

## Support

For issues or questions:
1. Check this documentation
2. Review `.github/bots/README.md`
3. Open an issue in the repository
