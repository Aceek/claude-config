#!/usr/bin/env python3
"""Display detailed usage statistics for /usage-stats command."""

import json
import os
from pathlib import Path
from datetime import datetime


def format_datetime(iso_string: str) -> str:
    """Format ISO datetime to readable format."""
    try:
        dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except (ValueError, AttributeError):
        return iso_string or "N/A"


def get_session_stats() -> dict:
    """Get stats from most recent session file."""
    tmp_files = list(Path("/tmp").glob("claude-session-stats-*.json"))
    if not tmp_files:
        return {}

    latest = max(tmp_files, key=lambda p: p.stat().st_mtime)
    try:
        with open(latest) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def get_project_stats() -> dict:
    """Get stats from project file."""
    project_file = Path(os.getcwd()) / ".claude" / "usage-stats.json"
    if not project_file.exists():
        return {}

    try:
        with open(project_file) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def count_items(items: list) -> dict:
    """Count occurrences of each item."""
    counts = {}
    for item in items:
        short_name = item.split(":")[-1]  # Remove prefix like "superpowers:"
        counts[short_name] = counts.get(short_name, 0) + 1
    return counts


def format_counts(counts: dict, limit: int = 5) -> str:
    """Format counts as comma-separated string."""
    if not counts:
        return "-"
    sorted_items = sorted(counts.items(), key=lambda x: -x[1])[:limit]
    return ", ".join(f"{name}({count})" for name, count in sorted_items)


def main():
    session = get_session_stats()
    project = get_project_stats()

    print("## Session Stats")
    if session:
        started = format_datetime(session.get("started_at", ""))
        print(f"Started: {started}")
        print()

        details = session.get("details", {"skills": [], "agents": []})
        skill_counts = count_items(details.get("skills", []))
        agent_counts = count_items(details.get("agents", []))

        print("| Type   | Count | Details |")
        print("|--------|-------|---------|")
        print(f"| Skills | {session.get('skills', 0)} | {format_counts(skill_counts)} |")
        print(f"| Agents | {session.get('agents', 0)} | {format_counts(agent_counts)} |")
    else:
        print("No session data yet.")

    print()
    print("## Project Stats (Total)")
    if project:
        updated = format_datetime(project.get("updated_at", ""))
        print(f"Last updated: {updated}")
        print()

        totals = project.get("totals", {})
        by_name = project.get("by_name", {"skills": {}, "agents": {}})

        print("| Type   | Count | Top Used |")
        print("|--------|-------|----------|")
        print(f"| Skills | {totals.get('skills', 0)} | {format_counts(by_name.get('skills', {}))} |")
        print(f"| Agents | {totals.get('agents', 0)} | {format_counts(by_name.get('agents', {}))} |")
    else:
        print("No project data yet.")


if __name__ == "__main__":
    main()
