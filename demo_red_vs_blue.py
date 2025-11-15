"""
AEGIS Red Team vs Blue Team Demo

⚠️ ETHICAL USE ONLY ⚠️
This is a RESEARCH and DEMONSTRATION tool.
Only use in authorized testing environments.

Purpose: Demonstrate AEGIS defensive capabilities by simulating real attacks.
"""

import time
import threading
from queue import Queue
from typing import Dict, Any

from src.red_team.offensive_agent import get_offensive_agent
from src.detector.event_processor import EventProcessor
from src.detector.pattern_detector import PatternDetector
from src.detector.rate_analyzer import RateAnalyzer


class RedVsBlueDemo:
    """
    Interactive demo showing offensive red team vs defensive blue team.
    """

    def __init__(self):
        self.event_queue = Queue()
        self.incident_queue = Queue()

        # Initialize defensive systems (Blue Team)
        self.rate_analyzer = RateAnalyzer(window_seconds=60)
        self.pattern_detector = PatternDetector()

        self.event_processor = EventProcessor(
            event_queue=self.event_queue,
            incident_queue=self.incident_queue,
            rate_analyzer=self.rate_analyzer,
            pattern_detector=self.pattern_detector
        )

        # Initialize offensive system (Red Team)
        self.offensive_agent = get_offensive_agent(self.event_queue, mode="demo")
        self.offensive_agent.authorized_target = True  # Explicitly authorize (demo environment)

        self.incidents_detected = []

    def run_demo(self, attack_type: str = "full_chain"):
        """
        Run red team vs blue team demonstration.

        Args:
            attack_type: Type of attack to simulate
        """

        print("\n" + "="*70)
        print("🎯 AEGIS RED TEAM VS BLUE TEAM DEMONSTRATION")
        print("="*70)
        print()
        print("📋 Demo Overview:")
        print("   🔴 RED TEAM (Offense): Simulates realistic cyber attacks")
        print("   🔵 BLUE TEAM (Defense): AEGIS autonomous detection & response")
        print()
        print("   Purpose: Validate defensive capabilities against real attack patterns")
        print("   Environment: Authorized testing (demo mode)")
        print("="*70 + "\n")

        # Start blue team (defensive monitoring)
        print("🔵 BLUE TEAM: Starting defensive monitoring...")
        processor_thread = threading.Thread(
            target=self.event_processor.start,
            daemon=True,
            name="BlueTeam-EventProcessor"
        )
        processor_thread.start()
        print("   ✓ Event processor active")
        print("   ✓ Detection engines armed")
        print("   ✓ Autonomous response ready\n")

        time.sleep(1)

        # Start red team attack
        print("🔴 RED TEAM: Initiating attack simulation...")
        attack_result = self.offensive_agent.run_attack_simulation(attack_type)

        # Wait for defense to process
        print("\n⏳ Waiting for defensive analysis...")
        time.sleep(3)

        # Check for incidents detected
        detected_count = 0
        while not self.incident_queue.empty():
            incident = self.incident_queue.get()
            self.incidents_detected.append(incident)
            detected_count += 1

        # Results
        print("\n" + "="*70)
        print("📊 DEMONSTRATION RESULTS")
        print("="*70)
        print(f"\n🔴 RED TEAM:")
        print(f"   Attack Type: {attack_result.get('attack_type', 'N/A')}")

        if 'phases' in attack_result:
            print(f"   Phases Executed: {len(attack_result['phases'])}")
            print(f"   Attack Chain: {' → '.join(attack_result['phases'])}")

        print(f"\n🔵 BLUE TEAM:")
        print(f"   Incidents Detected: {detected_count}")

        if detected_count > 0:
            print(f"   Detection Status: ✅ SUCCESS")
            print(f"\n   Detected Threats:")
            for i, incident in enumerate(self.incidents_detected, 1):
                print(f"      {i}. {incident.get('threat_type', 'Unknown')} "
                      f"(Severity: {incident.get('severity', 'N/A')})")
        else:
            print(f"   Detection Status: ⚠️ MISSED (Attack evaded detection)")

        print("\n" + "="*70)
        print("📈 DEFENSIVE EFFECTIVENESS SCORE")
        print("="*70)

        effectiveness = min(100, (detected_count / max(1, len(attack_result.get('phases', [1])))) * 100)
        print(f"\n   Score: {effectiveness:.1f}%")

        if effectiveness >= 80:
            print("   Rating: ✅ EXCELLENT - Strong defensive posture")
        elif effectiveness >= 60:
            print("   Rating: ✓ GOOD - Adequate detection coverage")
        elif effectiveness >= 40:
            print("   Rating: ⚠️ FAIR - Gaps in detection")
        else:
            print("   Rating: ❌ POOR - Significant blind spots")

        print("\n" + "="*70 + "\n")

        return {
            "attack": attack_result,
            "incidents_detected": detected_count,
            "effectiveness": effectiveness
        }


def main():
    """Run interactive demo."""

    print("\n" + "="*70)
    print("🎯 AEGIS OFFENSIVE/DEFENSIVE DEMONSTRATION")
    print("   Red Team vs Blue Team Security Validation")
    print("="*70)
    print()
    print("Available Attack Simulations:")
    print("   1. full_chain      - Complete cyber kill chain (7 phases)")
    print("   2. high_velocity   - Automated high-speed attack (velocity test)")
    print("   3. stealth         - Low-and-slow APT (behavioral test)")
    print("   4. ransomware      - Ransomware attack pattern")
    print("   5. credential_theft - Credential harvesting attack")
    print("   6. supply_chain    - Supply chain compromise")
    print("   7. api_abuse       - LLM API exploitation")
    print()

    attack_types = {
        "1": "full_chain",
        "2": "high_velocity",
        "3": "stealth",
        "4": "ransomware",
        "5": "credential_theft",
        "6": "supply_chain",
        "7": "api_abuse"
    }

    choice = input("Select attack type (1-7) [default: 2]: ").strip() or "2"

    attack_type = attack_types.get(choice, "high_velocity")

    demo = RedVsBlueDemo()
    results = demo.run_demo(attack_type)

    print("\n📝 LESSONS LEARNED:")
    print("   • Offensive capabilities help validate defensive effectiveness")
    print("   • Real attack patterns test detection accuracy")
    print("   • Red team exercises identify blind spots")
    print("   • Continuous testing improves defensive posture")
    print()
    print("🎓 Research Note:")
    print("   This demonstration shows why 'purple teaming' (red + blue collaboration)")
    print("   is essential for building robust security systems.")
    print()


if __name__ == "__main__":
    main()
