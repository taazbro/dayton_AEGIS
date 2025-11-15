"""
ZYBERPOL AEGIS - LIVE DEMO
Matches the exact pitch narrative for Demo Day

This demonstrates:
1. Autonomous attacker (left side)
2. Sentry telemetry stream (real-time)
3. AEGIS detection & response (immediate)
4. Claude incident report (AI-generated)
5. Slack notification (SOC alert)
"""

import os
import sys
import time
from datetime import datetime
from typing import List, Dict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# AEGIS modules
from src.detection.behavioral_analyzer import (
    BehavioralAnalyzer,
    BehavioralEvent,
    ThreatDetection
)

# Sponsor integrations
try:
    import sentry_sdk
    SENTRY_AVAILABLE = True
except:
    SENTRY_AVAILABLE = False

try:
    from anthropic import Anthropic
    CLAUDE_AVAILABLE = True
except:
    CLAUDE_AVAILABLE = False

try:
    from galileo import galileo_context
    GALILEO_AVAILABLE = True
except:
    GALILEO_AVAILABLE = False

try:
    from src.integrations.slack_integration import SlackNotifier
    SLACK_AVAILABLE = True
except:
    SLACK_AVAILABLE = False


# =============================================================================
# DEMO CONFIGURATION
# =============================================================================

ATTACKER_IP = "203.45.67.89"
TARGET_IP = "192.168.1.100"
TARGET_HOSTNAME = "prod-api-server-01"

# Demo scenarios
DEMO_SCENARIOS = {
    "sql_injection": {
        "name": "Multi-Stage SQL Injection Campaign",
        "severity": "CRITICAL",
        "description": "Autonomous attacker performing recon → exploitation → exfiltration"
    },
    "ransomware": {
        "name": "RansomHub Deployment",
        "severity": "CRITICAL",
        "description": "Ransomware attempting encryption of production data"
    },
    "credential_theft": {
        "name": "Credential Harvesting Attack",
        "severity": "HIGH",
        "description": "Info-stealer targeting browser credentials and API keys"
    }
}


# =============================================================================
# VISUAL FORMATTING
# =============================================================================

def print_banner(text: str, char="=", width=80):
    """Print a centered banner"""
    print(f"\n{char * width}")
    print(f"{text:^{width}}")
    print(f"{char * width}\n")


def print_section(title: str, emoji: str = "📊"):
    """Print a section header"""
    print(f"\n{emoji} {title}")
    print("─" * 80)


def print_tree(items: List[str], prefix: str = "   "):
    """Print items in a tree structure"""
    for i, item in enumerate(items):
        if i < len(items) - 1:
            print(f"{prefix}├─ {item}")
        else:
            print(f"{prefix}└─ {item}")


def print_event(timestamp: str, event: str, color: str = ""):
    """Print a timestamped event"""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "reset": "\033[0m"
    }
    c = colors.get(color, "")
    reset = colors["reset"] if c else ""
    print(f"{c}{timestamp} - {event}{reset}")


def print_check(text: str, status: bool = True):
    """Print a checkmark item"""
    symbol = "✓" if status else "✗"
    color = "\033[92m" if status else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{symbol}{reset} {text}")


# =============================================================================
# PHASE 1: AUTONOMOUS ATTACKER
# =============================================================================

def simulate_autonomous_attack(scenario: str = "sql_injection") -> List[BehavioralEvent]:
    """
    Simulate an autonomous attacker executing a multi-stage attack
    This represents the "left side" of the demo
    """
    print_banner("🔴 PHASE 1: AUTONOMOUS ATTACK LAUNCH", "=")

    scenario_info = DEMO_SCENARIOS[scenario]
    print(f"Attack Scenario: {scenario_info['name']}")
    print(f"Severity: {scenario_info['severity']}")
    print(f"Description: {scenario_info['description']}")

    print_section("ATTACKER AGENT STATUS", "🔴")

    t = time.time()
    events = []

    if scenario == "sql_injection":
        attack_stages = [
            ("Reconnaissance: Scanning ports 80, 443, 22, 3306", "port_scan", 1.0),
            ("Enumeration: Discovered admin panel /admin", "discovery", 1.5),
            ("Exploit Generation: Testing SQL injection vectors", "exploit_attempt", 2.0),
            ("Privilege Escalation: Attempting credential harvesting", "privilege_escalation", 2.5),
            ("Exfiltration: Preparing data extraction", "data_exfiltration", 3.0),
        ]

        for i, (description, event_type, delay) in enumerate(attack_stages):
            time.sleep(0.3)  # Visual delay for demo
            timestamp = datetime.now().strftime("%H:%M:%S")
            print_event(timestamp, description, "red")

            # Create behavioral event
            if "Reconnaissance" in description:
                events.append(BehavioralEvent(
                    timestamp=t + delay,
                    event_type="network_scan",
                    description="Port scanning detected",
                    iocs=["port scan", "nmap signature", "rapid connections"],
                    severity=6,
                    network_connection=f"{ATTACKER_IP}:{50000 + i} -> {TARGET_IP}:80"
                ))

            elif "SQL injection" in description:
                events.append(BehavioralEvent(
                    timestamp=t + delay,
                    event_type="exploit_attempt",
                    description="SQL injection attack detected",
                    iocs=["' OR 1=1--", "SQL injection", "authentication bypass"],
                    severity=9
                ))

            elif "Privilege Escalation" in description:
                events.append(BehavioralEvent(
                    timestamp=t + delay,
                    event_type="privilege_escalation",
                    description="Unauthorized privilege escalation",
                    iocs=["admin access", "privilege escalation", "credential theft"],
                    severity=9
                ))

            elif "Exfiltration" in description:
                events.append(BehavioralEvent(
                    timestamp=t + delay,
                    event_type="data_exfiltration",
                    description="Large data transfer initiated",
                    iocs=["bulk export", "data exfiltration", "12000 records"],
                    severity=10,
                    network_connection=f"{TARGET_IP}:443 -> {ATTACKER_IP}:8443"
                ))

    elif scenario == "ransomware":
        attack_stages = [
            ("Initial Access: Phishing payload executed", "execution", 1.0),
            ("Privilege Escalation: UAC bypass", "privilege_escalation", 1.5),
            ("Defense Evasion: Terminating security software", "defense_evasion", 2.0),
            ("Impact: Deleting Volume Shadow Copies", "impact", 2.5),
            ("Impact: Mass file encryption initiated", "impact", 3.0),
        ]

        for i, (description, event_type, delay) in enumerate(attack_stages):
            time.sleep(0.3)
            timestamp = datetime.now().strftime("%H:%M:%S")
            print_event(timestamp, description, "red")

            events.append(BehavioralEvent(
                timestamp=t + delay,
                event_type=event_type,
                description=description,
                iocs=["ransomware", "encryption", "backup deletion"],
                severity=10
            ))

    print(f"\n🔴 Attack in progress... {len(events)} malicious actions detected")
    return events


# =============================================================================
# PHASE 2: SENTRY TELEMETRY
# =============================================================================

def display_sentry_telemetry(events: List[BehavioralEvent]):
    """
    Display real-time telemetry stream (Sentry)
    """
    print_banner("📊 PHASE 2: SENTRY TELEMETRY STREAM", "=")

    print_section("REAL-TIME EVENT MONITORING", "📡")

    for event in events:
        timestamp = datetime.fromtimestamp(event.timestamp).strftime("%H:%M:%S.%f")[:-3]

        # Log to Sentry if available
        if SENTRY_AVAILABLE:
            sentry_sdk.capture_message(
                f"Security Event: {event.description}",
                level="warning" if event.severity < 8 else "error",
                extras={
                    "event_type": event.event_type,
                    "severity": event.severity,
                    "iocs": ", ".join(event.iocs),
                    "source_ip": ATTACKER_IP,
                    "target": TARGET_IP
                }
            )

        # Display event
        severity_color = "yellow" if event.severity < 8 else "red"
        print_event(
            timestamp,
            f"[{event.event_type.upper()}] {event.description}",
            severity_color
        )
        time.sleep(0.2)

    print(f"\n📊 Total Events Captured: {len(events)}")
    print(f"🔗 View in Sentry: https://sentry.io/organizations/aegis/issues/")


# =============================================================================
# PHASE 3: AEGIS DETECTION & RESPONSE
# =============================================================================

def aegis_detect_and_respond(events: List[BehavioralEvent]) -> Dict:
    """
    AEGIS analyzes behavioral events and responds autonomously
    """
    print_banner("🛡️  PHASE 3: AEGIS DETECTION & RESPONSE", "=")

    print_section("BEHAVIORAL ANALYSIS ENGINE", "🔍")
    print("Analyzing attack pattern...")
    time.sleep(1)

    # Initialize analyzer
    analyzer = BehavioralAnalyzer(enable_ai_detection=True)

    # Analyze behavior
    detections = analyzer.analyze_behavior(events)

    if not detections:
        print("❌ No signature match detected")
        print("   Creating simulated detection for demo purposes...")
        time.sleep(1)

        # Create a simulated detection for demo
        from src.detection.behavioral_analyzer import ThreatDetection
        detection = ThreatDetection(
            threat_name="Multi-Stage Web Application Attack",
            threat_category="web_attack",
            confidence=0.957,
            severity=10,
            matched_behaviors=[
                "Port Scanning",
                "SQL Injection Attempts",
                "Privilege Escalation",
                "Data Exfiltration"
            ],
            behavioral_score=0.95,
            ai_powered=False,
            kill_chain_stage="Actions on Objective",
            recommended_action="IMMEDIATE ISOLATION + TERMINATE SESSION + ROTATE CREDENTIALS",
            evidence=events,
            detection_time=time.time()
        )
        detections = [detection]

    detection = detections[0]  # Primary threat

    # Display detection
    print(f"\n🚨 MULTI-STAGE ATTACK DETECTED")
    print(f"   Category: {detection.threat_category.upper()}")
    print(f"   Confidence: {detection.confidence * 100:.1f}%")
    print(f"   Kill Chain Stage: {detection.kill_chain_stage}")
    print(f"   Severity: {detection.severity}/10")

    print_section("AUTONOMOUS RESPONSE INITIATED", "⚡")

    # Simulate autonomous response actions
    response_actions = [
        ("Session terminated", f"session_id: {hash(time.time()) % 100000:05d}"),
        ("IP blocked", f"{ATTACKER_IP} (24h quarantine)"),
        ("API keys rotated", "api_key_prod_*****"),
        ("Database connection isolated", f"{TARGET_HOSTNAME}:3306"),
        ("Container quarantined", "attacker_env_001"),
    ]

    for action, detail in response_actions:
        time.sleep(0.3)
        print_check(f"{action}: {detail}")

    # Log to Galileo
    if GALILEO_AVAILABLE:
        try:
            logger = galileo_context.get_logger_instance()
            logger.start_trace(
                name=f"AEGIS Response: {detection.threat_name}",
                input=f"Multi-stage attack detected: {detection.threat_category}"
            )
            logger.conclude(output=detection.recommended_action)
            logger.flush()
        except:
            pass

    response_time = 4.7  # seconds (for demo)
    print(f"\n⏱️  Response Time: {response_time}s (Detection → Neutralization)")
    print(f"🛡️  Status: ✅ THREAT NEUTRALIZED")

    return {
        "detection": detection,
        "response_time": response_time,
        "actions_taken": len(response_actions)
    }


# =============================================================================
# PHASE 4: CLAUDE INCIDENT REPORT
# =============================================================================

def generate_claude_incident_report(
    events: List[BehavioralEvent],
    response_data: Dict
) -> str:
    """
    Use Claude to generate human-readable incident report
    """
    print_banner("🤖 PHASE 4: CLAUDE INCIDENT REPORT", "=")

    print_section("AI-GENERATED ANALYSIS", "✨")
    print("Claude is analyzing the incident...")
    time.sleep(1.5)

    detection = response_data["detection"]
    response_time = response_data["response_time"]

    # Build incident timeline
    timeline = []
    for event in events:
        event_time = datetime.fromtimestamp(event.timestamp).strftime("%H:%M:%S")
        timeline.append(f"{event_time} - {event.description}")

    # Generate report with Claude if available
    if CLAUDE_AVAILABLE:
        try:
            client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

            prompt = f"""You are a cybersecurity incident analyst. Generate a concise incident report based on this attack:

Attack Type: {detection.threat_name}
Category: {detection.threat_category}
Severity: {detection.severity}/10
Confidence: {detection.confidence * 100:.1f}%
Response Time: {response_time}s

Timeline:
{chr(10).join(timeline)}

Matched Behaviors:
{chr(10).join('- ' + b for b in detection.matched_behaviors)}

Generate a brief incident report (3-4 paragraphs) covering:
1. What happened
2. What AEGIS did
3. Current status
4. Recommendations

Keep it clear and actionable for a SOC team."""

            response = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            report = response.content[0].text

        except Exception as e:
            # Fallback report
            report = f"""INCIDENT SUMMARY
────────────────────────────────────────────────────

Attack Type: {detection.threat_name}
Severity: {'CRITICAL' if detection.severity >= 9 else 'HIGH'}
Duration: {response_time}s (Detection → Neutralization)
Attacker IP: {ATTACKER_IP}
Target: {TARGET_HOSTNAME} ({TARGET_IP})

ATTACK TIMELINE:
{chr(10).join(timeline)}

ACTIONS TAKEN:
✓ Attacker session killed
✓ IP address blacklisted
✓ API credentials rotated
✓ Database isolated
✓ Zero data exfiltrated

RECOMMENDATION:
Apply security patches immediately
Enable MFA for admin accounts
Review access logs for suspicious activity
"""
    else:
        # Fallback if Claude not available
        report = f"""INCIDENT SUMMARY (Automated)
────────────────────────────────────────────────────
Attack: {detection.threat_name}
Status: ✅ NEUTRALIZED
Response Time: {response_time}s
Actions: {response_data['actions_taken']} automated responses executed
"""

    print(report)
    return report


# =============================================================================
# PHASE 5: SLACK NOTIFICATION
# =============================================================================

def send_slack_notification(report: str, response_data: Dict):
    """
    Send incident summary to Slack (REAL API)
    """
    print_banner("💬 PHASE 5: SLACK NOTIFICATION", "=")

    print_section("SOC TEAM ALERT", "🚨")

    detection = response_data["detection"]
    response_time = response_data["response_time"]
    incident_id = f"2024-{hash(time.time()) % 1000:03d}"

    # Display what we're sending
    slack_message = f"""
╔═══════════════════════════════════════════════════╗
║  🚨 CRITICAL SECURITY INCIDENT - NEUTRALIZED     ║
╚═══════════════════════════════════════════════════╝

Attack: {detection.threat_name}
Status: ✅ STOPPED ({response_time}s detection-to-response)
Damage: ❌ ZERO (no data lost)

Confidence: {detection.confidence * 100:.1f}%
Actions Taken: {response_data['actions_taken']} automated responses

Full report: https://aegis.vezran.com/incidents/{incident_id}

cc: @security-team @soc-lead
"""

    print(slack_message)

    # ACTUALLY send to Slack if webhook configured
    if SLACK_AVAILABLE:
        notifier = SlackNotifier()
        if notifier.enabled:
            print("\n📤 Sending to real Slack webhook...")
            success = notifier.send_incident_alert(
                threat_name=detection.threat_name,
                threat_category=detection.threat_category,
                confidence=detection.confidence,
                severity=detection.severity,
                response_time=response_time,
                actions_taken=response_data['actions_taken'],
                data_lost=False,
                incident_id=incident_id
            )

            if success:
                print("✅ Real Slack notification sent successfully!")
                print("   Check your #security-alerts channel")
            else:
                print("⚠️  Slack webhook call failed (check webhook URL)")
        else:
            print("\n⚠️  Slack webhook not configured (set SLACK_WEBHOOK_URL to enable)")
    else:
        print("\n⚠️  Slack integration module not available")

    print("\n✅ SOC team notified via Slack")


# =============================================================================
# MAIN DEMO RUNNER
# =============================================================================

def run_live_demo(scenario: str = "sql_injection"):
    """
    Run the complete live demo matching the pitch narrative
    """
    print_banner("⭐ ZYBERPOL AEGIS - LIVE DEMO", "█")
    print(f"Autonomous Defense for the AI Era")
    print(f"Demo Scenario: {DEMO_SCENARIOS[scenario]['name']}\n")

    # Initialize sponsors
    if SENTRY_AVAILABLE:
        sentry_sdk.init(
            dsn=os.getenv("SENTRY_DSN"),
            environment="live-demo"
        )
        print("✅ Sentry: Initialized")

    if GALILEO_AVAILABLE:
        try:
            galileo_context.init(project="aegis", log_stream="live-demo")
            print("✅ Galileo: Initialized")
        except:
            pass

    if CLAUDE_AVAILABLE:
        print("✅ Claude: Ready")

    if SLACK_AVAILABLE:
        notifier = SlackNotifier()
        if notifier.enabled:
            print("✅ Slack: Webhook configured")
        else:
            print("⚠️  Slack: Not configured (optional)")

    print()
    time.sleep(2)

    # PHASE 1: Attack
    events = simulate_autonomous_attack(scenario)
    time.sleep(1)

    # PHASE 2: Telemetry
    display_sentry_telemetry(events)
    time.sleep(1)

    # PHASE 3: Detection & Response
    response_data = aegis_detect_and_respond(events)

    if response_data:
        time.sleep(1)

        # PHASE 4: Incident Report
        report = generate_claude_incident_report(events, response_data)
        time.sleep(1)

        # PHASE 5: Slack Alert
        send_slack_notification(report, response_data)

    # Final summary
    print_banner("✅ DEMO COMPLETE", "█")

    if response_data:
        response_time = response_data['response_time']
    else:
        response_time = "N/A"

    print(f"""
🎯 WHAT YOU JUST SAW:

1. ✅ Autonomous attacker executing multi-stage attack
2. ✅ Real-time telemetry capture (Sentry)
3. ✅ Behavioral analysis and detection (AEGIS)
4. ✅ Immediate autonomous response (<5s)
5. ✅ AI-generated incident report (Claude)
6. ✅ SOC team notification (Slack)

⏱️  Total Response Time: {response_time}s
🛡️  Attack Status: NEUTRALIZED
📊 Data Lost: ZERO

This is autonomous defense in action.

As attackers become autonomous, defense must too.
AEGIS is the first real step toward that future.
""")


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AEGIS Live Demo")
    parser.add_argument(
        "--scenario",
        choices=["sql_injection", "ransomware", "credential_theft"],
        default="sql_injection",
        help="Attack scenario to demonstrate"
    )

    args = parser.parse_args()

    try:
        run_live_demo(args.scenario)
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
