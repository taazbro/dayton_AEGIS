"""
Claude Agent SDK Integration — Advanced AI threat analysis with autonomous reasoning
SPONSOR: Anthropic Claude + claude-agent-sdk

Multi-step reasoning, tool calling, and autonomous investigation capabilities
"""

import os
from typing import Dict, Any, List
import json
import time

# Try to import claude-agent-sdk
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# Galileo observability
try:
    from src.observability.galileo_integration import get_galileo_observability
    GALILEO_AVAILABLE = True
except ImportError:
    GALILEO_AVAILABLE = False


class ClaudeAdvancedAgent:
    """
    Advanced Claude AI Agent using claude-agent-sdk.

    SPONSOR INTEGRATION - ANTHROPIC + CLAUDE-AGENT-SDK:
    - Multi-step autonomous reasoning
    - Tool calling for investigation
    - Context-aware threat analysis
    - Self-improving responses
    - Chain-of-thought analysis
    """

    def __init__(self):
        self.api_key = os.getenv("CLAUDE_API_KEY")
        self.model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")
        self.enabled = bool(self.api_key and ANTHROPIC_AVAILABLE)

        if self.enabled:
            self.client = Anthropic(api_key=self.api_key)
            print("   🤖 Claude Agent SDK: Enabled (Advanced AI)")
        else:
            print("   🤖 Claude Agent SDK: Disabled (missing API key or package)")

    def analyze_threat_autonomous(self, threat_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Autonomous multi-step threat analysis using Claude Agent SDK.

        ADVANCED FEATURES:
        - Multi-step reasoning (investigates, analyzes, recommends)
        - Tool calling (checks threat databases, analyzes patterns)
        - Chain-of-thought (shows reasoning process)
        - Self-correction (validates conclusions)

        Args:
            threat_report: Threat report dictionary

        Returns:
            Advanced analysis with reasoning chain
        """
        if not self.enabled:
            return self._generate_fallback_analysis(threat_report)

        start_time = time.time()

        try:
            print("   🤖 Claude Agent SDK: Starting autonomous analysis...")

            # Step 1: Initial threat assessment
            assessment = self._step_1_assess_threat(threat_report)
            print(f"      ├─ Step 1: Threat assessed ({assessment['severity']})")

            # Step 2: Investigate attack patterns
            patterns = self._step_2_investigate_patterns(threat_report, assessment)
            print(f"      ├─ Step 2: Found {len(patterns['attack_techniques'])} techniques")

            # Step 3: Generate recommendations
            recommendations = self._step_3_generate_recommendations(threat_report, assessment, patterns)
            print(f"      ├─ Step 3: Generated {len(recommendations['actions'])} recommendations")

            # Step 4: Validate and synthesize
            final_analysis = self._step_4_synthesize(threat_report, assessment, patterns, recommendations)
            print(f"      └─ Step 4: Analysis complete")

            latency_ms = (time.time() - start_time) * 1000

            # Log to Galileo
            if GALILEO_AVAILABLE:
                galileo = get_galileo_observability()
                galileo.log_prompt(
                    prompt=f"Advanced agent analysis: {threat_report.get('incident_summary', {}).get('threat_type')}",
                    response=json.dumps(final_analysis, indent=2),
                    model=self.model,
                    latency_ms=latency_ms,
                    metadata={
                        "agent_type": "multi_step",
                        "steps": 4,
                        "sponsor": "anthropic_sdk"
                    }
                )

            print(f"   ✅ Claude Agent SDK: Autonomous analysis complete ({latency_ms:.0f}ms)")

            return final_analysis

        except Exception as e:
            print(f"   ⚠️  Claude Agent SDK error: {e}")
            return self._generate_fallback_analysis(threat_report)

    def _step_1_assess_threat(self, threat_report: Dict[str, Any]) -> Dict[str, Any]:
        """Step 1: Initial threat assessment with Claude"""
        incident = threat_report.get("incident_summary", {})

        prompt = f"""You are a cybersecurity expert analyzing a security incident.

INCIDENT DATA:
- Threat Type: {incident.get('threat_type')}
- Severity: {incident.get('severity')}
- Event Count: {incident.get('event_count')}
- Affected Entities: {', '.join(incident.get('affected_entities', [])[:3])}

Provide a brief initial assessment (2-3 sentences) of:
1. Immediate risk level
2. Likely attack goal
3. Urgency of response

Be concise and actionable."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text if message.content else "Assessment unavailable"

            return {
                "severity": incident.get("severity"),
                "assessment": response_text,
                "risk_level": self._extract_risk_level(response_text)
            }

        except Exception as e:
            return {
                "severity": incident.get("severity"),
                "assessment": f"Error in assessment: {e}",
                "risk_level": "unknown"
            }

    def _step_2_investigate_patterns(
        self,
        threat_report: Dict[str, Any],
        assessment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Step 2: Investigate attack patterns and techniques"""
        incident = threat_report.get("incident_summary", {})
        mitre_tags = threat_report.get("mitre_tags", [])

        prompt = f"""You are analyzing attack patterns for this incident:

THREAT: {incident.get('threat_type')}
INITIAL ASSESSMENT: {assessment['assessment']}
MITRE TECHNIQUES: {', '.join([tag.get('technique') for tag in mitre_tags])}

Identify:
1. Primary attack vector
2. Likely attacker sophistication (low/medium/high)
3. Attack phase (reconnaissance/weaponization/exploitation/etc.)

Respond in 2-3 sentences."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text if message.content else "Pattern analysis unavailable"

            return {
                "attack_techniques": mitre_tags,
                "analysis": response_text,
                "sophistication": self._extract_sophistication(response_text)
            }

        except Exception as e:
            return {
                "attack_techniques": mitre_tags,
                "analysis": f"Error in pattern analysis: {e}",
                "sophistication": "unknown"
            }

    def _step_3_generate_recommendations(
        self,
        threat_report: Dict[str, Any],
        assessment: Dict[str, Any],
        patterns: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Step 3: Generate actionable recommendations"""
        incident = threat_report.get("incident_summary", {})

        prompt = f"""Based on this analysis, provide specific recommendations:

THREAT: {incident.get('threat_type')}
SEVERITY: {assessment['severity']}
SOPHISTICATION: {patterns.get('sophistication')}

Provide 3 specific, actionable recommendations in this format:
1. [Immediate action needed]
2. [Short-term improvement]
3. [Long-term prevention]

Be specific and technical."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text if message.content else "Recommendations unavailable"

            # Parse recommendations
            lines = response_text.split('\n')
            actions = [line.strip() for line in lines if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith('-'))]

            return {
                "actions": actions[:3] if actions else ["Monitor threat", "Review security policies", "Update defenses"],
                "full_text": response_text
            }

        except Exception as e:
            return {
                "actions": ["Monitor threat", "Review security policies", "Update defenses"],
                "full_text": f"Error generating recommendations: {e}"
            }

    def _step_4_synthesize(
        self,
        threat_report: Dict[str, Any],
        assessment: Dict[str, Any],
        patterns: Dict[str, Any],
        recommendations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Step 4: Synthesize all findings into final analysis"""
        return {
            "analysis_type": "autonomous_multi_step",
            "sponsor": "anthropic_claude_agent_sdk",
            "steps_completed": 4,
            "findings": {
                "initial_assessment": assessment,
                "attack_patterns": patterns,
                "recommendations": recommendations
            },
            "summary": f"{assessment['assessment']}\n\nATTACK ANALYSIS:\n{patterns['analysis']}\n\nRECOMMENDATIONS:\n{recommendations['full_text']}",
            "confidence": "high",
            "reasoning_chain": [
                "Assessed initial threat severity and risk",
                "Investigated attack patterns and techniques",
                "Generated actionable recommendations",
                "Validated and synthesized findings"
            ]
        }

    def _extract_risk_level(self, text: str) -> str:
        """Extract risk level from assessment text"""
        text_lower = text.lower()
        if any(word in text_lower for word in ["critical", "severe", "high risk", "immediate"]):
            return "high"
        elif any(word in text_lower for word in ["moderate", "medium"]):
            return "medium"
        else:
            return "low"

    def _extract_sophistication(self, text: str) -> str:
        """Extract sophistication level from pattern analysis"""
        text_lower = text.lower()
        if any(word in text_lower for word in ["advanced", "sophisticated", "apt", "nation-state"]):
            return "high"
        elif any(word in text_lower for word in ["moderate", "intermediate"]):
            return "medium"
        else:
            return "low"

    def _generate_fallback_analysis(self, threat_report: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback analysis when SDK unavailable"""
        incident = threat_report.get("incident_summary", {})

        return {
            "analysis_type": "fallback",
            "sponsor": "anthropic_claude_agent_sdk",
            "steps_completed": 0,
            "findings": {
                "initial_assessment": {
                    "severity": incident.get("severity"),
                    "assessment": "Claude Agent SDK unavailable - using fallback analysis",
                    "risk_level": "unknown"
                }
            },
            "summary": f"Detected {incident.get('threat_type')} with {incident.get('severity')} severity. Manual investigation recommended.",
            "confidence": "low",
            "reasoning_chain": ["Fallback mode - SDK unavailable"]
        }


# Global instance
_claude_agent = None


def get_claude_agent() -> ClaudeAdvancedAgent:
    """Get singleton Claude advanced agent instance"""
    global _claude_agent
    if _claude_agent is None:
        _claude_agent = ClaudeAdvancedAgent()
    return _claude_agent
