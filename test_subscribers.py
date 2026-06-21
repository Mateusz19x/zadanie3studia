"""Unit tests for the subscribers module.

Tests cover subscriber management operations including adding, removing,
and querying subscribers with various edge cases.
"""

import pytest
from subscribers import Subscriber, SubscriberManager


class TestSubscriber:
    """Test the Subscriber dataclass."""
    
    def test_subscriber_creation(self) -> None:
        """Test creating a subscriber instance."""
        subscriber = Subscriber(email="test@example.com", name="Test User")
        assert subscriber.email == "test@example.com"
        assert subscriber.name == "Test User"
        assert subscriber.subscribed is True
    
    def test_subscriber_unsubscribed(self) -> None:
        """Test creating an unsubscribed subscriber."""
        subscriber = Subscriber(email="test@example.com", name="Test User", subscribed=False)
        assert subscriber.subscribed is False


class TestSubscriberManager:
    """Test the SubscriberManager class."""
    
    @pytest.fixture
    def manager(self) -> SubscriberManager:
        """Create a fresh manager instance for each test."""
        return SubscriberManager()
    
    def test_add_subscriber_success(self, manager: SubscriberManager) -> None:
        """Test successfully adding a subscriber."""
        result = manager.add_subscriber("john@example.com", "John Doe")
        assert result is True
        assert manager.get_subscriber_count() == 1
    
    def test_add_subscriber_duplicate(self, manager: SubscriberManager) -> None:
        """Test adding a duplicate subscriber."""
        manager.add_subscriber("john@example.com", "John Doe")
        result = manager.add_subscriber("john@example.com", "John Doe")
        assert result is False
        assert manager.get_subscriber_count() == 1
    
    def test_add_subscriber_empty_email(self, manager: SubscriberManager) -> None:
        """Test adding subscriber with empty email."""
        with pytest.raises(ValueError):
            manager.add_subscriber("", "John Doe")
    
    def test_add_subscriber_empty_name(self, manager: SubscriberManager) -> None:
        """Test adding subscriber with empty name."""
        with pytest.raises(ValueError):
            manager.add_subscriber("john@example.com", "")
    
    def test_add_subscriber_invalid_email(self, manager: SubscriberManager) -> None:
        """Test adding subscriber with invalid email format."""
        with pytest.raises(ValueError):
            manager.add_subscriber("invalid-email", "John Doe")
    
    def test_remove_subscriber_success(self, manager: SubscriberManager) -> None:
        """Test successfully removing a subscriber."""
        manager.add_subscriber("john@example.com", "John Doe")
        result = manager.remove_subscriber("john@example.com")
        assert result is True
        assert manager.get_subscriber_count() == 0
    
    def test_remove_subscriber_not_found(self, manager: SubscriberManager) -> None:
        """Test removing a non-existent subscriber."""
        result = manager.remove_subscriber("john@example.com")
        assert result is False
    
    def test_get_subscriber(self, manager: SubscriberManager) -> None:
        """Test getting a specific subscriber."""
        manager.add_subscriber("john@example.com", "John Doe")
        subscriber = manager.get_subscriber("john@example.com")
        assert subscriber is not None
        assert subscriber.email == "john@example.com"
        assert subscriber.name == "John Doe"
    
    def test_get_subscriber_not_found(self, manager: SubscriberManager) -> None:
        """Test getting a non-existent subscriber."""
        subscriber = manager.get_subscriber("john@example.com")
        assert subscriber is None
    
    def test_get_all_subscribers(self, manager: SubscriberManager) -> None:
        """Test getting all subscribers."""
        manager.add_subscriber("john@example.com", "John Doe")
        manager.add_subscriber("jane@example.com", "Jane Doe")
        subscribers = manager.get_all_subscribers()
        assert len(subscribers) == 2
    
    def test_unsubscribe_success(self, manager: SubscriberManager) -> None:
        """Test unsubscribing a subscriber."""
        manager.add_subscriber("john@example.com", "John Doe")
        result = manager.unsubscribe("john@example.com")
        assert result is True
        subscriber = manager.get_subscriber("john@example.com")
        assert subscriber.subscribed is False
    
    def test_unsubscribe_not_found(self, manager: SubscriberManager) -> None:
        """Test unsubscribing a non-existent subscriber."""
        result = manager.unsubscribe("john@example.com")
        assert result is False
    
    def test_resubscribe_success(self, manager: SubscriberManager) -> None:
        """Test resubscribing a subscriber."""
        manager.add_subscriber("john@example.com", "John Doe")
        manager.unsubscribe("john@example.com")
        result = manager.resubscribe("john@example.com")
        assert result is True
        subscriber = manager.get_subscriber("john@example.com")
        assert subscriber.subscribed is True
    
    def test_get_active_subscribers(self, manager: SubscriberManager) -> None:
        """Test getting active subscribers."""
        manager.add_subscriber("john@example.com", "John Doe")
        manager.add_subscriber("jane@example.com", "Jane Doe")
        manager.unsubscribe("john@example.com")
        active = manager.get_active_subscribers()
        assert len(active) == 1
        assert active[0].email == "jane@example.com"
    
    def test_get_active_subscriber_count(self, manager: SubscriberManager) -> None:
        """Test getting count of active subscribers."""
        manager.add_subscriber("john@example.com", "John Doe")
        manager.add_subscriber("jane@example.com", "Jane Doe")
        manager.unsubscribe("john@example.com")
        count = manager.get_active_subscriber_count()
        assert count == 1
    
    def test_validate_email_valid(self) -> None:
        """Test email validation with valid emails."""
        assert SubscriberManager._validate_email("test@example.com") is True
        assert SubscriberManager._validate_email("user+tag@domain.co.uk") is True
    
    def test_validate_email_invalid(self) -> None:
        """Test email validation with invalid emails."""
        assert SubscriberManager._validate_email("invalid") is False
        assert SubscriberManager._validate_email("@example.com") is False
        assert SubscriberManager._validate_email("test@") is False
