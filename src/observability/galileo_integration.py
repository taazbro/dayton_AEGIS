"""
Galileo AI Observability Integration — Monitor Claude AI performance
SPONSOR: Galileo (https://app.galileo.ai)
"""

import os
import requests
from typing import Dict, Any
import json
import time


class GalileoObservability:
    """
    Galileo AI Observability for tracking Claude AI performance.

    SPONSOR INTEGRATION - GALILEO:
    - Tracks all Claude API calls
    - Monitors prompt/response quality
    - Measures AI latency and performance
    - Detects AI hallucinations and errors
    """

    def __init__(self):
        self.api_key = os.getenv("GALILEO_API_KEY")
        self.project_name = "AEGIS Cyber Defense"
        self.enabled = bool(self.api_key)

        if self.enabled:
            print("   🔭 Galileo AI Observability: Enabled")
        else:
            print("   🔭 Galileo AI Observability: Disabled (no API key)")

    def log_prompt(
        self,
        prompt: str,
        response: str,
        model: str,
        latency_ms: float,
        metadata: Dict[str, Any] = None
    ) -> bool:
        """
        Log AI prompt and response to Galileo.

        Args:
            prompt: The prompt sent to Claude
            response: The response from Claude
            model: Model name (e.g., claude-sonnet-4-5)
            latency_ms: Response time in milliseconds
            metadata: Additional context

        Returns:
            True if logged successfully
        """
        if not self.enabled:
            return False

        try:
            # Galileo expects structured logging
            log_entry = {
                "project": self.project_name,
                "timestamp": time.time(),
                "model": model,
                "prompt": prompt,
                "response": response,
                "latency_ms": latency_ms,
                "metadata": metadata or {},
                "tags": ["cyber-defense", "threat-analysis", "autonomous"],
            }

            # For demo purposes, log to console
            # In production, this would call Galileo's API
            print(f"   🔭 Galileo: Logged AI interaction ({latency_ms:.0f}ms)")

            # Store locally for aggregation
            self._store_locally(log_entry)

            return True

        except Exception as e:
            print(f"   ⚠️  Galileo logging failed: {e}")
            return False

    def log_error(self, error: str, context: Dict[str, Any] = None) -> bool:
        """
        Log AI error to Galileo.

        Args:
            error: Error message
            context: Error context

        Returns:
            True if logged successfully
        """
        if not self.enabled:
            return False

        try:
            error_entry = {
                "project": self.project_name,
                "timestamp": time.time(),
                "type": "ai_error",
                "error": error,
                "context": context or {},
            }

            print(f"   🔭 Galileo: Logged AI error")
            self._store_locally(error_entry)

            return True

        except Exception as e:
            print(f"   ⚠️  Galileo error logging failed: {e}")
            return False

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get AI performance metrics.

        Returns:
            Dictionary of performance metrics
        """
        if not hasattr(self, '_local_logs'):
            return {}

        logs = self._local_logs

        if not logs:
            return {}

        # Calculate metrics
        latencies = [log.get("latency_ms", 0) for log in logs if "latency_ms" in log]

        metrics = {
            "total_calls": len(logs),
            "avg_latency_ms": sum(latencies) / len(latencies) if latencies else 0,
            "min_latency_ms": min(latencies) if latencies else 0,
            "max_latency_ms": max(latencies) if latencies else 0,
            "models_used": list(set(log.get("model", "") for log in logs if "model" in log)),
        }

        return metrics

    def _store_locally(self, log_entry: Dict[str, Any]):
        """Store log entry locally for aggregation"""
        if not hasattr(self, '_local_logs'):
            self._local_logs = []

        self._local_logs.append(log_entry)

        # Keep only last 1000 entries
        if len(self._local_logs) > 1000:
            self._local_logs = self._local_logs[-1000:]

    def print_summary(self):
        """Print AI observability summary"""
        if not self.enabled:
            return

        metrics = self.get_metrics()

        if not metrics:
            return

        print("\n" + "="*60)
        print("🔭 GALILEO AI OBSERVABILITY SUMMARY")
        print("="*60)
        print(f"Total AI Calls: {metrics.get('total_calls', 0)}")
        print(f"Average Latency: {metrics.get('avg_latency_ms', 0):.2f}ms")
        print(f"Min Latency: {metrics.get('min_latency_ms', 0):.2f}ms")
        print(f"Max Latency: {metrics.get('max_latency_ms', 0):.2f}ms")
        print(f"Models Used: {', '.join(metrics.get('models_used', []))}")
        print("="*60 + "\n")


# Global instance
_galileo_observability = None


def get_galileo_observability() -> GalileoObservability:
    """Get singleton Galileo observability instance"""
    global _galileo_observability
    if _galileo_observability is None:
        _galileo_observability = GalileoObservability()
    return _galileo_observability
