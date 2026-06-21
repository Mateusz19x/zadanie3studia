# Mailer - Email Management System

A production-grade Python application for managing mailing lists and sending emails to subscribers.

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Helper Scripts](#helper-scripts)
- [Running the Program](#running-the-program)
- [Running Tests](#running-tests)
- [Code Quality](#code-quality)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)

---

## ✨ Features

- **Subscriber Management**: Add, remove, query, and manage email subscribers
- **Email Sending**: Send single and bulk emails to subscribers
- **REST API**: Full-featured Flask API with comprehensive endpoints
- **Email Validation**: Built-in email format validation
- **Subscription Lifecycle**: Subscribe, unsubscribe, and resubscribe functionality
- **Statistics**: Track subscriber counts and email sending metrics
- **Comprehensive Testing**: 41 unit tests with 80%+ code coverage
- **Code Quality**: Automated linting and formatting with pylint and black

---

## 📦 Requirements

- **Python**: 3.9+
- **Virtual Environment**: Recommended (venv)
- **Package Manager**: pip

---

## 🚀 Installation

### 1. Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **Flask** (2.3.0) - Web framework
- **pytest** (7.4.0) - Testing framework
- **pytest-cov** (4.1.0) - Coverage reporting
- **pylint** (3.0.0) - Code linting
- **black** (23.9.0) - Code formatting

---

## 🛠️ Helper Scripts

The project includes helper scripts for common tasks. Choose your preferred method:

### Option 1: PowerShell Scripts (Windows)

```powershell
# Run the application
.\run.ps1

# Run tests
.\test.ps1

# Run linting
.\lint.ps1

# Format code
.\format.ps1
```

### Option 2: Batch Scripts (Windows)

```batch
# Run the application
run.bat

# Run tests
test.bat

# Run linting
lint.bat

# Format code
format.bat
```

### Option 3: Python Helper Script (Cross-Platform)

```bash
# Run the application
python helpers.py run

# Run tests
python helpers.py test

# Run linting
python helpers.py lint

# Format code
python helpers.py format
```

### Option 4: Makefile (Unix/Linux/macOS)

```bash
# Install dependencies
make install

# Run the application
make run

# Run tests
make test

# Run linting
make lint

# Format code
make format

# Help
make help
```

---

## ▶️ Running the Program

### Method 1: Using Helper Script

```bash
# PowerShell
.\run.ps1

# Python (cross-platform)
python helpers.py run

# Batch
run.bat

# Makefile
make run
```

### Method 2: Direct Python

```bash
python web.py
```

**Output:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

**Access the server:**
- Health check: `http://localhost:5000/health`
- API stats: `http://localhost:5000/api/stats`

---

## 🧪 Running Tests

### Method 1: Using Helper Script

```bash
# PowerShell
.\test.ps1

# Python (cross-platform)
python helpers.py test

# Batch
test.bat

# Makefile
make test
```

### Method 2: Direct pytest

```bash
# Run all tests
pytest -v

# Run with coverage report
pytest --cov

# Run specific test file
pytest test_subscribers.py -v
```

**Expected Output:**
```
============================= test session starts =============================
collected 41 items

test_subscribers.py::TestSubscriber::test_subscriber_creation PASSED     [  2%]
test_subscribers.py::TestSubscriber::test_subscriber_unsubscribed PASSED [  4%]
...
============================= 41 passed in 0.70s =============================
```

---

## 🔍 Code Quality

### Linting

Lint the code for style violations and potential errors:

```bash
# PowerShell
.\lint.ps1

# Python (cross-platform)
python helpers.py lint

# Batch
lint.bat

# Makefile
make lint
```

### Formatting

Format code to comply with PEP 8 standards using black:

```bash
# PowerShell
.\format.ps1

# Python (cross-platform)
python helpers.py format

# Batch
format.bat

# Makefile
make format
```

---

## 📁 Project Structure

```
zadanie3studia/
├── subscribers.py           # Subscriber management module
├── email_sender.py          # Email sending module
├── web.py                  # Flask REST API application
├── __init__.py             # Package initialization
├── test_subscribers.py      # Unit tests for subscribers
├── test_email_sender.py     # Unit tests for email sender
├── helpers.py              # Python helper script
├── requirements.txt        # Python dependencies
├── pytest.ini              # Pytest configuration
├── Makefile                # Makefile for Unix/Linux/macOS
├── run.ps1 / run.bat       # Run application helper
├── test.ps1 / test.bat     # Run tests helper
├── lint.ps1 / lint.bat     # Linting helper
├── format.ps1 / format.bat # Formatting helper
├── .github/
│   ├── agents/
│   │   └── python-solution-coder.agent.md
│   └── skills/
│       └── git-commit-jira-format/
│           ├── SKILL.md
│           ├── COMMIT_TEMPLATE.md
│           └── git_commit_helper.py
└── README.md               # This file
```

---

## 🔌 API Endpoints

### Health Check

```bash
GET /health
```

**Response:** `{"status": "healthy"}`

### Subscriber Management

```bash
# Get all subscribers
GET /api/subscribers

# Get active subscribers only
GET /api/subscribers/active

# Add a new subscriber
POST /api/subscribers
Body: {"email": "user@example.com", "name": "User Name"}

# Remove a subscriber
DELETE /api/subscribers/<email>

# Unsubscribe (soft delete)
POST /api/subscribers/<email>/unsubscribe
```

### Email Sending

```bash
# Send email to one recipient
POST /api/send-email
Body: {"to": "user@example.com", "subject": "Subject", "body": "Body text"}

# Send bulk email to all active subscribers
POST /api/send-bulk-email
Body: {"subject": "Newsletter", "body": "Content here"}
```

### Statistics

```bash
GET /api/stats
```

**Response:**
```json
{
  "total_subscribers": 10,
  "active_subscribers": 8,
  "emails_sent": 42
}
```

---

## 📊 Test Coverage

Run tests with coverage report:

```bash
pytest --cov --cov-report=html
```

Then open `htmlcov/index.html` in your browser to see detailed coverage.

**Current Coverage:**
- `subscribers.py`: 98%
- `email_sender.py`: 100%
- `__init__.py`: 100%
- Overall: 80%+

---

## 🔧 Development Workflow

1. **Make code changes**
2. **Format code**: `python helpers.py format`
3. **Run tests**: `python helpers.py test`
4. **Check linting**: `python helpers.py lint`
5. **Commit with JIRA ID**: See `.github/skills/git-commit-jira-format/SKILL.md`

---

## 📝 Git Commits

Use the standardized JIRA-formatted commits for better commit history:

```bash
LAB-### One-line summary of changes

- Detailed description point 1
- Detailed description point 2
```

See `.github/skills/git-commit-jira-format/SKILL.md` for full documentation.

---

## 🤝 Contributing

- All code must pass tests
- Code formatting with black is required
- Follow PEP 8 standards
- Include type hints in all functions
- Write Google-style docstrings
- Test coverage minimum: 80%

---

## 📄 License

This project is part of a university assignment.

---

## 📞 Support

For issues or questions about the Mailer system, refer to:
- Code documentation in docstrings
- Test cases for usage examples
- API endpoint documentation above
