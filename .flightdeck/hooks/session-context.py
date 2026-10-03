#!/usr/bin/env python3
"""SessionStart: tell the agent its session id and the exact fd-add line, and remember the id in
.flightdeck/session.json (git-ignored) so `fd.py add` can default --session from it.
   Claude Code: `python3 .flightdeck/hooks/session-context.py`            (hookSpecificOutput.additionalContext)
   Codex:       `python3 .flightdeck/hooks/session-context.py --codex`    (same shape)
   Cursor:      `python3 .flightdeck/hooks/session-context.py --cursor`   ({"additional_context": ...})"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import ROOT, emit, read_stdin, vendor  # noqa: E402


def main():
    v = vendor(sys.argv)
    d = read_stdin()
    sid = d.get("session_id") or ""
    harness = v if v in ("claude", "codex") else "cursor"
    tag = f"{harness}:{sid}" if sid else harness
    try:
        with open(os.path.join(ROOT, ".flightdeck", "session.json"), "w", encoding="utf8") as f:
            json.dump({"harness": harness, "session_id": sid, "session": tag, "started": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "cwd": d.get("cwd")}, f)
    except OSError:
        pass
    text = (f"Flight Deck project. Your session id is {tag}. File deliverables with: "
            f"python3 .flightdeck/fd.py add <file> --id <id> --type <type> --title \"<title>\" --prompt \"<the user's words>\" "
            f"--ingredient src/<script that made it> (fd-add skill, .agents/skills/fd-add; it reads your session and model itself). "
            f"Never write into artifacts/ by hand; run python3 .flightdeck/fd.py check --strict . before finishing. "
            f"Flight Deck hooks active.")
    if v == "cursor":
        emit({"additional_context": text})
    else:
        emit({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": text}})
    return 0


if __name__ == "__main__":
    sys.exit(main())
