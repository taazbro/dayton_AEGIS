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
from src.detector.ai_attack_detector import get_ai_attack_detector
from src.detector.advanced_ai_malware_detector import get_advanced_ai_malware_detector
from src.responder.kill_switch import activate_kill_switch
from src.responder.rotate_credentials import rotate_credentials
from src.responder.quarantine import quarantine_asset
from src.browseruse_agent.replay_attack import replay_attack
from src.forensics.threat_report import generate_threat_report
from src.forensics.claude_interface import get_claude_summary
from src.forensics.claude_agent_sdk import get_claude_agent
from src.dashboard.tui import run_dashboard

# New API integrations (maximizing API usage)
from src.alerts.pagerduty_notifier import get_pagerduty_notifier
from src.alerts.teams_notifier import get_teams_notifier
from src.alerts.discord_notifier import get_discord_notifier
from src.monitoring.datadog_integration import get_datadog_monitoring
from src.monitoring.splunk_hec import get_splunk_hec
from src.threat_intel.mitre_attack_api import get_mitre_api
from src.integrations.jira_integration import get_jira_integration
from src.threat_intel.virustotal_api import get_virustotal_api
from src.monitoring.prometheus_exporter import get_prometheus_exporter

# HACKATHON SPONSOR INTEGRATIONS
from src.observability.galileo_integration import get_galileo_observability
from src.integrations.daytona_sync import get_daytona_sync
from src.integrations.coderabbit_review import get_coderabbit_review


def handle_incident(incident: Dict[str, Any], event_queue: Queue) -> None:
    """
    Handle detected security incident by triggering appropriate response.

    Args:
        incident: Detected incident with action recommendation
        event_queue: Queue for logging response events
    """
    start_time = time.time()

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

    # === BEHAVIORAL PATTERN ANALYSIS ===
    # Note: These detectors identify malicious behavior patterns observed in real-world
    # incidents (including cases where attackers used AI tools). The key insight:
    # "Malware written by AI behaves like malware written by humans" - IBM X-Force

    print("🔍 Analyzing behavioral patterns (high-velocity, automation indicators)...")
    ai_detector = get_ai_attack_detector()
    events = incident.get("events", [])
    behavioral_detection = ai_detector.detect_ai_attack(events)

    if behavioral_detection.get("is_ai_attack"):
        print("\n" + "="*70)
        print("🚨 AUTOMATED ATTACK PATTERN DETECTED")
        print("   (Behavioral signatures: velocity, automation, credential harvesting)")
        print("="*70)
        ai_report = ai_detector.generate_ai_attack_report(behavioral_detection)
        print(ai_report)
        print("="*70 + "\n")

        # Add to threat report
        report["behavioral_attack_detection"] = behavioral_detection

    # === ADVANCED BEHAVIORAL SIGNATURES ===
    print("🔍 Checking for known attack family signatures...")
    advanced_malware_detector = get_advanced_ai_malware_detector()

    # Check for network data in incident
    network_data = incident.get("network_data", None)
    signature_detection = advanced_malware_detector.detect_ai_malware_family(events, network_data)

    if signature_detection.get("ai_malware_detected"):
        print("\n" + "="*70)
        print("🦠 MALWARE FAMILY SIGNATURE MATCHED")
        print("   (Focus: What it does, not how it was written)")
        print("="*70)
        malware_report = advanced_malware_detector.generate_detection_report(signature_detection)
        print(malware_report)
        print("="*70 + "\n")

        # Add to threat report
        report["signature_detection"] = signature_detection

    # === API INTEGRATIONS (Maximizing API usage) ===

    # 1. MITRE ATT&CK enrichment (no API key required)
    print("🔍 Enriching with MITRE ATT&CK data...")
    mitre_api = get_mitre_api()
    report = mitre_api.enrich_threat_report(report)

    # 2. VirusTotal threat intelligence
    print("🔍 Checking VirusTotal intelligence...")
    vt_api = get_virustotal_api()
    report = vt_api.enrich_threat_report(report)

    # 3. Claude AI Analysis (Two-tier approach)
    severity = incident.get("severity", "").upper()

    # Basic analysis for all threats
    claude_summary = get_claude_summary(report)
    print(f"\n📊 CLAUDE BASIC ANALYSIS:\n{claude_summary}\n")

    # Advanced multi-step analysis for HIGH/CRITICAL threats
    if severity in ["HIGH", "CRITICAL"]:
        print("🚀 Triggering ADVANCED Claude Agent SDK (Multi-step reasoning)...")
        claude_agent = get_claude_agent()
        advanced_analysis = claude_agent.analyze_threat_autonomous(report)

        print(f"\n🤖 CLAUDE AGENT SDK - AUTONOMOUS ANALYSIS:")
        print(f"{'='*60}")
        print(f"Analysis Type: {advanced_analysis['analysis_type']}")
        print(f"Confidence: {advanced_analysis['confidence']}")
        print(f"Steps: {advanced_analysis['steps_completed']}")
        print(f"\nREASONING CHAIN:")
        for i, step in enumerate(advanced_analysis.get('reasoning_chain', []), 1):
            print(f"  {i}. {step}")
        print(f"\nFINDINGS:\n{advanced_analysis.get('summary', 'N/A')}")
        print(f"{'='*60}\n")

        # Store advanced analysis in report
        report["advanced_analysis"] = advanced_analysis

    # 4. Datadog metrics and events
    print("📊 Sending to Datadog...")
    datadog = get_datadog_monitoring()
    datadog.send_threat_metrics(report)
    datadog.send_event(report)

    # 5. Splunk HEC event forwarding
    print("📊 Forwarding to Splunk...")
    splunk = get_splunk_hec()
    splunk.send_event(report)

    # 6. Prometheus metrics
    print("📊 Recording Prometheus metrics...")
    prometheus = get_prometheus_exporter()
    prometheus.record_threat(report)
    detection_latency = (time.time() - start_time) * 1000  # ms
    prometheus.record_detection_latency(detection_latency)
    prometheus.record_response_action(action)

    # 7. Multi-channel notifications
    print("📢 Sending notifications...")

    # PagerDuty (critical incidents only)
    pagerduty = get_pagerduty_notifier()
    pagerduty.trigger_incident(report)

    # Microsoft Teams
    teams = get_teams_notifier()
    teams.send_alert(report)

    # Discord
    discord = get_discord_notifier()
    discord.send_alert(report)

    # 8. Jira ticket creation (medium+ severity)
    print("🎫 Creating Jira ticket...")
    jira = get_jira_integration()
    jira.create_incident_ticket(report)

    # === HACKATHON SPONSOR INTEGRATIONS ===

    # 9. Daytona project sync
    print("🚀 Syncing to Daytona IDE...")
    daytona = get_daytona_sync()
    daytona.sync_incident(report)

    # 10. CodeRabbit code review
    print("🐰 CodeRabbit AI reviewing response code...")
    coderabbit = get_coderabbit_review()
    code_review = coderabbit.review_response_code(action, {"incident": incident})
    coderabbit.store_review(code_review)

    print(f"\n✅ Incident handled in {detection_latency:.2f}ms")
    print(f"📊 Sponsor tools used: 6/6 (Sentry, Claude, Galileo, BrowserUse, Daytona, CodeRabbit)")
    print("=" * 60)


def main() -> None:
    """Main entry point for Zyberpol AEGIS."""

    print("=" * 70)
    print("🔥 AEGIS — Autonomous Cyber Defense Agent")
    print("   Daytona HackSprint 2025")
    print("=" * 70)
    print("\n⚡ BEHAVIORAL THREAT DETECTION - FUNDAMENTALS FIRST")
    print("   Focus: Detect malicious behavior, not hype")
    print("   Reality: Malware written by AI behaves like malware written by humans")
    print("   Strategy: Pattern recognition + behavioral analysis + anomaly detection")
    print("=" * 70)
    print("\n🏆 HACKATHON SPONSOR INTEGRATIONS (6/6):")
    print("=" * 70)
    print("1. 🚨 SENTRY        - Error tracking & performance monitoring")
    print("2. 🤖 CLAUDE AI     - Advanced threat analysis (Anthropic Sonnet 4.5)")
    print("                    ├─ Basic: Cached, rate-limited analysis")
    print("                    └─ Advanced: Multi-step autonomous reasoning (SDK)")
    print("3. 🔭 GALILEO       - AI observability & prompt monitoring")
    print("4. 🎬 BROWSERUSE    - AI-powered forensic browser automation")
    print("5. 🚀 DAYTONA       - Real-time project sync & dev metrics")
    print("6. 🐰 CODERABBIT    - AI code review & quality analysis")
    print("=" * 70)
    print("\n📡 ADDITIONAL API INTEGRATIONS (9):")
    print("   ✓ Datadog APM & metrics")
    print("   ✓ Splunk HEC event forwarding")
    print("   ✓ Prometheus metrics exporter")
    print("   ✓ PagerDuty incident escalation")
    print("   ✓ Jira ticket creation")
    print("   ✓ Microsoft Teams notifications")
    print("   ✓ Discord notifications")
    print("   ✓ MITRE ATT&CK enrichment (FREE)")
    print("   ✓ VirusTotal threat intelligence")
    print("=" * 70)
    print(f"\n💡 TOTAL: 15 API integrations | 6/6 sponsor tools active")
    print("=" * 70 + "\n")

    # Initialize Sentry monitoring (SPONSOR 1)
    init_sentry()

    # Initialize Galileo AI observability (SPONSOR 3)
    galileo = get_galileo_observability()

    # Initialize Daytona sync (SPONSOR 5)
    daytona = get_daytona_sync()

    # Initialize CodeRabbit review (SPONSOR 6)
    coderabbit = get_coderabbit_review()

    # Start Prometheus exporter HTTP server
    prometheus_port = int(os.getenv("PROMETHEUS_EXPORTER_PORT", "9090"))
    prometheus = get_prometheus_exporter()
    prometheus.start_http_server(prometheus_port)

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
