#!/usr/bin/env python3
"""Stop: run `fd.py check --strict .` on the project and hand what is wrong back to the agent, once per stop.
Blocking by default, because a non-blocking Stop hook's output reaches only the transcript, never the model
(research 07 §1). It blocks at most once per stop cycle: when the harness says this stop is already the result of a
Stop hook (`stop_hook_active`), it reports to stderr and lets the agent finish, so a check it cannot fix never traps
it in a loop. FD_STOP_BLOCK=0 in the environment turns blocking off.
   Claude Code / Codex: prints {"decision": "block", "reason": "..."}
   Cursor (--cursor):   prints {"followup_message": "..."} (Cursor's loop_limit caps the follow-ups)"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import ROOT, emit, read_stdin, vendor  # noqa: E402


def main():
    v = vendor(sys.argv)
    d = read_stdin()
    r = subprocess.run([sys.executable, os.path.join(ROOT, ".flightdeck", "fd.py"), "check", "--strict", ROOT], capture_output=True, text=True)
    if r.returncode == 0:
        return 0
    lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()][:20]
    reason = ("fd check --strict failed:\n" + "\n".join(lines) +
              "\nFix these (file deliverables with python3 .flightdeck/fd.py add ...), or tell the user why you can't, then finish.")
    if os.environ.get("FD_STOP_BLOCK") == "0" or d.get("stop_hook_active"):
        sys.stderr.write(reason + "\n")
    elif v == "cursor":
        emit({"followup_message": reason})
    else:
        emit({"decision": "block", "reason": reason})
    return 0


if __name__ == "__main__":
    sys.exit(main())
