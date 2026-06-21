---
name: mailer-complete-testing
description: "Complete testing skill for all Mailer components. Use when: writing tests for subscribers, email sending, Flask API, validation, or integration scenarios."
topics:
  - testing
  - pytest
  - email
  - flask
  - validation
  - unit-tests
  - integration-tests
applyTo:
  - path: "**/tests/**"
  - path: "test_*.py"
  - path: "**/test_*"
---

# Mailer Complete Testing Skill

Comprehensive testing patterns and best practices for all components of the Mailer project.

---

## Testing Strategy Overview

### Components to Test

1. **Email Validation** - Format checking, edge cases
2. **Email Sending** - Single/bulk emails, error handling
3. **Subscribers Management** - CRUD operations, list operations
4. **Web Interface** - Flask routes, status codes, response formats
5. **Integration** - End-to-end workflows

### Testing Framework Stack

- **Framework**: pytest
- **Coverage**: pytest-cov
- **Mocking**: unittest.mock
- **Fixtures**: pytest fixtures with dependency injection
- **Parametrization**: @pytest.mark.parametrize

---

## Component 1: Email Validation Testing

### Test Template

```python
import pytest
from email_validator import EmailValidator

class TestEmailValidation:
    """Test email format validation."""
    
    @pytest.mark.parametrize("email,expected", [
        # Valid formats
        ("user@example.com", True),
        ("user+tag@domain.co.uk", True),
        ("user.name@example.org", True),
        
        # Invalid formats
        ("invalid", False),
        ("@example.com", False),
        ("user@", False),
        ("", False),
        (None, False),
    ])
    def test_email_validation(self, email, expected):
        """Test validation with various email formats."""
        assert EmailValidator.validate(email) == expected
    
    def test_edge_cases(self):
        """Test boundary conditions."""
        # Too short
        assert EmailValidator.validate("a@b") is False
        
        # Whitespace
        assert EmailValidator.validate("  user@example.com  ") is True
        
        # Special chars
        assert EmailValidator.validate("user+tag@example.com") is True
```

---

## Component 2: Email Sending Testing

### Unit Test Template

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from email_sender import EmailSender, Email
from datetime import datetime

class TestEmailSender:
    """Test email sending functionality."""
    
    @pytest.fixture
    def sender(self):
        """Create EmailSender instance for testing."""
        return EmailSender(
            smtp_server="localhost",
            smtp_port=587,
            sender_email="test@example.com",
            sender_password="test_password"
        )
    
    def test_send_single_email_success(self, sender):
        """Test successful single email sending."""
        result = sender.send_email(
            "recipient@example.com",
            "Test Subject",
            "Test Body"
        )
        
        assert result is True
        assert sender.get_sent_count() == 1
    
    def test_send_email_invalid_recipient(self, sender):
        """Test sending to invalid email."""
        with pytest.raises(ValueError, match="Invalid recipient"):
            sender.send_email(
                "invalid-email",
                "Subject",
                "Body"
            )
    
    def test_send_email_empty_fields(self, sender):
        """Test sending with empty required fields."""
        with pytest.raises(ValueError):
            sender.send_email("", "Subject", "Body")
        
        with pytest.raises(ValueError):
            sender.send_email("user@example.com", "", "Body")
        
        with pytest.raises(ValueError):
            sender.send_email("user@example.com", "Subject", "")
    
    def test_send_bulk_email_success(self, sender):
        """Test bulk email sending."""
        recipients = [
            "user1@example.com",
            "user2@example.com",
            "user3@example.com",
        ]
        
        count = sender.send_bulk_email(
            recipients,
            "Newsletter",
            "Content"
        )
        
        assert count == 3
        assert sender.get_sent_count() == 3
    
    def test_send_bulk_email_with_invalid_recipients(self, sender):
        """Test bulk sending skips invalid recipients."""
        recipients = [
            "valid@example.com",
            "invalid-email",
            "another@example.com",
        ]
        
        count = sender.send_bulk_email(
            recipients,
            "Subject",
            "Body"
        )
        
        # Only valid emails sent
        assert count == 2
    
    def test_email_history_tracking(self, sender):
        """Test email history is properly tracked."""
        sender.send_email("user@example.com", "Subject", "Body")
        
        emails = sender.get_sent_emails()
        assert len(emails) == 1
        
        email = emails[0]
        assert email.to == "user@example.com"
        assert email.subject == "Subject"
        assert email.body == "Body"
        assert isinstance(email.sent_at, datetime)
    
    def test_clear_history(self, sender):
        """Test clearing email history."""
        sender.send_email("user@example.com", "Subject", "Body")
        assert sender.get_sent_count() == 1
        
        sender.clear_history()
        assert sender.get_sent_count() == 0
```

---

## Component 3: Subscribers Management Testing

### Unit Test Template

```python
import pytest
from subscribers import SubscriberManager, Subscriber

class TestSubscriberManager:
    """Test subscriber management CRUD operations."""
    
    @pytest.fixture
    def manager(self):
        """Create fresh manager for each test."""
        return SubscriberManager()
    
    def test_add_subscriber_success(self, manager):
        """Test successfully adding subscriber."""
        result = manager.add_subscriber("john@example.com", "John Doe")
        
        assert result is True
        assert manager.get_subscriber_count() == 1
    
    def test_add_subscriber_duplicate_fails(self, manager):
        """Test duplicate subscriber prevention."""
        manager.add_subscriber("john@example.com", "John Doe")
        result = manager.add_subscriber("john@example.com", "John Doe")
        
        assert result is False
        assert manager.get_subscriber_count() == 1
    
    def test_add_subscriber_invalid_email(self, manager):
        """Test adding with invalid email format."""
        with pytest.raises(ValueError):
            manager.add_subscriber("invalid-email", "John")
    
    def test_add_subscriber_empty_fields(self, manager):
        """Test adding with empty fields."""
        with pytest.raises(ValueError):
            manager.add_subscriber("", "John")
        
        with pytest.raises(ValueError):
            manager.add_subscriber("john@example.com", "")
    
    def test_remove_subscriber_success(self, manager):
        """Test successfully removing subscriber."""
        manager.add_subscriber("john@example.com", "John Doe")
        result = manager.remove_subscriber("john@example.com")
        
        assert result is True
        assert manager.get_subscriber_count() == 0
    
    def test_remove_nonexistent_subscriber(self, manager):
        """Test removing non-existent subscriber."""
        result = manager.remove_subscriber("john@example.com")
        assert result is False
    
    def test_get_subscriber(self, manager):
        """Test retrieving specific subscriber."""
        manager.add_subscriber("john@example.com", "John Doe")
        
        sub = manager.get_subscriber("john@example.com")
        assert sub is not None
        assert sub.email == "john@example.com"
        assert sub.name == "John Doe"
        assert sub.subscribed is True
    
    def test_get_nonexistent_subscriber(self, manager):
        """Test getting non-existent subscriber."""
        sub = manager.get_subscriber("john@example.com")
        assert sub is None
    
    def test_unsubscribe_subscriber(self, manager):
        """Test soft delete (unsubscribe)."""
        manager.add_subscriber("john@example.com", "John Doe")
        result = manager.unsubscribe("john@example.com")
        
        assert result is True
        
        sub = manager.get_subscriber("john@example.com")
        assert sub.subscribed is False
    
    def test_get_active_subscribers(self, manager):
        """Test filtering active subscribers."""
        manager.add_subscriber("john@example.com", "John")
        manager.add_subscriber("jane@example.com", "Jane")
        manager.unsubscribe("john@example.com")
        
        active = manager.get_active_subscribers()
        assert len(active) == 1
        assert active[0].email == "jane@example.com"
    
    def test_subscriber_statistics(self, manager):
        """Test subscriber count statistics."""
        manager.add_subscriber("user1@example.com", "User 1")
        manager.add_subscriber("user2@example.com", "User 2")
        manager.add_subscriber("user3@example.com", "User 3")
        manager.unsubscribe("user1@example.com")
        
        assert manager.get_subscriber_count() == 3
        assert manager.get_active_subscriber_count() == 2
```

---

## Component 4: Flask API Testing

### Integration Test Template

```python
import pytest
import json
from web import create_app

class TestFlaskAPI:
    """Test Flask REST API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create Flask test client."""
        app = create_app()
        app.config['TESTING'] = True
        
        with app.test_client() as client:
            yield client
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        
        assert response.status_code == 200
        assert response.json['status'] == 'healthy'
    
    def test_get_subscribers_empty(self, client):
        """Test getting subscribers when empty."""
        response = client.get('/api/subscribers')
        
        assert response.status_code == 200
        data = response.json
        assert data['count'] == 0
        assert data['subscribers'] == []
    
    def test_add_subscriber(self, client):
        """Test adding subscriber via API."""
        response = client.post(
            '/api/subscribers',
            data=json.dumps({
                'email': 'john@example.com',
                'name': 'John Doe'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        assert response.json['message'] == 'Subscriber added successfully'
    
    def test_add_subscriber_duplicate(self, client):
        """Test adding duplicate subscriber."""
        # Add first
        client.post(
            '/api/subscribers',
            data=json.dumps({
                'email': 'john@example.com',
                'name': 'John Doe'
            }),
            content_type='application/json'
        )
        
        # Try duplicate
        response = client.post(
            '/api/subscribers',
            data=json.dumps({
                'email': 'john@example.com',
                'name': 'John Doe'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 409
        assert 'already exists' in response.json['error']
    
    def test_add_subscriber_invalid_email(self, client):
        """Test adding with invalid email."""
        response = client.post(
            '/api/subscribers',
            data=json.dumps({
                'email': 'invalid-email',
                'name': 'John'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        assert 'Invalid email' in response.json['error']
    
    def test_send_email(self, client):
        """Test sending email via API."""
        response = client.post(
            '/api/send-email',
            data=json.dumps({
                'to': 'user@example.com',
                'subject': 'Test',
                'body': 'Test body'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert 'sent successfully' in response.json['message']
    
    def test_get_statistics(self, client):
        """Test statistics endpoint."""
        # Add subscriber
        client.post(
            '/api/subscribers',
            data=json.dumps({
                'email': 'john@example.com',
                'name': 'John'
            }),
            content_type='application/json'
        )
        
        # Get stats
        response = client.get('/api/stats')
        
        assert response.status_code == 200
        stats = response.json
        assert stats['total_subscribers'] == 1
        assert 'emails_sent' in stats
```

---

## Coverage Requirements

### Minimum Coverage Goals

| Component | Minimum | Target |
|-----------|---------|--------|
| Functions | 100% | 100% |
| Branches | 80% | 90% |
| Lines | 85% | 95% |
| **Overall** | **80%** | **90%** |

### Running Coverage

```bash
# Generate coverage report
pytest --cov --cov-report=html

# View results
open htmlcov/index.html
```

---

## Best Practices

1. **Use fixtures** for setup/teardown
2. **Parametrize tests** for multiple scenarios
3. **Mock external services** (SMTP, databases)
4. **Test happy paths** and error cases
5. **Use descriptive names** for test functions
6. **One assertion per test** (or related assertions)
7. **Arrange-Act-Assert** pattern
8. **No test interdependencies** (tests should be independent)

---

## Common Patterns

### Pattern 1: Fixture with Setup/Teardown

```python
@pytest.fixture
def manager():
    """Setup fresh manager, teardown after."""
    manager = SubscriberManager()
    yield manager
    # Cleanup after test
    manager = None
```

### Pattern 2: Parametrized Test

```python
@pytest.mark.parametrize("input,expected", [
    ("valid@example.com", True),
    ("invalid", False),
    ("", False),
])
def test_validation(input, expected):
    assert validate(input) == expected
```

### Pattern 3: Error Testing

```python
def test_raises_error():
    """Test that specific error is raised."""
    with pytest.raises(ValueError, match="Email cannot be empty"):
        function_under_test("")
```

---

## Tools & Commands

### Run All Tests
```bash
pytest -v
```

### Run Specific Test File
```bash
pytest test_subscribers.py -v
```

### Run Specific Test Class
```bash
pytest test_subscribers.py::TestSubscriberManager -v
```

### Run Specific Test Method
```bash
pytest test_subscribers.py::TestSubscriberManager::test_add_subscriber_success -v
```

### Run with Coverage
```bash
pytest --cov --cov-report=html
```

### Run in Quiet Mode
```bash
pytest -q
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Import errors | Check sys.path and PYTHONPATH |
| Fixture not found | Ensure conftest.py exists or fixture is in same file |
| Tests not discovered | Use test_ prefix for functions, Test prefix for classes |
| Coverage too low | Add tests for edge cases and error paths |
| Test timeout | Increase timeout or optimize test performance |

---

## Integration with CI/CD

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    pip install -r requirements.txt
    pytest --cov --cov-report=xml

- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
```

---

**Skill Version**: 1.0  
**Test Framework**: pytest 7.4.0  
**Minimum Python**: 3.9  
**Last Updated**: 2026-06-21
