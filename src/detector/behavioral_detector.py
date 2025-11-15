"""
Behavioral Detector — User/entity behavior analysis for AEGIS
"""

from typing import Dict, List, Any, Optional
from collections import defaultdict
import time


class BehavioralDetector:
    """Detects threats based on behavioral patterns."""

    def __init__(self):
        """Initialize the behavioral detector."""
        self.user_profiles: Dict[str, Dict[str, Any]] = defaultdict(self._default_profile)
        self.ip_profiles: Dict[str, Dict[str, Any]] = defaultdict(self._default_profile)

    def _default_profile(self) -> Dict[str, Any]:
        """Create default profile structure."""
        return {
            "first_seen": time.time(),
            "last_seen": time.time(),
            "event_count": 0,
            "event_types": defaultdict(int),
            "failed_attempts": 0,
            "suspicious_score": 0,
        }

    def update_profile(self, event: Dict[str, Any]) -> None:
        """
        Update behavioral profile based on event.

        Args:
            event: Event to process
        """
        source_ip = event.get("source_ip")
        if not source_ip:
            return

        profile = self.ip_profiles[source_ip]
        profile["last_seen"] = event.get("timestamp", time.time())
        profile["event_count"] += 1
        profile["event_types"][event.get("type", "unknown")] += 1

        # Update suspicious score based on event type
        event_type = event.get("type", "")
        if event_type in ["cred-guess", "exploit", "exfil"]:
            profile["suspicious_score"] += 10
        elif event_type in ["scan"]:
            profile["suspicious_score"] += 5

        # Track failed attempts
        if "fail" in event_type or "denied" in event_type:
            profile["failed_attempts"] += 1

    def detect_behavioral_anomaly(self, source_ip: str) -> Optional[Dict[str, Any]]:
        """
        Detect behavioral anomalies for a source IP.

        Args:
            source_ip: Source IP to analyze

        Returns:
            Incident if behavioral anomaly detected, None otherwise
        """
        if source_ip not in self.ip_profiles:
            return None

        profile = self.ip_profiles[source_ip]

        # Check for rapid escalation
        if profile["event_count"] > 20 and (time.time() - profile["first_seen"]) < 60:
            return {
                "threat_type": "rapid_escalation",
                "action": "quarantine",
                "severity": "high",
                "reason": f"Rapid activity escalation: {profile['event_count']} events in < 1 minute",
                "source_ip": source_ip,
            }

        # Check for high suspicious score
        if profile["suspicious_score"] > 50:
            return {
                "threat_type": "suspicious_behavior",
                "action": "quarantine",
                "severity": "high",
                "reason": f"High suspicious score: {profile['suspicious_score']}",
                "source_ip": source_ip,
                "profile": dict(profile["event_types"]),
            }

        # Check for repeated failures
        if profile["failed_attempts"] > 10:
            return {
                "threat_type": "repeated_failures",
                "action": "monitor",
                "severity": "medium",
                "reason": f"Repeated failed attempts: {profile['failed_attempts']}",
                "source_ip": source_ip,
            }

        return None

    def detect_lateral_movement(self, events: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Detect lateral movement patterns.

        Args:
            events: Recent events to analyze

        Returns:
            Incident if lateral movement detected, None otherwise
        """
        # Track target diversity from single source
        source_targets = defaultdict(set)

        for event in events:
            source_ip = event.get("source_ip")
            target = event.get("target", "unknown")
            if source_ip:
                source_targets[source_ip].add(target)

        # Detect single source hitting multiple targets
        for source_ip, targets in source_targets.items():
            if len(targets) > 5:
                return {
                    "threat_type": "lateral_movement",
                    "action": "kill",
                    "severity": "critical",
                    "reason": f"Lateral movement detected: {source_ip} accessing {len(targets)} targets",
                    "source_ip": source_ip,
                    "target_count": len(targets),
                }

        return None

    def detect_privilege_escalation(self, events: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Detect privilege escalation attempts.

        Args:
            events: Recent events to analyze

        Returns:
            Incident if privilege escalation detected, None otherwise
        """
        # Look for patterns: normal activity -> exploit -> admin actions
        for i in range(len(events) - 2):
            if (events[i].get("type") == "recon" and
                events[i+1].get("type") == "exploit" and
                events[i+2].get("type") in ["admin-access", "config-change"]):

                return {
                    "threat_type": "privilege_escalation",
                    "action": "kill",
                    "severity": "critical",
                    "reason": "Privilege escalation pattern detected",
                    "source_ip": events[i].get("source_ip"),
                }

        return None
