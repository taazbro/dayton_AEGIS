"""
Webhook Notifier — Send alerts to external systems via webhooks
"""

import os
import json
import time
from typing import Dict, List, Any, Optional
import requests


class WebhookNotifier:
    """Sends alert notifications via webhooks."""

    def __init__(self):
        """Initialize webhook notifier."""
        self.slack_webhook = os.getenv("SLACK_WEBHOOK")
        self.custom_webhooks: List[str] = []
        self.retry_attempts = 3
        self.timeout = 5

    def add_webhook(self, webhook_url: str) -> None:
        """
        Add a custom webhook URL.

        Args:
            webhook_url: Webhook URL to add
        """
        self.custom_webhooks.append(webhook_url)

    def send_slack_alert(self, incident: Dict[str, Any]) -> bool:
        """
        Send alert to Slack.

        Args:
            incident: Incident to alert about

        Returns:
            True if successful, False otherwise
        """
        if not self.slack_webhook:
            print("⚠️  Slack webhook not configured")
            return False

        # Build Slack message
        message = self._build_slack_message(incident)

        return self._send_webhook(self.slack_webhook, message)

    def _build_slack_message(self, incident: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build Slack-formatted message.

        Args:
            incident: Incident details

        Returns:
            Slack message payload
        """
        threat_type = incident.get("threat_type", "Unknown")
        severity = incident.get("severity", "unknown")
        reason = incident.get("reason", "No reason provided")
        action = incident.get("action", "none")

        # Color based on severity
        color_map = {
            "critical": "#FF0000",
            "high": "#FF8C00",
            "medium": "#FFD700",
            "low": "#00FF00",
        }
        color = color_map.get(severity.lower(), "#808080")

        # Emoji based on severity
        emoji_map = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢",
        }
        emoji = emoji_map.get(severity.lower(), "⚪")

        return {
            "text": f"{emoji} AEGIS Security Alert",
            "attachments": [
                {
                    "color": color,
                    "title": f"Threat Detected: {threat_type}",
                    "fields": [
                        {
                            "title": "Severity",
                            "value": severity.upper(),
                            "short": True
                        },
                        {
                            "title": "Action",
                            "value": action.upper(),
                            "short": True
                        },
                        {
                            "title": "Details",
                            "value": reason,
                            "short": False
                        },
                    ],
                    "footer": "Zyberpol AEGIS",
                    "ts": int(time.time())
                }
            ]
        }

    def send_generic_webhook(self, incident: Dict[str, Any], webhook_url: str) -> bool:
        """
        Send alert to generic webhook.

        Args:
            incident: Incident to alert about
            webhook_url: Webhook URL

        Returns:
            True if successful, False otherwise
        """
        message = {
            "alert_type": "security_incident",
            "timestamp": time.time(),
            "incident": incident,
            "source": "zyberpol-aegis",
        }

        return self._send_webhook(webhook_url, message)

    def _send_webhook(self, webhook_url: str, payload: Dict[str, Any]) -> bool:
        """
        Send webhook with retry logic.

        Args:
            webhook_url: Webhook URL
            payload: Message payload

        Returns:
            True if successful, False otherwise
        """
        for attempt in range(self.retry_attempts):
            try:
                response = requests.post(
                    webhook_url,
                    json=payload,
                    timeout=self.timeout,
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code == 200:
                    print(f"✓ Webhook alert sent successfully")
                    return True
                else:
                    print(f"⚠️  Webhook returned status {response.status_code}")

            except requests.exceptions.Timeout:
                print(f"⚠️  Webhook timeout (attempt {attempt + 1}/{self.retry_attempts})")
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Webhook error: {e}")

            if attempt < self.retry_attempts - 1:
                time.sleep(1)  # Wait before retry

        return False

    def broadcast_incident(self, incident: Dict[str, Any]) -> Dict[str, bool]:
        """
        Send incident to all configured webhooks.

        Args:
            incident: Incident to broadcast

        Returns:
            Dict mapping webhook types to success status
        """
        results = {}

        # Send to Slack if configured
        if self.slack_webhook:
            results["slack"] = self.send_slack_alert(incident)

        # Send to custom webhooks
        for i, webhook_url in enumerate(self.custom_webhooks):
            success = self.send_generic_webhook(incident, webhook_url)
            results[f"custom_webhook_{i}"] = success

        return results

    def send_test_alert(self) -> None:
        """Send a test alert to verify webhook configuration."""
        test_incident = {
            "threat_type": "test_alert",
            "severity": "low",
            "action": "monitor",
            "reason": "This is a test alert from Zyberpol AEGIS",
            "timestamp": time.time(),
        }

        print("\n🧪 Sending test alerts...")
        results = self.broadcast_incident(test_incident)

        print("\nResults:")
        for webhook_type, success in results.items():
            status = "✓ Success" if success else "✗ Failed"
            print(f"  {webhook_type}: {status}")


class EmailNotifier:
    """Send email notifications (mock implementation)."""

    def __init__(self):
        """Initialize email notifier."""
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = os.getenv("SMTP_PORT", "587")
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("ALERT_FROM_EMAIL", "aegis@zyberpol.io")
        self.to_emails: List[str] = []

    def add_recipient(self, email: str) -> None:
        """
        Add email recipient.

        Args:
            email: Email address
        """
        self.to_emails.append(email)

    def send_email_alert(self, incident: Dict[str, Any]) -> bool:
        """
        Send email alert (mocked for hackathon).

        Args:
            incident: Incident to alert about

        Returns:
            True (always succeeds in mock mode)
        """
        print("\n📧 EMAIL ALERT (MOCKED)")
        print(f"To: {', '.join(self.to_emails) if self.to_emails else 'No recipients'}")
        print(f"Subject: [AEGIS] {incident.get('severity', 'UNKNOWN').upper()} - {incident.get('threat_type', 'Unknown Threat')}")
        print(f"Body: {incident.get('reason', 'No details')}")
        print()

        return True
