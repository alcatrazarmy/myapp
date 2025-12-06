#!/usr/bin/env python3
"""
Regular Bot Orchestrator PoC - Bronze Level

This is a proof-of-concept bot that orchestrates Bronze-level CI tasks.
It's designed to be lightweight and fast, focusing on deterministic checks.

Usage:
    python regular_bot.py [--check-format] [--lint] [--smoke-test]
"""

import argparse
import subprocess
import sys
from pathlib import Path


class BronzeBot:
    """Bronze-level CI bot orchestrator."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.results: list[tuple[str, bool, str]] = []

    def detect_languages(self) -> dict:
        """Detect languages present in the repository."""
        languages = {
            "python": False,
            "cpp": False,
            "dart": False,
        }

        # Check for Python
        if (self.repo_root / "pyproject.toml").exists() or list(
            self.repo_root.glob("*.py")
        ):
            languages["python"] = True

        # Check for C/C++
        if (
            (self.repo_root / "CMakeLists.txt").exists()
            or list(self.repo_root.glob("*.cpp"))
            or list(self.repo_root.glob("*.c"))
            or list(self.repo_root.glob("*.h"))
        ):
            languages["cpp"] = True

        # Check for Dart/Flutter
        if (self.repo_root / "pubspec.yaml").exists():
            languages["dart"] = True

        return languages

    def run_command(self, cmd: list[str], name: str, allow_fail: bool = False) -> bool:
        """Run a command and track results."""
        print(f"\n{'='*60}")
        print(f"Running: {name}")
        print(f"Command: {' '.join(cmd)}")
        print(f"{'='*60}")

        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=not allow_fail,
            )
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)

            success = result.returncode == 0
            self.results.append((name, success, result.stdout + result.stderr))
            return success

        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}")
            print(e.stdout)
            if e.stderr:
                print("STDERR:", e.stderr)
            self.results.append((name, False, str(e)))
            if not allow_fail:
                return False
            return True
        except FileNotFoundError:
            print(f"Command not found: {cmd[0]}")
            self.results.append((name, False, f"Command not found: {cmd[0]}"))
            return False

    def check_format(self) -> bool:
        """Run formatting checks."""
        print("\n🎨 Running format checks...")
        languages = self.detect_languages()
        all_passed = True

        if languages["python"]:
            print("Checking Python formatting with black...")
            if not self.run_command(["black", "--check", "."], "Black format check"):
                all_passed = False

        if languages["cpp"]:
            print("Checking C/C++ formatting with clang-format...")
            # This is a simplified check - full implementation would check all files
            self.run_command(
                ["clang-format", "--version"], "clang-format version", allow_fail=True
            )

        if languages["dart"]:
            print("Checking Dart formatting...")
            self.run_command(
                ["dart", "format", "--set-exit-if-changed", "."],
                "Dart format check",
                allow_fail=True,
            )

        return all_passed

    def lint(self) -> bool:
        """Run linting checks."""
        print("\n🔍 Running linting checks...")
        languages = self.detect_languages()
        all_passed = True

        if languages["python"]:
            print("Linting Python with ruff...")
            if not self.run_command(
                ["ruff", "check", "."], "Ruff lint", allow_fail=True
            ):
                all_passed = False

        if languages["dart"]:
            print("Analyzing Dart/Flutter...")
            self.run_command(["flutter", "analyze"], "Flutter analyze", allow_fail=True)

        return all_passed

    def smoke_test(self) -> bool:
        """Run smoke tests."""
        print("\n🧪 Running smoke tests...")
        languages = self.detect_languages()

        if languages["python"]:
            print("Running Python smoke tests...")
            self.run_command(
                ["pytest", "-q", "-m", "smoke"],
                "Python smoke tests",
                allow_fail=True,
            )

        if languages["dart"]:
            print("Running Flutter tests...")
            self.run_command(["flutter", "test"], "Flutter tests", allow_fail=True)

        return True  # Smoke tests are advisory

    def print_summary(self):
        """Print summary of all checks."""
        print("\n" + "=" * 60)
        print("BRONZE BOT SUMMARY")
        print("=" * 60)

        passed = sum(1 for _, success, _ in self.results if success)
        total = len(self.results)

        for name, success, _ in self.results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status}: {name}")

        print(f"\nResults: {passed}/{total} checks passed")
        print("=" * 60)

        return passed == total


def main():
    parser = argparse.ArgumentParser(description="Bronze-level CI bot orchestrator")
    parser.add_argument("--check-format", action="store_true", help="Run format checks")
    parser.add_argument("--lint", action="store_true", help="Run linting checks")
    parser.add_argument("--smoke-test", action="store_true", help="Run smoke tests")
    parser.add_argument("--all", action="store_true", help="Run all checks")

    args = parser.parse_args()

    # Default to all if nothing specified
    if not any([args.check_format, args.lint, args.smoke_test, args.all]):
        args.all = True

    repo_root = Path.cwd()
    bot = BronzeBot(repo_root)

    print("🤖 Bronze Bot starting...")
    print(f"Repository: {repo_root}")

    languages = bot.detect_languages()
    print(f"Detected languages: {', '.join(k for k, v in languages.items() if v)}")

    overall_success = True

    if args.all or args.check_format:
        if not bot.check_format():
            overall_success = False

    if args.all or args.lint:
        if not bot.lint():
            overall_success = False

    if args.all or args.smoke_test:
        if not bot.smoke_test():
            overall_success = False

    all_passed = bot.print_summary()

    sys.exit(0 if (overall_success and all_passed) else 1)


if __name__ == "__main__":
    main()
