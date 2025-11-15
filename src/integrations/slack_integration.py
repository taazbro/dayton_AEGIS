"""
AEGIS Slack Integration
Sends real-time security alerts to Slack channels via webhook
"""

import os
import json
import requests
from typing import Dict, Optional
from datetime import datetime


class SlackNotifier:
    """
    Sends formatted security alerts to Slack
    """

    def __init__(self, webhook_url: Optional[str] = None):
        """
        Initialize Slack notifier

        Args:
            webhook_url: Slack webhook URL (or set SLACK_WEBHOOK_URL env var)
        """
        self.webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
        self.enabled = bool(self.webhook_url)

    def send_alert(
        self,
        title: str,
        message: str,
        severity: str = "high",
        fields: Optional[Dict[str, str]] = None,
        incident_url: Optional[str] = None
    ) -> bool:
        """
        Send security alert to Slack

        Args:
            title: Alert title
            message: Alert message
            severity: 'critical', 'high', 'medium', 'low'
            fields: Additional fields to display
            incident_url: Link to full incident report

        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            return False

        # Color coding by severity
        colors = {
            "critical": "#DC143C",  # Crimson
            "high": "#FF4500",      # OrangeRed
            "medium": "#FFA500",    # Orange
            "low": "#FFD700"        # Gold
        }
        color = colors.get(severity.lower(), "#808080")

        # Build Slack message blocks
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚨 {title}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }
        ]

        # Add fields if provided
        if fields:
            field_blocks = []
            for key, value in fields.items():
                field_blocks.append({
                    "type": "mrkdwn",
                    "text": f"*{key}:*\n{value}"
                })

            blocks.append({
                "type": "section",
                "fields": field_blocks
            })

        # Add incident link if provided
        if incident_url:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<{incident_url}|📄 View Full Incident Report>"
                }
            })

        # Add timestamp
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
                }
            ]
        })

        # Build payload
        payload = {
            "attachments": [
                {
                    "color": color,
                    "blocks": blocks
                }
            ]
        }

        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Slack notification failed: {e}")
            return False

    def send_incident_alert(
        self,
        threat_name: str,
        threat_category: str,
        confidence: float,
        severity: int,
        response_time: float,
        actions_taken: int,
        data_lost: bool = False,
        incident_id: Optional[str] = None
    ) -> bool:
        """
        Send formatted incident alert

        Args:
            threat_name: Name of detected threat
            threat_category: Category (ransomware, infostealer, etc)
            confidence: Detection confidence (0-1)
            severity: Threat severity (1-10)
            response_time: Time to neutralize (seconds)
            actions_taken: Number of automated actions
            data_lost: Whether data was exfiltrated
            incident_id: Incident report ID

        Returns:
            True if sent successfully
        """
        # Determine severity level
        if severity >= 9:
            severity_level = "critical"
            status_emoji = "🔴"
        elif severity >= 7:
            severity_level = "high"
            status_emoji = "🟠"
        elif severity >= 5:
            severity_level = "medium"
            status_emoji = "🟡"
        else:
            severity_level = "low"
            status_emoji = "🟢"

        # Build message
        title = "SECURITY INCIDENT - NEUTRALIZED"

        message = f"""
*Attack Type:* {threat_name}
*Category:* {threat_category.upper()}
*Status:* ✅ STOPPED ({response_time:.1f}s detection-to-response)
*Damage:* {"❌ DATA LOST" if data_lost else "✅ ZERO (no data lost)"}
"""

        fields = {
            "Confidence": f"{confidence * 100:.1f}%",
            "Severity": f"{status_emoji} {severity}/10",
            "Response Time": f"{response_time:.1f}s",
            "Actions Taken": f"{actions_taken} automated responses"
        }

        incident_url = None
        if incident_id:
            incident_url = f"https://aegis.vezran.com/incidents/{incident_id}"

        return self.send_alert(
            title=title,
            message=message,
            severity=severity_level,
            fields=fields,
            incident_url=incident_url
        )

    def send_test_alert(self) -> bool:
        """Send a test alert to verify integration"""
        return self.send_alert(
            title="AEGIS Integration Test",
            message="✅ Slack integration is working!\n\nAEGIS autonomous defense is now connected to your SOC channel.",
            severity="low",
            fields={
                "Integration": "Slack Webhook",
                "Status": "✅ Active",
                "Sponsor": "AEGIS Hackathon Project"
            }
        )


# Test function
if __name__ == "__main__":
    print("🧪 Testing Slack Integration\n")
    print("=" * 70)

    notifier = SlackNotifier()

    if not notifier.enabled:
        print("⚠️  Slack webhook not configured")
        print("   Set SLACK_WEBHOOK_URL environment variable to enable")
        print("\nTo test with a webhook URL:")
        print("   export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/...'")
        print("   python3 src/integrations/slack_integration.py")
    else:
        print("✅ Slack webhook configured")
        print(f"   URL: {notifier.webhook_url[:50]}...")

        print("\n📤 Sending test alert...")
        success = notifier.send_test_alert()

        if success:
            print("✅ Test alert sent successfully!")
            print("   Check your Slack channel for the message")

            print("\n📤 Sending sample incident alert...")
            success = notifier.send_incident_alert(
                threat_name="Multi-Stage SQL Injection",
                threat_category="web_attack",
                confidence=0.957,
                severity=10,
                response_time=4.7,
                actions_taken=5,
                data_lost=False,
                incident_id="2024-001"
            )

            if success:
                print("✅ Incident alert sent successfully!")
            else:
                print("❌ Incident alert failed")
        else:
            print("❌ Test alert failed")
            print("   Check your webhook URL and try again")
