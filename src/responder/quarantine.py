"""
Quarantine — Isolate compromised assets (MOCKED)
"""

from typing import Dict, Any
import time


def quarantine_asset(incident: Dict[str, Any]) -> None:
    """
    Quarantine compromised or suspicious assets.

    IMPORTANT: This is MOCKED behavior for hackathon safety.
    No actual network changes are made.

    Args:
        incident: Incident details triggering quarantine
    """
    print("\n" + "-" * 60)
    print("🚧 QUARANTINE INITIATED")
    print("-" * 60)

    threat_type = incident.get("threat_type", "unknown")
    reason = incident.get("reason", "No reason provided")

    print(f"Threat Type: {threat_type}")
    print(f"Reason: {reason}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Extract affected entities from incident
    event_counts = incident.get("event_counts", {})
    event_sequence = incident.get("event_sequence", [])

    print("\n⚠️  MOCK ACTIONS (no real isolation performed):")
    print("  • Moving asset to quarantine VLAN")
    print("  • Blocking lateral movement")
    print("  • Enabling enhanced monitoring")
    print("  • Capturing memory dump")
    print("  • Preserving logs for analysis")

    if event_counts:
        print(f"\nEvent Summary: {event_counts}")

    if event_sequence:
        print(f"Attack Sequence: {' → '.join(event_sequence)}")

    print("\n✓ Quarantine procedure completed")
    print("-" * 60 + "\n")

    # In production, this would:
    # - Move to isolated network segment
    # - Apply strict firewall rules
    # - Enable packet capture
    # - Trigger forensic collection
    # - Update CMDB status
