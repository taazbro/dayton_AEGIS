"""
Claude Interface — Get AI-powered threat analysis from Claude
Optimized with caching, rate limiting, and severity gating
Monitored with Galileo AI Observability

SPONSOR INTEGRATIONS:
- Anthropic Claude API for threat analysis
- Galileo for AI observability and monitoring
"""

import os
from typing import Dict, Any
import json
import hashlib
import time
from functools import lru_cache
from collections import deque

# Galileo observability integration
try:
    from src.observability.galileo_integration import get_galileo_observability
    GALILEO_AVAILABLE = True
except ImportError:
    GALILEO_AVAILABLE = False


# === OPTIMIZATION: Rate Limiter ===
class ClaudeRateLimiter:
    """Rate limiter to reduce Claude API calls"""
    def __init__(self, max_calls_per_minute: int = 10):
        self.max_calls = max_calls_per_minute
        self.call_times = deque(maxlen=max_calls_per_minute)

    def can_call(self) -> bool:
        """Check if we can make another API call"""
        now = time.time()
        # Remove calls older than 60 seconds
        while self.call_times and now - self.call_times[0] > 60:
            self.call_times.popleft()

        return len(self.call_times) < self.max_calls

    def record_call(self):
        """Record that we made an API call"""
        self.call_times.append(time.time())


# === OPTIMIZATION: Response Cache ===
class ClaudeCache:
    """Simple TTL cache for Claude responses"""
    def __init__(self, ttl_seconds: int = 300):  # 5 minute cache
        self.cache = {}
        self.ttl = ttl_seconds

    def get_cache_key(self, threat_report: Dict[str, Any]) -> str:
        """Generate cache key from threat characteristics"""
        # Cache based on threat type + severity + attack pattern
        incident = threat_report.get("incident_summary", {})
        key_parts = [
            incident.get("threat_type", ""),
            incident.get("severity", ""),
            incident.get("attack_pattern", ""),
        ]
        key_string = "|".join(str(p) for p in key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()

    def get(self, cache_key: str) -> str | None:
        """Get cached response if still valid"""
        if cache_key in self.cache:
            response, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.ttl:
                return response
            else:
                del self.cache[cache_key]
        return None

    def set(self, cache_key: str, response: str):
        """Cache a response"""
        self.cache[cache_key] = (response, time.time())


# Global instances
_rate_limiter = ClaudeRateLimiter(max_calls_per_minute=10)
_cache = ClaudeCache(ttl_seconds=300)


def get_claude_summary(threat_report: Dict[str, Any]) -> str:
    """
    Get Claude AI (Anthropic Sponsor) analysis of the threat report.

    SPONSOR INTEGRATION - ANTHROPIC CLAUDE:
    - Smart severity-based AI usage (MEDIUM+)
    - 5-minute intelligent cache for similar threats
    - Rate-limited to 10 calls/minute
    - Graceful offline fallback for LOW severity

    Args:
        threat_report: Threat report dictionary

    Returns:
        Analysis summary string
    """
    api_key = os.getenv("CLAUDE_API_KEY")

    # === OPTIMIZATION 1: Check cache first ===
    cache_key = _cache.get_cache_key(threat_report)
    cached_response = _cache.get(cache_key)
    if cached_response:
        return f"[CACHED] {cached_response}"

    # === OPTIMIZATION 2: Severity gating - smart AI usage ===
    incident = threat_report.get("incident_summary", {})
    severity = incident.get("severity", "").upper()

    # Call Claude for MEDIUM or higher (demo-friendly while still optimized)
    # LOW severity uses offline analysis
    if severity not in ["MEDIUM", "HIGH", "CRITICAL"]:
        print("   🤖 Claude: Skipped (LOW severity - offline analysis used)")
        return _generate_offline_summary(threat_report)

    print(f"   🤖 Claude AI: Analyzing {severity} severity threat...")

    # === OPTIMIZATION 3: Rate limiting ===
    if not _rate_limiter.can_call():
        return f"[RATE LIMITED] {_generate_offline_summary(threat_report)}"

    if not api_key:
        return _generate_offline_summary(threat_report)

    try:
        # Record API call for rate limiting
        _rate_limiter.record_call()

        # Attempt to call Claude API
        analysis = _call_claude_api(threat_report, api_key)

        # Cache the response
        _cache.set(cache_key, analysis)

        print(f"   ✅ Claude AI: Analysis complete!")

        return analysis
    except Exception as e:
        print(f"   ⚠️  Claude API call failed: {e}")
        return _generate_offline_summary(threat_report)


def _call_claude_api(threat_report: Dict[str, Any], api_key: str) -> str:
    """
    Call Claude API for threat analysis with Galileo observability.

    SPONSOR INTEGRATIONS:
    - Anthropic Claude: AI threat analysis
    - Galileo: AI performance monitoring

    Args:
        threat_report: Threat report dictionary
        api_key: Claude API key

    Returns:
        Claude's analysis
    """
    start_time = time.time()

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

        prompt = _build_analysis_prompt(threat_report)
        model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")

        message = client.messages.create(
            model=model,
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

        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000

        # Log to Galileo observability
        if GALILEO_AVAILABLE:
            galileo = get_galileo_observability()
            galileo.log_prompt(
                prompt=prompt,
                response=analysis,
                model=model,
                latency_ms=latency_ms,
                metadata={
                    "threat_type": threat_report.get("incident_summary", {}).get("threat_type"),
                    "severity": threat_report.get("incident_summary", {}).get("severity"),
                    "sponsor": "anthropic"
                }
            )

        return analysis

    except ImportError:
        print("   ⚠️  anthropic package not installed, using offline summary")
        if GALILEO_AVAILABLE:
            galileo = get_galileo_observability()
            galileo.log_error("Anthropic package not installed", {"threat_report": threat_report})
        return _generate_offline_summary(threat_report)
    except Exception as e:
        print(f"   ⚠️  Error calling Claude API: {e}")
        if GALILEO_AVAILABLE:
            galileo = get_galileo_observability()
            galileo.log_error(str(e), {"threat_report": threat_report})
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
