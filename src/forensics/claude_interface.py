"""
Claude Interface — Get AI-powered threat analysis from Claude
"""

import os
from typing import Dict, Any
import json


def get_claude_summary(threat_report: Dict[str, Any]) -> str:
    """
    Get Claude AI analysis of the threat report.

    Falls back to offline summary if API key not available.

    Args:
        threat_report: Threat report dictionary

    Returns:
        Analysis summary string
    """
    api_key = os.getenv("CLAUDE_API_KEY")

    if not api_key:
        return _generate_offline_summary(threat_report)

    try:
        # Attempt to call Claude API
        return _call_claude_api(threat_report, api_key)
    except Exception as e:
        print(f"⚠️  Claude API call failed: {e}")
        return _generate_offline_summary(threat_report)


def _call_claude_api(threat_report: Dict[str, Any], api_key: str) -> str:
    """
    Call Claude API for threat analysis.

    Args:
        threat_report: Threat report dictionary
        api_key: Claude API key

    Returns:
        Claude's analysis
    """
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

        prompt = _build_analysis_prompt(threat_report)

        message = client.messages.create(
            model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929"),
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extract text from response
        analysis = message.content[0].text if message.content else "No analysis generated"

        return analysis

    except ImportError:
        print("⚠️  anthropic package not installed, using offline summary")
        return _generate_offline_summary(threat_report)
    except Exception as e:
        print(f"⚠️  Error calling Claude API: {e}")
        return _generate_offline_summary(threat_report)


def _build_analysis_prompt(threat_report: Dict[str, Any]) -> str:
    """
    Build prompt for Claude analysis.

    Args:
        threat_report: Threat report dictionary

    Returns:
        Prompt string
    """
    report_json = json.dumps(threat_report, indent=2)

    prompt = f"""You are a cybersecurity analyst for Zyberpol AEGIS, an autonomous defense system.

Analyze this security incident and provide:
1. Threat assessment (severity, likelihood of success)
2. Attack technique identification (MITRE ATT&CK if applicable)
3. Immediate next steps
4. Long-term security improvements

INCIDENT REPORT:
{report_json}

Provide a concise analysis (3-5 sentences max) focusing on actionable insights."""

    return prompt


def _generate_offline_summary(threat_report: Dict[str, Any]) -> str:
    """
    Generate offline threat summary without Claude API.

    Args:
        threat_report: Threat report dictionary

    Returns:
        Offline analysis summary
    """
    incident = threat_report.get("incident_summary", {})
    threat_type = incident.get("threat_type", "unknown")
    severity = incident.get("severity", "unknown")
    action = incident.get("action_taken", "none")

    summary_lines = [
        f"OFFLINE ANALYSIS (Claude API unavailable):",
        f"",
        f"Detected {threat_type} with {severity} severity.",
        f"Response action: {action}.",
    ]

    # Add threat-specific analysis
    if "exfil" in threat_type.lower():
        summary_lines.append(
            "Data exfiltration attempts require immediate investigation. "
            "Review all egress traffic and identify compromised data."
        )
    elif "exploit" in threat_type.lower():
        summary_lines.append(
            "Active exploitation detected. Patch vulnerable systems immediately "
            "and review all affected assets for indicators of compromise."
        )
    elif "credential" in threat_type.lower():
        summary_lines.append(
            "Credential attack detected. Enforce MFA, rotate passwords, "
            "and review authentication logs for successful breaches."
        )
    elif "scan" in threat_type.lower():
        summary_lines.append(
            "Reconnaissance activity suggests pre-attack preparation. "
            "Monitor for follow-up exploitation attempts."
        )

    # Add recommendations count
    rec_count = len(threat_report.get("recommendations", []))
    summary_lines.append(f"\n{rec_count} security recommendations generated.")

    return '\n'.join(summary_lines)
