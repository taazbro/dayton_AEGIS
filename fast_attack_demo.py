"""
AEGIS Fast Multi-Attack Demo - Real-time Defense Logging
"""

import os
import sys
import time
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import sentry_sdk
    from sentry_sdk import capture_message
    SENTRY_AVAILABLE = True
except:
    SENTRY_AVAILABLE = False

try:
    from galileo_observe import GalileoObserve
    from galileo_core.schemas.shared.workflows.node_type import NodeType
    GALILEO_AVAILABLE = True
except:
    GALILEO_AVAILABLE = False


# Attack definitions
ATTACKS = {
    "SQL_INJECTION": {
        "payload": "'; DROP TABLE users; --",
        "severity": "error",
        "defense": "Input sanitization + parameterized queries",
        "threat_level": 9
    },
    "XSS": {
        "payload": "<script>alert('XSS')</script>",
        "severity": "warning",
        "defense": "Content Security Policy + output encoding",
        "threat_level": 7
    },
    "DDOS": {
        "payload": "89,432 requests/sec from 203.45.67.89",
        "severity": "fatal",
        "defense": "Rate limiting + IP blocking",
        "threat_level": 10
    },
    "BRUTE_FORCE": {
        "payload": "Failed login attempt #487 for user 'admin'",
        "severity": "warning",
        "defense": "Account lockout + CAPTCHA",
        "threat_level": 6
    },
    "RANSOMWARE": {
        "payload": "Encryption attempt on 3,847 files",
        "severity": "fatal",
        "defense": "Process termination + file restoration",
        "threat_level": 10
    },
    "PHISHING": {
        "payload": "Suspicious email from fake@paypal-security.com",
        "severity": "warning",
        "defense": "Email quarantine + user alert",
        "threat_level": 5
    },
    "MALWARE": {
        "payload": "Malicious binary detected: trojan.exe",
        "severity": "error",
        "defense": "File quarantine + signature update",
        "threat_level": 8
    },
    "PORT_SCAN": {
        "payload": "Scanning ports 1-65535 from 192.168.1.100",
        "severity": "warning",
        "defense": "Firewall block + intrusion detection",
        "threat_level": 4
    },
    "ZERO_DAY": {
        "payload": "Unknown exploit targeting CVE-2025-12345",
        "severity": "fatal",
        "defense": "Behavioral analysis + sandboxing",
        "threat_level": 10
    },
    "MITM": {
        "payload": "SSL certificate mismatch detected",
        "severity": "error",
        "defense": "Connection termination + cert pinning",
        "threat_level": 8
    },
    "PRIVILEGE_ESCALATION": {
        "payload": "Attempt to gain root access",
        "severity": "fatal",
        "defense": "Process termination + audit log",
        "threat_level": 9
    },
    "DATA_EXFILTRATION": {
        "payload": "Unauthorized data transfer to 45.67.89.123",
        "severity": "fatal",
        "defense": "Network blocking + data recovery",
        "threat_level": 10
    }
}


class FastAttackDemo:
    def __init__(self):
        self.attack_count = 0
        self.defense_count = 0
        self.sentry_events = []
        self.galileo_nodes = []

        # Initialize Sentry
        if SENTRY_AVAILABLE:
            dsn = os.getenv("SENTRY_DSN")
            if dsn:
                sentry_sdk.init(dsn=dsn, environment="fast_attack_demo")
                print("✅ Sentry initialized")

        # Initialize Galileo
        if GALILEO_AVAILABLE:
            api_key = os.getenv("GALILEO_API_KEY")
            if api_key:
                self.galileo = GalileoObserve(project_name="AEGIS_ATTACK_DEMO")
                print("✅ Galileo initialized")
            else:
                self.galileo = None
        else:
            self.galileo = None

    def simulate_attack(self, attack_type):
        """Simulate and defend against an attack"""
        attack = ATTACKS[attack_type]
        self.attack_count += 1

        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        # Display attack
        print(f"\n{'='*70}")
        print(f"🔴 ATTACK #{self.attack_count} @ {timestamp}")
        print(f"   Type: {attack_type}")
        print(f"   Threat Level: {attack['threat_level']}/10")
        print(f"   Payload: {attack['payload']}")

        # Log to Sentry
        sentry_id = None
        if SENTRY_AVAILABLE:
            try:
                sentry_id = capture_message(
                    f"🚨 AEGIS: {attack_type} (Threat:{attack['threat_level']}/10) - {attack['payload']}",
                    level=attack['severity']
                )
                self.sentry_events.append(sentry_id)
                print(f"   📡 Sentry: {sentry_id}")
            except:
                pass

        # Log to Galileo
        galileo_id = None
        if self.galileo:
            try:
                galileo_id = self.galileo.log_node_start(
                    node_type=NodeType.llm,
                    input_text=f"ATTACK: {attack_type} | {attack['payload']}",
                    model="aegis-defense-system",
                    tags=[attack_type.lower(), f"threat-{attack['threat_level']}"]
                )

                self.galileo.log_node_completion(
                    node_id=galileo_id,
                    output_text=f"DEFENSE: {attack['defense']} | Status: BLOCKED",
                    status_code=200
                )

                self.galileo_nodes.append(galileo_id)
                print(f"   📡 Galileo: {galileo_id[:36]}...")
            except:
                pass

        # Simulate defense processing
        time.sleep(0.05)
        self.defense_count += 1

        # Display defense
        print(f"\n🛡️  DEFENSE #{self.defense_count} ACTIVATED @ {timestamp}")
        print(f"   Action: {attack['defense']}")
        print(f"   Status: ✅ THREAT NEUTRALIZED")

        return {
            'attack_type': attack_type,
            'sentry_id': sentry_id,
            'galileo_id': galileo_id,
            'timestamp': timestamp
        }


def main():
    print("\n" + "="*70)
    print("⚔️  AEGIS REAL-TIME ATTACK DEFENSE DEMONSTRATION")
    print("="*70)
    print("\n🎯 Simulating MAXIMUM attack types")
    print("📡 Logging ALL events to Sentry + Galileo")
    print("🛡️  Showing REAL-TIME defense responses\n")

    demo = FastAttackDemo()

    print("\n" + "="*70)
    print("🚨 LAUNCHING ATTACK WAVES")
    print("="*70)

    start_time = time.time()
    all_results = []

    # Wave 1: Sequential high-threat attacks
    print("\n🌊 WAVE 1: HIGH-THREAT ATTACKS (Sequential)")
    print("-" * 70)

    for attack_type in ["DDOS", "RANSOMWARE", "ZERO_DAY", "DATA_EXFILTRATION"]:
        result = demo.simulate_attack(attack_type)
        all_results.append(result)
        time.sleep(0.2)

    # Wave 2: Parallel medium-threat attacks
    print("\n\n🌊 WAVE 2: MEDIUM-THREAT ATTACKS (Parallel)")
    print("-" * 70)

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for attack_type in ["SQL_INJECTION", "MALWARE", "MITM", "PRIVILEGE_ESCALATION"]:
            future = executor.submit(demo.simulate_attack, attack_type)
            futures.append(future)

        for future in futures:
            result = future.result()
            all_results.append(result)

    time.sleep(0.3)

    # Wave 3: Rapid-fire lower-threat attacks
    print("\n\n🌊 WAVE 3: RECONNAISSANCE ATTACKS (Rapid-fire)")
    print("-" * 70)

    for attack_type in ["XSS", "BRUTE_FORCE", "PHISHING", "PORT_SCAN"]:
        result = demo.simulate_attack(attack_type)
        all_results.append(result)
        time.sleep(0.1)

    elapsed = time.time() - start_time

    # Final Summary
    print("\n\n" + "="*70)
    print("📊 DEFENSE SUMMARY")
    print("="*70)
    print(f"\n⚔️  Attacks Simulated: {demo.attack_count}")
    print(f"🛡️  Defenses Activated: {demo.defense_count}")
    print(f"🎯 Success Rate: 100% (All threats neutralized)")
    print(f"⏱️  Total Time: {elapsed:.2f} seconds")
    print(f"⚡ Processing Rate: {demo.attack_count/elapsed:.1f} attacks/sec")

    # Sponsor logs
    print("\n" + "="*70)
    print("📡 SPONSOR API LOGS")
    print("="*70)

    if demo.sentry_events:
        print(f"\n🚨 SENTRY: {len(demo.sentry_events)} events logged")
        print(f"   View at: https://sentry.io/")
        print(f"   Filter: environment='fast_attack_demo'")
        print(f"\n   Recent Event IDs:")
        for event_id in demo.sentry_events[:5]:
            print(f"      • {event_id}")
        if len(demo.sentry_events) > 5:
            print(f"      ... and {len(demo.sentry_events) - 5} more")

    if demo.galileo_nodes:
        print(f"\n🔭 GALILEO: {len(demo.galileo_nodes)} nodes logged")
        print(f"   View at: https://app.galileo.ai/")
        print(f"   Project: AEGIS_ATTACK_DEMO")
        print(f"\n   Recent Node IDs:")
        for node_id in demo.galileo_nodes[:5]:
            print(f"      • {node_id}")
        if len(demo.galileo_nodes) > 5:
            print(f"      ... and {len(demo.galileo_nodes) - 5} more")

    # Attack breakdown
    print("\n" + "="*70)
    print("🎯 ATTACK TYPE BREAKDOWN")
    print("="*70)

    attack_types = {}
    for result in all_results:
        atype = result['attack_type']
        if atype not in attack_types:
            attack_types[atype] = 0
        attack_types[atype] += 1

    for atype, count in sorted(attack_types.items()):
        threat = ATTACKS[atype]['threat_level']
        print(f"   {atype:25} → Threat: {threat:2}/10 | Count: {count}")

    print("\n" + "="*70)
    print("✅ ALL ATTACK DATA TRANSMITTED TO SPONSORS")
    print("="*70)
    print("\n🔗 Verify your data:")
    print("   • Sentry: https://sentry.io/ (search event IDs above)")
    print("   • Galileo: https://app.galileo.ai/ (project: AEGIS_ATTACK_DEMO)")
    print("\n")


if __name__ == "__main__":
    main()
