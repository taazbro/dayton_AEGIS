"""
Zyberpol AEGIS — Main Orchestrator
Autonomous cyber-defense agent for Daytona HackSprint
"""

import os
import threading
import time
from queue import Queue
from typing import Dict, Any

from src.sentry_init import init_sentry
from src.attack_simulator.simulate_attack import AttackSimulator
from src.detector.event_processor import EventProcessor
from src.detector.pattern_detector import PatternDetector
from src.detector.rate_analyzer import RateAnalyzer
from src.responder.kill_switch import activate_kill_switch
from src.responder.rotate_credentials import rotate_credentials
from src.responder.quarantine import quarantine_asset
from src.browseruse_agent.replay_attack import replay_attack
from src.forensics.threat_report import generate_threat_report
from src.forensics.claude_interface import get_claude_summary
from src.dashboard.tui import run_dashboard


def handle_incident(incident: Dict[str, Any], event_queue: Queue) -> None:
    """
    Handle detected security incident by triggering appropriate response.

    Args:
        incident: Detected incident with action recommendation
        event_queue: Queue for logging response events
    """
    action = incident.get("action", "monitor")
    threat_type = incident.get("threat_type", "unknown")

    print(f"\n🚨 INCIDENT DETECTED: {threat_type}")
    print(f"   Recommended Action: {action}")

    if action == "kill":
        activate_kill_switch(incident)
    elif action == "quarantine":
        quarantine_asset(incident)
        rotate_credentials(incident)
    elif action == "monitor":
        print("   ℹ️  Monitoring threat...")

    # Attempt BrowserUse replay
    replay_artifacts = replay_attack(incident)

    # Generate forensics report
    report = generate_threat_report(incident, replay_artifacts)

    # Get Claude analysis
    claude_summary = get_claude_summary(report)

    print(f"\n📊 CLAUDE ANALYSIS:\n{claude_summary}\n")


def main() -> None:
    """Main entry point for Zyberpol AEGIS."""

    print("=" * 60)
    print("🔥 Zyberpol AEGIS — Autonomous Cyber Defense Agent")
    print("=" * 60)

    # Initialize Sentry monitoring
    init_sentry()

    # Create event queue for inter-component communication
    event_queue: Queue = Queue()
    incident_queue: Queue = Queue()

    # Initialize components
    rate_analyzer = RateAnalyzer(window_seconds=60)
    pattern_detector = PatternDetector()
    event_processor = EventProcessor(
        event_queue=event_queue,
        incident_queue=incident_queue,
        rate_analyzer=rate_analyzer,
        pattern_detector=pattern_detector
    )

    # Start event processor in background thread
    processor_thread = threading.Thread(
        target=event_processor.start,
        daemon=True,
        name="EventProcessor"
    )
    processor_thread.start()
    print("✓ Event processor started")

    # Start dashboard in background thread
    dashboard_thread = threading.Thread(
        target=run_dashboard,
        args=(incident_queue,),
        daemon=True,
        name="Dashboard"
    )
    dashboard_thread.start()
    print("✓ Dashboard started")

    # Start attack simulator
    simulator = AttackSimulator(event_queue)
    simulator_thread = threading.Thread(
        target=simulator.run,
        daemon=True,
        name="AttackSimulator"
    )
    simulator_thread.start()
    print("✓ Attack simulator started\n")

    print("🎯 System operational. Monitoring for threats...\n")

    # Main incident handling loop
    try:
        while True:
            if not incident_queue.empty():
                incident = incident_queue.get()
                handle_incident(incident, event_queue)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down AEGIS...")
        print("=" * 60)


if __name__ == "__main__":
    main()
