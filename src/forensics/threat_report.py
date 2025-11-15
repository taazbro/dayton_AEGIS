"""
Threat Report — Generate structured forensics report
"""

from typing import Dict, Any
import time
import json


def generate_threat_report(
    incident: Dict[str, Any],
    replay_artifacts: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate comprehensive threat report for Claude analysis.

    Args:
        incident: Detected incident details
        replay_artifacts: Artifacts from BrowserUse replay

    Returns:
        Structured threat report
    """
    report = {
        "report_id": f"AEGIS-{int(time.time())}",
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "incident_summary": {
            "threat_type": incident.get("threat_type", "unknown"),
            "severity": incident.get("severity", "unknown"),
            "action_taken": incident.get("action", "none"),
            "reason": incident.get("reason", "No reason provided"),
        },
        "event_analysis": {
            "event_counts": incident.get("event_counts", {}),
            "event_sequence": incident.get("event_sequence", []),
        },
        "replay_analysis": {
            "success": replay_artifacts.get("success", False),
            "steps_executed": replay_artifacts.get("steps_executed", []),
            "artifacts_collected": {
                "screenshots": replay_artifacts.get("screenshots_captured", 0),
                "network_traces": len(replay_artifacts.get("network_traces", [])),
                "dom_snapshots": len(replay_artifacts.get("dom_snapshots", [])),
            },
        },
        "recommendations": _generate_recommendations(incident),
    }

    return report


def _generate_recommendations(incident: Dict[str, Any]) -> list[str]:
    """
    Generate security recommendations based on incident type.

    Args:
        incident: Incident details

    Returns:
        List of recommendation strings
    """
    threat_type = incident.get("threat_type", "unknown")
    recommendations = []

    if "exfil" in threat_type.lower():
        recommendations.extend([
            "Implement DLP (Data Loss Prevention) policies",
            "Review egress firewall rules",
            "Enable enhanced logging for data access",
            "Conduct immediate data classification audit",
        ])

    if "credential" in threat_type.lower():
        recommendations.extend([
            "Enforce MFA on all accounts",
            "Implement rate limiting on authentication endpoints",
            "Review password policies and complexity requirements",
            "Deploy account lockout mechanisms",
        ])

    if "exploit" in threat_type.lower():
        recommendations.extend([
            "Patch affected systems immediately",
            "Deploy WAF rules to block exploit patterns",
            "Conduct vulnerability assessment",
            "Review application security controls",
        ])

    if "scan" in threat_type.lower():
        recommendations.extend([
            "Implement port scan detection and blocking",
            "Review network segmentation",
            "Deploy honeypots to detect reconnaissance",
        ])

    if not recommendations:
        recommendations.append("Continue monitoring for suspicious activity")

    return recommendations


def format_report_for_display(report: Dict[str, Any]) -> str:
    """
    Format threat report for console display.

    Args:
        report: Threat report dictionary

    Returns:
        Formatted string
    """
    lines = [
        "\n" + "=" * 60,
        f"📊 THREAT REPORT: {report['report_id']}",
        "=" * 60,
        f"\nTimestamp: {report['timestamp']}",
        f"\nThreat Type: {report['incident_summary']['threat_type']}",
        f"Severity: {report['incident_summary']['severity']}",
        f"Action Taken: {report['incident_summary']['action_taken']}",
        f"\nReason: {report['incident_summary']['reason']}",
    ]

    # Event analysis
    if report['event_analysis']['event_counts']:
        lines.append("\nEvent Counts:")
        for event_type, count in report['event_analysis']['event_counts'].items():
            lines.append(f"  • {event_type}: {count}")

    if report['event_analysis']['event_sequence']:
        sequence = ' → '.join(report['event_analysis']['event_sequence'])
        lines.append(f"\nAttack Sequence: {sequence}")

    # Replay analysis
    lines.append(f"\nReplay Success: {report['replay_analysis']['success']}")
    lines.append(f"Steps Executed: {len(report['replay_analysis']['steps_executed'])}")

    # Recommendations
    if report['recommendations']:
        lines.append("\n🎯 Recommendations:")
        for rec in report['recommendations']:
            lines.append(f"  • {rec}")

    lines.append("=" * 60 + "\n")

    return '\n'.join(lines)


def export_report_json(report: Dict[str, Any], filepath: str) -> None:
    """
    Export report to JSON file.

    Args:
        report: Threat report dictionary
        filepath: Output file path
    """
    with open(filepath, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"✓ Report exported to: {filepath}")
