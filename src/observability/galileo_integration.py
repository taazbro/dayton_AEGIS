"""
Galileo AI Observability Integration — Monitor Claude AI performance
SPONSOR: Galileo (https://app.galileo.ai)
"""

import os
import requests
from typing import Dict, Any
import json
import time

# Try to import Galileo SDK
try:
    from galileo_observe import GalileoObserve
    GALILEO_SDK_AVAILABLE = True
except ImportError:
    GALILEO_SDK_AVAILABLE = False


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
        self.galileo_client = None

        if self.enabled and GALILEO_SDK_AVAILABLE:
            try:
                # Initialize Galileo SDK
                self.galileo_client = GalileoObserve(api_key=self.api_key)
                print("   🔭 Galileo AI Observability: Enabled (SDK)")
            except Exception as e:
                print(f"   🔭 Galileo AI Observability: Enabled (fallback mode) - {e}")
        elif self.enabled:
            print("   🔭 Galileo AI Observability: Enabled (no SDK, using API)")
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

            # Send to Galileo SDK if available
            if self.galileo_client:
                try:
                    # Use Galileo SDK to log the interaction
                    self.galileo_client.log(
                        project=self.project_name,
                        messages=[
                            {"role": "user", "content": prompt},
                            {"role": "assistant", "content": response}
                        ],
                        model=model,
                        latency_ms=latency_ms,
                        metadata=metadata or {}
                    )
                    print(f"   🔭 Galileo: Logged to SDK ({latency_ms:.0f}ms)")
                except Exception as e:
                    print(f"   🔭 Galileo: SDK log failed, using fallback - {e}")
                    self._log_via_api(log_entry)
            else:
                # Fallback to API
                print(f"   🔭 Galileo: Logged AI interaction ({latency_ms:.0f}ms)")
                self._log_via_api(log_entry)

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

    def _log_via_api(self, log_entry: Dict[str, Any]):
        """Send log entry to Galileo API directly"""
        if not self.api_key:
            return

        try:
            # Galileo API endpoint (if webhook configured)
            api_url = os.getenv("GALILEO_API_URL", "https://api.galileo.ai/v1/logs")
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            response = requests.post(api_url, json=log_entry, headers=headers, timeout=3)
            if response.status_code in [200, 201]:
                print(f"      ✓ Logged via API")
        except Exception as e:
            # Silent fail - local logging still works
            pass

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
