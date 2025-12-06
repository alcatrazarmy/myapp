#!/usr/bin/env python3
"""
Simple test script to verify Bronze Bot functionality.
Can be run as part of CI or locally for development.
"""

import sys
import subprocess
import json
from pathlib import Path


def test_bot_status():
    """Test that the bot status command works."""
    print("Testing bot status command...")
    result = subprocess.run(
        ["python", ".github/bots/bronze-bot.py", "status"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Status command failed: {result.stderr}"
    assert "Bronze Bot Status" in result.stdout
    print("✓ Bot status command works")


def test_bot_detect_languages():
    """Test language detection."""
    print("Testing language detection...")
    result = subprocess.run(
        ["python", ".github/bots/bronze-bot.py", "detect-languages"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Language detection failed: {result.stderr}"
    data = json.loads(result.stdout)
    assert "languages" in data
    assert "dart" in data["languages"]
    print(f"✓ Language detection works: {data['languages']}")


def test_bot_health_check():
    """Test health check."""
    print("Testing health check...")
    result = subprocess.run(
        ["python", ".github/bots/bronze-bot.py", "health-check"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Health check failed: {result.stderr}"
    data = json.loads(result.stdout)
    assert data["has_ci"] is True
    assert data["has_precommit"] is True
    assert data["has_gitignore"] is True
    assert data["has_readme"] is True
    print("✓ Health check passed")


def test_workflow_yaml_valid():
    """Test that workflow YAML is valid."""
    print("Testing workflow YAML validity...")
    import yaml

    workflow_file = Path(".github/workflows/bronze-ci.yml")
    assert workflow_file.exists(), "Workflow file not found"

    with open(workflow_file) as f:
        data = yaml.safe_load(f)

    assert "name" in data
    assert "jobs" in data
    assert "bronze-checks" in data["jobs"]
    print("✓ Workflow YAML is valid")


def test_precommit_yaml_valid():
    """Test that pre-commit config YAML is valid."""
    print("Testing pre-commit config YAML validity...")
    import yaml

    precommit_file = Path(".pre-commit-config.yaml")
    assert precommit_file.exists(), "Pre-commit config file not found"

    with open(precommit_file) as f:
        data = yaml.safe_load(f)

    assert "repos" in data
    print("✓ Pre-commit config YAML is valid")


def main():
    """Run all tests."""
    print("=== Running Bronze CI Tests ===\n")

    tests = [
        test_bot_status,
        test_bot_detect_languages,
        test_bot_health_check,
        test_workflow_yaml_valid,
        test_precommit_yaml_valid,
    ]

    failed = []
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed.append(test.__name__)

    print("\n=== Test Summary ===")
    if failed:
        print(f"Failed tests: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
