"""
AEGIS Red Team Agent — Offensive Capabilities for Defense Validation

⚠️ ETHICAL USE ONLY ⚠️
This module is designed EXCLUSIVELY for:
- Security research and testing
- Defensive capability validation
- Penetration testing engagements
- CTF competitions and training
- Educational demonstrations

UNAUTHORIZED USE IS PROHIBITED AND ILLEGAL.

Purpose: Simulate realistic attack patterns to validate AEGIS defensive capabilities.
The best way to build strong defense is to think like an attacker.
"""

import random
import time
from typing import Dict, Any, List
from queue import Queue


class OffensiveAgent:
    """
    Red team agent that simulates realistic attack patterns.

    Ethical Use Statement:
    - This is a RESEARCH and TESTING tool
    - Only use against systems you OWN or have WRITTEN AUTHORIZATION to test
    - Designed to validate defensive capabilities
    - NOT for malicious use

    Based on MITRE ATT&CK framework and real-world threat actor TTPs.
    """

    def __init__(self, event_queue: Queue, mode: str = "demo"):
        """
        Initialize offensive agent.

        Args:
            event_queue: Queue to send simulated attack events
            mode: "demo" (safe), "realistic" (aggressive), "stealth" (low-and-slow)
        """
        self.event_queue = event_queue
        self.mode = mode
        self.attack_history = []

        # Ethical boundary enforcement
        self.ethical_mode = True  # Always enabled
        self.authorized_target = False  # Must be explicitly set to True

    def run_attack_simulation(self, attack_type: str = "full_chain") -> Dict[str, Any]:
        """
        Run attack simulation to test defensive capabilities.

        Args:
            attack_type: Type of attack chain to simulate

        Returns:
            Attack results and defensive response data
        """

        # Ethical check
        if not self.authorized_target:
            return {
                "error": "ETHICAL_VIOLATION",
                "message": "Target not authorized. Set authorized_target=True only for owned/authorized systems."
            }

        print("\n" + "="*70)
        print("🔴 RED TEAM AGENT ACTIVATED")
        print(f"   Mode: {self.mode}")
        print(f"   Attack Type: {attack_type}")
        print(f"   Purpose: Defense validation and testing")
        print("="*70 + "\n")

        attack_chains = {
            "full_chain": self._full_kill_chain_attack,
            "high_velocity": self._high_velocity_attack,
            "stealth": self._stealth_apt_attack,
            "ransomware": self._ransomware_simulation,
            "credential_theft": self._credential_theft_attack,
            "supply_chain": self._supply_chain_attack,
            "api_abuse": self._api_abuse_attack
        }

        if attack_type in attack_chains:
            return attack_chains[attack_type]()
        else:
            return {"error": "Unknown attack type"}

    def _full_kill_chain_attack(self) -> Dict[str, Any]:
        """
        Simulate full cyber kill chain (Lockheed Martin framework).

        Phases:
        1. Reconnaissance
        2. Weaponization
        3. Delivery
        4. Exploitation
        5. Installation
        6. Command & Control
        7. Actions on Objectives
        """

        results = {
            "attack_type": "full_kill_chain",
            "phases": [],
            "detected": False,
            "detection_phase": None,
            "defense_effectiveness": 0
        }

        # Phase 1: Reconnaissance
        print("🔴 Phase 1: Reconnaissance")
        recon_events = [
            {"type": "port_scan", "target": "192.168.1.0/24", "ports": "1-1000"},
            {"type": "dns_enumeration", "domain": "target.local"},
            {"type": "whois_lookup", "target": "target.com"},
            {"type": "osint_gathering", "source": "linkedin"}
        ]

        for event in recon_events:
            self.event_queue.put(event)
            time.sleep(0.1 if self.mode == "demo" else 0.5)

        results["phases"].append("reconnaissance")
        print("   ✓ Reconnaissance complete\n")

        # Phase 2: Weaponization
        print("🔴 Phase 2: Weaponization")
        weaponization_events = [
            {"type": "payload_creation", "malware_type": "trojan", "obfuscation": "base64"},
            {"type": "exploit_dev", "vulnerability": "CVE-2024-1234"},
            {"type": "command_injection", "payload": "calc.exe"}
        ]

        for event in weaponization_events:
            self.event_queue.put(event)
            time.sleep(0.1 if self.mode == "demo" else 0.5)

        results["phases"].append("weaponization")
        print("   ✓ Weaponization complete\n")

        # Phase 3: Delivery
        print("🔴 Phase 3: Delivery")
        delivery_events = [
            {"type": "phishing_email", "target": "admin@target.com", "attachment": "invoice.pdf.exe"},
            {"type": "watering_hole", "compromised_site": "industry-news.com"},
            {"type": "usb_drop", "location": "parking_lot"}
        ]

        for event in delivery_events:
            self.event_queue.put(event)
            time.sleep(0.1 if self.mode == "demo" else 0.5)

        results["phases"].append("delivery")
        print("   ✓ Delivery complete\n")

        # Phase 4: Exploitation
        print("🔴 Phase 4: Exploitation")
        exploitation_events = [
            {"type": "buffer_overflow", "target": "web_server", "rce": True},
            {"type": "sql_injection", "payload": "' OR '1'='1", "extraction": "credentials"},
            {"type": "xss", "payload": "<script>steal_cookies()</script>"}
        ]

        for event in exploitation_events:
            self.event_queue.put(event)
            time.sleep(0.1 if self.mode == "demo" else 0.5)

        results["phases"].append("exploitation")
        print("   ✓ Exploitation complete\n")

        # Phase 5: Installation
        print("🔴 Phase 5: Installation")
        installation_events = [
            {"type": "backdoor_install", "path": "/tmp/.hidden_backdoor", "persistence": True},
            {"type": "rootkit", "kernel_module": "malicious.ko"},
            {"type": "scheduled_task", "task": "evil_cron", "frequency": "hourly"}
        ]

        for event in installation_events:
            self.event_queue.put(event)
            time.sleep(0.1 if self.mode == "demo" else 0.5)

        results["phases"].append("installation")
        print("   ✓ Installation complete\n")

        # Phase 6: Command & Control
        print("🔴 Phase 6: Command & Control")
        c2_events = [
            {"type": "c2_beacon", "server": "evil.com", "port": 443, "protocol": "https"},
            {"type": "dns_tunneling", "queries": 100},
            {"type": "covert_channel", "method": "icmp"}
        ]

        for event in c2_events:
            self.event_queue.put(event)
            time.sleep(0.1 if self.mode == "demo" else 0.5)

        results["phases"].append("c2")
        print("   ✓ C2 established\n")

        # Phase 7: Actions on Objectives
        print("🔴 Phase 7: Actions on Objectives")
        objectives_events = [
            {"type": "data_exfiltration", "data": "customer_database.sql", "size_mb": 500},
            {"type": "lateral_movement", "target": "dc01.domain.local"},
            {"type": "privilege_escalation", "method": "token_impersonation"}
        ]

        for event in objectives_events:
            self.event_queue.put(event)
            time.sleep(0.1 if self.mode == "demo" else 0.5)

        results["phases"].append("objectives")
        print("   ✓ Objectives complete\n")

        print("🔴 ATTACK CHAIN COMPLETE")
        print("   Waiting for defensive response...\n")

        return results

    def _high_velocity_attack(self) -> Dict[str, Any]:
        """
        Simulate high-velocity automated attack (Chinese APT pattern).

        Goal: Test if AEGIS behavioral detector catches extreme velocity.
        """

        print("🔴 HIGH-VELOCITY ATTACK SIMULATION")
        print("   Pattern: Automated scanning (thousands of requests)")
        print("   Expected Detection: Behavioral velocity detector\n")

        # Rapid-fire events to trigger velocity detection
        for i in range(150):  # Exceeds velocity threshold
            self.event_queue.put({
                "type": "scan",
                "target": f"endpoint_{i}",
                "timestamp": time.time()
            })

            if i % 50 == 0:
                print(f"   📊 Sent {i} requests...")

        print("   ✓ High-velocity attack complete")
        print("   🎯 Testing if AEGIS detects extreme velocity...\n")

        return {
            "attack_type": "high_velocity",
            "requests_sent": 150,
            "pattern": "automated_scanning"
        }

    def _stealth_apt_attack(self) -> Dict[str, Any]:
        """
        Simulate stealthy APT (Advanced Persistent Threat) attack.

        Goal: Low-and-slow to evade rate-based detection.
        Test behavioral and anomaly detectors.
        """

        print("🔴 STEALTH APT SIMULATION")
        print("   Pattern: Low-and-slow (evade rate detection)")
        print("   Expected Detection: Behavioral anomaly detector\n")

        # Slow, deliberate actions
        apt_phases = [
            {"phase": "Initial Access", "action": "spear_phishing"},
            {"phase": "Persistence", "action": "registry_run_key"},
            {"phase": "Privilege Escalation", "action": "exploit_local_vuln"},
            {"phase": "Defense Evasion", "action": "disable_av"},
            {"phase": "Credential Access", "action": "mimikatz"},
            {"phase": "Discovery", "action": "network_enum"},
            {"phase": "Lateral Movement", "action": "psexec"},
            {"phase": "Collection", "action": "screenshot_capture"},
            {"phase": "Exfiltration", "action": "dns_tunneling"}
        ]

        for phase_info in apt_phases:
            print(f"   🕵️ {phase_info['phase']}: {phase_info['action']}")
            self.event_queue.put({
                "type": phase_info["action"],
                "phase": phase_info["phase"],
                "timestamp": time.time()
            })

            if self.mode == "stealth":
                time.sleep(2)  # Very slow to avoid rate detection
            else:
                time.sleep(0.2)  # Demo speed

        print("   ✓ Stealth APT complete")
        print("   🎯 Testing if AEGIS detects behavioral anomalies...\n")

        return {
            "attack_type": "stealth_apt",
            "phases_executed": len(apt_phases),
            "pattern": "low_and_slow"
        }

    def _ransomware_simulation(self) -> Dict[str, Any]:
        """
        Simulate ransomware attack pattern.

        Goal: Test signature and behavioral detection of ransomware.
        """

        print("🔴 RANSOMWARE SIMULATION")
        print("   Pattern: File encryption + ransom demand")
        print("   Expected Detection: Signature detector\n")

        # Ransomware kill chain
        events = [
            {"type": "ransomware", "action": "drop_payload", "file": "cryptor.exe"},
            {"type": "ransomware", "action": "delete_shadow_copies"},
            {"type": "ransomware", "action": "disable_recovery"},
            {"type": "ransomware", "action": "enumerate_files"},
            {"type": "ransomware", "action": "encrypt_files", "count": 5000},
            {"type": "ransomware", "action": "drop_ransom_note", "amount": "1 BTC"},
            {"type": "ransomware", "action": "wallpaper_change"},
            {"type": "ransomware", "action": "c2_notify", "victim_id": "12345"}
        ]

        for event in events:
            print(f"   💀 {event['action']}")
            self.event_queue.put(event)
            time.sleep(0.1)

        print("   ✓ Ransomware simulation complete")
        print("   🎯 Testing if AEGIS detects ransomware signatures...\n")

        return {
            "attack_type": "ransomware",
            "files_encrypted": 5000,
            "ransom_amount": "1 BTC"
        }

    def _credential_theft_attack(self) -> Dict[str, Any]:
        """
        Simulate credential theft attack.

        Goal: Test detection of credential harvesting patterns.
        """

        print("🔴 CREDENTIAL THEFT SIMULATION")
        print("   Pattern: Credential harvesting + exfiltration")
        print("   Expected Detection: Behavioral credential detector\n")

        # Credential theft techniques
        events = [
            {"type": "credential", "action": "lsass_dump"},
            {"type": "credential", "action": "sam_database_copy"},
            {"type": "credential", "action": "ntds_dit_extraction"},
            {"type": "credential", "action": "browser_password_steal"},
            {"type": "credential", "action": "keylogger_install"},
            {"type": "credential", "action": "phishing_capture"},
            {"type": "credential", "action": "token_theft"},
            {"type": "credential", "action": "kerberoasting"}
        ]

        for event in events:
            print(f"   🔑 {event['action']}")
            self.event_queue.put(event)
            time.sleep(0.1)

        # Exfiltration
        print("   📤 Exfiltrating credentials...")
        self.event_queue.put({
            "type": "exfil",
            "data": "credentials.txt",
            "count": 500
        })

        print("   ✓ Credential theft complete")
        print("   🎯 Testing if AEGIS detects credential harvesting...\n")

        return {
            "attack_type": "credential_theft",
            "credentials_stolen": 500,
            "techniques_used": len(events)
        }

    def _supply_chain_attack(self) -> Dict[str, Any]:
        """
        Simulate supply chain attack.

        Goal: Test detection of supply chain compromise patterns.
        """

        print("🔴 SUPPLY CHAIN ATTACK SIMULATION")
        print("   Pattern: Dependency compromise")
        print("   Expected Detection: Signature detector\n")

        events = [
            {"type": "supply_chain", "action": "compromise_package", "package": "popular-lib"},
            {"type": "supply_chain", "action": "inject_backdoor", "version": "2.3.4"},
            {"type": "supply_chain", "action": "publish_malicious"},
            {"type": "supply_chain", "action": "wait_for_adoption"},
            {"type": "supply_chain", "action": "activate_payload"}
        ]

        for event in events:
            print(f"   📦 {event['action']}")
            self.event_queue.put(event)
            time.sleep(0.2)

        print("   ✓ Supply chain attack complete\n")

        return {
            "attack_type": "supply_chain",
            "compromised_package": "popular-lib"
        }

    def _api_abuse_attack(self) -> Dict[str, Any]:
        """
        Simulate API abuse (similar to GTIG malware families).

        Goal: Test detection of unusual API usage patterns.
        """

        print("🔴 API ABUSE SIMULATION")
        print("   Pattern: LLM API exploitation")
        print("   Expected Detection: Advanced signature detector\n")

        # Simulate patterns from PROMPTFLUX, PROMPTSTEAL, etc.
        events = [
            {"type": "api_call", "service": "huggingface", "model": "qwen", "prompt": "generate_windows_commands"},
            {"type": "api_call", "service": "gemini", "model": "flash", "prompt": "obfuscate_vbscript"},
            {"type": "api_call", "service": "openai", "model": "gpt-4", "prompt": "create_exploit_code"},
            {"type": "network", "domain": "api-inference.huggingface.co", "requests": 50},
            {"type": "network", "domain": "generativelanguage.googleapis.com", "requests": 30},
            {"type": "file", "path": "/tmp/thinking_robot_log.txt"},
            {"type": "file", "path": "C:\\Programdata\\info\\stolen.zip"}
        ]

        for event in events:
            print(f"   🌐 API abuse: {event.get('service', event.get('domain', 'file_operation'))}")
            self.event_queue.put(event)
            time.sleep(0.1)

        print("   ✓ API abuse complete")
        print("   🎯 Testing if AEGIS detects API abuse patterns...\n")

        return {
            "attack_type": "api_abuse",
            "apis_abused": ["huggingface", "gemini", "openai"]
        }


# Global instance
_offensive_agent = None


def get_offensive_agent(event_queue: Queue, mode: str = "demo") -> OffensiveAgent:
    """Get offensive agent instance."""
    global _offensive_agent
    if _offensive_agent is None:
        _offensive_agent = OffensiveAgent(event_queue, mode)
    return _offensive_agent
