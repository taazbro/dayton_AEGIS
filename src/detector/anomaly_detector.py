"""
Anomaly Detector — Statistical anomaly detection for AEGIS
"""

from typing import Dict, List, Any, Optional
from collections import defaultdict
import time
import statistics


class AnomalyDetector:
    """Detects anomalies using statistical methods."""

    def __init__(self, baseline_window: int = 300):
        """
        Initialize the anomaly detector.

        Args:
            baseline_window: Seconds of data to use for baseline (default 5 min)
        """
        self.baseline_window = baseline_window
        self.event_history: List[Dict[str, Any]] = []
        self.baselines: Dict[str, Dict[str, float]] = {}

    def add_event(self, event: Dict[str, Any]) -> None:
        """
        Add event to history for baseline calculation.

        Args:
            event: Event to add
        """
        self.event_history.append(event)
        self._prune_old_events()
        self._update_baselines()

    def _prune_old_events(self) -> None:
        """Remove events outside the baseline window."""
        current_time = time.time()
        cutoff_time = current_time - self.baseline_window

        self.event_history = [
            event for event in self.event_history
            if event.get("timestamp", 0) > cutoff_time
        ]

    def _update_baselines(self) -> None:
        """Update baseline statistics from event history."""
        if len(self.event_history) < 10:
            # Not enough data for baseline
            return

        # Calculate baseline event rates per type
        event_counts = defaultdict(list)
        window_size = 60  # 1 minute windows

        # Group events into time windows
        if not self.event_history:
            return

        min_time = min(e.get("timestamp", 0) for e in self.event_history)
        max_time = max(e.get("timestamp", 0) for e in self.event_history)

        current_window = min_time
        while current_window < max_time:
            window_end = current_window + window_size

            # Count events in this window by type
            window_events = defaultdict(int)
            for event in self.event_history:
                event_time = event.get("timestamp", 0)
                if current_window <= event_time < window_end:
                    event_type = event.get("type", "unknown")
                    window_events[event_type] += 1

            # Record counts
            for event_type, count in window_events.items():
                event_counts[event_type].append(count)

            current_window = window_end

        # Calculate statistics for each event type
        for event_type, counts in event_counts.items():
            if len(counts) >= 3:
                self.baselines[event_type] = {
                    "mean": statistics.mean(counts),
                    "stdev": statistics.stdev(counts) if len(counts) > 1 else 0,
                    "max": max(counts),
                }

    def detect_anomaly(self, current_rate: Dict[str, int]) -> Optional[Dict[str, Any]]:
        """
        Detect anomalies in current event rates.

        Args:
            current_rate: Current event counts by type

        Returns:
            Anomaly incident if detected, None otherwise
        """
        if not self.baselines:
            return None

        anomalies = []

        for event_type, count in current_rate.items():
            if event_type not in self.baselines:
                continue

            baseline = self.baselines[event_type]
            mean = baseline["mean"]
            stdev = baseline["stdev"]

            # Detect spike (> 3 standard deviations above mean)
            if stdev > 0:
                z_score = (count - mean) / stdev
                if z_score > 3.0:
                    anomalies.append({
                        "type": event_type,
                        "current": count,
                        "baseline_mean": mean,
                        "z_score": z_score,
                    })

        if anomalies:
            return {
                "threat_type": "statistical_anomaly",
                "action": "monitor",
                "severity": "medium",
                "reason": f"Statistical anomaly detected: {len(anomalies)} event type(s) spiking",
                "anomalies": anomalies,
            }

        return None

    def detect_time_based_anomaly(self) -> Optional[Dict[str, Any]]:
        """
        Detect time-based anomalies (unusual activity patterns).

        Returns:
            Anomaly incident if detected, None otherwise
        """
        if len(self.event_history) < 20:
            return None

        current_time = time.time()
        current_hour = int((current_time % 86400) / 3600)

        # Detect unusual activity during off-hours (e.g., 2 AM - 5 AM)
        if 2 <= current_hour <= 5:
            recent_events = [
                e for e in self.event_history
                if current_time - e.get("timestamp", 0) < 300
            ]

            if len(recent_events) > 50:
                return {
                    "threat_type": "time_anomaly",
                    "action": "monitor",
                    "severity": "medium",
                    "reason": f"Unusual activity during off-hours: {len(recent_events)} events in 5 minutes",
                    "hour": current_hour,
                }

        return None

    def detect_geographic_anomaly(self, events: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Detect geographic anomalies (impossible travel, distributed attacks).

        Args:
            events: List of recent events

        Returns:
            Anomaly incident if detected, None otherwise
        """
        # Track unique source IPs
        source_ips = set(e.get("source_ip") for e in events)

        # Detect distributed attack (many unique IPs in short time)
        if len(source_ips) > 20:
            return {
                "threat_type": "distributed_attack",
                "action": "quarantine",
                "severity": "high",
                "reason": f"Distributed attack detected: {len(source_ips)} unique source IPs",
                "source_count": len(source_ips),
            }

        return None
