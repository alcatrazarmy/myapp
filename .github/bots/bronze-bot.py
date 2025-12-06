#!/usr/bin/env python3
"""
Bronze-level Regular Bot Orchestrator PoC

This is a proof-of-concept for a regular bot that can be triggered
by CI workflows or scheduled events to perform routine tasks.

Features:
- Auto-label PRs based on changed files
- Run periodic health checks
- Trigger Bronze-level CI checks
"""

import os
import sys
import json
from pathlib import Path


class BronzeBot:
    """Simple bot orchestrator for Bronze-level automation."""

    def __init__(self, workspace=None):
        self.workspace = workspace or os.getenv("GITHUB_WORKSPACE", ".")
        self.workspace_path = Path(self.workspace)

    def detect_languages(self):
        """Detect programming languages in the repository."""
        languages = []

        if (self.workspace_path / "pubspec.yaml").exists():
            languages.append("dart")

        if (self.workspace_path / "pyproject.toml").exists() or any(
            self.workspace_path.glob("*.py")
        ):
            languages.append("python")

        if (self.workspace_path / "package.json").exists():
            languages.append("javascript")

        if (self.workspace_path / "CMakeLists.txt").exists() or any(
            self.workspace_path.glob(f"*.{ext}")
            for ext in ["cpp", "c", "h"]
        ):
            languages.append("c/c++")


        return languages

    def suggest_pr_labels(self, changed_files):
        """Suggest labels for a PR based on changed files."""
        labels = set()

        for file in changed_files:
            file_path = Path(file)

            # Language-based labels
            if file_path.suffix in [".dart"]:
                labels.add("dart")
            elif file_path.suffix in [".py"]:
                labels.add("python")
            elif file_path.suffix in [".js", ".ts", ".jsx", ".tsx"]:
                labels.add("javascript")
            elif file_path.suffix in [".cpp", ".c", ".h", ".hpp"]:
                labels.add("c/c++")

            # Component-based labels
            if ".github/workflows" in file:
                labels.add("ci/cd")
            elif "test" in file.lower():
                labels.add("testing")
            elif "doc" in file.lower() or file_path.suffix == ".md":
                labels.add("documentation")

        return list(labels)

    def run_health_check(self):
        """Run a basic health check on the repository."""
        checks = {}

        # Check for CI configuration
        checks["has_ci"] = (
            self.workspace_path / ".github" / "workflows" / "bronze-ci.yml"
        ).exists()

        # Check for pre-commit hooks
        checks["has_precommit"] = (
            self.workspace_path / ".pre-commit-config.yaml"
        ).exists()

        # Check for gitignore
        checks["has_gitignore"] = (self.workspace_path / ".gitignore").exists()

        # Check for README
        checks["has_readme"] = (self.workspace_path / "README.md").exists()

        return checks

    def print_status(self):
        """Print current status and detected configuration."""
        print("=== Bronze Bot Status ===")
        print(f"Workspace: {self.workspace}")
        print(f"Languages detected: {', '.join(self.detect_languages())}")

        health = self.run_health_check()
        print("\n=== Repository Health ===")
        for check, status in health.items():
            status_icon = "✓" if status else "✗"
            print(f"{status_icon} {check}: {status}")


def main():
    """Main entry point for the bot."""
    bot = BronzeBot()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "status":
            bot.print_status()
        elif command == "detect-languages":
            languages = bot.detect_languages()
            print(json.dumps({"languages": languages}))
        elif command == "health-check":
            health = bot.run_health_check()
            print(json.dumps(health, indent=2))
            sys.exit(0 if all(health.values()) else 1)
        else:
            print(f"Unknown command: {command}")
            print("Available commands: status, detect-languages, health-check")
            sys.exit(1)
    else:
        bot.print_status()


if __name__ == "__main__":
    main()
