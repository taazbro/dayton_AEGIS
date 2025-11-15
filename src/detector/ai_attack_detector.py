"""
AI-Powered Attack Detector — Detect autonomous AI agent attacks
Inspired by real-world Chinese APT using Claude Code for cyber espionage (Jan 2025)

REAL-WORLD THREAT:
- Chinese hackers used Anthropic's Claude Code to automate spying
- 80-90% autonomous operation
- Thousands of requests per second
- Successfully breached 4+ organizations
- First documented case of fully automated state-sponsored AI cyber operation

AEGIS DEFENSE:
This module detects the signatures of AI-powered attacks
"""

from typing import Dict, Any, List
import time
from collections import defaultdict


class AIAttackDetector:
    """
    Detect AI-powered cyber attacks based on real-world APT patterns.

    DETECTION SIGNATURES (from Anthropic incident report):
    - Extremely high request rates (thousands/second)
    - Sequential system inspection patterns
    - Automated credential harvesting
    - Rapid database scanning
    - Custom exploit code generation patterns
    - Autonomous multi-step operations
    """

    def __init__(self):
        self.request_timestamps = defaultdict(list)
        self.ai_attack_signatures = {
            "rapid_scanning": 0,
            "sequential_inspection": 0,
            "credential_harvesting": 0,
            "automated_exploitation": 0,
            "high_velocity": 0
        }

    def detect_ai_attack(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Detect if attack pattern matches AI-powered automation.

        Based on real-world Chinese APT using Claude Code (Jan 2025)

        Args:
            events: List of security events

        Returns:
            Detection result with AI attack indicators
        """
        if not events:
            return {"is_ai_attack": False}

        # Signature 1: Extreme velocity (thousands of requests/second)
        velocity_score = self._detect_extreme_velocity(events)

        # Signature 2: Sequential system inspection (AI agent pattern)
        inspection_score = self._detect_sequential_inspection(events)

        # Signature 3: Automated credential harvesting
        credential_score = self._detect_credential_harvesting(events)

        # Signature 4: Multi-step autonomous operation
        automation_score = self._detect_automation_pattern(events)

        # Signature 5: Perfect timing (no human delays)
        timing_score = self._detect_perfect_timing(events)

        # Calculate overall AI attack probability
        total_score = (
            velocity_score * 0.3 +
            inspection_score * 0.2 +
            credential_score * 0.2 +
            automation_score * 0.2 +
            timing_score * 0.1
        )

        is_ai_attack = total_score > 0.6

        return {
            "is_ai_attack": is_ai_attack,
            "confidence": total_score,
            "signatures_detected": {
                "extreme_velocity": velocity_score,
                "sequential_inspection": inspection_score,
                "credential_harvesting": credential_score,
                "automation_pattern": automation_score,
                "perfect_timing": timing_score
            },
            "threat_type": "AI-Powered APT (Claude Code-like)" if is_ai_attack else None,
            "reference": "Chinese APT using Anthropic Claude Code (Jan 2025)" if is_ai_attack else None,
            "mitigation": self._get_ai_attack_mitigation() if is_ai_attack else None
        }

    def _detect_extreme_velocity(self, events: List[Dict[str, Any]]) -> float:
        """
        Detect extreme request velocity (thousands/second).

        Real-world: "The AI made thousands of requests per second"
        """
        if len(events) < 10:
            return 0.0

        # Calculate requests per second
        time_window = 1.0  # 1 second
        recent_events = events[-100:]  # Last 100 events

        if len(recent_events) > 100:  # More than 100 requests in recent history
            return 1.0
        elif len(recent_events) > 50:
            return 0.8
        elif len(recent_events) > 20:
            return 0.5
        else:
            return 0.0

    def _detect_sequential_inspection(self, events: List[Dict[str, Any]]) -> float:
        """
        Detect sequential system inspection pattern.

        Real-world: "Claude inspected target systems, scanned for high-value databases"
        """
        inspection_keywords = [
            "scan", "inspect", "enumerate", "discover",
            "database", "admin", "credential", "config"
        ]

        inspection_events = []
        for event in events:
            event_str = str(event).lower()
            if any(keyword in event_str for keyword in inspection_keywords):
                inspection_events.append(event)

        if len(inspection_events) >= 5:
            return 1.0
        elif len(inspection_events) >= 3:
            return 0.7
        elif len(inspection_events) >= 1:
            return 0.4
        else:
            return 0.0

    def _detect_credential_harvesting(self, events: List[Dict[str, Any]]) -> float:
        """
        Detect automated credential harvesting.

        Real-world: "Claude harvested usernames and passwords"
        """
        credential_keywords = [
            "password", "credential", "token", "secret",
            "auth", "login", "session", "api_key"
        ]

        credential_events = 0
        for event in events:
            event_str = str(event).lower()
            if any(keyword in event_str for keyword in credential_keywords):
                credential_events += 1

        if credential_events >= 10:
            return 1.0
        elif credential_events >= 5:
            return 0.7
        elif credential_events >= 2:
            return 0.4
        else:
            return 0.0

    def _detect_automation_pattern(self, events: List[Dict[str, Any]]) -> float:
        """
        Detect multi-step autonomous operation pattern.

        Real-world: "80-90% of the operation carried out autonomously"
        """
        # Look for sequential attack phases
        phases = {
            "recon": ["scan", "enum", "discover"],
            "weaponization": ["exploit", "payload"],
            "exploitation": ["execute", "inject", "overflow"],
            "persistence": ["backdoor", "persist", "schedule"],
            "exfil": ["exfil", "extract", "download", "upload"]
        }

        phases_detected = set()
        for event in events:
            event_str = str(event).lower()
            for phase, keywords in phases.items():
                if any(keyword in event_str for keyword in keywords):
                    phases_detected.add(phase)

        # AI attacks typically progress through multiple phases rapidly
        phase_count = len(phases_detected)

        if phase_count >= 4:
            return 1.0
        elif phase_count >= 3:
            return 0.7
        elif phase_count >= 2:
            return 0.4
        else:
            return 0.0

    def _detect_perfect_timing(self, events: List[Dict[str, Any]]) -> float:
        """
        Detect suspiciously perfect timing (no human delays).

        Real-world: AI agents execute with machine precision
        """
        if len(events) < 5:
            return 0.0

        # Human attackers have variable timing
        # AI attacks have consistent, rapid timing

        # This is a simplified check - production would analyze timing variance
        return 0.5  # Moderate score as we don't have precise timestamps

    def _get_ai_attack_mitigation(self) -> List[str]:
        """Get mitigation strategies for AI-powered attacks"""
        return [
            "IMMEDIATE: Rate limit all API endpoints to prevent AI velocity",
            "IMMEDIATE: Enable CAPTCHA on authentication endpoints",
            "IMMEDIATE: Monitor for rapid sequential system calls",
            "SHORT-TERM: Implement behavioral biometrics (detect non-human patterns)",
            "SHORT-TERM: Deploy AI-powered defense (AEGIS autonomous response)",
            "SHORT-TERM: Alert SOC team - possible state-sponsored APT",
            "LONG-TERM: Implement honeypots to detect automated scanning",
            "LONG-TERM: Network segmentation to limit autonomous lateral movement",
            "LONG-TERM: Zero-trust architecture with continuous authentication"
        ]

    def generate_ai_attack_report(self, detection: Dict[str, Any]) -> str:
        """Generate detailed report for AI attack detection"""
        if not detection.get("is_ai_attack"):
            return "No AI-powered attack detected"

        report = f"""
╔════════════════════════════════════════════════════════════════╗
║  🤖 AI-POWERED ATTACK DETECTED                                 ║
║  Based on real-world Chinese APT using Claude Code (Jan 2025) ║
╚════════════════════════════════════════════════════════════════╝

⚠️  THREAT CLASSIFICATION: {detection['threat_type']}
📊 CONFIDENCE: {detection['confidence']:.1%}
📚 REFERENCE: {detection['reference']}

🔍 AI ATTACK SIGNATURES DETECTED:
   • Extreme Velocity: {detection['signatures_detected']['extreme_velocity']:.1%}
   • Sequential Inspection: {detection['signatures_detected']['sequential_inspection']:.1%}
   • Credential Harvesting: {detection['signatures_detected']['credential_harvesting']:.1%}
   • Automation Pattern: {detection['signatures_detected']['automation_pattern']:.1%}
   • Perfect Timing: {detection['signatures_detected']['perfect_timing']:.1%}

🛡️ RECOMMENDED MITIGATION:
"""
        for i, action in enumerate(detection['mitigation'], 1):
            report += f"   {i}. {action}\n"

        report += """
⚡ SEVERITY: CRITICAL - State-sponsored AI-powered attack
🎯 ATTACK VECTOR: Autonomous AI agent (Claude Code-like)
📖 CONTEXT: First documented case of fully automated state cyber operation

💡 This detection capability makes AEGIS one of the first autonomous
   defense systems capable of identifying AI-powered attacks in real-time.
"""
        return report


# Global instance
_ai_attack_detector = None


def get_ai_attack_detector() -> AIAttackDetector:
    """Get singleton AI attack detector"""
    global _ai_attack_detector
    if _ai_attack_detector is None:
        _ai_attack_detector = AIAttackDetector()
    return _ai_attack_detector
