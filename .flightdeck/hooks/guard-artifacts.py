#!/usr/bin/env python3
"""PreToolUse guard: deny direct writes into artifacts/ (the fd-add skill is the only door).
   Claude Code / Codex: `python3 .flightdeck/hooks/guard-artifacts.py` (stdin: tool_name, tool_input, cwd; JSON deny)
   Cursor preToolUse / beforeShellExecution: add `--cursor` (stdin: tool_name+tool_input, or command; {"permission"} out)
Allowed calls print nothing and exit 0. A deny carries the exact `fd add` line for the file (research 07 §3)."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import emit, fix_reason, read_stdin, under_artifacts, under_root, vendor  # noqa: E402

# a shell command that writes into artifacts/: redirections, cp/mv/tee/install/rsync/ln targets, mkdir, rm, touch
SHELL_WRITE = re.compile(
    r"(?:(?:>|>>|\btee\b|\bcp\b|\bmv\b|\binstall\b|\brsync\b|\bln\b|\bmkdir\b|\btouch\b|\brm\b|\bsed\s+-i\S*)[^;&|]*?)"
    r"(?:^|[\s=\"'])(?:\./)?artifacts/", re.M)
WRITE_VERB = re.compile(r"(>|\btee\b|\bcp\b|\bmv\b|\binstall\b|\brsync\b|\bln\b|\bmkdir\b|\btouch\b|\brm\b|\bsed\s+-i)")

# a quoted artifacts/ path passed straight to a write call in inline code: savefig('artifacts/x.png'),
# open("artifacts/x", "w"), df.to_csv('artifacts/…'), Path('artifacts/…').write_text(…), shutil.copy(src, 'artifacts/…')
Q = r"""f?["']([^"'\s]*artifacts/[^"'\s]*)["']"""
INLINE_WRITES = [re.compile(p) for p in (
    r"(?:savefig|to_csv|to_parquet|to_json|to_file|imwrite|imsave|write_image|write_html|\.save)\(\s*" + Q,
    r"\bopen\(\s*" + Q + r"\s*,\s*f?[\"'][wax]",
    r"Path\(\s*" + Q + r"\s*\)\.(?:write_\w+|mkdir|touch)",
    r"(?:copy\w*|move|rename|replace|symlink)\([^)]*?,\s*" + Q,
    r"(?:makedirs|mkdir)\(\s*" + Q)]


def written(seg):
    """the part of one shell segment that names what it writes: everything after the write verb, or only the last
    argument for cp/install/rsync/ln (their sources are reads)"""
    verb = WRITE_VERB.search(seg)
    if not verb:
        return ""
    rest = seg[verb.end():]
    if verb.group(1) in ("cp", "install", "rsync", "ln") and " -t" not in rest:
        return (rest.split() or [""])[-1]
    return rest


def strip_heredocs(cmd):
    """the command without its heredoc bodies (a `python3 - <<'EOF' … EOF` body is code, not shell)"""
    out, lines, i = [], cmd.split("\n"), 0
    while i < len(lines):
        out.append(lines[i])
        m = re.search(r"<<-?\s*['\"]?(\w+)['\"]?", lines[i])
        i += 1
        if m:
            while i < len(lines) and lines[i].strip() != m.group(1):
                i += 1
            i += 1
    return "\n".join(out)


def shell_writes(cmd, cwd):
    """the artifacts/ path a shell command writes to ("artifacts/" when it can't tell which), else None"""
    if not cmd:
        return None
    full, cmd = cmd, strip_heredocs(cmd)
    if SHELL_WRITE.search(cmd):
        m = re.search(r"(?:\./)?(artifacts/[^\s;&|\"']*)", cmd)
        return os.path.join(cwd or ".", m.group(1)) if m else "artifacts/"
    # any other path that resolves into this project's artifacts/ (absolute, ../artifacts from a subfolder, …)
    # (only paths AFTER the write verb in the same segment: `ls ../artifacts > list.txt` is a read)
    for seg in re.split(r"[;&|]+", cmd):
        for m in re.finditer(r"([^\s\"'<>=]*artifacts(?:/[^\s\"'<>]*)?)(?![\w.-])", written(seg)):
            if under_artifacts(m.group(1), cwd):
                return os.path.join(cwd or ".", m.group(1))
    # an output flag pointing into artifacts/ (`--out artifacts/x.png`, `-o ../artifacts/x`, `--output=…`)
    for m in re.finditer(r"(?:^|\s)(?:-o|--out(?:put)?(?:-file|-dir)?)(?:\s+|=)[\"']?([^\s\"';&|]+)", cmd):
        if under_artifacts(m.group(1), cwd):
            return os.path.join(cwd or ".", m.group(1))
    # inline code that writes a quoted artifacts/ path (`python3 -c "…savefig('artifacts/x.png')"`, heredocs)
    if re.search(r"\b(?:python3?|node|ruby|perl|Rscript|deno|bun)\b[^;&|]*(?:\s-[ce]\s|<<)", full):
        for rx in INLINE_WRITES:
            for m in rx.finditer(full):
                if under_artifacts(m.group(1), cwd):
                    return os.path.join(cwd or ".", m.group(1))
    # `cd artifacts/x && cp y .`: a write after changing into artifacts/
    segs = re.split(r"[;&|]+", cmd)
    for i, seg in enumerate(segs):
        m = re.match(r"\s*(?:cd|pushd)\s+[\"']?([^\s\"']+)", seg)
        if m and under_artifacts(m.group(1), cwd) and any(WRITE_VERB.search(x) for x in segs[i + 1:]):
            return os.path.join(cwd or ".", m.group(1))
    return None


def patch_body(ti):
    """the apply_patch text of a call, wherever the harness put it (command / input / patch), else None"""
    for key in ("command", "input", "patch"):
        v = ti.get(key)
        if isinstance(v, str) and "*** Begin Patch" in v:
            return v
    return None


def patch_writes(body, cwd):
    """the first file an apply_patch body adds, updates, deletes or moves into artifacts/"""
    for m in re.finditer(r"^\*\*\* (?:Add File|Update File|Delete File|Move to): (.+?)\s*$", body, re.M):
        if under_artifacts(m.group(1), cwd):
            return m.group(1)
    return None


MANIFEST = ("artifacts.yaml", "artifacts.lock.json")
MANIFEST_REASON = ("%s is written by fd, not by hand: `python3 .flightdeck/fd.py add` files a version, `fd.py adopt` "
                   "records stray files, `fd.py fill` rewrites the lock. If fd can't make the change you need, ask the user.")


def manifest_write(tool, ti, cwd):
    """the manifest file a call would hand-edit in a way only fd may (versions, paths, the lock), else None.
    Editing a title or note in artifacts.yaml stays allowed."""
    body = patch_body(ti)
    if body:
        for m in re.finditer(r"^\*\*\* (?:Add|Update|Delete) File: (.+?)\s*$", body, re.M):
            name = os.path.basename(m.group(1))
            if name in MANIFEST and under_root(m.group(1), cwd):
                added = "\n".join(l[1:] for l in body[m.end():].split("\n*** ")[0].splitlines() if l.startswith("+"))
                if name == "artifacts.lock.json" or re.search(r"(?m)^\s*(?:-\s*)?(?:v|path|sha256):", added) or "Add File" in m.group(0):
                    return name
        return None
    if tool in ("bash", "shell"):
        cmd = strip_heredocs(ti.get("command", "") if isinstance(ti.get("command"), str) else "")
        for seg in re.split(r"[;&|]+", cmd):
            for name in MANIFEST:
                if name in written(seg):
                    return name
        return None
    path = ti.get("file_path") or ti.get("path") or ""
    name = os.path.basename(path)
    if name not in MANIFEST or not under_root(path, cwd):
        return None
    if name == "artifacts.lock.json" or tool == "write":
        return name
    new = ti.get("new_string", "") + "".join(e.get("new_string", "") for e in ti.get("edits") or [] if isinstance(e, dict))
    return name if re.search(r"(?m)^\s*(?:-\s*)?(?:v|path|sha256):", new) else None


def main():
    v = vendor(sys.argv)
    d = read_stdin()
    cwd = d.get("cwd")
    tool = (d.get("tool_name") or "").lower()
    ti = d.get("tool_input") or {}
    deny = None
    if "command" in d and not tool:                      # Cursor beforeShellExecution
        deny = shell_writes(d.get("command", ""), cwd)
    elif patch_body(ti):                                  # Codex apply_patch: the patch arrives as tool_input.command
        deny = patch_writes(patch_body(ti), cwd)
    elif tool in ("bash", "shell") or "command" in ti:
        deny = shell_writes(ti.get("command", "") or (ti.get("input", "") if isinstance(ti.get("input"), str) else ""), cwd)
    else:                                                 # Write / Edit / MultiEdit / NotebookEdit and Cursor file tools
        for key in ("file_path", "path", "notebook_path"):
            if under_artifacts(ti.get(key), cwd):
                deny = ti.get(key)
    man = None if deny else manifest_write(tool, ti, cwd)
    if not deny and not man:
        return 0
    reason = (MANIFEST_REASON % man) if man else fix_reason(deny if os.path.isabs(deny) else os.path.join(cwd or ".", deny), v)
    if v == "cursor":
        emit({"permission": "deny", "user_message": reason, "agent_message": reason})
    else:
        emit({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": reason}})
    return 0


if __name__ == "__main__":
    sys.exit(main())
