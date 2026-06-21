---
name: git-commit-jira-format
description: "Use when: committing changes to git with standardized JIRA-formatted commit messages. Includes JIRA ID, one-line summary, and detailed description of changes for better commit history tracking."
---

# Git Commit with JIRA Format

## Purpose

This skill provides a structured workflow for creating well-formatted git commits that follow the JIRA-based commit message standard. It ensures consistent, searchable commit history with clear traceability to project issues.

## Commit Message Format

```
JIRA-123 Brief one-line description of changes

Detailed description of the changes made:
- What was changed
- Why it was changed
- How it impacts the project
- Any important notes or considerations
```

### Format Components

1. **JIRA ID** (required)
   - Format: `JIRA-###` or `PROJECT-###`
   - Example: `MAILER-42`, `LAB-001`
   - Must be at the start of the commit message

2. **One-Line Summary** (required)
   - Concise description (50-72 characters)
   - Imperative mood: "Add feature" not "Added feature"
   - No period at the end

3. **Blank Line** (required)
   - Separates summary from detailed description

4. **Detailed Description** (recommended)
   - Bullet points or paragraphs explaining:
     - What specific changes were made
     - Why these changes were necessary
     - How they solve the problem or add functionality
     - Side effects or migration notes if applicable
   - Wrap lines at 72 characters for readability

## Workflow Steps

### Step 1: Identify the JIRA ID
- Determine which issue this commit addresses
- Format: `PROJECT-NUMBER` (e.g., `MAILER-42`, `LAB-001`)
- If no specific issue, use a general category like `MISC` or `CHORE`

### Step 2: Stage Your Changes
```bash
git add <files>
```

### Step 3: Craft the Summary Line
- Keep it short (50-72 chars max)
- Use imperative mood
- Be specific about what changed
- Examples:
  - ✅ "MAILER-42 Add email validation to subscriber module"
  - ✅ "LAB-001 Fix unsubscribe endpoint in Flask API"
  - ❌ "MAILER-42 Fixed stuff" (too vague)
  - ❌ "MAILER-42 Added email validation to subscriber module" (too long)

### Step 4: Write the Detailed Description
Explain the "why" and "what":
- What specific functionality was added/changed/fixed
- Why the change was necessary
- Any breaking changes or migrations required
- Performance implications if any
- Related issues or PRs

### Step 5: Commit and Push
```bash
git commit -m "JIRA-123 One-line summary

Detailed description here..."
git push origin <branch>
```

## Example Commits

### Example 1: Feature Addition
```
MAILER-42 Add email validation to subscriber module

- Implemented regex-based email validation
- Added validation on subscriber add and bulk operations
- Returns descriptive error messages for invalid emails
- Improves data quality by catching malformed addresses early
- Test coverage: 98% of validation logic
```

### Example 2: Bug Fix
```
LAB-001 Fix unsubscribe endpoint returning incorrect status code

- Changed HTTP response from 200 to 204 No Content on successful unsubscribe
- Added proper error handling for non-existent subscribers (404)
- Updated API documentation to reflect correct status codes
- All existing tests updated and passing
```

### Example 3: Refactor/Improvement
```
MAILER-15 Refactor EmailSender to use dependency injection

- Moved SMTP configuration into constructor parameters
- Enables easier testing with mock SMTP servers
- Decouples email sending from configuration management
- Backward compatible with existing code
- Tests added for new configuration patterns
```

## Quick Command Template

```bash
# Interactive commit with multi-line message
git commit -m "PROJECT-### One-line summary

- Detailed point one
- Detailed point two
- Detailed point three"
```

## Hooks (Optional)

For automated enforcement, add a `.git/hooks/prepare-commit-msg` hook to validate format:

```bash
#!/bin/bash
# Validate commit message format

COMMIT_MSG=$(cat "$1")

# Check for JIRA ID pattern
if ! [[ "$COMMIT_MSG" =~ ^[A-Z0-9]+-[0-9]+ ]]; then
    echo "Error: Commit must start with JIRA ID (e.g., MAILER-42)"
    exit 1
fi

exit 0
```

## Common Mistakes to Avoid

❌ **Missing JIRA ID**
```
Add email validation
```

❌ **JIRA ID not at start**
```
Added email validation (MAILER-42)
```

❌ **Using past tense**
```
MAILER-42 Added email validation
```
✅ Use: `MAILER-42 Add email validation`

❌ **No detailed description**
```
MAILER-42 Fix stuff
```
✅ Provide context and reasoning

## Integration with Issue Tracking

When using JIRA or GitHub Issues:
- Including the issue ID allows automatic linking
- Tools can cross-reference commits with issues
- Makes it easy to track what code addresses each issue
- Enables better release notes generation

## Related Customizations

- **`copilot-instructions.md`** – Global coding standards (can reference this skill)
- **`prepare-commit-msg` hook** – Automated format validation
- **`.github/CONTRIBUTING.md`** – Contribution guidelines
