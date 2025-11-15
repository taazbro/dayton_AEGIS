"""
Dashboard TUI — Real-time monitoring dashboard using Rich
"""

import time
from queue import Queue, Empty
from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict


def run_dashboard(incident_queue: Queue) -> None:
    """
    Run the enhanced Rich TUI dashboard for monitoring incidents.

    Args:
        incident_queue: Queue to read incidents from
    """
    try:
        from rich.console import Console
        from rich.live import Live
        from rich.table import Table
        from rich.panel import Panel
        from rich.layout import Layout
        from rich.text import Text
        from rich import box

        console = Console()
        incidents: List[Dict[str, Any]] = []

        # Statistics
        stats = {
            "total_incidents": 0,
            "by_severity": defaultdict(int),
            "by_type": defaultdict(int),
            "by_action": defaultdict(int),
        }

        def create_dashboard() -> Layout:
            """Create the dashboard layout."""
            layout = Layout()
            layout.split_column(
                Layout(name="header", size=3),
                Layout(name="body"),
                Layout(name="footer", size=3)
            )

            layout["body"].split_row(
                Layout(name="incidents", ratio=2),
                Layout(name="stats", ratio=1)
            )

            return layout

        def render_header() -> Panel:
            """Render the header."""
            title = Text("🔥 ZYBERPOL AEGIS", style="bold red", justify="center")
            subtitle = Text("Autonomous Cyber Defense Agent", style="cyan", justify="center")
            timestamp = Text(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="dim", justify="center")

            content = Text()
            content.append(title)
            content.append("\n")
            content.append(subtitle)
            content.append("\n")
            content.append(timestamp)

            return Panel(content, border_style="bright_blue", box=box.DOUBLE)

        def render_incidents() -> Panel:
            """Render the incidents table."""
            table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
            table.add_column("Time", style="cyan", width=10)
            table.add_column("Severity", width=10)
            table.add_column("Threat Type", style="yellow", width=25)
            table.add_column("Action", style="green", width=12)

            # Show last 15 incidents
            for incident in reversed(incidents[-15:]):
                time_str = incident.get("detected_at", "")
                severity = incident.get("severity", "unknown").upper()
                threat_type = incident.get("threat_type", "unknown")
                action = incident.get("action", "none").upper()

                # Color severity
                if severity == "CRITICAL":
                    severity_colored = f"[red bold]{severity}[/]"
                elif severity == "HIGH":
                    severity_colored = f"[orange1]{severity}[/]"
                elif severity == "MEDIUM":
                    severity_colored = f"[yellow]{severity}[/]"
                else:
                    severity_colored = f"[green]{severity}[/]"

                # Color action
                if action == "KILL":
                    action_colored = f"[red bold]{action}[/]"
                elif action == "QUARANTINE":
                    action_colored = f"[orange1]{action}[/]"
                else:
                    action_colored = f"[cyan]{action}[/]"

                table.add_row(time_str, severity_colored, threat_type, action_colored)

            if not incidents:
                table.add_row("--:--:--", "[dim]Waiting...[/]", "[dim]No incidents yet[/]", "[dim]--[/]")

            return Panel(table, title="[bold]🚨 Recent Incidents[/]", border_style="red")

        def render_stats() -> Panel:
            """Render the statistics panel."""
            from rich.tree import Tree

            tree = Tree("📊 Statistics", style="bold cyan")

            # Total incidents
            total_branch = tree.add(f"[bold]Total Incidents: {stats['total_incidents']}[/]")

            # By severity
            severity_branch = tree.add("[bold yellow]By Severity[/]")
            for severity in ["critical", "high", "medium", "low"]:
                count = stats['by_severity'].get(severity, 0)
                if count > 0:
                    emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}[severity]
                    severity_branch.add(f"{emoji} {severity.capitalize()}: {count}")

            # By action
            action_branch = tree.add("[bold green]By Action[/]")
            for action in ["kill", "quarantine", "monitor"]:
                count = stats['by_action'].get(action, 0)
                if count > 0:
                    action_branch.add(f"{action.capitalize()}: {count}")

            # Top threats
            if stats['by_type']:
                threat_branch = tree.add("[bold red]Top Threats[/]")
                top_threats = sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True)[:5]
                for threat_type, count in top_threats:
                    threat_branch.add(f"{threat_type}: {count}")

            return Panel(tree, title="[bold]📈 Analytics[/]", border_style="green")

        def render_footer() -> Panel:
            """Render the footer."""
            status = Text()
            status.append("🟢 ", style="green bold")
            status.append("System Operational", style="green")
            status.append(" | ", style="dim")
            status.append("Press CTRL+C to stop", style="dim italic")

            return Panel(status, border_style="dim", box=box.SIMPLE)

        def update_display(layout: Layout) -> None:
            """Update the display."""
            layout["header"].update(render_header())
            layout["incidents"].update(render_incidents())
            layout["stats"].update(render_stats())
            layout["footer"].update(render_footer())

        # Create layout
        layout = create_dashboard()

        # Run live display
        with Live(layout, refresh_per_second=2, screen=True) as live:
            while True:
                try:
                    # Check for new incidents
                    try:
                        incident = incident_queue.get(timeout=0.5)
                        incidents.append({
                            **incident,
                            "detected_at": datetime.now().strftime("%H:%M:%S")
                        })

                        # Update statistics
                        stats["total_incidents"] += 1
                        stats["by_severity"][incident.get("severity", "unknown").lower()] += 1
                        stats["by_type"][incident.get("threat_type", "unknown")] += 1
                        stats["by_action"][incident.get("action", "none").lower()] += 1

                    except Empty:
                        pass

                    # Update display
                    update_display(layout)

                except KeyboardInterrupt:
                    break

    except ImportError:
        # Fallback to simple dashboard if Rich not available
        print("⚠️  Rich library not available, using simple dashboard")
        run_simple_dashboard(incident_queue)


def run_simple_dashboard(incident_queue: Queue) -> None:
    """
    Fallback simple dashboard without Rich.

    Args:
        incident_queue: Queue to read incidents from
    """
    incidents: List[Dict[str, Any]] = []
    max_display = 10

    print("\n" + "=" * 60)
    print("📊 AEGIS MONITORING DASHBOARD")
    print("=" * 60)
    print("Waiting for incidents...\n")

    while True:
        try:
            # Check for new incidents
            try:
                incident = incident_queue.get(timeout=1.0)
                incidents.append({
                    **incident,
                    "detected_at": datetime.now().strftime("%H:%M:%S")
                })

                # Keep only recent incidents
                if len(incidents) > max_display:
                    incidents = incidents[-max_display:]

                _display_simple_dashboard(incidents)

            except Empty:
                # No new incidents, just continue
                pass

            time.sleep(1.0)

        except KeyboardInterrupt:
            break


def _display_simple_dashboard(incidents: List[Dict[str, Any]]) -> None:
    """
    Display simple dashboard.

    Args:
        incidents: List of recent incidents
    """
    print("\n" * 2)
    print("=" * 60)
    print(f"📊 AEGIS DASHBOARD — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print(f"Total Incidents: {len(incidents)}\n")

    if not incidents:
        print("No incidents detected yet...\n")
        return

    # Display recent incidents
    print("RECENT INCIDENTS:")
    print("-" * 60)

    for idx, incident in enumerate(reversed(incidents), 1):
        threat_type = incident.get("threat_type", "unknown")
        severity = incident.get("severity", "unknown")
        action = incident.get("action", "none")
        detected_at = incident.get("detected_at", "unknown")

        # Color coding based on severity
        severity_icon = _get_severity_icon(severity)

        print(f"{idx}. [{detected_at}] {severity_icon} {threat_type}")
        print(f"   Severity: {severity.upper()} | Action: {action}")
        print()

    print("=" * 60)


def _get_severity_icon(severity: str) -> str:
    """
    Get emoji icon for severity level.

    Args:
        severity: Severity level string

    Returns:
        Emoji icon
    """
    icons = {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢",
    }
    return icons.get(severity.lower(), "⚪")
