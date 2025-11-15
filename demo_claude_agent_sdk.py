"""
DEMO: Claude Agent SDK - Advanced Multi-Step Threat Analysis
Showcases autonomous reasoning, multi-step investigation, and tool calling

Run this demo to see the Claude Agent SDK in action!
"""

import os
import sys
from typing import Dict, Any

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.forensics.claude_agent_sdk import get_claude_agent
from src.forensics.threat_report import generate_threat_report
from src.observability.galileo_integration import get_galileo_observability


def create_demo_incident(threat_type: str, severity: str) -> Dict[str, Any]:
    """Create a demo incident for testing"""
    return {
        "threat_type": threat_type,
        "severity": severity,
        "event_count": 42,
        "affected_entities": ["192.168.1.100", "web-server-01", "database-prod"],
        "attack_pattern": "multi_stage_attack",
        "action": "quarantine",
        "event_sequence": ["recon", "scan", "exploit", "exfil"],
        "detection_engines": ["pattern", "signature", "anomaly"],
        "events": [
            {"type": "scan", "timestamp": "2025-01-15 10:00:00"},
            {"type": "exploit", "timestamp": "2025-01-15 10:05:00"},
            {"type": "exfil", "timestamp": "2025-01-15 10:10:00"},
        ]
    }


def run_basic_demo():
    """Run a basic demo of the Claude Agent SDK"""
    print("="*80)
    print("🤖 CLAUDE AGENT SDK DEMO - Basic Multi-Step Analysis")
    print("="*80)
    print("\nThis demo shows how Claude Agent SDK performs autonomous")
    print("multi-step threat analysis with reasoning chains.\n")

    # Create demo incident
    incident = create_demo_incident("SQL Injection Attempt", "HIGH")

    print("📋 DEMO INCIDENT:")
    print(f"   Threat Type: {incident['threat_type']}")
    print(f"   Severity: {incident['severity']}")
    print(f"   Affected Systems: {', '.join(incident['affected_entities'][:2])}")
    print(f"   Attack Sequence: {' → '.join(incident['event_sequence'])}")

    # Generate threat report
    print("\n🔍 Generating threat report with MITRE tags...")
    from src.browseruse_agent.replay_attack import replay_attack
    replay_artifacts = replay_attack(incident)
    threat_report = generate_threat_report(incident, replay_artifacts)

    # Run Claude Agent SDK analysis
    print("\n🚀 Initiating Claude Agent SDK Autonomous Analysis...")
    print("-"*80)

    agent = get_claude_agent()
    analysis = agent.analyze_threat_autonomous(threat_report)

    # Display results
    print("\n" + "="*80)
    print("🤖 CLAUDE AGENT SDK - ANALYSIS RESULTS")
    print("="*80)

    print(f"\n📊 ANALYSIS METADATA:")
    print(f"   Type: {analysis['analysis_type']}")
    print(f"   Sponsor: {analysis['sponsor']}")
    print(f"   Steps Completed: {analysis['steps_completed']}")
    print(f"   Confidence: {analysis['confidence']}")

    print(f"\n🧠 REASONING CHAIN:")
    for i, step in enumerate(analysis.get('reasoning_chain', []), 1):
        print(f"   {i}. {step}")

    print(f"\n📝 DETAILED FINDINGS:")

    findings = analysis.get('findings', {})

    # Initial Assessment
    if 'initial_assessment' in findings:
        assess = findings['initial_assessment']
        print(f"\n   STEP 1: Initial Threat Assessment")
        print(f"   {'─'*70}")
        print(f"   Severity: {assess.get('severity')}")
        print(f"   Risk Level: {assess.get('risk_level')}")
        print(f"   Assessment: {assess.get('assessment')}")

    # Attack Patterns
    if 'attack_patterns' in findings:
        patterns = findings['attack_patterns']
        print(f"\n   STEP 2: Attack Pattern Investigation")
        print(f"   {'─'*70}")
        print(f"   Sophistication: {patterns.get('sophistication')}")
        print(f"   Analysis: {patterns.get('analysis')}")
        print(f"   Techniques Found: {len(patterns.get('attack_techniques', []))}")

    # Recommendations
    if 'recommendations' in findings:
        recs = findings['recommendations']
        print(f"\n   STEP 3: Actionable Recommendations")
        print(f"   {'─'*70}")
        for action in recs.get('actions', []):
            print(f"   • {action}")

    print(f"\n💡 SUMMARY:")
    print(f"   {'-'*70}")
    summary_lines = analysis.get('summary', '').split('\n')
    for line in summary_lines:
        if line.strip():
            print(f"   {line}")

    print("\n" + "="*80)
    print("✅ Demo Complete!")
    print("="*80)


def run_comparison_demo():
    """Run a comparison demo showing basic vs advanced analysis"""
    print("="*80)
    print("🔬 CLAUDE AGENT SDK DEMO - Basic vs Advanced Comparison")
    print("="*80)
    print("\nThis demo compares basic Claude analysis with advanced")
    print("Claude Agent SDK multi-step autonomous reasoning.\n")

    # Create demo incident
    incident = create_demo_incident("Advanced Persistent Threat (APT)", "CRITICAL")

    print("📋 DEMO INCIDENT:")
    print(f"   Threat Type: {incident['threat_type']}")
    print(f"   Severity: {incident['severity']}")
    print(f"   Attack Sophistication: CRITICAL")

    # Generate threat report
    from src.browseruse_agent.replay_attack import replay_attack
    replay_artifacts = replay_attack(incident)
    threat_report = generate_threat_report(incident, replay_artifacts)

    # Basic Analysis
    print("\n" + "="*80)
    print("📊 BASIC CLAUDE ANALYSIS")
    print("="*80)

    from src.forensics.claude_interface import get_claude_summary
    basic_summary = get_claude_summary(threat_report)
    print(basic_summary)

    # Advanced Analysis
    print("\n" + "="*80)
    print("🤖 ADVANCED CLAUDE AGENT SDK ANALYSIS")
    print("="*80)

    agent = get_claude_agent()
    advanced_analysis = agent.analyze_threat_autonomous(threat_report)

    print(f"\nAnalysis Type: {advanced_analysis['analysis_type']}")
    print(f"Steps: {advanced_analysis['steps_completed']}")
    print(f"Confidence: {advanced_analysis['confidence']}")

    print(f"\n🧠 Reasoning Chain:")
    for i, step in enumerate(advanced_analysis.get('reasoning_chain', []), 1):
        print(f"   {i}. {step}")

    print(f"\n💡 Advanced Summary:")
    print(advanced_analysis.get('summary', 'N/A'))

    print("\n" + "="*80)
    print("🎯 KEY DIFFERENCES:")
    print("="*80)
    print("   Basic Analysis:")
    print("   • Single-step reasoning")
    print("   • General recommendations")
    print("   • Faster but less detailed")
    print()
    print("   Advanced SDK Analysis:")
    print("   • Multi-step autonomous reasoning (4 steps)")
    print("   • Investigates attack patterns")
    print("   • Context-aware recommendations")
    print("   • Self-validating and synthesizing")
    print("   • Shows reasoning chain (explainable AI)")
    print("="*80)


def run_interactive_demo():
    """Run an interactive demo allowing custom input"""
    print("="*80)
    print("🎮 CLAUDE AGENT SDK DEMO - Interactive Mode")
    print("="*80)
    print("\nCreate your own threat scenario!\n")

    # Get user input
    print("Select threat type:")
    print("1. SQL Injection")
    print("2. Ransomware Attack")
    print("3. Data Exfiltration")
    print("4. Advanced Persistent Threat (APT)")
    print("5. DDoS Attack")

    choice = input("\nEnter choice (1-5): ").strip()

    threat_types = {
        "1": "SQL Injection Attempt",
        "2": "Ransomware Attack",
        "3": "Data Exfiltration",
        "4": "Advanced Persistent Threat (APT)",
        "5": "Distributed Denial of Service (DDoS)"
    }

    threat_type = threat_types.get(choice, "Unknown Threat")

    print("\nSelect severity:")
    print("1. LOW")
    print("2. MEDIUM")
    print("3. HIGH")
    print("4. CRITICAL")

    sev_choice = input("\nEnter choice (1-4): ").strip()

    severities = {"1": "LOW", "2": "MEDIUM", "3": "HIGH", "4": "CRITICAL"}
    severity = severities.get(sev_choice, "MEDIUM")

    # Create and analyze
    incident = create_demo_incident(threat_type, severity)

    print(f"\n📋 Created Incident:")
    print(f"   Type: {threat_type}")
    print(f"   Severity: {severity}")

    from src.browseruse_agent.replay_attack import replay_attack
    replay_artifacts = replay_attack(incident)
    threat_report = generate_threat_report(incident, replay_artifacts)

    print("\n🤖 Running Claude Agent SDK Analysis...\n")

    agent = get_claude_agent()
    analysis = agent.analyze_threat_autonomous(threat_report)

    # Display
    print("="*80)
    print("🤖 ANALYSIS RESULTS")
    print("="*80)
    print(f"\nConfidence: {analysis['confidence']}")
    print(f"\n💡 Summary:\n{analysis.get('summary', 'N/A')}")
    print("="*80)


def main():
    """Main demo entry point"""
    print("\n" + "="*80)
    print("🚀 CLAUDE AGENT SDK DEMONSTRATION")
    print("   Autonomous Multi-Step Threat Analysis")
    print("="*80)

    print("\nSelect demo mode:")
    print("1. Basic Demo - See multi-step analysis in action")
    print("2. Comparison Demo - Basic vs Advanced analysis")
    print("3. Interactive Demo - Create your own scenario")
    print("4. Run All Demos")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        run_basic_demo()
    elif choice == "2":
        run_comparison_demo()
    elif choice == "3":
        run_interactive_demo()
    elif choice == "4":
        print("\n🎬 Running all demos...\n")
        run_basic_demo()
        print("\n" + "="*80 + "\n")
        run_comparison_demo()
    else:
        print("Invalid choice. Running basic demo...")
        run_basic_demo()

    # Show Galileo summary if available
    try:
        galileo = get_galileo_observability()
        galileo.print_summary()
    except Exception:
        pass

    print("\n✨ Thank you for watching the Claude Agent SDK demo!")
    print("   For hackathon judges: This showcases advanced Anthropic integration\n")


if __name__ == "__main__":
    main()
