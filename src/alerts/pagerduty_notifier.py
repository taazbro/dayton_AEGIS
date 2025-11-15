"""
PagerDuty Integration — Escalate critical incidents to on-call responders
"""

import os
import requests
from typing import Dict, Any
import json


class PagerDutyNotifier:
    """Send incidents to PagerDuty for on-call escalation"""

    def __init__(self):
        self.integration_key = os.getenv("PAGERDUTY_INTEGRATION_KEY")
        self.api_url = "https://events.pagerduty.com/v2/enqueue"

    def trigger_incident(self, threat_report: Dict[str, Any]) -> bool:
        """
        Trigger a PagerDuty incident for critical threats.

        Args:
            threat_report: Threat report dictionary

        Returns:
            True if incident created successfully
        """
        if not self.integration_key:
            print("⚠️  PagerDuty integration key not configured")
            return False

        try:
            incident = threat_report.get("incident_summary", {})
            severity = incident.get("severity", "UNKNOWN").upper()

            # Only escalate HIGH or CRITICAL incidents
            if severity not in ["HIGH", "CRITICAL"]:
                return False

            payload = {
                "routing_key": self.integration_key,
                "event_action": "trigger",
                "payload": {
                    "summary": f"🚨 {incident.get('threat_type', 'Unknown Threat')} Detected",
                    "severity": self._map_severity(severity),
                    "source": "AEGIS Cyber Defense",
                    "component": "Threat Detector",
                    "group": "Security Operations",
                    "class": incident.get("attack_pattern", "cyber_attack"),
                    "custom_details": {
                        "threat_type": incident.get("threat_type"),
                        "severity": severity,
                        "action_taken": incident.get("action_taken"),
                        "affected_entities": incident.get("affected_entities", []),
                        "event_count": incident.get("event_count", 0),
                        "detection_engines": threat_report.get("detection_engines", []),
                        "mitre_techniques": [tag.get("technique") for tag in threat_report.get("mitre_tags", [])],
                    }
                },
                "dedup_key": self._generate_dedup_key(threat_report),
                "links": [],
                "images": []
            }

            response = requests.post(
                self.api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=5
            )

            if response.status_code == 202:
                print(f"✅ PagerDuty incident triggered: {incident.get('threat_type')}")
                return True
            else:
                print(f"❌ PagerDuty API error: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"❌ PagerDuty notification failed: {e}")
            return False

    def _map_severity(self, aegis_severity: str) -> str:
        """Map AEGIS severity to PagerDuty severity"""
        mapping = {
            "CRITICAL": "critical",
            "HIGH": "error",
            "MEDIUM": "warning",
            "LOW": "info"
        }
        return mapping.get(aegis_severity, "error")

    def _generate_dedup_key(self, threat_report: Dict[str, Any]) -> str:
        """Generate deduplication key to prevent duplicate incidents"""
        incident = threat_report.get("incident_summary", {})
        # Group similar incidents within 1 hour
        import hashlib
        import time
        key_parts = [
            incident.get("threat_type", ""),
            incident.get("severity", ""),
            str(int(time.time() // 3600))  # Hour bucket
        ]
        return hashlib.md5("|".join(key_parts).encode()).hexdigest()


# Global instance
_pagerduty_notifier = None


def get_pagerduty_notifier() -> PagerDutyNotifier:
    """Get singleton PagerDuty notifier"""
    global _pagerduty_notifier
    if _pagerduty_notifier is None:
        _pagerduty_notifier = PagerDutyNotifier()
    return _pagerduty_notifier
