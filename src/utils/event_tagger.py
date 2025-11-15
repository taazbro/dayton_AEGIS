"""
Event Tagger — Tag events with metadata for better categorization
"""

from typing import Dict, List, Any, Set
import re


class EventTagger:
    """Tags events with metadata for classification and analysis."""

    def __init__(self):
        """Initialize event tagger."""
        self.tag_rules = self._load_tag_rules()

    def _load_tag_rules(self) -> List[Dict[str, Any]]:
        """
        Load tag rules.

        Returns:
            List of tag rules
        """
        return [
            # Attack stage tags
            {
                "tag": "recon",
                "condition": lambda e: e.get("type") in ["recon", "scan"],
            },
            {
                "tag": "weaponization",
                "condition": lambda e: "exploit" in str(e.get("type", "")).lower(),
            },
            {
                "tag": "delivery",
                "condition": lambda e: "payload" in e or "download" in str(e.get("type", "")).lower(),
            },
            {
                "tag": "exploitation",
                "condition": lambda e: e.get("type") == "exploit",
            },
            {
                "tag": "installation",
                "condition": lambda e: "install" in str(e.get("type", "")).lower() or "persistence" in str(e.get("type", "")).lower(),
            },
            {
                "tag": "command_and_control",
                "condition": lambda e: "c2" in str(e.get("type", "")).lower() or "beacon" in str(e.get("type", "")).lower(),
            },
            {
                "tag": "actions_on_objectives",
                "condition": lambda e: e.get("type") in ["exfil", "ransom", "destroy"],
            },

            # MITRE ATT&CK tactics
            {
                "tag": "initial_access",
                "condition": lambda e: e.get("type") in ["phish", "exploit", "cred-guess"],
            },
            {
                "tag": "persistence",
                "condition": lambda e: "persist" in str(e.get("type", "")).lower() or "cron" in str(e.get("type", "")).lower(),
            },
            {
                "tag": "privilege_escalation",
                "condition": lambda e: "privesc" in str(e.get("type", "")).lower() or "sudo" in str(e.get("type", "")).lower(),
            },
            {
                "tag": "defense_evasion",
                "condition": lambda e: "obfuscate" in str(e.get("type", "")).lower() or "hide" in str(e.get("type", "")).lower(),
            },
            {
                "tag": "credential_access",
                "condition": lambda e: e.get("type") in ["cred-guess", "cred-dump", "keylog"],
            },
            {
                "tag": "discovery",
                "condition": lambda e: e.get("type") in ["recon", "enum"],
            },
            {
                "tag": "lateral_movement",
                "condition": lambda e: "lateral" in str(e.get("type", "")).lower() or "pivot" in str(e.get("type", "")).lower(),
            },
            {
                "tag": "collection",
                "condition": lambda e: "collect" in str(e.get("type", "")).lower() or "archive" in str(e.get("type", "")).lower(),
            },
            {
                "tag": "exfiltration",
                "condition": lambda e: e.get("type") == "exfil",
            },
            {
                "tag": "impact",
                "condition": lambda e: e.get("type") in ["ransom", "destroy", "ddos"],
            },

            # Severity-based tags
            {
                "tag": "critical_severity",
                "condition": lambda e: e.get("severity") == "critical",
            },
            {
                "tag": "high_severity",
                "condition": lambda e: e.get("severity") == "high",
            },

            # Target-based tags
            {
                "tag": "production_target",
                "condition": lambda e: "prod" in str(e.get("target", "")).lower(),
            },
            {
                "tag": "database_target",
                "condition": lambda e: "db" in str(e.get("target", "")).lower() or "database" in str(e.get("target", "")).lower(),
            },

            # Geographic tags
            {
                "tag": "internal_source",
                "condition": lambda e: str(e.get("source_ip", "")).startswith(("10.", "192.168.", "172.")),
            },
            {
                "tag": "external_source",
                "condition": lambda e: not str(e.get("source_ip", "")).startswith(("10.", "192.168.", "172.")),
            },
        ]

    def tag_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add tags to an event.

        Args:
            event: Event to tag

        Returns:
            Event with tags added
        """
        if "tags" not in event:
            event["tags"] = set()

        # Apply all matching tag rules
        for rule in self.tag_rules:
            try:
                if rule["condition"](event):
                    event["tags"].add(rule["tag"])
            except Exception:
                # Skip rules that fail
                continue

        # Convert set to list for JSON serialization
        event["tags"] = list(event["tags"])

        # Add auto-generated tags
        event["tags"].extend(self._generate_auto_tags(event))

        # Remove duplicates
        event["tags"] = list(set(event["tags"]))

        return event

    def _generate_auto_tags(self, event: Dict[str, Any]) -> List[str]:
        """
        Generate automatic tags based on event properties.

        Args:
            event: Event to analyze

        Returns:
            List of generated tags
        """
        tags = []

        # Tag by event type
        event_type = event.get("type", "unknown")
        tags.append(f"type:{event_type}")

        # Tag by source IP class
        source_ip = event.get("source_ip", "")
        if source_ip:
            octets = source_ip.split(".")
            if len(octets) >= 2:
                tags.append(f"source_class:{octets[0]}.{octets[1]}.x.x")

        # Tag by target
        target = event.get("target")
        if target:
            tags.append(f"target:{target}")

        # Tag by time of day
        import time
        timestamp = event.get("timestamp", time.time())
        hour = int((timestamp % 86400) / 3600)

        if 0 <= hour < 6:
            tags.append("time:night")
        elif 6 <= hour < 12:
            tags.append("time:morning")
        elif 12 <= hour < 18:
            tags.append("time:afternoon")
        else:
            tags.append("time:evening")

        return tags

    def filter_by_tags(self, events: List[Dict[str, Any]], tags: Set[str]) -> List[Dict[str, Any]]:
        """
        Filter events by tags.

        Args:
            events: List of events
            tags: Set of tags to filter by

        Returns:
            Filtered events
        """
        filtered = []

        for event in events:
            event_tags = set(event.get("tags", []))
            if tags.intersection(event_tags):
                filtered.append(event)

        return filtered

    def get_tag_statistics(self, events: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Get statistics about tag usage.

        Args:
            events: List of events

        Returns:
            Dict mapping tags to counts
        """
        tag_counts = {}

        for event in events:
            for tag in event.get("tags", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        return tag_counts
