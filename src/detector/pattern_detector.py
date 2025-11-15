"""
Pattern Detector — Rule-based attack pattern detection
"""

from typing import Dict, Any, Optional, List


class PatternDetector:
    """Detects attack patterns using simple heuristics."""

    def __init__(self):
        """Initialize the pattern detector with detection rules."""
        # Thresholds for different attack types
        self.thresholds = {
            "cred-guess": 3,  # 3+ credential guesses = suspicious
            "scan": 5,        # 5+ scans = port scanning
            "exploit": 2,     # 2+ exploits = active attack
            "exfil": 1,       # Any exfiltration = critical
        }

    def analyze_event_counts(self, event_counts: Dict[str, int]) -> Optional[Dict[str, Any]]:
        """
        Analyze event counts and detect attack patterns.

        Args:
            event_counts: Dictionary of event type to count

        Returns:
            Incident dict if pattern detected, None otherwise
        """
        # Check for data exfiltration (highest priority)
        if event_counts.get("exfil", 0) >= self.thresholds["exfil"]:
            return {
                "threat_type": "data_exfiltration",
                "action": "kill",
                "severity": "critical",
                "reason": f"Data exfiltration detected ({event_counts['exfil']} events)",
                "event_counts": event_counts,
            }

        # Check for exploitation attempts
        if event_counts.get("exploit", 0) >= self.thresholds["exploit"]:
            return {
                "threat_type": "active_exploitation",
                "action": "quarantine",
                "severity": "high",
                "reason": f"Multiple exploitation attempts ({event_counts['exploit']} events)",
                "event_counts": event_counts,
            }

        # Check for credential guessing (brute force)
        if event_counts.get("cred-guess", 0) >= self.thresholds["cred-guess"]:
            return {
                "threat_type": "credential_attack",
                "action": "quarantine",
                "severity": "high",
                "reason": f"Credential brute-force detected ({event_counts['cred-guess']} attempts)",
                "event_counts": event_counts,
            }

        # Check for port scanning
        if event_counts.get("scan", 0) >= self.thresholds["scan"]:
            return {
                "threat_type": "port_scanning",
                "action": "monitor",
                "severity": "medium",
                "reason": f"Port scanning detected ({event_counts['scan']} scans)",
                "event_counts": event_counts,
            }

        # Check for reconnaissance combined with other activity
        if event_counts.get("recon", 0) > 0 and len(event_counts) > 1:
            return {
                "threat_type": "reconnaissance",
                "action": "monitor",
                "severity": "low",
                "reason": "Reconnaissance activity with follow-up actions",
                "event_counts": event_counts,
            }

        return None

    def analyze_event_sequence(self, events: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Analyze sequence of events from the same source.

        Args:
            events: List of events from same source IP

        Returns:
            Incident dict if attack pattern detected, None otherwise
        """
        if len(events) < 2:
            return None

        # Extract event types in order
        event_types = [event.get("type") for event in events]

        # Detect kill-chain pattern: recon -> scan -> exploit
        if self._contains_sequence(event_types, ["recon", "scan", "exploit"]):
            return {
                "threat_type": "kill_chain_attack",
                "action": "kill",
                "severity": "critical",
                "reason": "Complete attack kill-chain detected (recon → scan → exploit)",
                "event_sequence": event_types,
            }

        # Detect exfiltration after exploitation
        if self._contains_sequence(event_types, ["exploit", "exfil"]):
            return {
                "threat_type": "post_exploit_exfil",
                "action": "kill",
                "severity": "critical",
                "reason": "Data exfiltration following exploitation",
                "event_sequence": event_types,
            }

        return None

    def _contains_sequence(self, events: List[str], pattern: List[str]) -> bool:
        """
        Check if event list contains a specific sequence.

        Args:
            events: List of event types
            pattern: Pattern to search for

        Returns:
            True if pattern found in sequence
        """
        if len(pattern) > len(events):
            return False

        for i in range(len(events) - len(pattern) + 1):
            if events[i:i + len(pattern)] == pattern:
                return True

        return False
