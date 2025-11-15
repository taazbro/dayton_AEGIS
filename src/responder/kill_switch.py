"""
Kill Switch — Emergency shutdown response (MOCKED for safety)
"""

from typing import Dict, Any
import time


def activate_kill_switch(incident: Dict[str, Any]) -> None:
    """
    Activate emergency kill switch to stop critical threat.

    IMPORTANT: This is MOCKED behavior for hackathon safety.
    No actual system commands are executed.

    Args:
        incident: Incident details triggering the kill switch
    """
    print("\n" + "=" * 60)
    print("🔴 KILL SWITCH ACTIVATED 🔴")
    print("=" * 60)

    threat_type = incident.get("threat_type", "unknown")
    reason = incident.get("reason", "No reason provided")

    print(f"Threat Type: {threat_type}")
    print(f"Reason: {reason}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n⚠️  MOCK ACTIONS (no real commands executed):")
    print("  • Blocking all inbound traffic")
    print("  • Terminating suspicious processes")
    print("  • Disconnecting affected servers")
    print("  • Alerting security team")
    print("  • Capturing forensic snapshot")

    print("\n✓ Kill switch procedure completed")
    print("=" * 60 + "\n")

    # In production, this would execute real defensive actions:
    # - iptables rules
    # - process termination
    # - network segmentation
    # - automated notifications
