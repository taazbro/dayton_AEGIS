"""
Event Processor — Consumes events and detects incidents
"""

import time
from queue import Queue, Empty
from typing import Dict, Any

from src.detector.rate_analyzer import RateAnalyzer
from src.detector.pattern_detector import PatternDetector


class EventProcessor:
    """Processes security events and detects incidents."""

    def __init__(
        self,
        event_queue: Queue,
        incident_queue: Queue,
        rate_analyzer: RateAnalyzer,
        pattern_detector: PatternDetector,
    ):
        """
        Initialize the event processor.

        Args:
            event_queue: Queue to receive events from
            incident_queue: Queue to send detected incidents to
            rate_analyzer: Rate analyzer instance
            pattern_detector: Pattern detector instance
        """
        self.event_queue = event_queue
        self.incident_queue = incident_queue
        self.rate_analyzer = rate_analyzer
        self.pattern_detector = pattern_detector
        self.running = False

    def process_event(self, event: Dict[str, Any]) -> None:
        """
        Process a single security event.

        Args:
            event: Event to process
        """
        # Add to rate analyzer
        self.rate_analyzer.add_event(event)

        # Get current event counts
        event_counts = self.rate_analyzer.get_event_counts()

        # Check for rate-based patterns
        incident = self.pattern_detector.analyze_event_counts(event_counts)

        if incident:
            print(f"⚠️  Pattern detected: {incident['threat_type']}")
            self.incident_queue.put(incident)
            return

        # Check for sequence-based patterns from same source
        source_ip = event.get("source_ip")
        if source_ip:
            source_events = self.rate_analyzer.get_events_by_source(source_ip)
            if len(source_events) >= 2:
                sequence_incident = self.pattern_detector.analyze_event_sequence(source_events)
                if sequence_incident:
                    print(f"⚠️  Sequence pattern detected: {sequence_incident['threat_type']}")
                    self.incident_queue.put(sequence_incident)

    def start(self) -> None:
        """Start the event processor loop."""
        self.running = True
        print("👁️  Event Processor: Monitoring events...")

        while self.running:
            try:
                # Get event from queue with timeout
                event = self.event_queue.get(timeout=1.0)
                self.process_event(event)

            except Empty:
                # No events in queue, continue
                continue

            except Exception as e:
                print(f"❌ Error processing event: {e}")
                continue

    def stop(self) -> None:
        """Stop the event processor."""
        self.running = False
