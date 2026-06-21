#!/usr/bin/env python3
"""
Helper script to run the Mailer Flask application.

Usage:
    python helpers.py run
"""

import subprocess
import sys
from pathlib import Path


def run_program() -> int:
    """Start the Flask web application."""
    print("🚀 Starting Mailer Flask Application...")
    try:
        result = subprocess.run([sys.executable, "web.py"], check=False)
        return result.returncode
    except KeyboardInterrupt:
        print("\n⏹️  Application stopped.")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def run_tests() -> int:
    """Run the test suite with pytest."""
    print("🧪 Running Mailer tests with pytest...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v", "--tb=short"], check=False
        )
        return result.returncode
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def run_linting() -> int:
    """Run pylint on the source files."""
    print("🔍 Running pylint on Python files...")
    files = ["subscribers.py", "email_sender.py", "web.py", "__init__.py"]

    try:
        result = subprocess.run([sys.executable, "-m", "pylint"] + files, check=False)
        return result.returncode
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def run_formatting() -> int:
    """Format Python code with black."""
    print("✨ Formatting Python code with black...")
    files = ["subscribers.py", "email_sender.py", "web.py", "__init__.py"]

    try:
        result = subprocess.run([sys.executable, "-m", "black"] + files, check=False)
        if result.returncode == 0:
            print("✅ Formatting complete!")
        return result.returncode
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python helpers.py <command>")
        print("\nAvailable commands:")
        print("  run       - Start the Flask application")
        print("  test      - Run the test suite")
        print("  lint      - Run pylint linting")
        print("  format    - Format code with black")
        return 1

    command = sys.argv[1].lower()

    if command == "run":
        return run_program()
    elif command == "test":
        return run_tests()
    elif command == "lint":
        return run_linting()
    elif command == "format":
        return run_formatting()
    else:
        print(f"❌ Unknown command: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
