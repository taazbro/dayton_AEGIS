"""
Discord Integration — Send threat alerts to Discord channels
"""

import os
import requests
from typing import Dict, Any
import json


class DiscordNotifier:
    """Send threat alerts to Discord via webhook"""

    def __init__(self):
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def send_alert(self, threat_report: Dict[str, Any]) -> bool:
        """
        Send threat alert to Discord.

        Args:
            threat_report: Threat report dictionary

        Returns:
            True if alert sent successfully
        """
        if not self.webhook_url:
            print("⚠️  Discord webhook URL not configured")
            return False

        try:
            incident = threat_report.get("incident_summary", {})
            severity = incident.get("severity", "UNKNOWN").upper()

            # Build Discord embed
            embed = {
                "title": f"🛡️ AEGIS Cyber Defense Alert",
                "description": f"**{incident.get('threat_type', 'Unknown Threat')}** detected",
                "color": self._get_color(severity),
                "fields": [
                    {
                        "name": "🎯 Threat Type",
                        "value": incident.get("threat_type", "N/A"),
                        "inline": True
                    },
                    {
                        "name": "⚠️ Severity",
                        "value": severity,
                        "inline": True
                    },
                    {
                        "name": "🔧 Action Taken",
                        "value": incident.get("action_taken", "None"),
                        "inline": True
                    },
                    {
                        "name": "📊 Event Count",
                        "value": str(incident.get("event_count", 0)),
                        "inline": True
                    },
                    {
                        "name": "👥 Affected Entities",
                        "value": ", ".join(incident.get("affected_entities", [])[:3]) or "None",
                        "inline": False
                    },
                    {
                        "name": "🔍 Detection Engines",
                        "value": ", ".join(threat_report.get("detection_engines", [])),
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "AEGIS Autonomous Cyber Defense",
                    "icon_url": "https://cdn-icons-png.flaticon.com/512/2913/2913133.png"
                },
                "timestamp": threat_report.get("timestamp", "")
            }

            # Add MITRE ATT&CK tags if available
            mitre_tags = threat_report.get("mitre_tags", [])
            if mitre_tags:
                techniques = [f"`{tag.get('technique')}` ({tag.get('tactic')})" for tag in mitre_tags[:3]]
                embed["fields"].append({
                    "name": "🎭 MITRE ATT&CK Techniques",
                    "value": "\n".join(techniques),
                    "inline": False
                })

            payload = {
                "username": "AEGIS Defense Bot",
                "avatar_url": "https://cdn-icons-png.flaticon.com/512/2913/2913133.png",
                "embeds": [embed]
            }

            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=5
            )

            if response.status_code in [200, 204]:
                print(f"✅ Discord alert sent: {incident.get('threat_type')}")
                return True
            else:
                print(f"❌ Discord API error: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"❌ Discord notification failed: {e}")
            return False

    def _get_color(self, severity: str) -> int:
        """Get color code based on severity"""
        colors = {
            "CRITICAL": 0xFF0000,  # Red
            "HIGH": 0xFF6600,      # Orange
            "MEDIUM": 0xFFD700,    # Gold
            "LOW": 0x00AA00        # Green
        }
        return colors.get(severity, 0x808080)  # Gray default


# Global instance
_discord_notifier = None


def get_discord_notifier() -> DiscordNotifier:
    """Get singleton Discord notifier"""
    global _discord_notifier
    if _discord_notifier is None:
        _discord_notifier = DiscordNotifier()
    return _discord_notifier
