"""
Prometheus Metrics Exporter — Export AEGIS metrics for Prometheus scraping
"""

import os
from typing import Dict, Any
from collections import defaultdict
import time
from threading import Lock


class PrometheusExporter:
    """Export metrics in Prometheus format"""

    def __init__(self):
        self.metrics = defaultdict(int)
        self.gauges = {}
        self.histograms = defaultdict(list)
        self.lock = Lock()

        # Initialize counters
        self.metrics["aegis_threats_total"] = 0
        self.metrics["aegis_critical_threats_total"] = 0
        self.metrics["aegis_high_threats_total"] = 0
        self.metrics["aegis_medium_threats_total"] = 0
        self.metrics["aegis_low_threats_total"] = 0

    def record_threat(self, threat_report: Dict[str, Any]):
        """
        Record a threat detection event.

        Args:
            threat_report: Threat report dictionary
        """
        with self.lock:
            incident = threat_report.get("incident_summary", {})
            severity = incident.get("severity", "UNKNOWN").upper()
            threat_type = incident.get("threat_type", "unknown")

            # Increment total threats counter
            self.metrics["aegis_threats_total"] += 1

            # Increment severity-specific counters
            severity_key = f"aegis_{severity.lower()}_threats_total"
            self.metrics[severity_key] += 1

            # Increment threat-type counters
            threat_type_key = f"aegis_threat_type_{threat_type.replace(' ', '_').lower()}_total"
            self.metrics[threat_type_key] += 1

            # Record detection engine usage
            for engine in threat_report.get("detection_engines", []):
                engine_key = f"aegis_detection_engine_{engine.replace(' ', '_').lower()}_total"
                self.metrics[engine_key] += 1

            # Update gauge for current threat level
            self.gauges["aegis_current_threat_level"] = self._severity_to_level(severity)

    def record_response_action(self, action_type: str):
        """
        Record a response action.

        Args:
            action_type: Type of response action taken
        """
        with self.lock:
            action_key = f"aegis_response_action_{action_type.replace(' ', '_').lower()}_total"
            self.metrics[action_key] += 1

    def record_detection_latency(self, latency_ms: float):
        """
        Record detection latency.

        Args:
            latency_ms: Latency in milliseconds
        """
        with self.lock:
            self.histograms["aegis_detection_latency_ms"].append(latency_ms)

    def export_metrics(self) -> str:
        """
        Export metrics in Prometheus format.

        Returns:
            Prometheus-formatted metrics string
        """
        with self.lock:
            lines = []

            # Add metadata
            lines.append("# HELP aegis_threats_total Total number of threats detected")
            lines.append("# TYPE aegis_threats_total counter")

            # Export counters
            for metric_name, value in sorted(self.metrics.items()):
                lines.append(f"{metric_name} {value}")

            # Export gauges
            for gauge_name, value in sorted(self.gauges.items()):
                lines.append(f"# HELP {gauge_name} Current threat level")
                lines.append(f"# TYPE {gauge_name} gauge")
                lines.append(f"{gauge_name} {value}")

            # Export histograms (as summaries)
            for hist_name, values in sorted(self.histograms.items()):
                if values:
                    lines.append(f"# HELP {hist_name} Detection latency histogram")
                    lines.append(f"# TYPE {hist_name} summary")
                    lines.append(f"{hist_name}_sum {sum(values)}")
                    lines.append(f"{hist_name}_count {len(values)}")

                    # Calculate quantiles
                    sorted_values = sorted(values)
                    quantiles = [0.5, 0.9, 0.95, 0.99]
                    for q in quantiles:
                        idx = int(len(sorted_values) * q)
                        if idx < len(sorted_values):
                            lines.append(f'{hist_name}{{quantile="{q}"}} {sorted_values[idx]}')

            return "\n".join(lines) + "\n"

    def get_metrics_dict(self) -> Dict[str, Any]:
        """
        Get metrics as a dictionary.

        Returns:
            Dictionary of all metrics
        """
        with self.lock:
            return {
                "counters": dict(self.metrics),
                "gauges": dict(self.gauges),
                "histograms": {k: len(v) for k, v in self.histograms.items()}
            }

    def _severity_to_level(self, severity: str) -> int:
        """Convert severity to numeric level"""
        levels = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1,
            "UNKNOWN": 0
        }
        return levels.get(severity, 0)

    def start_http_server(self, port: int = 9090):
        """
        Start HTTP server to expose metrics.

        Args:
            port: Port to listen on
        """
        from http.server import HTTPServer, BaseHTTPRequestHandler

        exporter = self

        class MetricsHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/metrics':
                    metrics_output = exporter.export_metrics()
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/plain; version=0.0.4')
                    self.end_headers()
                    self.wfile.write(metrics_output.encode('utf-8'))
                elif self.path == '/health':
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "healthy"}')
                else:
                    self.send_response(404)
                    self.end_headers()

            def log_message(self, format, *args):
                # Suppress default logging
                pass

        server = HTTPServer(('0.0.0.0', port), MetricsHandler)
        print(f"✅ Prometheus exporter started on port {port}")
        print(f"   Metrics available at http://localhost:{port}/metrics")

        import threading
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()


# Global instance
_prometheus_exporter = None


def get_prometheus_exporter() -> PrometheusExporter:
    """Get singleton Prometheus exporter instance"""
    global _prometheus_exporter
    if _prometheus_exporter is None:
        _prometheus_exporter = PrometheusExporter()
    return _prometheus_exporter
