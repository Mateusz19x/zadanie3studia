# Git Commit Template

## Quick Reference Format
```
PROJECT-### One-line summary of changes

- What was changed
- Why it was changed
- How it impacts the project
```

## Step-by-Step Guide

### 1. Get JIRA ID
Find the issue identifier from your project (e.g., MAILER-42, LAB-001)

### 2. Stage Changes
```bash
git add .
```

### 3. Commit with Format
```bash
git commit -m "JIRA-ID Brief description

- Bullet point 1
- Bullet point 2
- Bullet point 3"
```

## Real Examples

**Feature:**
```
MAILER-42 Add subscriber management endpoints

- Implement GET /subscribers for listing all subscribers
- Implement POST /subscribers for adding new subscribers
- Include email validation for all new subscriptions
- Add comprehensive error handling and logging
```

**Bug Fix:**
```
LAB-15 Fix race condition in email sending queue

- Resolved concurrent access issue in bulk email sender
- Implemented mutex lock for shared email history
- Added unit tests for concurrent scenarios
- No performance impact; operations under 10ms
```

**Refactor:**
```
MAILER-08 Refactor SubscriberManager to use dataclass

- Migrated Subscriber from dict to @dataclass
- Improved type safety and IDE autocomplete
- Updated all related tests and documentation
- Backward compatible with existing serialization
```

**Documentation:**
```
CHORE-01 Update README with API endpoint documentation

- Added endpoint reference with examples
- Documented authentication requirements
- Included curl command examples
- Fixed outdated configuration instructions
```

## Tips

- Keep the summary under 72 characters
- Use imperative mood: "Add", "Fix", "Update" not "Added", "Fixed"
- Explain the "why", not just the "what"
- Mention test coverage if applicable
- Reference other issues or PRs if needed

## See Also

- `.github/skills/git-commit-jira-format/SKILL.md` – Full workflow guide
- `CONTRIBUTING.md` – Project contribution guidelines
