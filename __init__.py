"""Mailer package.

A complete email and mailing list management system with Flask web interface.

Modules:
    subscribers: Subscriber management functionality.
    email_sender: Email sending operations.
    web: Flask web application and API endpoints.
"""

__version__ = "1.0.0"
__author__ = "Mailer Team"

from subscribers import Subscriber, SubscriberManager
from email_sender import Email, EmailSender
from web import create_app

__all__ = [
    "Subscriber",
    "SubscriberManager",
    "Email",
    "EmailSender",
    "create_app",
]
