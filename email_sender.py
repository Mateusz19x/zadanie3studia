"""Email sending module for the Mailer application.

This module provides functionality to send emails to subscribers.
It handles email composition, validation, and sending operations.

Example:
    >>> sender = EmailSender()
    >>> sender.send_email("john@example.com", "Subject", "Body text")
    True
"""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Email:
    """Represents an email message.

    Attributes:
        to: Recipient email address.
        subject: Email subject line.
        body: Email body content.
        sent_at: Timestamp when email was sent.
    """

    to: str
    subject: str
    body: str
    sent_at: Optional[datetime] = None


class EmailSender:
    """Handles email sending operations.

    This class provides functionality to send individual emails and
    batch emails to multiple recipients.
    """

    def __init__(
        self,
        smtp_server: str = "localhost",
        smtp_port: int = 587,
        sender_email: Optional[str] = None,
        sender_password: Optional[str] = None,
    ) -> None:
        """Initialize the email sender with SMTP configuration.

        Args:
            smtp_server: SMTP server address.
            smtp_port: SMTP server port.
            sender_email: Sender's email address.
            sender_password: Sender's email password.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self._sent_emails: List[Email] = []

    @staticmethod
    def _validate_recipient(email: str) -> bool:
        """Validate recipient email address.

        Args:
            email: Email address to validate.

        Returns:
            True if email is valid, False otherwise.
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    @staticmethod
    def _validate_subject(subject: str) -> bool:
        """Validate email subject.

        Args:
            subject: Subject line to validate.

        Returns:
            True if subject is valid, False otherwise.
        """
        return bool(subject and len(subject) > 0 and len(subject) <= 255)

    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send an email to a single recipient.

        Args:
            to: Recipient email address.
            subject: Email subject line.
            body: Email body content.

        Returns:
            True if email was sent successfully, False otherwise.

        Raises:
            ValueError: If email, subject, or body is invalid.
        """
        if not to or not subject or not body:
            raise ValueError("To, subject, and body cannot be empty")

        if not self._validate_recipient(to):
            raise ValueError(f"Invalid recipient email: {to}")

        if not self._validate_subject(subject):
            raise ValueError(f"Invalid subject: {subject}")

        # For now, simulate email sending
        # In production, this would connect to SMTP server
        email = Email(to=to, subject=subject, body=body, sent_at=datetime.now())
        self._sent_emails.append(email)
        return True

    def send_bulk_email(self, recipients: List[str], subject: str, body: str) -> int:
        """Send the same email to multiple recipients.

        Args:
            recipients: List of recipient email addresses.
            subject: Email subject line.
            body: Email body content.

        Returns:
            Number of emails sent successfully.

        Raises:
            ValueError: If inputs are invalid.
        """
        if not recipients:
            raise ValueError("Recipients list cannot be empty")

        if not subject or not body:
            raise ValueError("Subject and body cannot be empty")

        sent_count = 0
        for recipient in recipients:
            try:
                if self.send_email(recipient, subject, body):
                    sent_count += 1
            except ValueError:
                # Skip invalid recipients
                continue

        return sent_count

    def get_sent_emails(self) -> List[Email]:
        """Get list of all sent emails.

        Returns:
            List of Email objects that were sent.
        """
        return self._sent_emails.copy()

    def get_sent_count(self) -> int:
        """Get total number of emails sent.

        Returns:
            Number of sent emails.
        """
        return len(self._sent_emails)

    def clear_history(self) -> None:
        """Clear the email sending history."""
        self._sent_emails.clear()
