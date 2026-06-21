"""Subscriber management module for the Mailer application.

This module provides functionality to manage email subscribers and mailing lists.
It handles adding, removing, and querying subscribers with full validation.

Example:
    >>> manager = SubscriberManager()
    >>> manager.add_subscriber("john@example.com", "John Doe")
    >>> subscribers = manager.get_all_subscribers()
    >>> manager.remove_subscriber("john@example.com")
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import re


@dataclass
class Subscriber:
    """Represents an email subscriber.
    
    Attributes:
        email: Email address of the subscriber.
        name: Full name of the subscriber.
        subscribed: Whether the subscriber is active.
    """
    email: str
    name: str
    subscribed: bool = True


class SubscriberManager:
    """Manages email subscribers and mailing lists.
    
    This class provides functionality to add, remove, and query subscribers
    in a mailing system.
    """
    
    def __init__(self) -> None:
        """Initialize the subscriber manager with an empty subscriber list."""
        self._subscribers: Dict[str, Subscriber] = {}
    
    @staticmethod
    def _validate_email(email: str) -> bool:
        """Validate email address format.
        
        Args:
            email: Email address to validate.
            
        Returns:
            True if email is valid, False otherwise.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
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
        if not email or not name:
            raise ValueError("Email and name cannot be empty")
        
        if not self._validate_email(email):
            raise ValueError(f"Invalid email format: {email}")
        
        if email in self._subscribers:
            return False
        
        self._subscribers[email] = Subscriber(email=email, name=name)
        return True
    
    def remove_subscriber(self, email: str) -> bool:
        """Remove a subscriber from the mailing list.
        
        Args:
            email: Email address of the subscriber to remove.
            
        Returns:
            True if subscriber was removed, False if not found.
        """
        if email not in self._subscribers:
            return False
        
        del self._subscribers[email]
        return True
    
    def unsubscribe(self, email: str) -> bool:
        """Mark a subscriber as unsubscribed (soft delete).
        
        Args:
            email: Email address of the subscriber.
            
        Returns:
            True if subscriber was unsubscribed, False if not found.
        """
        if email not in self._subscribers:
            return False
        
        self._subscribers[email].subscribed = False
        return True
    
    def resubscribe(self, email: str) -> bool:
        """Reactivate an unsubscribed subscriber.
        
        Args:
            email: Email address of the subscriber.
            
        Returns:
            True if subscriber was reactivated, False if not found.
        """
        if email not in self._subscribers:
            return False
        
        self._subscribers[email].subscribed = True
        return True
    
    def get_subscriber(self, email: str) -> Optional[Subscriber]:
        """Get a specific subscriber by email.
        
        Args:
            email: Email address to look up.
            
        Returns:
            Subscriber object if found, None otherwise.
        """
        return self._subscribers.get(email)
    
    def get_all_subscribers(self) -> List[Subscriber]:
        """Get all subscribers in the mailing list.
        
        Returns:
            List of all Subscriber objects.
        """
        return list(self._subscribers.values())
    
    def get_active_subscribers(self) -> List[Subscriber]:
        """Get all active (subscribed) subscribers.
        
        Returns:
            List of active Subscriber objects.
        """
        return [s for s in self._subscribers.values() if s.subscribed]
    
    def get_subscriber_count(self) -> int:
        """Get total number of subscribers.
        
        Returns:
            Number of subscribers in the system.
        """
        return len(self._subscribers)
    
    def get_active_subscriber_count(self) -> int:
        """Get number of active subscribers.
        
        Returns:
            Number of active subscribers.
        """
        return len(self.get_active_subscribers())
