"""Unit tests for the email_sender module.

Tests cover email sending operations including single emails, bulk emails,
and validation with various edge cases.
"""

import pytest
from datetime import datetime
from email_sender import Email, EmailSender


class TestEmail:
    """Test the Email dataclass."""
    
    def test_email_creation(self) -> None:
        """Test creating an email instance."""
        email = Email(to="test@example.com", subject="Test", body="Body text")
        assert email.to == "test@example.com"
        assert email.subject == "Test"
        assert email.body == "Body text"
        assert email.sent_at is None
    
    def test_email_with_timestamp(self) -> None:
        """Test creating an email with timestamp."""
        now = datetime.now()
        email = Email(to="test@example.com", subject="Test", body="Body", sent_at=now)
        assert email.sent_at == now


class TestEmailSender:
    """Test the EmailSender class."""
    
    @pytest.fixture
    def sender(self) -> EmailSender:
        """Create a fresh sender instance for each test."""
        return EmailSender()
    
    def test_sender_creation(self) -> None:
        """Test creating an email sender instance."""
        sender = EmailSender()
        assert sender.smtp_server == "localhost"
        assert sender.smtp_port == 587
        assert sender.get_sent_count() == 0
    
    def test_sender_with_credentials(self) -> None:
        """Test creating sender with credentials."""
        sender = EmailSender(
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            sender_email="user@gmail.com",
            sender_password="password"
        )
        assert sender.smtp_server == "smtp.gmail.com"
        assert sender.sender_email == "user@gmail.com"
    
    def test_send_email_success(self, sender: EmailSender) -> None:
        """Test successfully sending an email."""
        result = sender.send_email(
            "recipient@example.com",
            "Test Subject",
            "Test body"
        )
        assert result is True
        assert sender.get_sent_count() == 1
    
    def test_send_email_empty_to(self, sender: EmailSender) -> None:
        """Test sending email with empty recipient."""
        with pytest.raises(ValueError):
            sender.send_email("", "Subject", "Body")
    
    def test_send_email_empty_subject(self, sender: EmailSender) -> None:
        """Test sending email with empty subject."""
        with pytest.raises(ValueError):
            sender.send_email("test@example.com", "", "Body")
    
    def test_send_email_empty_body(self, sender: EmailSender) -> None:
        """Test sending email with empty body."""
        with pytest.raises(ValueError):
            sender.send_email("test@example.com", "Subject", "")
    
    def test_send_email_invalid_recipient(self, sender: EmailSender) -> None:
        """Test sending email with invalid recipient."""
        with pytest.raises(ValueError):
            sender.send_email("invalid-email", "Subject", "Body")
    
    def test_send_email_subject_too_long(self, sender: EmailSender) -> None:
        """Test sending email with very long subject."""
        long_subject = "a" * 300
        with pytest.raises(ValueError):
            sender.send_email("test@example.com", long_subject, "Body")
    
    def test_send_email_updates_timestamp(self, sender: EmailSender) -> None:
        """Test that sent emails have timestamps."""
        sender.send_email("test@example.com", "Subject", "Body")
        emails = sender.get_sent_emails()
        assert len(emails) == 1
        assert emails[0].sent_at is not None
        assert isinstance(emails[0].sent_at, datetime)
    
    def test_send_bulk_email_success(self, sender: EmailSender) -> None:
        """Test successfully sending bulk emails."""
        recipients = [
            "john@example.com",
            "jane@example.com",
            "bob@example.com"
        ]
        count = sender.send_bulk_email(recipients, "Subject", "Body")
        assert count == 3
        assert sender.get_sent_count() == 3
    
    def test_send_bulk_email_empty_recipients(self, sender: EmailSender) -> None:
        """Test sending bulk email with empty recipients list."""
        with pytest.raises(ValueError):
            sender.send_bulk_email([], "Subject", "Body")
    
    def test_send_bulk_email_empty_subject(self, sender: EmailSender) -> None:
        """Test sending bulk email with empty subject."""
        with pytest.raises(ValueError):
            sender.send_bulk_email(["test@example.com"], "", "Body")
    
    def test_send_bulk_email_with_invalid_recipients(self, sender: EmailSender) -> None:
        """Test sending bulk email skips invalid recipients."""
        recipients = [
            "john@example.com",
            "invalid-email",
            "jane@example.com"
        ]
        count = sender.send_bulk_email(recipients, "Subject", "Body")
        assert count == 2
    
    def test_get_sent_emails(self, sender: EmailSender) -> None:
        """Test retrieving sent emails."""
        sender.send_email("test1@example.com", "Subject 1", "Body 1")
        sender.send_email("test2@example.com", "Subject 2", "Body 2")
        emails = sender.get_sent_emails()
        assert len(emails) == 2
        assert emails[0].to == "test1@example.com"
        assert emails[1].to == "test2@example.com"
    
    def test_get_sent_emails_returns_copy(self, sender: EmailSender) -> None:
        """Test that get_sent_emails returns a copy, not reference."""
        sender.send_email("test@example.com", "Subject", "Body")
        emails = sender.get_sent_emails()
        emails.clear()
        # Original list should still have the email
        assert sender.get_sent_count() == 1
    
    def test_clear_history(self, sender: EmailSender) -> None:
        """Test clearing email history."""
        sender.send_email("test@example.com", "Subject", "Body")
        assert sender.get_sent_count() == 1
        sender.clear_history()
        assert sender.get_sent_count() == 0
    
    def test_validate_recipient_valid(self) -> None:
        """Test recipient validation with valid emails."""
        assert EmailSender._validate_recipient("test@example.com") is True
        assert EmailSender._validate_recipient("user+tag@domain.co.uk") is True
    
    def test_validate_recipient_invalid(self) -> None:
        """Test recipient validation with invalid emails."""
        assert EmailSender._validate_recipient("invalid") is False
        assert EmailSender._validate_recipient("@example.com") is False
    
    def test_validate_subject_valid(self) -> None:
        """Test subject validation with valid subjects."""
        assert EmailSender._validate_subject("Test Subject") is True
        assert EmailSender._validate_subject("a") is True
    
    def test_validate_subject_invalid(self) -> None:
        """Test subject validation with invalid subjects."""
        assert EmailSender._validate_subject("") is False
        assert EmailSender._validate_subject("a" * 300) is False
