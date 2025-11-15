"""
AEGIS Behavioral Analysis Engine
Real-time behavioral detection using AI-powered pattern recognition
"""

import os
import time
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

# Import our malware database
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from src.detection.malware_signatures import (
    MALWARE_DATABASE,
    AI_POWERED_THREATS,
    MalwareSignature,
    BehavioralIndicator,
    ThreatSeverity
)


class DetectionConfidence(Enum):
    """Confidence level for threat detection"""
    DEFINITE = 1.0  # 95-100% match
    HIGH = 0.8      # 80-95% match
    MEDIUM = 0.6    # 60-80% match
    LOW = 0.4       # 40-60% match
    SUSPICIOUS = 0.2  # 20-40% match


@dataclass
class BehavioralEvent:
    """A single observed behavioral event"""
    timestamp: float
    event_type: str
    description: str
    iocs: List[str]  # Indicators observed
    severity: int  # 1-10
    process_name: Optional[str] = None
    network_connection: Optional[str] = None
    file_path: Optional[str] = None
    registry_key: Optional[str] = None


@dataclass
class ThreatDetection:
    """Result of behavioral analysis"""
    threat_name: str
    threat_category: str
    confidence: float  # 0.0 to 1.0
    severity: int  # 1-10
    matched_behaviors: List[str]
    behavioral_score: float
    ai_powered: bool
    kill_chain_stage: str
    recommended_action: str
    evidence: List[BehavioralEvent]
    detection_time: float


class BehavioralAnalyzer:
    """
    AI-Powered Behavioral Analysis Engine

    This is "Guard 2" from our analogy - it doesn't look at signatures,
    it watches BEHAVIOR to detect threats.
    """

    def __init__(self, enable_ai_detection: bool = True):
        self.enable_ai_detection = enable_ai_detection
        self.event_buffer = []  # Recent behavioral events
        self.detection_history = []  # Past detections
        self.baseline_established = False

        # Baseline "normal" behavior (would be learned over time)
        self.baseline = {
            "normal_processes": ["explorer.exe", "chrome.exe", "firefox.exe"],
            "normal_network_ports": [80, 443, 53],
            "normal_file_ops_per_sec": 10,
            "normal_registry_writes_per_min": 5,
        }

        print("   🛡️  Behavioral Analyzer: Initialized")
        print(f"      AI Detection: {'Enabled' if enable_ai_detection else 'Disabled'}")
        print(f"      Monitoring {len(MALWARE_DATABASE)} malware signatures")
        if enable_ai_detection:
            print(f"      Monitoring {len(AI_POWERED_THREATS)} AI-powered threat patterns")

    def add_event(self, event: BehavioralEvent):
        """Add a new behavioral event for analysis"""
        self.event_buffer.append(event)

        # Keep only last 1000 events
        if len(self.event_buffer) > 1000:
            self.event_buffer = self.event_buffer[-1000:]

    def analyze_behavior(
        self,
        events: List[BehavioralEvent],
        context: Optional[Dict] = None
    ) -> List[ThreatDetection]:
        """
        Analyze a sequence of behavioral events to detect threats.

        This is the CORE of behavioral analysis - we look at WHAT the
        program is DOING, not what file it is.
        """
        detections = []

        # Analyze against known malware signatures
        for malware_name, signature in MALWARE_DATABASE.items():
            detection = self._match_signature(events, signature, context)
            if detection:
                detections.append(detection)

        # Analyze against AI-powered threat patterns
        if self.enable_ai_detection:
            for threat_name, threat_pattern in AI_POWERED_THREATS.items():
                detection = self._match_ai_threat(events, threat_name, threat_pattern, context)
                if detection:
                    detections.append(detection)

        # Sort by confidence (highest first)
        detections.sort(key=lambda d: d.confidence, reverse=True)

        # Store in history
        self.detection_history.extend(detections)

        return detections

    def _match_signature(
        self,
        events: List[BehavioralEvent],
        signature: MalwareSignature,
        context: Optional[Dict]
    ) -> Optional[ThreatDetection]:
        """
        Match events against a known malware signature.

        This is behavioral analysis - we score based on how many
        "suspicious behaviors" we see.
        """
        matched_behaviors = []
        total_weight = 0.0
        matched_weight = 0.0
        evidence_events = []

        # Check each behavioral indicator
        for behavior in signature.behaviors:
            total_weight += behavior.weight

            # See if we observed this behavior in our events
            for event in events:
                # Check if any of the behavior's IOCs match the event
                for ioc in behavior.iocs:
                    if self._ioc_matches_event(ioc, event):
                        matched_behaviors.append(behavior.name)
                        matched_weight += behavior.weight
                        evidence_events.append(event)
                        break  # Move to next behavior

                if behavior.name in matched_behaviors:
                    break  # Already matched this behavior

        # Calculate behavioral score (0.0 to 1.0)
        behavioral_score = matched_weight / total_weight if total_weight > 0 else 0.0

        # Determine if this is a confident detection
        confidence = behavioral_score

        # Threshold: Need at least 60% behavioral match
        if confidence < 0.6:
            return None

        # Determine kill chain stage based on matched behaviors
        kill_chain_stage = self._determine_kill_chain_stage(matched_behaviors, signature)

        # Recommended action based on severity and confidence
        recommended_action = self._get_recommended_action(
            signature.severity.value,
            confidence
        )

        return ThreatDetection(
            threat_name=signature.name,
            threat_category=signature.category.value,
            confidence=confidence,
            severity=signature.severity.value,
            matched_behaviors=matched_behaviors,
            behavioral_score=behavioral_score,
            ai_powered=False,
            kill_chain_stage=kill_chain_stage,
            recommended_action=recommended_action,
            evidence=evidence_events,
            detection_time=time.time()
        )

    def _match_ai_threat(
        self,
        events: List[BehavioralEvent],
        threat_name: str,
        threat_pattern: Dict,
        context: Optional[Dict]
    ) -> Optional[ThreatDetection]:
        """Match events against AI-powered threat patterns"""
        matched_behaviors = []
        total_weight = 0.0
        matched_weight = 0.0
        evidence_events = []

        # Check each behavioral pattern
        for behavior in threat_pattern['behaviors']:
            total_weight += behavior['weight']

            # See if we observed this behavior
            for event in events:
                for ioc in behavior['iocs']:
                    if self._ioc_matches_event(ioc, event):
                        matched_behaviors.append(behavior['name'])
                        matched_weight += behavior['weight']
                        evidence_events.append(event)
                        break

                if behavior['name'] in matched_behaviors:
                    break

        behavioral_score = matched_weight / total_weight if total_weight > 0 else 0.0
        confidence = behavioral_score

        # Threshold for AI threats is higher (70%) because they're more sophisticated
        if confidence < 0.7:
            return None

        # AI threats are all CRITICAL
        severity = 10

        return ThreatDetection(
            threat_name=threat_pattern['name'],
            threat_category="AI-Powered Attack",
            confidence=confidence,
            severity=severity,
            matched_behaviors=matched_behaviors,
            behavioral_score=behavioral_score,
            ai_powered=True,
            kill_chain_stage="Execution (AI-Autonomous)",
            recommended_action="IMMEDIATE ISOLATION - AI-Powered Threat",
            evidence=evidence_events,
            detection_time=time.time()
        )

    def _ioc_matches_event(self, ioc: str, event: BehavioralEvent) -> bool:
        """
        Check if an IOC (Indicator of Compromise) matches a behavioral event.

        This is where the "pattern matching" happens.
        """
        # Check in event description
        if ioc.lower() in event.description.lower():
            return True

        # Check in event IOCs list
        for event_ioc in event.iocs:
            if ioc.lower() in event_ioc.lower():
                return True

        # Check specific fields
        if event.process_name and ioc.lower() in event.process_name.lower():
            return True

        if event.network_connection and ioc.lower() in event.network_connection.lower():
            return True

        if event.file_path and ioc.lower() in event.file_path.lower():
            return True

        if event.registry_key and ioc.lower() in event.registry_key.lower():
            return True

        return False

    def _determine_kill_chain_stage(
        self,
        matched_behaviors: List[str],
        signature: MalwareSignature
    ) -> str:
        """Determine which stage of the kill chain we're seeing"""
        behavior_str = " ".join(matched_behaviors).lower()

        if "backup deletion" in behavior_str or "encryption" in behavior_str:
            return "Impact"
        elif "exfiltration" in behavior_str or "data theft" in behavior_str:
            return "Exfiltration"
        elif "lateral movement" in behavior_str or "spreading" in behavior_str:
            return "Lateral Movement"
        elif "credential" in behavior_str or "mimikatz" in behavior_str:
            return "Credential Access"
        elif "evasion" in behavior_str or "edr killer" in behavior_str:
            return "Defense Evasion"
        elif "persistence" in behavior_str or "registry" in behavior_str:
            return "Persistence"
        else:
            return "Execution"

    def _get_recommended_action(self, severity: int, confidence: float) -> str:
        """
        Get recommended action based on threat severity and confidence.

        This is the "DESTROY" phase - what should the AI agent do?
        """
        if severity >= 9 and confidence >= 0.8:
            return "IMMEDIATE ISOLATION + TERMINATE PROCESS + ALERT SOC"
        elif severity >= 8 and confidence >= 0.7:
            return "ISOLATE HOST + INVESTIGATE + ALERT"
        elif severity >= 6 and confidence >= 0.6:
            return "MONITOR CLOSELY + LOG ALL ACTIVITY"
        else:
            return "FLAG FOR MANUAL REVIEW"

    def check_anomaly(self, event: BehavioralEvent) -> Optional[str]:
        """
        Check if an event deviates from baseline "normal" behavior.

        This is the "behavioral" part - does this LOOK wrong?
        """
        anomalies = []

        # Check for unusual process names
        if event.process_name:
            if event.process_name not in self.baseline["normal_processes"]:
                # Check for process disguise (e.g., "svchost.exe" in weird location)
                if "svchost" in event.process_name.lower() or "explorer" in event.process_name.lower():
                    anomalies.append(f"Suspicious process: {event.process_name}")

        # Check for unusual network activity
        if event.network_connection:
            # Look for connections to known bad indicators
            if "api.gemini.google.com" in event.network_connection and event.event_type == "script_execution":
                anomalies.append("AI-Polymorphic: Script calling LLM API for self-modification")

            if "pastebin.com" in event.network_connection:
                anomalies.append("C2 Communication: Pastebin used as C2 server")

            if "tor" in event.network_connection.lower():
                anomalies.append("Suspicious network: Tor connection detected")

        # Check for rapid file modifications (ransomware indicator)
        recent_file_mods = [e for e in self.event_buffer[-100:] if e.event_type == "file_modification"]
        if len(recent_file_mods) > 50:
            anomalies.append("RANSOMWARE INDICATOR: Rapid mass file modification")

        # Check for registry persistence
        if event.registry_key:
            if "\\Run" in event.registry_key or "\\RunOnce" in event.registry_key:
                anomalies.append("Persistence: Registry Run key modification")

        return "; ".join(anomalies) if anomalies else None

    def get_detection_summary(self) -> Dict:
        """Get summary of all detections"""
        if not self.detection_history:
            return {"total": 0, "by_severity": {}, "by_category": {}}

        summary = {
            "total": len(self.detection_history),
            "by_severity": {},
            "by_category": {},
            "ai_powered_count": len([d for d in self.detection_history if d.ai_powered]),
        }

        for detection in self.detection_history:
            # Count by severity
            sev_key = f"Severity_{detection.severity}"
            summary["by_severity"][sev_key] = summary["by_severity"].get(sev_key, 0) + 1

            # Count by category
            summary["by_category"][detection.threat_category] = \
                summary["by_category"].get(detection.threat_category, 0) + 1

        return summary


# ============================================================================
# SIMULATED BEHAVIORAL EVENTS (for testing)
# ============================================================================

def simulate_ransomware_behavior() -> List[BehavioralEvent]:
    """Simulate a ransomware attack sequence"""
    t = time.time()

    return [
        BehavioralEvent(
            timestamp=t,
            event_type="process_execution",
            description="Unknown process executed",
            iocs=["unknown executable", "suspicious origin"],
            severity=5,
            process_name="invoice_2024.exe"
        ),
        BehavioralEvent(
            timestamp=t + 1,
            event_type="command_execution",
            description="Shadow copy deletion command",
            iocs=["vssadmin delete shadows /all /quiet"],
            severity=9,
            process_name="cmd.exe"
        ),
        BehavioralEvent(
            timestamp=t + 2,
            event_type="security_software_termination",
            description="Antivirus process terminated",
            iocs=["security software termination", "process kill"],
            severity=9,
            process_name="powershell.exe"
        ),
        BehavioralEvent(
            timestamp=t + 3,
            event_type="file_modification",
            description="Mass file encryption in progress",
            iocs=["rapid file modification", "file extension change", ".encrypted"],
            severity=10,
            file_path="C:\\Users\\*\\Documents\\*.encrypted"
        ),
        BehavioralEvent(
            timestamp=t + 4,
            event_type="network_connection",
            description="Connection to Tor network",
            iocs=["Tor", "onion routing"],
            severity=8,
            network_connection="tor-exit-node.onion:9050"
        ),
    ]


def simulate_ai_polymorphic_attack() -> List[BehavioralEvent]:
    """Simulate an AI-powered polymorphic malware"""
    t = time.time()

    return [
        BehavioralEvent(
            timestamp=t,
            event_type="script_execution",
            description="VBScript execution detected",
            iocs=["wscript.exe", "obfuscated script"],
            severity=6,
            process_name="wscript.exe"
        ),
        BehavioralEvent(
            timestamp=t + 1,
            event_type="network_connection",
            description="Script connecting to Gemini API",
            iocs=["api.gemini.google.com", "HTTPS POST"],
            severity=9,
            network_connection="api.gemini.google.com:443"
        ),
        BehavioralEvent(
            timestamp=t + 2,
            event_type="file_creation",
            description="Script created new file with different hash",
            iocs=["self-modification", "hash change", "new file creation"],
            severity=8,
            file_path="C:\\Users\\Public\\update_v2.vbs"
        ),
        BehavioralEvent(
            timestamp=t + 3,
            event_type="persistence",
            description="Added to Startup folder",
            iocs=["Startup folder", "persistence"],
            severity=7,
            file_path="C:\\Users\\*\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\update.lnk"
        ),
    ]


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔬 AEGIS BEHAVIORAL ANALYSIS ENGINE - DEMO")
    print("="*70)

    # Initialize analyzer
    analyzer = BehavioralAnalyzer(enable_ai_detection=True)

    print("\n" + "-"*70)
    print("TEST 1: Simulating Ransomware Attack")
    print("-"*70)

    ransomware_events = simulate_ransomware_behavior()
    print(f"\n📊 Analyzing {len(ransomware_events)} behavioral events...")

    for event in ransomware_events:
        print(f"\n   Event: {event.description}")
        print(f"   IOCs: {', '.join(event.iocs[:2])}")

        # Check for anomalies
        anomaly = analyzer.check_anomaly(event)
        if anomaly:
            print(f"   ⚠️  Anomaly: {anomaly}")

    # Analyze the full sequence
    detections = analyzer.analyze_behavior(ransomware_events)

    if detections:
        print(f"\n🚨 THREATS DETECTED: {len(detections)}")
        for det in detections:
            print(f"\n   ════════════════════════════════════════════════════════════")
            print(f"   🔴 {det.threat_name} ({det.threat_category})")
            print(f"   ════════════════════════════════════════════════════════════")
            print(f"   Confidence: {det.confidence*100:.1f}%")
            print(f"   Severity: {det.severity}/10")
            print(f"   Kill Chain Stage: {det.kill_chain_stage}")
            print(f"   Matched Behaviors ({len(det.matched_behaviors)}):")
            for behavior in det.matched_behaviors:
                print(f"      • {behavior}")
            print(f"   ⚡ Recommended Action: {det.recommended_action}")

    print("\n" + "-"*70)
    print("TEST 2: Simulating AI-Powered Polymorphic Malware")
    print("-"*70)

    ai_events = simulate_ai_polymorphic_attack()
    print(f"\n📊 Analyzing {len(ai_events)} behavioral events...")

    for event in ai_events:
        print(f"\n   Event: {event.description}")
        anomaly = analyzer.check_anomaly(event)
        if anomaly:
            print(f"   ⚠️  Anomaly: {anomaly}")

    detections = analyzer.analyze_behavior(ai_events)

    if detections:
        print(f"\n🚨 THREATS DETECTED: {len(detections)}")
        for det in detections:
            print(f"\n   ════════════════════════════════════════════════════════════")
            print(f"   🔴 {det.threat_name}")
            print(f"   ════════════════════════════════════════════════════════════")
            print(f"   AI-Powered: {'YES' if det.ai_powered else 'NO'}")
            print(f"   Confidence: {det.confidence*100:.1f}%")
            print(f"   Severity: {det.severity}/10")
            print(f"   Matched Behaviors:")
            for behavior in det.matched_behaviors:
                print(f"      • {behavior}")
            print(f"   ⚡ Recommended Action: {det.recommended_action}")

    # Summary
    summary = analyzer.get_detection_summary()
    print("\n" + "="*70)
    print("📊 DETECTION SUMMARY")
    print("="*70)
    print(f"Total Detections: {summary['total']}")
    print(f"AI-Powered Threats: {summary['ai_powered_count']}")
    print(f"\nBy Severity:")
    for sev, count in sorted(summary['by_severity'].items()):
        print(f"   {sev}: {count}")
    print(f"\nBy Category:")
    for cat, count in summary['by_category'].items():
        print(f"   {cat}: {count}")
    print("\n" + "="*70 + "\n")
