"""
Latency Tracker — Performance and latency measurement for AEGIS
"""

import time
from typing import Dict, List, Any, Optional
from collections import defaultdict
import statistics


class LatencyTracker:
    """Tracks latency and performance metrics for AEGIS components."""

    def __init__(self):
        """Initialize latency tracker."""
        self.measurements: Dict[str, List[float]] = defaultdict(list)
        self.max_samples = 1000  # Keep last 1000 samples per metric

    def start_measurement(self, operation: str) -> float:
        """
        Start measuring an operation.

        Args:
            operation: Name of operation being measured

        Returns:
            Start timestamp
        """
        return time.time()

    def end_measurement(self, operation: str, start_time: float) -> float:
        """
        End measurement and record latency.

        Args:
            operation: Name of operation
            start_time: Start timestamp from start_measurement

        Returns:
            Latency in milliseconds
        """
        latency_ms = (time.time() - start_time) * 1000

        # Record measurement
        self.measurements[operation].append(latency_ms)

        # Keep only recent samples
        if len(self.measurements[operation]) > self.max_samples:
            self.measurements[operation] = self.measurements[operation][-self.max_samples:]

        return latency_ms

    def get_stats(self, operation: str) -> Optional[Dict[str, float]]:
        """
        Get statistics for an operation.

        Args:
            operation: Operation name

        Returns:
            Statistics dict or None if no data
        """
        if operation not in self.measurements or not self.measurements[operation]:
            return None

        data = self.measurements[operation]

        return {
            "count": len(data),
            "min_ms": min(data),
            "max_ms": max(data),
            "mean_ms": statistics.mean(data),
            "median_ms": statistics.median(data),
            "p95_ms": self._percentile(data, 95),
            "p99_ms": self._percentile(data, 99),
        }

    def _percentile(self, data: List[float], percentile: int) -> float:
        """
        Calculate percentile of data.

        Args:
            data: List of values
            percentile: Percentile to calculate (0-100)

        Returns:
            Percentile value
        """
        if not data:
            return 0.0

        sorted_data = sorted(data)
        index = int((percentile / 100) * len(sorted_data))
        index = min(index, len(sorted_data) - 1)

        return sorted_data[index]

    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """
        Get statistics for all operations.

        Returns:
            Dict mapping operation names to stats
        """
        all_stats = {}

        for operation in self.measurements:
            stats = self.get_stats(operation)
            if stats:
                all_stats[operation] = stats

        return all_stats

    def print_stats(self) -> None:
        """Print formatted statistics."""
        print("\n" + "=" * 70)
        print("📊 AEGIS PERFORMANCE METRICS")
        print("=" * 70)

        all_stats = self.get_all_stats()

        if not all_stats:
            print("No performance data available yet.")
            print("=" * 70 + "\n")
            return

        for operation, stats in sorted(all_stats.items()):
            print(f"\n{operation}:")
            print(f"  Count: {stats['count']}")
            print(f"  Mean:   {stats['mean_ms']:.2f} ms")
            print(f"  Median: {stats['median_ms']:.2f} ms")
            print(f"  P95:    {stats['p95_ms']:.2f} ms")
            print(f"  P99:    {stats['p99_ms']:.2f} ms")
            print(f"  Min:    {stats['min_ms']:.2f} ms")
            print(f"  Max:    {stats['max_ms']:.2f} ms")

        print("\n" + "=" * 70 + "\n")

    def check_performance_anomaly(self, operation: str, latency_ms: float) -> Optional[Dict[str, Any]]:
        """
        Check if latency indicates a performance anomaly.

        Args:
            operation: Operation name
            latency_ms: Measured latency in milliseconds

        Returns:
            Incident if anomaly detected, None otherwise
        """
        stats = self.get_stats(operation)

        if not stats or stats["count"] < 10:
            return None

        # Check if latency is significantly higher than P99
        if latency_ms > stats["p99_ms"] * 2:
            return {
                "threat_type": "performance_degradation",
                "action": "monitor",
                "severity": "medium",
                "reason": f"Performance degradation in {operation}: {latency_ms:.2f}ms (normal P99: {stats['p99_ms']:.2f}ms)",
                "operation": operation,
                "latency_ms": latency_ms,
                "baseline_p99_ms": stats["p99_ms"],
            }

        return None


class MetricsCollector:
    """Collects general metrics for AEGIS."""

    def __init__(self):
        """Initialize metrics collector."""
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}

    def increment(self, metric: str, value: int = 1) -> None:
        """
        Increment a counter metric.

        Args:
            metric: Metric name
            value: Amount to increment by
        """
        self.counters[metric] += value

    def set_gauge(self, metric: str, value: float) -> None:
        """
        Set a gauge metric.

        Args:
            metric: Metric name
            value: Metric value
        """
        self.gauges[metric] = value

    def get_counter(self, metric: str) -> int:
        """
        Get counter value.

        Args:
            metric: Metric name

        Returns:
            Counter value
        """
        return self.counters.get(metric, 0)

    def get_gauge(self, metric: str) -> Optional[float]:
        """
        Get gauge value.

        Args:
            metric: Metric name

        Returns:
            Gauge value or None
        """
        return self.gauges.get(metric)

    def get_all_metrics(self) -> Dict[str, Any]:
        """
        Get all metrics.

        Returns:
            Dict with all counters and gauges
        """
        return {
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
        }

    def print_metrics(self) -> None:
        """Print formatted metrics."""
        print("\n" + "=" * 70)
        print("📈 AEGIS METRICS")
        print("=" * 70)

        if self.counters:
            print("\nCounters:")
            for metric, value in sorted(self.counters.items()):
                print(f"  {metric}: {value}")

        if self.gauges:
            print("\nGauges:")
            for metric, value in sorted(self.gauges.items()):
                print(f"  {metric}: {value:.2f}")

        print("\n" + "=" * 70 + "\n")
