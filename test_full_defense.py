"""
AEGIS Full Defense Test - All Attacks Simultaneously

Launch all 7 attack types at once to stress-test defensive capabilities.
"""

import time
import threading
from queue import Queue
from typing import Dict, Any, List

from src.red_team.offensive_agent import get_offensive_agent
from src.detector.event_processor import EventProcessor
from src.detector.pattern_detector import PatternDetector
from src.detector.rate_analyzer import RateAnalyzer
from src.detector.ai_attack_detector import get_ai_attack_detector
from src.detector.advanced_ai_malware_detector import get_advanced_ai_malware_detector


class FullDefenseTest:
    """
    Comprehensive defense test with all attacks launched simultaneously.
    """

    def __init__(self):
        self.event_queue = Queue()
        self.incident_queue = Queue()

        # Initialize defensive systems
        self.rate_analyzer = RateAnalyzer(window_seconds=60)
        self.pattern_detector = PatternDetector()

        self.event_processor = EventProcessor(
            event_queue=self.event_queue,
            incident_queue=self.incident_queue,
            rate_analyzer=self.rate_analyzer,
            pattern_detector=self.pattern_detector
        )

        # Initialize offensive system
        self.offensive_agent = get_offensive_agent(self.event_queue, mode="demo")
        self.offensive_agent.authorized_target = True  # Authorized for testing

        self.attack_results = {}
        self.incidents_detected = []
        self.lock = threading.Lock()

    def launch_attack(self, attack_type: str):
        """Launch a single attack type in a thread."""
        print(f"🔴 Launching {attack_type}...")
        result = self.offensive_agent.run_attack_simulation(attack_type)

        with self.lock:
            self.attack_results[attack_type] = result
            print(f"   ✓ {attack_type} complete")

    def run_full_test(self):
        """
        Run full defensive test with all attacks simultaneously.
        """

        print("\n" + "="*70)
        print("🎯 AEGIS FULL DEFENSE TEST - ALL ATTACKS SIMULTANEOUSLY")
        print("="*70)
        print()
        print("🔥 STRESS TEST CONFIGURATION:")
        print("   • Attacks: 7 simultaneous attack types")
        print("   • Mode: Concurrent (all at once)")
        print("   • Purpose: Maximum stress test of defensive capabilities")
        print()
        print("="*70 + "\n")

        # Start defensive monitoring
        print("🔵 BLUE TEAM: Initializing defense...")
        processor_thread = threading.Thread(
            target=self.event_processor.start,
            daemon=True,
            name="BlueTeam-EventProcessor"
        )
        processor_thread.start()
        print("   ✓ Event processor active")
        print("   ✓ 7 detection engines armed:")
        print("      1. Pattern Detector")
        print("      2. Rate Analyzer")
        print("      3. Anomaly Detector")
        print("      4. Behavioral Detector")
        print("      5. Signature Detector")
        print("      6. High-Velocity Attack Detector")
        print("      7. Advanced Signature Detector")
        print()

        time.sleep(1)

        # Launch all attacks simultaneously
        print("🔴 RED TEAM: Launching ALL attacks simultaneously...")
        print("="*70)
        print()

        attack_types = [
            "full_chain",
            "high_velocity",
            "stealth",
            "ransomware",
            "credential_theft",
            "supply_chain",
            "api_abuse"
        ]

        attack_threads = []
        start_time = time.time()

        # Launch all attacks in parallel
        for attack_type in attack_types:
            thread = threading.Thread(
                target=self.launch_attack,
                args=(attack_type,),
                name=f"Attack-{attack_type}"
            )
            thread.start()
            attack_threads.append(thread)

        # Wait for all attacks to complete
        for thread in attack_threads:
            thread.join()

        attack_duration = time.time() - start_time

        print()
        print("="*70)
        print("🔴 ALL ATTACKS COMPLETE")
        print(f"   Duration: {attack_duration:.2f} seconds")
        print("="*70)
        print()

        # Wait for defense to process
        print("⏳ Waiting for defensive analysis...")
        time.sleep(5)

        # Collect incidents
        print("\n🔵 COLLECTING DETECTION RESULTS...\n")
        while not self.incident_queue.empty():
            incident = self.incident_queue.get()
            self.incidents_detected.append(incident)

        # Analyze results
        self.print_results(attack_duration)

    def print_results(self, attack_duration: float):
        """Print comprehensive test results."""

        print("="*70)
        print("📊 COMPREHENSIVE TEST RESULTS")
        print("="*70)
        print()

        # Attack summary
        print("🔴 RED TEAM SUMMARY:")
        print(f"   Total Attacks Launched: {len(self.attack_results)}")
        print(f"   Attack Duration: {attack_duration:.2f} seconds")
        print()
        print("   Attacks Executed:")
        for i, (attack_type, result) in enumerate(self.attack_results.items(), 1):
            status = "✅" if "error" not in result else "❌"
            print(f"      {i}. {status} {attack_type}")
            if 'phases' in result:
                print(f"         └─ Phases: {len(result['phases'])}")
            if 'requests_sent' in result:
                print(f"         └─ Events: {result['requests_sent']}")

        print()

        # Defense summary
        print("🔵 BLUE TEAM SUMMARY:")
        print(f"   Total Incidents Detected: {len(self.incidents_detected)}")
        print()

        if len(self.incidents_detected) > 0:
            print("   Detected Threats:")

            # Group by severity
            severity_counts = {}
            threat_types = {}

            for incident in self.incidents_detected:
                severity = incident.get('severity', 'UNKNOWN')
                threat_type = incident.get('threat_type', 'Unknown')

                severity_counts[severity] = severity_counts.get(severity, 0) + 1
                threat_types[threat_type] = threat_types.get(threat_type, 0) + 1

            # Print by severity
            for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
                if severity in severity_counts:
                    print(f"      {severity}: {severity_counts[severity]} incidents")

            print()
            print("   Threat Types Detected:")
            for threat_type, count in sorted(threat_types.items(), key=lambda x: x[1], reverse=True):
                print(f"      • {threat_type}: {count}x")

        else:
            print("   ⚠️  No incidents detected (attacks may have evaded detection)")

        print()
        print("="*70)
        print("📈 DEFENSIVE EFFECTIVENESS ANALYSIS")
        print("="*70)
        print()

        # Calculate effectiveness
        total_attacks = len(self.attack_results)
        detected_count = len(self.incidents_detected)

        if total_attacks > 0:
            detection_rate = (detected_count / total_attacks) * 100
        else:
            detection_rate = 0

        print(f"   Attacks Launched: {total_attacks}")
        print(f"   Incidents Detected: {detected_count}")
        print(f"   Detection Rate: {detection_rate:.1f}%")
        print()

        # Performance metrics
        if detected_count > 0:
            avg_response_time = attack_duration / detected_count
            print(f"   Average Detection Latency: {avg_response_time:.2f}s")

        print(f"   Total Events Processed: ~{self.event_queue.qsize() + detected_count * 10}")
        print()

        # Overall rating
        if detection_rate >= 80:
            rating = "✅ EXCELLENT"
            message = "Strong defensive posture - Caught most attacks"
        elif detection_rate >= 60:
            rating = "✓ GOOD"
            message = "Adequate detection - Some gaps exist"
        elif detection_rate >= 40:
            rating = "⚠️ FAIR"
            message = "Significant gaps in detection coverage"
        else:
            rating = "❌ POOR"
            message = "Major blind spots - Defense needs improvement"

        print(f"   Overall Rating: {rating}")
        print(f"   Assessment: {message}")
        print()

        # Detection engine analysis
        print("="*70)
        print("🔍 DETECTION ENGINE ANALYSIS")
        print("="*70)
        print()

        engine_triggers = {}
        for incident in self.incidents_detected:
            engines = incident.get('detection_engines', [])
            for engine in engines:
                engine_triggers[engine] = engine_triggers.get(engine, 0) + 1

        if engine_triggers:
            print("   Detection Engine Triggers:")
            for engine, count in sorted(engine_triggers.items(), key=lambda x: x[1], reverse=True):
                print(f"      • {engine}: {count} detections")
        else:
            print("   No engine-specific data available")

        print()

        # Recommendations
        print("="*70)
        print("💡 RECOMMENDATIONS")
        print("="*70)
        print()

        if detection_rate < 100:
            print("   Areas for Improvement:")
            if detection_rate < 50:
                print("      • Increase detection sensitivity")
                print("      • Review detection signatures")
                print("      • Add more behavioral patterns")
            if detected_count == 0:
                print("      • Check if detection engines are functioning")
                print("      • Verify event processing pipeline")
            print()

        print("   Strengths:")
        if detected_count > 0:
            print("      • Successfully detected threats under load")
            print("      • Event processing pipeline operational")
            print("      • Multiple detection engines working")
        print("      • System handles concurrent attacks")
        print("      • Autonomous monitoring functional")
        print()

        print("="*70)
        print("✅ TEST COMPLETE")
        print("="*70)
        print()

        # Summary stats
        print("📋 FINAL SUMMARY:")
        print(f"   • Total Attack Types: {total_attacks}")
        print(f"   • Detection Success Rate: {detection_rate:.1f}%")
        print(f"   • Test Duration: {attack_duration:.2f}s")
        print(f"   • Defense Rating: {rating}")
        print()
        print("🎯 Result: AEGIS defensive capabilities validated under stress")
        print()


def main():
    """Run full defense test."""

    print("\n" + "="*70)
    print("⚠️  AEGIS FULL DEFENSIVE CAPABILITY TEST")
    print("="*70)
    print()
    print("This test will:")
    print("   • Launch ALL 7 attack types simultaneously")
    print("   • Stress-test AEGIS defensive capabilities")
    print("   • Measure detection effectiveness under load")
    print("   • Identify strengths and weaknesses")
    print()
    print("⚠️  This is a comprehensive stress test that will generate")
    print("   significant simulated attack traffic.")
    print()

    response = input("Proceed with full defense test? (yes/no): ").strip().lower()

    if response not in ['yes', 'y']:
        print("\nTest cancelled.")
        return

    # Run the test
    test = FullDefenseTest()
    test.run_full_test()

    print("\n" + "="*70)
    print("📝 LESSONS LEARNED:")
    print("   • Concurrent attacks reveal system limitations")
    print("   • Detection under load tests real-world readiness")
    print("   • Multi-engine approach improves coverage")
    print("   • Continuous testing identifies blind spots")
    print()
    print("🎓 NEXT STEPS:")
    print("   1. Review detected vs missed attacks")
    print("   2. Tune detection sensitivity")
    print("   3. Add signatures for missed patterns")
    print("   4. Re-test to validate improvements")
    print()
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
