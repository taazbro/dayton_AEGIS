"""
Microsoft Teams Integration — Send threat alerts to Teams channels
"""

import os
import requests
from typing import Dict, Any
import json


class TeamsNotifier:
    """Send threat alerts to Microsoft Teams via webhook"""

    def __init__(self):
        self.webhook_url = os.getenv("TEAMS_WEBHOOK_URL")

    def send_alert(self, threat_report: Dict[str, Any]) -> bool:
        """
        Send threat alert to Microsoft Teams.

        Args:
            threat_report: Threat report dictionary

        Returns:
            True if alert sent successfully
        """
        if not self.webhook_url:
            print("⚠️  Teams webhook URL not configured")
            return False

        try:
            incident = threat_report.get("incident_summary", {})
            severity = incident.get("severity", "UNKNOWN").upper()

            # Build Adaptive Card for Teams
            card = {
                "@type": "MessageCard",
                "@context": "https://schema.org/extensions",
                "summary": f"AEGIS Alert: {incident.get('threat_type')}",
                "themeColor": self._get_color(severity),
                "title": f"🛡️ AEGIS Cyber Defense Alert",
                "sections": [
                    {
                        "activityTitle": f"**{incident.get('threat_type', 'Unknown Threat')}**",
                        "activitySubtitle": f"Severity: **{severity}**",
                        "activityImage": "https://cdn-icons-png.flaticon.com/512/2913/2913133.png",
                        "facts": [
                            {
                                "name": "Threat Type:",
                                "value": incident.get("threat_type", "N/A")
                            },
                            {
                                "name": "Severity:",
                                "value": severity
                            },
                            {
                                "name": "Action Taken:",
                                "value": incident.get("action_taken", "None")
                            },
                            {
                                "name": "Event Count:",
                                "value": str(incident.get("event_count", 0))
                            },
                            {
                                "name": "Affected Entities:",
                                "value": ", ".join(incident.get("affected_entities", [])[:3]) or "None"
                            },
                            {
                                "name": "Detection Engines:",
                                "value": ", ".join(threat_report.get("detection_engines", []))
                            }
                        ],
                        "markdown": True
                    }
                ],
                "potentialAction": [
                    {
                        "@type": "OpenUri",
                        "name": "View Dashboard",
                        "targets": [
                            {
                                "os": "default",
                                "uri": "http://localhost:8080/dashboard"
                            }
                        ]
                    }
                ]
            }

            # Add MITRE ATT&CK tags if available
            mitre_tags = threat_report.get("mitre_tags", [])
            if mitre_tags:
                techniques = [f"{tag.get('technique')} ({tag.get('tactic')})" for tag in mitre_tags[:3]]
                card["sections"][0]["facts"].append({
                    "name": "MITRE Techniques:",
                    "value": ", ".join(techniques)
                })

            response = requests.post(
                self.webhook_url,
                json=card,
                headers={"Content-Type": "application/json"},
                timeout=5
            )

            if response.status_code == 200:
                print(f"✅ Teams alert sent: {incident.get('threat_type')}")
                return True
            else:
                print(f"❌ Teams API error: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"❌ Teams notification failed: {e}")
            return False

    def _get_color(self, severity: str) -> str:
        """Get color theme based on severity"""
        colors = {
            "CRITICAL": "FF0000",  # Red
            "HIGH": "FF6600",      # Orange
            "MEDIUM": "FFD700",    # Gold
            "LOW": "00AA00"        # Green
        }
        return colors.get(severity, "808080")  # Gray default


# Global instance
_teams_notifier = None


def get_teams_notifier() -> TeamsNotifier:
    """Get singleton Teams notifier"""
    global _teams_notifier
    if _teams_notifier is None:
        _teams_notifier = TeamsNotifier()
    return _teams_notifier
