#!/usr/bin/env python3
"""
Git Commit Helper with JIRA Format

A utility script to help create properly formatted git commits with JIRA IDs.

Usage:
    python git_commit_helper.py -i JIRA-123 -s "Brief description" -d "Detailed description"
    
    Or interactively:
    python git_commit_helper.py
"""

import subprocess
import sys
import re
from typing import Optional, Tuple


def validate_jira_id(jira_id: str) -> bool:
    """Validate JIRA ID format (e.g., MAILER-42, LAB-001)."""
    return bool(re.match(r'^[A-Z0-9]+-\d+$', jira_id.strip()))


def validate_summary(summary: str) -> bool:
    """Validate one-line summary (50-72 characters)."""
    length = len(summary.strip())
    return 10 <= length <= 72


def get_staged_files() -> int:
    """Get count of staged files."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True,
            text=True,
            check=True
        )
        return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
    except subprocess.CalledProcessError:
        return 0


def commit_with_format(jira_id: str, summary: str, details: str) -> bool:
    """Create a git commit with JIRA format."""
    # Build commit message
    message = f"{jira_id} {summary}"
    if details.strip():
        message += f"\n\n{details}"
    
    try:
        subprocess.run(
            ['git', 'commit', '-m', message],
            check=True
        )
        print(f"✅ Commit created: {jira_id} {summary}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Commit failed: {e}")
        return False


def interactive_mode() -> None:
    """Interactive commit message builder."""
    print("=" * 60)
    print("Git Commit with JIRA Format")
    print("=" * 60)
    
    # Check staged files
    staged = get_staged_files()
    if staged == 0:
        print("⚠️  No staged files. Run 'git add' first.")
        sys.exit(1)
    
    print(f"📦 {staged} file(s) staged for commit\n")
    
    # Get JIRA ID
    while True:
        jira_id = input("Enter JIRA ID (e.g., MAILER-42): ").strip()
        if validate_jira_id(jira_id):
            break
        print("❌ Invalid format. Use PROJECT-NUMBER (e.g., MAILER-42)")
    
    # Get summary
    while True:
        summary = input(f"\nEnter one-line summary (max 72 chars): ").strip()
        if validate_summary(summary):
            print(f"✅ Summary length: {len(summary)} characters")
            break
        print(f"❌ Summary must be 10-72 characters (current: {len(summary)})")
    
    # Get detailed description
    print("\nEnter detailed description (press Enter twice to finish):")
    print("Tip: Use bullet points for clarity")
    details_lines = []
    empty_count = 0
    
    while empty_count < 2:
        line = input()
        if not line:
            empty_count += 1
        else:
            empty_count = 0
            details_lines.append(line)
    
    details = "\n".join(details_lines).rstrip()
    
    # Preview
    print("\n" + "=" * 60)
    print("Commit Message Preview:")
    print("=" * 60)
    print(f"{jira_id} {summary}")
    if details:
        print()
        print(details)
    print("=" * 60)
    
    # Confirm
    confirm = input("\nCreate this commit? (y/n): ").strip().lower()
    if confirm == 'y':
        if commit_with_format(jira_id, summary, details):
            print("\n✅ Commit successful!")
            sys.exit(0)
        else:
            print("\n❌ Commit failed!")
            sys.exit(1)
    else:
        print("Commit cancelled.")
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Argument mode not yet implemented. Use interactive mode.")
        sys.exit(1)
    
    interactive_mode()
