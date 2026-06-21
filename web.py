"""Flask web application for the Mailer system.

This module provides a web interface for managing subscribers and sending emails.
It includes endpoints for subscriber management and bulk email operations.

Example:
    >>> from web import create_app
    >>> app = create_app()
    >>> app.run(debug=True)
"""

from typing import Any, Dict, Tuple

from flask import Flask, jsonify, request

from email_sender import EmailSender
from subscribers import SubscriberManager


def create_app() -> Flask:
    """Create and configure the Flask application.

    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__)

    # Initialize managers
    subscriber_manager = SubscriberManager()
    email_sender = EmailSender()

    # ===== SUBSCRIBER ENDPOINTS =====

    @app.route("/api/subscribers", methods=["GET"])
    def get_subscribers() -> Tuple[Dict[str, Any], int]:
        """Get all subscribers.

        Returns:
            JSON response with list of subscribers and HTTP status code.
        """
        subscribers = subscriber_manager.get_all_subscribers()
        data = [
            {"email": s.email, "name": s.name, "subscribed": s.subscribed}
            for s in subscribers
        ]
        return jsonify({"subscribers": data, "count": len(data)}), 200

    @app.route("/api/subscribers/active", methods=["GET"])
    def get_active_subscribers() -> Tuple[Dict[str, Any], int]:
        """Get active subscribers only.

        Returns:
            JSON response with list of active subscribers and HTTP status code.
        """
        subscribers = subscriber_manager.get_active_subscribers()
        data = [{"email": s.email, "name": s.name} for s in subscribers]
        return jsonify({"subscribers": data, "count": len(data)}), 200

    @app.route("/api/subscribers", methods=["POST"])
    def add_subscriber() -> Tuple[Dict[str, Any], int]:
        """Add a new subscriber.

        Expected JSON body:
            {
                "email": "user@example.com",
                "name": "John Doe"
            }

        Returns:
            JSON response with status and HTTP status code.
        """
        try:
            data = request.get_json()

            if not data or "email" not in data or "name" not in data:
                return jsonify({"error": "Email and name are required"}), 400

            success = subscriber_manager.add_subscriber(data["email"], data["name"])

            if not success:
                return jsonify({"error": "Subscriber already exists"}), 409

            return jsonify({"message": "Subscriber added successfully"}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/api/subscribers/<email>", methods=["DELETE"])
    def remove_subscriber(email: str) -> Tuple[Dict[str, Any], int]:
        """Remove a subscriber.

        Args:
            email: Email address of subscriber to remove.

        Returns:
            JSON response with status and HTTP status code.
        """
        success = subscriber_manager.remove_subscriber(email)

        if not success:
            return jsonify({"error": "Subscriber not found"}), 404

        return jsonify({"message": "Subscriber removed successfully"}), 200

    @app.route("/api/subscribers/<email>/unsubscribe", methods=["POST"])
    def unsubscribe(email: str) -> Tuple[Dict[str, Any], int]:
        """Unsubscribe a subscriber (soft delete).

        Args:
            email: Email address of subscriber to unsubscribe.

        Returns:
            JSON response with status and HTTP status code.
        """
        success = subscriber_manager.unsubscribe(email)

        if not success:
            return jsonify({"error": "Subscriber not found"}), 404

        return jsonify({"message": "Subscriber unsubscribed"}), 200

    # ===== EMAIL SENDING ENDPOINTS =====

    @app.route("/api/send-email", methods=["POST"])
    def send_single_email() -> Tuple[Dict[str, Any], int]:
        """Send an email to a single recipient.

        Expected JSON body:
            {
                "to": "user@example.com",
                "subject": "Hello",
                "body": "Email content"
            }

        Returns:
            JSON response with status and HTTP status code.
        """
        try:
            data = request.get_json()

            if (
                not data
                or "to" not in data
                or "subject" not in data
                or "body" not in data
            ):
                return jsonify({"error": "To, subject, and body are required"}), 400

            success = email_sender.send_email(data["to"], data["subject"], data["body"])

            if not success:
                return jsonify({"error": "Failed to send email"}), 500

            return jsonify({"message": "Email sent successfully"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/api/send-bulk-email", methods=["POST"])
    def send_bulk_email_endpoint() -> Tuple[Dict[str, Any], int]:
        """Send the same email to multiple subscribers.

        Expected JSON body:
            {
                "subject": "Newsletter",
                "body": "Email content"
            }

        Sends to all active subscribers.

        Returns:
            JSON response with count of emails sent and HTTP status code.
        """
        try:
            data = request.get_json()

            if not data or "subject" not in data or "body" not in data:
                return jsonify({"error": "Subject and body are required"}), 400

            active_subscribers = subscriber_manager.get_active_subscribers()
            recipient_emails = [s.email for s in active_subscribers]

            if not recipient_emails:
                return jsonify({"error": "No active subscribers found"}), 400

            sent_count = email_sender.send_bulk_email(
                recipient_emails, data["subject"], data["body"]
            )

            return (
                jsonify(
                    {
                        "message": f"Emails sent to {sent_count} recipients",
                        "count": sent_count,
                    }
                ),
                200,
            )
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    # ===== STATS ENDPOINTS =====

    @app.route("/api/stats", methods=["GET"])
    def get_stats() -> Tuple[Dict[str, Any], int]:
        """Get system statistics.

        Returns:
            JSON response with statistics and HTTP status code.
        """
        stats = {
            "total_subscribers": subscriber_manager.get_subscriber_count(),
            "active_subscribers": subscriber_manager.get_active_subscriber_count(),
            "emails_sent": email_sender.get_sent_count(),
        }
        return jsonify(stats), 200

    # ===== HEALTH CHECK =====

    @app.route("/health", methods=["GET"])
    def health_check() -> Tuple[Dict[str, str], int]:
        """Health check endpoint.

        Returns:
            JSON response indicating service is healthy and HTTP status code.
        """
        return jsonify({"status": "healthy"}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
