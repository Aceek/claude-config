#!/usr/bin/env python3
"""Track Skill and Agent usage from PreToolUse hook."""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timezone


def update_stats_file(file_path: Path, category: str, item_name: str, is_session: bool):
    """Update a stats file with new usage."""

    # Ensure directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing or create new
    if file_path.exists():
        try:
            with open(file_path) as f:
                stats = json.load(f)
        except (json.JSONDecodeError, IOError):
            stats = {}
    else:
        stats = {}

    if is_session:
        # Session format - initialize with metadata if new file
        if "session_id" not in stats:
            stats["session_id"] = file_path.stem.replace("claude-session-stats-", "")
            stats["started_at"] = datetime.now(timezone.utc).isoformat()
        stats.setdefault("skills", 0)
        stats.setdefault("agents", 0)
        stats.setdefault("details", {"skills": [], "agents": []})

        stats[category] += 1
        stats["details"][category].append(item_name)
        # Track last used for statusline display
        stats["last_used"] = {"type": category, "name": item_name}
    else:
        # Project format
        stats["updated_at"] = datetime.now(timezone.utc).isoformat()
        stats.setdefault("totals", {"skills": 0, "agents": 0, "sessions": 0})
        stats.setdefault("by_name", {"skills": {}, "agents": {}})

        stats["totals"][category] += 1
        stats["by_name"][category][item_name] = stats["by_name"][category].get(item_name, 0) + 1

    # Write back
    with open(file_path, "w") as f:
        json.dump(stats, f, indent=2)


def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # Silent fail, don't block Claude

    session_id = hook_input.get("session_id", "unknown")
    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})
    cwd = hook_input.get("cwd", os.getcwd())

    # Determine category and name
    if tool_name == "Skill":
        category = "skills"
        item_name = tool_input.get("skill", "unknown")
    elif tool_name == "Task":
        category = "agents"
        item_name = tool_input.get("subagent_type", "unknown")
    else:
        sys.exit(0)  # Not tracking this tool

    # Update session stats
    session_file = Path(f"/tmp/claude-session-stats-{session_id}.json")
    update_stats_file(session_file, category, item_name, is_session=True)

    # Update project stats
    project_file = Path(cwd) / ".claude" / "usage-stats.json"
    update_stats_file(project_file, category, item_name, is_session=False)


if __name__ == "__main__":
    main()
