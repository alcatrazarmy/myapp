"""Smoke tests for Bronze CI bot."""

import sys
from pathlib import Path

import pytest


@pytest.mark.smoke
def test_bot_exists():
    """Smoke test: Verify the bot file exists."""
    bot_path = Path(__file__).parent.parent / ".github" / "bots" / "regular_bot.py"
    assert bot_path.exists(), "Bronze bot should exist"


@pytest.mark.smoke
def test_workflow_exists():
    """Smoke test: Verify the Bronze CI workflow exists."""
    workflow_path = (
        Path(__file__).parent.parent / ".github" / "workflows" / "bronze-ci.yml"
    )
    assert workflow_path.exists(), "Bronze CI workflow should exist"


@pytest.mark.smoke
def test_precommit_config_exists():
    """Smoke test: Verify pre-commit config exists."""
    config_path = Path(__file__).parent.parent / ".pre-commit-config.yaml"
    assert config_path.exists(), "Pre-commit config should exist"


def test_bot_imports():
    """Verify bot can be imported without errors."""
    # Add bot directory to path
    bot_dir = Path(__file__).parent.parent / ".github" / "bots"
    sys.path.insert(0, str(bot_dir))

    try:
        import regular_bot

        assert hasattr(regular_bot, "BronzeBot"), "BronzeBot class should exist"
        assert hasattr(regular_bot, "main"), "main function should exist"
    finally:
        sys.path.remove(str(bot_dir))


def test_bronze_bot_language_detection():
    """Test language detection in BronzeBot."""
    bot_dir = Path(__file__).parent.parent / ".github" / "bots"
    sys.path.insert(0, str(bot_dir))

    try:
        from regular_bot import BronzeBot

        repo_root = Path(__file__).parent.parent
        bot = BronzeBot(repo_root)

        languages = bot.detect_languages()

        # This is a Flutter/Dart project
        assert "dart" in languages
        assert languages["dart"] is True, "Should detect Dart/Flutter project"

        # We have a pyproject.toml now
        assert "python" in languages

        # Has C++ files in platform directories
        assert "cpp" in languages

    finally:
        sys.path.remove(str(bot_dir))
