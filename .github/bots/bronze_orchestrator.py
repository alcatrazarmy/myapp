#!/usr/bin/env python3
"""
Bronze-level CI Bot/Orchestrator PoC
A simple bot that orchestrates Bronze-level CI tasks (format, lint, smoke tests) and provides feedback.
"""

import os
import sys
import json
import subprocess
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class CheckResult:
    """Result of a single check."""
    name: str
    passed: bool
    message: str
    details: Optional[str] = None


class BronzeOrchestrator:
    """Orchestrates Bronze-level CI checks and provides feedback."""

    def __init__(self, workspace: str):
        self.workspace = workspace
        self.results: List[CheckResult] = []

    def run_command(self, cmd: List[str], check_name: str) -> CheckResult:
        """Run a command and return the result."""
        try:
            result = subprocess.run(
                cmd,
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                return CheckResult(
                    name=check_name,
                    passed=True,
                    message=f"{check_name} passed",
                    details=result.stdout
                )
            else:
                return CheckResult(
                    name=check_name,
                    passed=False,
                    message=f"{check_name} failed",
                    details=result.stderr or result.stdout
                )
        except subprocess.TimeoutExpired:
            return CheckResult(
                name=check_name,
                passed=False,
                message=f"{check_name} timed out",
                details="Command exceeded 5 minute timeout"
            )
        except Exception as e:
            return CheckResult(
                name=check_name,
                passed=False,
                message=f"{check_name} error",
                details=str(e)
            )

    def detect_languages(self) -> Dict[str, bool]:
        """Detect which languages are present in the repository."""
        languages = {
            'python': os.path.exists(os.path.join(self.workspace, 'pyproject.toml')),
            'dart': os.path.exists(os.path.join(self.workspace, 'pubspec.yaml')),
            'cpp': os.path.exists(os.path.join(self.workspace, 'CMakeLists.txt'))
        }
        
        # Check for C/C++ files if CMakeLists.txt doesn't exist
        if not languages['cpp']:
            try:
                for f in os.listdir(self.workspace):
                    if f.endswith(('.cpp', '.c', '.h')):
                        languages['cpp'] = True
                        break
            except OSError:
                # If workspace is not accessible, assume no C/C++ files
                pass
        
        return languages

    def run_python_checks(self) -> List[CheckResult]:
        """Run Python-specific checks."""
        results = []
        
        # Black formatting check
        results.append(self.run_command(
            ['black', '--check', '.'],
            'Python Black Format Check'
        ))
        
        # Ruff linting
        results.append(self.run_command(
            ['ruff', 'check', '.'],
            'Python Ruff Lint Check'
        ))
        
        # Pytest smoke tests (if tests exist)
        if os.path.exists(os.path.join(self.workspace, 'tests')):
            results.append(self.run_command(
                ['pytest', '-q', '-k', 'smoke'],
                'Python Smoke Tests'
            ))
        
        return results

    def run_dart_checks(self) -> List[CheckResult]:
        """Run Dart/Flutter-specific checks."""
        results = []
        
        # Flutter format check
        results.append(self.run_command(
            ['flutter', 'format', '--set-exit-if-changed', '--dry-run', '.'],
            'Dart Format Check'
        ))
        
        # Flutter analyze
        results.append(self.run_command(
            ['flutter', 'analyze'],
            'Dart Analyze Check'
        ))
        
        return results

    def run_all_checks(self) -> bool:
        """Run all applicable checks based on detected languages."""
        print("🤖 Bronze Orchestrator Bot - Starting checks...")
        
        languages = self.detect_languages()
        print(f"Detected languages: {[k for k, v in languages.items() if v]}")
        
        if languages['python']:
            print("\n📋 Running Python checks...")
            self.results.extend(self.run_python_checks())
        
        if languages['dart']:
            print("\n📋 Running Dart/Flutter checks...")
            self.results.extend(self.run_dart_checks())
        
        # Print summary
        print("\n" + "="*60)
        print("📊 Check Summary:")
        print("="*60)
        
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        
        for result in self.results:
            status = "✅" if result.passed else "❌"
            print(f"{status} {result.name}: {result.message}")
            if result.details and not result.passed:
                print(f"   Details: {result.details[:200]}...")
        
        print(f"\n📈 Results: {passed} passed, {failed} failed")
        
        return failed == 0

    def generate_report(self) -> Dict:
        """Generate a JSON report of all check results."""
        return {
            'total_checks': len(self.results),
            'passed': sum(1 for r in self.results if r.passed),
            'failed': sum(1 for r in self.results if not r.passed),
            'checks': [
                {
                    'name': r.name,
                    'passed': r.passed,
                    'message': r.message,
                    'details': r.details
                }
                for r in self.results
            ]
        }


def main():
    """Main entry point for the bot."""
    workspace = os.getenv('GITHUB_WORKSPACE', os.getcwd())
    
    orchestrator = BronzeOrchestrator(workspace)
    success = orchestrator.run_all_checks()
    
    # Write report to file
    report_path = os.path.join(workspace, 'bronze-report.json')
    with open(report_path, 'w') as f:
        json.dump(orchestrator.generate_report(), f, indent=2)
    
    print(f"\n📄 Report written to: {report_path}")
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
