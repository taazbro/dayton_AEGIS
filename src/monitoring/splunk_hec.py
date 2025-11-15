"""
Splunk HEC Integration — Forward events to Splunk HTTP Event Collector
"""

import os
import requests
from typing import Dict, Any
import json
import time


class SplunkHEC:
    """Forward security events to Splunk via HTTP Event Collector"""

    def __init__(self):
        self.hec_token = os.getenv("SPLUNK_HEC_TOKEN")
        self.hec_url = os.getenv("SPLUNK_HEC_URL", "https://localhost:8088/services/collector/event")
        self.index = os.getenv("SPLUNK_INDEX", "aegis_security")
        self.source = "aegis:defense"
        self.sourcetype = "_json"

    def send_event(self, threat_report: Dict[str, Any]) -> bool:
        """
        Send threat event to Splunk HEC.

        Args:
            threat_report: Threat report dictionary

        Returns:
            True if event sent successfully
        """
        if not self.hec_token:
            print("⚠️  Splunk HEC token not configured")
            return False

        try:
            incident = threat_report.get("incident_summary", {})

            # Build Splunk HEC event
            event = {
                "time": time.time(),
                "host": "aegis-defense",
                "source": self.source,
                "sourcetype": self.sourcetype,
                "index": self.index,
                "event": {
                    "event_type": "threat_detected",
                    "threat_type": incident.get("threat_type"),
                    "severity": incident.get("severity"),
                    "action_taken": incident.get("action_taken"),
                    "event_count": incident.get("event_count", 0),
                    "affected_entities": incident.get("affected_entities", []),
                    "attack_pattern": incident.get("attack_pattern"),
                    "detection_engines": threat_report.get("detection_engines", []),
                    "mitre_tags": threat_report.get("mitre_tags", []),
                    "timestamp": threat_report.get("timestamp"),
                    "recommendations": threat_report.get("recommendations", [])
                },
                "fields": {
                    "threat_type": incident.get("threat_type"),
                    "severity": incident.get("severity"),
                    "action": incident.get("action_taken")
                }
            }

            headers = {
                "Authorization": f"Splunk {self.hec_token}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                self.hec_url,
                json=event,
                headers=headers,
                verify=False,  # For self-signed certs in dev
                timeout=5
            )

            if response.status_code == 200:
                print(f"✅ Splunk HEC event sent: {incident.get('threat_type')}")
                return True
            else:
                print(f"❌ Splunk HEC error: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"❌ Splunk HEC failed: {e}")
            return False

    def send_metrics(self, metric_data: Dict[str, Any]) -> bool:
        """
        Send metric data to Splunk.

        Args:
            metric_data: Metric dictionary

        Returns:
            True if metrics sent successfully
        """
        if not self.hec_token:
            return False

        try:
            event = {
                "time": time.time(),
                "host": "aegis-defense",
                "source": "aegis:metrics",
                "sourcetype": "aegis:metrics",
                "index": self.index,
                "event": "metric",
                "fields": metric_data
            }

            headers = {
                "Authorization": f"Splunk {self.hec_token}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                self.hec_url,
                json=event,
                headers=headers,
                verify=False,
                timeout=5
            )

            return response.status_code == 200

        except Exception as e:
            print(f"❌ Splunk metrics failed: {e}")
            return False


# Global instance
_splunk_hec = None


def get_splunk_hec() -> SplunkHEC:
    """Get singleton Splunk HEC instance"""
    global _splunk_hec
    if _splunk_hec is None:
        _splunk_hec = SplunkHEC()
    return _splunk_hec
