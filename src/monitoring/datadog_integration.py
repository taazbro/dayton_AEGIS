"""
Datadog Integration — Send metrics, traces, and events to Datadog
"""

import os
import requests
from typing import Dict, Any, List
import json
import time


class DatadogMonitoring:
    """Send metrics and events to Datadog for comprehensive monitoring"""

    def __init__(self):
        self.api_key = os.getenv("DATADOG_API_KEY")
        self.app_key = os.getenv("DATADOG_APP_KEY")
        self.site = os.getenv("DATADOG_SITE", "datadoghq.com")
        self.metrics_url = f"https://api.{self.site}/api/v2/series"
        self.events_url = f"https://api.{self.site}/api/v1/events"

    def send_metrics(self, metrics: List[Dict[str, Any]]) -> bool:
        """
        Send custom metrics to Datadog.

        Args:
            metrics: List of metric dictionaries

        Returns:
            True if metrics sent successfully
        """
        if not self.api_key:
            return False

        try:
            payload = {
                "series": metrics
            }

            headers = {
                "Content-Type": "application/json",
                "DD-API-KEY": self.api_key
            }

            response = requests.post(
                self.metrics_url,
                json=payload,
                headers=headers,
                timeout=5
            )

            return response.status_code == 202

        except Exception as e:
            print(f"❌ Datadog metrics failed: {e}")
            return False

    def send_threat_metrics(self, threat_report: Dict[str, Any]) -> bool:
        """
        Send threat-related metrics to Datadog.

        Args:
            threat_report: Threat report dictionary

        Returns:
            True if metrics sent successfully
        """
        incident = threat_report.get("incident_summary", {})
        severity = incident.get("severity", "UNKNOWN").upper()

        # Map severity to numeric value
        severity_map = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        severity_value = severity_map.get(severity, 0)

        timestamp = int(time.time())

        metrics = [
            {
                "metric": "aegis.threats.detected",
                "type": 1,  # Counter
                "points": [{"timestamp": timestamp, "value": 1}],
                "tags": [
                    f"threat_type:{incident.get('threat_type', 'unknown')}",
                    f"severity:{severity.lower()}",
                    f"action:{incident.get('action_taken', 'none')}"
                ]
            },
            {
                "metric": "aegis.threats.severity",
                "type": 0,  # Gauge
                "points": [{"timestamp": timestamp, "value": severity_value}],
                "tags": [
                    f"threat_type:{incident.get('threat_type', 'unknown')}"
                ]
            },
            {
                "metric": "aegis.events.count",
                "type": 0,  # Gauge
                "points": [{"timestamp": timestamp, "value": incident.get("event_count", 0)}],
                "tags": [
                    f"threat_type:{incident.get('threat_type', 'unknown')}"
                ]
            }
        ]

        # Add detection engine metrics
        for engine in threat_report.get("detection_engines", []):
            metrics.append({
                "metric": "aegis.detection.engine",
                "type": 1,  # Counter
                "points": [{"timestamp": timestamp, "value": 1}],
                "tags": [
                    f"engine:{engine}",
                    f"threat_type:{incident.get('threat_type', 'unknown')}"
                ]
            })

        return self.send_metrics(metrics)

    def send_event(self, threat_report: Dict[str, Any]) -> bool:
        """
        Send threat event to Datadog Events.

        Args:
            threat_report: Threat report dictionary

        Returns:
            True if event sent successfully
        """
        if not self.api_key:
            return False

        try:
            incident = threat_report.get("incident_summary", {})
            severity = incident.get("severity", "UNKNOWN").upper()

            event = {
                "title": f"AEGIS: {incident.get('threat_type', 'Unknown Threat')}",
                "text": f"""
**Threat Type:** {incident.get('threat_type')}
**Severity:** {severity}
**Action Taken:** {incident.get('action_taken', 'None')}
**Event Count:** {incident.get('event_count', 0)}
**Affected Entities:** {', '.join(incident.get('affected_entities', []))}
**Detection Engines:** {', '.join(threat_report.get('detection_engines', []))}
                """.strip(),
                "alert_type": self._map_alert_type(severity),
                "tags": [
                    f"threat_type:{incident.get('threat_type', 'unknown')}",
                    f"severity:{severity.lower()}",
                    "source:aegis"
                ]
            }

            headers = {
                "Content-Type": "application/json",
                "DD-API-KEY": self.api_key
            }

            response = requests.post(
                self.events_url,
                json=event,
                headers=headers,
                timeout=5
            )

            if response.status_code == 202:
                print(f"✅ Datadog event sent: {incident.get('threat_type')}")
                return True
            else:
                return False

        except Exception as e:
            print(f"❌ Datadog event failed: {e}")
            return False

    def _map_alert_type(self, severity: str) -> str:
        """Map AEGIS severity to Datadog alert type"""
        mapping = {
            "CRITICAL": "error",
            "HIGH": "error",
            "MEDIUM": "warning",
            "LOW": "info"
        }
        return mapping.get(severity, "info")


# Global instance
_datadog_monitoring = None


def get_datadog_monitoring() -> DatadogMonitoring:
    """Get singleton Datadog monitoring instance"""
    global _datadog_monitoring
    if _datadog_monitoring is None:
        _datadog_monitoring = DatadogMonitoring()
    return _datadog_monitoring
