# GitHub Copilot Instructions - Mailer Project

Global guidelines and standards for the Mailer project. All contributors should follow these guidelines when working with GitHub Copilot.

---

## 1. Python i Zależności

### Version Requirements
- **Python**: 3.9 or higher
- **Package Manager**: pip with requirements.txt

### Code Style
- Follow **PEP 8** strictly
- Use **black** for code formatting
- Use **pylint** for linting
- **Type hints** are mandatory for all functions and methods
- Keep `requirements.txt` always up-to-date with pinned versions

### Import Organization
```python
# Standard library imports
import os
import sys
from datetime import datetime

# Third-party imports
from flask import Flask, request, jsonify

# Local imports
from subscribers import SubscriberManager
from email_sender import EmailSender
```

---

## 2. Struktura Kodu

### Module Size
- **Maximum file size**: 500 lines per module
- **Maximum function size**: 50 lines
- **One responsibility per class** (Single Responsibility Principle)

### Naming Conventions
```python
# Classes: PascalCase
class SubscriberManager:
    pass

# Functions/Methods: snake_case
def send_email(recipient: str) -> bool:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_EMAIL_LENGTH = 255
RETRY_ATTEMPTS = 3

# Private: _leading_underscore
def _validate_email(email: str) -> bool:
    pass
```

### Documentation
- **Docstrings**: Google format for all functions, classes, and modules
- **Type Hints**: Required for all parameters and return types
- **Comments**: Explain WHY, not WHAT (code should be self-documenting)

Example:
```python
def add_subscriber(self, email: str, name: str) -> bool:
    """Add a new subscriber to the mailing list.
    
    Args:
        email: Email address of the subscriber.
        name: Full name of the subscriber.
        
    Returns:
        True if subscriber was added, False if already exists or invalid.
        
    Raises:
        ValueError: If email or name is invalid.
    """
```

---

## 3. Testowanie

### Coverage Requirements
- **Minimum code coverage**: 80%
- **Target coverage**: 90%+
- All public functions must have tests

### Testing Framework
- **Framework**: pytest
- **Coverage tool**: pytest-cov
- **Mocking**: unittest.mock

### Test Organization
```python
# File naming
test_<module_name>.py

# Class naming
class Test<ClassName>:
    pass

# Method naming
def test_function_does_something():
    """Descriptive test name following: test_<what>_<condition>_<result>"""
    pass
```

### Test Structure
```python
import pytest
from module import Function

class TestFunction:
    @pytest.fixture
    def setup(self):
        """Setup test data."""
        return Function()
    
    def test_happy_path(self, setup):
        """Test main scenario."""
        pass
    
    def test_edge_cases(self, setup):
        """Test boundary conditions."""
        pass
    
    def test_error_handling(self, setup):
        """Test error scenarios."""
        pass
```

### Running Tests
```bash
# Run all tests with coverage
pytest --cov --cov-report=html

# Run specific test file
pytest test_subscribers.py -v

# Run with verbose output
pytest -v
```

---

## 4. Bezpieczeństwo

### Secrets Management
- ❌ **NEVER** commit credentials, passwords, API keys
- ✅ **ALWAYS** use environment variables for secrets
- ✅ Create `.env` file locally (add to `.gitignore`)

Example:
```python
import os

SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
API_KEY = os.getenv('API_KEY')

if not SMTP_PASSWORD:
    raise ValueError("SMTP_PASSWORD environment variable not set")
```

### Input Validation
- Validate all user input
- Check type, length, format
- Raise descriptive errors

```python
def add_subscriber(self, email: str, name: str) -> bool:
    if not email or not isinstance(email, str):
        raise ValueError("Email cannot be empty")
    if not self._validate_email(email):
        raise ValueError(f"Invalid email format: {email}")
```

### Error Handling
- Catch specific exceptions, never bare `except:`
- Provide informative error messages
- Log security-relevant events

```python
# ❌ BAD
except:
    pass

# ✅ GOOD
except ValueError as e:
    logger.error(f"Validation error: {e}")
    raise
```

### SQL/Injection Prevention
- Use parameterized queries (if using database)
- Escape user input
- Never build SQL strings with string concatenation

---

## 5. Git & Commits

### Commit Convention
Use **JIRA-formatted commits** for better traceability:

```
PROJECT-### Brief one-line description

- Detailed description point 1
- Detailed description point 2
- Why this change was necessary
```

Example:
```
LAB-003 Implement venv setup and helper scripts

- Added pylint and black to requirements.txt
- Created cross-platform helper scripts (Python, PowerShell, Batch, Makefile)
- Applied black formatting to all modules
- Fixed pylint issues with import order
- All 41 tests passing with 80% coverage
```

See `.github/skills/git-commit-jira-format/SKILL.md` for full documentation.

### Branch Naming
```
feature/feature-name        # New features
bugfix/bug-description      # Bug fixes
docs/documentation-topic    # Documentation updates
refactor/refactoring-topic  # Code refactoring
```

### Pull Requests
- Descriptive title and description
- Include related JIRA ID
- All tests must pass
- Code review required before merge

---

## 6. Architektura

### Project Structure
```
zadanie3studia/
├── subscribers.py           # Subscriber management
├── email_sender.py          # Email sending
├── web.py                  # Flask REST API
├── __init__.py             # Package init
├── test_subscribers.py      # Subscriber tests
├── test_email_sender.py     # Email sender tests
├── helpers.py              # Helper scripts
├── requirements.txt        # Dependencies
├── .github/
│   ├── agents/             # Custom agents
│   ├── skills/             # Custom skills
│   └── README.md           # Copilot configuration
└── README_IMPLEMENTATION.md # Implementation guide
```

### Design Principles
- **Separation of Concerns**: Each module has single responsibility
- **Dependency Injection**: Pass dependencies, don't create them inside functions
- **DRY**: Don't Repeat Yourself - extract common code
- **SOLID Principles**: Apply SOLID principles where applicable

### MVC Pattern (for Flask)
- **Model**: `subscribers.py`, `email_sender.py` (business logic)
- **View**: HTML templates (in `templates/` folder)
- **Controller**: Routes in `web.py`

```python
# ❌ BAD: Tight coupling
class EmailSender:
    def __init__(self):
        self.smtp = SMTPConnection()  # Created inside

# ✅ GOOD: Dependency injection
class EmailSender:
    def __init__(self, smtp_config: dict):
        self.smtp_config = smtp_config
```

---

## 7. Tools & Automation

### Code Formatting
```bash
# Format code with black
python helpers.py format

# Or directly
python -m black *.py
```

### Linting
```bash
# Lint with pylint
python helpers.py lint

# Or directly
python -m pylint *.py
```

### Running Application
```bash
# Start Flask server
python helpers.py run

# Or directly
python web.py
```

### Running Tests
```bash
# Run all tests
python helpers.py test

# Or directly
python -m pytest -v
```

---

## 8. Best Practices for AI-Assisted Development

### When Using Copilot
- ✅ **Read generated code** - Understand what Copilot suggests
- ✅ **Verify functionality** - Test generated code thoroughly
- ✅ **Use appropriate skills** - Refer to project skills for patterns
- ✅ **Follow instructions** - These guidelines apply to AI suggestions too

### Available Skills
- `git-commit-jira-format` – JIRA-formatted commit messages
- `email-validation` – Email validation patterns
- `mailer-complete-testing` – Comprehensive testing guide

Invoke with:
```
@copilot use [skill-name] skill
```

### Common Patterns
Use these patterns for consistency:

**API Endpoint Pattern:**
```python
@app.route('/api/subscribers', methods=['GET'])
def get_subscribers() -> Tuple[Dict[str, Any], int]:
    """Get all subscribers."""
    subscribers = manager.get_all_subscribers()
    return jsonify({'subscribers': subscribers}), 200
```

**Data Validation Pattern:**
```python
if not email or not name:
    raise ValueError("Email and name cannot be empty")
if not self._validate_email(email):
    raise ValueError(f"Invalid email: {email}")
```

---

## 9. Code Review Checklist

Before requesting code review:
- [ ] All tests pass
- [ ] Code formatted with black
- [ ] No pylint warnings
- [ ] Type hints on all functions
- [ ] Docstrings present and accurate
- [ ] No hardcoded secrets/credentials
- [ ] Follows project structure
- [ ] Commit message follows JIRA format

---

## 10. Emergency Contacts & Resources

### Documentation
- [PEP 8 Style Guide](https://pep8.org/)
- [Google Python Docstring Style](https://google.github.io/styleguide/pyguide.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pytest Documentation](https://docs.pytest.org/)

### Project Files
- Implementation guide: `README_IMPLEMENTATION.md`
- Commit format guide: `.github/skills/git-commit-jira-format/SKILL.md`
- Testing patterns: `.github/skills/mailer-complete-testing/SKILL.md`

---

**Last Updated**: 2026-06-21  
**Version**: 1.0  
**Maintained By**: Development Team
