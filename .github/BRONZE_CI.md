# Bronze CI Pipeline - Quick Reference

## Overview

The Bronze CI pipeline provides fast, deterministic checks for code quality and formatting. It's designed to run in under 2 minutes and catch common issues early in the development cycle.

## Components

### 1. GitHub Actions Workflow (`.github/workflows/bronze-ci.yml`)
Automatically runs on:
- Pull requests (opened, reopened, synchronized)
- Pushes to `main` branch
- Manual workflow dispatch

**Checks performed:**
- **Python**: black (formatting), ruff (linting), pytest smoke tests
- **Dart/Flutter**: dart format
- **C/C++**: clang-format (if available)
- **JavaScript/TypeScript**: prettier, eslint (if configured)

### 2. Pre-commit Hooks (`.pre-commit-config.yaml`)
Local development hooks that run before commits:
- Trailing whitespace removal
- End-of-file fixer
- YAML validation
- Large file detection
- Merge conflict detection
- Python formatting (black, ruff)
- Dart formatting

**Installation:**
```bash
pip install pre-commit
pre-commit install
```

**Usage:**
```bash
# Run on all files
pre-commit run --all-files

# Run on staged files (automatic on commit)
git commit
```

### 3. Bronze Bot (`.github/bots/bronze-bot.py`)
Automation helper for repository maintenance:
- Language detection
- Repository health checks
- PR label suggestions (PoC)

**Usage:**
```bash
# Check status
python .github/bots/bronze-bot.py status

# Detect languages
python .github/bots/bronze-bot.py detect-languages

# Run health check
python .github/bots/bronze-bot.py health-check
```

## Smoke Tests

Smoke tests are fast, minimal tests that verify basic functionality.

**Naming conventions:**
- Python: `test_smoke_*.py` or use `@pytest.mark.smoke`
- Dart: `*_smoke_test.dart`
- JavaScript: `*.smoke.test.js`

**Running smoke tests:**
```bash
# Python
pytest -m smoke -v

# Dart
flutter test --name=smoke
```

See `.github/SMOKE_TESTS.md` for detailed guide.

## Local Development Workflow

1. **Install pre-commit hooks:**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

2. **Make changes to code**

3. **Pre-commit hooks run automatically on commit**

4. **Push changes** - Bronze CI runs automatically

5. **Fix any issues** reported by CI

## CI Performance

Bronze CI is designed for speed:
- Target: < 2 minutes total
- Parallel execution where possible
- Caching of dependencies
- Fail-fast on formatting issues

## Troubleshooting

### Pre-commit hooks fail
```bash
# Skip hooks temporarily (not recommended)
git commit --no-verify

# Update hooks
pre-commit autoupdate

# Clean cache
pre-commit clean
```

### CI fails on formatting
```bash
# Python
black .
ruff --fix .

# Dart
dart format .
```

### Bot health check fails
Run the bot locally to see which checks fail:
```bash
python .github/bots/bronze-bot.py health-check
```

## Next Steps

Bronze CI is the first tier. Future tiers:
- **Silver CI**: Extended testing, coverage reports
- **Gold CI**: Integration tests, performance benchmarks
- **Platinum CI**: Security scanning, deployment validation

## Contributing

To add new checks:
1. Update `.github/workflows/bronze-ci.yml`
2. Add corresponding pre-commit hook if applicable
3. Update this documentation
4. Test with `.github/bots/test_bronze_bot.py`
