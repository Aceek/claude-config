#!/usr/bin/env python3
"""Read stats and output formatted line for ccstatusline."""

import json
import sys
import os
from pathlib import Path


def main():
    # Read session_id from stdin (ccstatusline passes Claude Code JSON)
    session_id = ""
    try:
        stdin_data = json.load(sys.stdin)
        session_id = stdin_data.get("session_id", "")
    except (json.JSONDecodeError, IOError):
        pass

    # Session stats
    session = {"skills": 0, "agents": 0}
    if session_id:
        session_file = Path(f"/tmp/claude-session-stats-{session_id}.json")
        if session_file.exists():
            try:
                with open(session_file) as f:
                    session = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
    # No fallback - if no session_id, show zeros (new session)

    # Project stats
    project = {"skills": 0, "agents": 0}
    project_file = Path(os.getcwd()) / ".claude" / "usage-stats.json"
    if project_file.exists():
        try:
            with open(project_file) as f:
                data = json.load(f)
                project = data.get("totals", project)
        except (json.JSONDecodeError, IOError):
            pass

    # Output formatted line
    s_session = session.get("skills", 0)
    a_session = session.get("agents", 0)
    s_project = project.get("skills", 0)
    a_project = project.get("agents", 0)

    # Get last used skill or agent
    last_used_data = session.get("last_used", {})
    last_used = ""

    if last_used_data:
        item_type = last_used_data.get("type", "")
        name = last_used_data.get("name", "")
        # Shorten: "superpowers:brainstorming" → "brainstorming" / "error-memory" → "error-memory"
        short_name = name.split(":")[-1][:20]
        # Prefix with S: or A: to indicate type
        prefix = "S" if item_type == "skills" else "A"
        last_used = f"{prefix}:{short_name}"

    # Format output
    if last_used:
        print(f"⚡ S:{s_session} A:{a_session} │ ↳ {last_used}")
    else:
        print(f"⚡ S:{s_session} A:{a_session} │ Σ S:{s_project} A:{a_project}")


if __name__ == "__main__":
    main()
