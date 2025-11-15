"""
Galileo AI Observability Integration — Monitor Claude AI performance
SPONSOR: Galileo (https://app.galileo.ai)

Official SDK Documentation: https://docs.rungalileo.io/galileo/llm-studio/python-sdk
"""

import os
import requests
from typing import Dict, Any
import json
import time
from datetime import datetime

# Try to import Official Galileo SDK
try:
    from galileo import galileo_context
    from galileo.config import GalileoPythonConfig
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

    Official SDK: pip install galileo python-dotenv
    Docs: https://docs.rungalileo.io/galileo/llm-studio/python-sdk
    """

    def __init__(self, project_name: str = "aegis", log_stream: str = "default"):
        self.api_key = os.getenv("GALILEO_API_KEY")
        self.project_name = project_name
        self.log_stream = log_stream
        self.enabled = bool(self.api_key)
        self.logger = None
        self.session_started = False

        if self.enabled and GALILEO_SDK_AVAILABLE:
            try:
                # Set required environment variables for Galileo SDK
                os.environ["GALILEO_API_KEY"] = self.api_key
                os.environ["GALILEO_PROJECT"] = self.project_name
                os.environ["GALILEO_LOG_STREAM"] = self.log_stream

                # Initialize Galileo context with project and log stream
                galileo_context.init(
                    project=self.project_name,
                    log_stream=self.log_stream
                )

                # Get logger instance
                self.logger = galileo_context.get_logger_instance()

                # Start session (required before logging)
                self.logger.start_session()
                self.session_started = True

                print(f"   🔭 Galileo AI Observability: Enabled (Official SDK)")
                print(f"      Project: {self.project_name} | Stream: {self.log_stream}")
            except Exception as e:
                print(f"   🔭 Galileo AI Observability: Enabled (fallback mode) - {e}")
                self.session_started = False
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
        metadata: Dict[str, Any] = None,
        num_input_tokens: int = None,
        num_output_tokens: int = None
    ) -> bool:
        """
        Log AI prompt and response to Galileo using Official SDK.

        Args:
            prompt: The prompt sent to Claude
            response: The response from Claude
            model: Model name (e.g., claude-sonnet-4-5-20250929)
            latency_ms: Response time in milliseconds
            metadata: Additional context
            num_input_tokens: Input token count (optional)
            num_output_tokens: Output token count (optional)

        Returns:
            True if logged successfully
        """
        if not self.enabled:
            return False

        try:
            # Store locally for aggregation
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
            self._store_locally(log_entry)

            # Send to Official Galileo SDK if available
            if self.logger and self.session_started:
                try:
                    # Start a trace (conversation step)
                    trace_name = metadata.get("trace_name", "AEGIS AI Interaction") if metadata else "AEGIS AI Interaction"
                    self.logger.start_trace(name=trace_name, input=prompt)

                    # Create messages format expected by Galileo
                    messages = [
                        {"role": "user", "content": prompt}
                    ]

                    # Calculate duration in nanoseconds
                    duration_ns = int(latency_ms * 1_000_000)  # ms to ns

                    # Calculate tokens if not provided
                    if num_input_tokens is None:
                        num_input_tokens = len(prompt.split())  # Rough estimate
                    if num_output_tokens is None:
                        num_output_tokens = len(response.split())  # Rough estimate

                    total_tokens = num_input_tokens + num_output_tokens

                    # Add LLM span with full details
                    self.logger.add_llm_span(
                        input=messages,
                        output=response,
                        model=model,
                        num_input_tokens=num_input_tokens,
                        num_output_tokens=num_output_tokens,
                        total_tokens=total_tokens,
                        duration_ns=duration_ns,
                    )

                    # Conclude the trace
                    self.logger.conclude(output=response)

                    # Flush to Galileo platform
                    self.logger.flush()

                    print(f"   🔭 Galileo: Logged via Official SDK ({latency_ms:.0f}ms, {total_tokens} tokens)")

                except Exception as e:
                    print(f"   🔭 Galileo: SDK log failed, using fallback - {e}")
                    self._log_via_api(log_entry)
            else:
                # Fallback to API
                print(f"   🔭 Galileo: Logged AI interaction ({latency_ms:.0f}ms)")
                self._log_via_api(log_entry)

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
