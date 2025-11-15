"""
Attack Simulator — Generates synthetic attack events for testing
"""

import time
import random
from queue import Queue
from typing import Dict, Any, List


class AttackSimulator:
    """Simulates various cyber attack patterns for AEGIS testing."""

    def __init__(self, event_queue: Queue):
        """
        Initialize the attack simulator.

        Args:
            event_queue: Queue to send simulated events to
        """
        self.event_queue = event_queue
        self.attack_sequences = [
            # Classic sequences
            ["recon", "scan", "exploit"],
            ["recon", "scan", "cred-guess", "cred-guess", "cred-guess"],
            ["scan", "exploit", "exfil"],
            ["recon", "cred-guess", "exploit", "exfil"],

            # Web application attacks
            ["sqli", "sqli", "db-dump"],
            ["xss", "session-hijack", "account-takeover"],
            ["lfi", "rce", "backdoor"],

            # Advanced persistent threat
            ["recon", "phish", "exploit", "lateral-move", "exfil"],
            ["watering-hole", "exploit", "persist", "c2-beacon"],

            # DDoS attacks
            ["ddos-syn", "ddos-syn", "ddos-syn", "ddos-syn"],
            ["ddos-http", "ddos-http", "ddos-http"],

            # Ransomware
            ["phish", "exploit", "encrypt-files", "ransom-note"],
            ["rdp-brute", "exploit", "lateral-move", "encrypt-files"],

            # Supply chain
            ["supply-chain", "backdoor", "persist", "c2-beacon"],

            # Crypto mining
            ["exploit", "crypto-miner", "persist"],
        ]

    def generate_event(self, event_type: str, source_ip: str = None) -> Dict[str, Any]:
        """
        Generate a single attack event.

        Args:
            event_type: Type of attack event
            source_ip: Source IP address (random if not provided)

        Returns:
            Event dictionary
        """
        if source_ip is None:
            source_ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"

        event = {
            "timestamp": time.time(),
            "type": event_type,
            "source_ip": source_ip,
            "target": self._get_target(event_type),
            "severity": self._get_severity(event_type),
        }

        # Add attack-specific payloads
        if event_type in ["sqli", "xss", "lfi", "rce"]:
            event["payload"] = self._generate_payload(event_type)

        return event

    def _get_target(self, event_type: str) -> str:
        """Get appropriate target for event type."""
        target_map = {
            "sqli": "db-server-01",
            "db-dump": "db-server-01",
            "xss": "web-app-01",
            "ddos-syn": "loadbalancer-01",
            "ddos-http": "web-app-01",
            "crypto-miner": "compute-cluster-01",
        }
        return target_map.get(event_type, "server-prod-01")

    def _generate_payload(self, event_type: str) -> str:
        """Generate realistic attack payload."""
        payloads = {
            "sqli": "' OR 1=1; DROP TABLE users--",
            "xss": "<script>alert('XSS')</script>",
            "lfi": "../../../../etc/passwd",
            "rce": "system('cat /etc/passwd')",
        }
        return payloads.get(event_type, "")

    def _get_severity(self, event_type: str) -> str:
        """Determine severity level based on event type."""
        severity_map = {
            # Reconnaissance
            "recon": "low",
            "scan": "medium",

            # Initial access
            "phish": "medium",
            "exploit": "high",
            "cred-guess": "medium",
            "rdp-brute": "high",

            # Web attacks
            "sqli": "high",
            "xss": "high",
            "lfi": "high",
            "rce": "critical",
            "csrf": "medium",

            # Lateral movement
            "lateral-move": "critical",
            "pivot": "high",

            # Persistence
            "backdoor": "critical",
            "persist": "high",
            "rootkit": "critical",

            # C2
            "c2-beacon": "high",
            "c2-command": "critical",

            # Data theft
            "exfil": "critical",
            "db-dump": "critical",
            "cred-dump": "high",

            # Impact
            "ransom-note": "critical",
            "encrypt-files": "critical",
            "destroy-data": "critical",
            "ddos-syn": "high",
            "ddos-http": "high",
            "ddos-udp": "high",
            "crypto-miner": "medium",

            # Advanced
            "supply-chain": "critical",
            "watering-hole": "high",
            "zero-day": "critical",
            "session-hijack": "high",
            "account-takeover": "critical",
        }
        return severity_map.get(event_type, "medium")

    def simulate_attack_sequence(self, sequence: List[str]) -> None:
        """
        Simulate a complete attack sequence.

        Args:
            sequence: List of attack event types in order
        """
        source_ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"

        for event_type in sequence:
            event = self.generate_event(event_type, source_ip)
            self.event_queue.put(event)
            print(f"🔴 Simulated: {event_type} from {source_ip}")
            time.sleep(random.uniform(0.5, 2.0))

    def run(self) -> None:
        """Run the attack simulator continuously."""
        print("🎭 Attack Simulator: Starting...\n")

        while True:
            # Random delay between attack sequences
            time.sleep(random.uniform(5, 15))

            # Select random attack sequence
            sequence = random.choice(self.attack_sequences)

            print(f"\n🎯 Launching attack sequence: {' → '.join(sequence)}")
            self.simulate_attack_sequence(sequence)
