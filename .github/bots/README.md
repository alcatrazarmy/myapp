# Bronze Bot - Regular Orchestrator PoC

This directory contains the Bronze-level bot orchestrator proof-of-concept.

## Overview

The Bronze Bot is a simple automation tool that helps maintain repository health and assists with common development tasks.

## Features

- **Language Detection**: Automatically detects programming languages in use
- **PR Labeling**: Suggests labels based on changed files (PoC)
- **Health Checks**: Validates repository has essential configurations
- **CI Integration**: Works with Bronze CI workflow

## Usage

### Check Status
```bash
python .github/bots/bronze-bot.py status
```

### Detect Languages
```bash
python .github/bots/bronze-bot.py detect-languages
```

### Run Health Check
```bash
python .github/bots/bronze-bot.py health-check
```

## Integration with CI

The Bronze Bot can be called from GitHub Actions workflows:

```yaml
- name: Run Bronze Bot Health Check
  run: python .github/bots/bronze-bot.py health-check
```

## Future Enhancements

As this is a PoC (Proof of Concept), future versions could include:

- Automatic PR labeling via GitHub API
- Scheduled repository maintenance tasks
- Integration with issue management
- Automated code quality reports
- Dependency update notifications

## Requirements

- Python 3.11+
- Standard library only (no external dependencies for PoC)

## Architecture

The bot is designed to be:
- **Lightweight**: Minimal dependencies
- **Fast**: Quick startup and execution
- **Extensible**: Easy to add new commands
- **CI-friendly**: Integrates with GitHub Actions
