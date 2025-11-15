"""
Rate Analyzer — Maintains sliding window of events for rate-based detection
"""

import time
from typing import Dict, List, Any
from collections import defaultdict


class RateAnalyzer:
    """Analyzes event rates using a sliding time window."""

    def __init__(self, window_seconds: int = 60):
        """
        Initialize the rate analyzer.

        Args:
            window_seconds: Size of sliding window in seconds
        """
        self.window_seconds = window_seconds
        self.events: List[Dict[str, Any]] = []

    def add_event(self, event: Dict[str, Any]) -> None:
        """
        Add event to the sliding window.

        Args:
            event: Event to add
        """
        self.events.append(event)
        self._prune_old_events()

    def _prune_old_events(self) -> None:
        """Remove events outside the sliding window."""
        current_time = time.time()
        cutoff_time = current_time - self.window_seconds

        self.events = [
            event for event in self.events
            if event.get("timestamp", 0) > cutoff_time
        ]

    def get_event_counts(self) -> Dict[str, int]:
        """
        Get count of each event type in the current window.

        Returns:
            Dictionary mapping event types to counts
        """
        self._prune_old_events()

        counts = defaultdict(int)
        for event in self.events:
            event_type = event.get("type", "unknown")
            counts[event_type] += 1

        return dict(counts)

    def get_events_by_source(self, source_ip: str) -> List[Dict[str, Any]]:
        """
        Get all events from a specific source IP.

        Args:
            source_ip: Source IP address to filter by

        Returns:
            List of events from that source
        """
        self._prune_old_events()
        return [
            event for event in self.events
            if event.get("source_ip") == source_ip
        ]

    def get_rate(self, event_type: str) -> float:
        """
        Get events per second for a specific event type.

        Args:
            event_type: Type of event to measure

        Returns:
            Events per second
        """
        counts = self.get_event_counts()
        count = counts.get(event_type, 0)
        return count / self.window_seconds if self.window_seconds > 0 else 0.0

    def get_total_events(self) -> int:
        """
        Get total number of events in the current window.

        Returns:
            Total event count
        """
        self._prune_old_events()
        return len(self.events)
