"""shared bits for the project hooks: locate the project root, read stdin JSON, vendor flag"""
import json
import os
import re
import shlex
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))     # <project>/.flightdeck/hooks -> <project>
REASON = ("artifacts/ is governed: file outputs with the fd-add skill "
          "(python3 .flightdeck/fd.py add <file> --id <id> ...), never write there by hand")


def session_tag(harness):
    """<harness>:<id> of the session running this hook, from its environment, else from .flightdeck/session.json"""
    for env, h in (("CLAUDE_CODE_SESSION_ID", "claude"), ("CODEX_THREAD_ID", "codex"), ("CODEX_SESSION_ID", "codex")):
        if os.environ.get(env):
            return "%s:%s" % (h, os.environ[env])
    try:
        with open(os.path.join(ROOT, ".flightdeck", "session.json"), encoding="utf8") as f:
            return json.load(f).get("session") or harness
    except Exception:
        return harness


def fix_reason(target, harness, session=None):
    """the deny message with the fix in it: the exact `fd add` line for the file the agent tried to write
    (research 07 §3: a deny that hands over the command costs one turn instead of a detour)"""
    base = os.path.basename((target or "").rstrip("/")) or "<file>"
    parts = os.path.relpath(os.path.abspath(target), os.path.join(ROOT, "artifacts")).split(os.sep) if target else []
    aid = parts[0] if len(parts) > 1 and parts[0] not in ("", ".", "..") else re.sub(r"-v\d+$", "", os.path.splitext(base)[0])
    aid = re.sub(r"[^a-z0-9]+", "-", aid.lower()).strip("-") or "<id>"
    src = "src/out/" + re.sub(r"-v\d+(?=\.)", "", base)
    return ("artifacts/ is written only by fd. Write the file to <project>/%s instead, then file it (add --type/--title for a new id, "
            "--ingredient for the script that made it):\n  cd %s && python3 .flightdeck/fd.py add %s --id %s --by %s --session %s "
            "--prompt \"<the user's words>\"" % (src, shlex.quote(ROOT), src, aid, harness, session or session_tag(harness)))


def vendor(argv):
    """claude (default) | codex | cursor, from the first flag"""
    for a in argv[1:]:
        if a in ("--claude", "--codex", "--cursor"):
            return a[2:]
    return "claude"


def read_stdin():
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def under_artifacts(path, cwd=None):
    """true when `path` (absolute or relative to cwd/root) lands inside <project>/artifacts/"""
    if not path:
        return False
    base = cwd or ROOT
    p = os.path.abspath(path if os.path.isabs(path) else os.path.join(base, path))
    art = os.path.join(ROOT, "artifacts")
    return p == art or p.startswith(art + os.sep)


def under_root(path, cwd=None):
    """true when `path` is inside this project"""
    if not path:
        return False
    p = os.path.abspath(path if os.path.isabs(path) else os.path.join(cwd or ROOT, path))
    return p == ROOT or p.startswith(ROOT + os.sep)


def emit(obj):
    sys.stdout.write(json.dumps(obj))
    sys.stdout.flush()
