#!/usr/bin/env python3
"""fd — the Flight Deck project tool (spec: docs/PROJECTS.md).

  fd new <name> [--template base] [--summary "…"] [--harness claude] [--into ~] [--github]   scaffold + git init (+ private repo)
  fd init [folder] --name <name> [--summary "…"] [--harness claude]   fill the {{placeholders}} of a copy made from the GitHub template
  fd check [--strict] [--json] [folder ...]   rules 1–7: project.yaml, manifest, artifacts/, names, formats, lock
  fd fill [folder]                            artifacts.lock.json: sha256 / size / mime / media facts
  fd add <file> --id <id> [--type film --title "…"] [--note …] [--by claude --model … --session … --prompt …]
                [--ingredient p …] [--public] [--copy] [--force] [--date YYYY-MM-DD] [--folder .]
                                              file it as artifacts/<id>/<id>-v<N>.<ext>, prepend the version, refresh the lock
  fd adopt [folder]                           entries for unreferenced files under artifacts/; minimal project.yaml
  fd list [--deck http://127.0.0.1:8098]      the projects this machine's deck knows (GET /projects)
  fd attest [--id X] [--all] [--dry-run]      sign the in-toto statements keyless with cosign -> attestations/*.sigstore.json
  fd verify [--id X] [--identity … --issuer …] verify the bundles with cosign

Provenance: `add` records by / model / session (`<harness>:<id>`, defaulted from .flightdeck/session.json when a hook
wrote it; the model is read from that session's transcript, not trusted from --model) / prompt (or `sha256:…` with --redact-prompt) / ingredients / built_at / commit in the manifest; `fill` digests
the ingredients and the prompt into the lock and writes one in-toto Statement v1 with a SLSA provenance v1 predicate per
version at attestations/<id>-v<N>.intoto.json; `attest` signs them, `verify` checks them, `check --strict` refuses a stale one.

Installed as ~/.local/bin/fd-project (`fd` is the file finder); a project's .flightdeck/fd.py is this same file and
finds artifacts_check.py + the schemas beside itself. Python 3.9, stdlib + PyYAML, jsonschema optional.
"""
import argparse
import datetime
import hashlib
import socket
import tempfile
import fnmatch
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
try:
    import artifacts_check as ac
except ImportError:
    _vendored = os.path.join(os.getcwd(), ".flightdeck")
    if not os.path.isfile(os.path.join(_vendored, "artifacts_check.py")):
        sys.exit("fd: artifacts_check.py must sit beside fd.py or in ./.flightdeck/")
    sys.path.insert(0, _vendored)
    import artifacts_check as ac
yaml, jsonschema = ac.yaml, ac.jsonschema

PROJECT_NAMES = ("project.yaml", "project.yml")
PROJECT_SCHEMA_PATHS = (os.path.join(HERE, "..", "schemas", "project-1.json"), os.path.join(HERE, "project-1.json"))
TEMPLATE_DIRS = (os.path.join(HERE, "..", "templates"), os.path.expanduser("~/agent-status/templates"))
DECK_URL = "http://127.0.0.1:8098"
LAYOUT = {"code": "src", "artifacts": "artifacts", "data": "data", "notes": "notes"}
CATEGORY_OF = {t: c for c, ts in ac.CATEGORIES.items() for t in ts}
TYPE_BY_EXT = {"mp4": "film", "mov": "film", "webm": "film", "png": "figure", "jpg": "figure", "jpeg": "figure",
               "svg": "figure", "webp": "figure", "md": "doc", "csv": "dataset", "parquet": "dataset", "json": "dataset"}
IMAGE_EXT = {"png", "jpg", "jpeg", "gif", "webp", "svg", "bmp", "tif", "tiff"}
VIDEO_EXT = {"mp4", "mov", "m4v", "webm", "mkv"}
VNAME_RE = re.compile(r"^(?P<stem>.+?)-v(?P<v>\d+(?:\.\d+)*)\.(?P<ext>[A-Za-z0-9]+)$")
ATTEST_DIR = "attestations"
STATEMENT_TYPE = "https://in-toto.io/Statement/v1"
PREDICATE_TYPE = "https://slsa.dev/provenance/v1"
BUILD_TYPE = "https://flightdeck.dmarz.xyz/buildtype/agent-session/v1"
BUILDER_BASE = "https://flightdeck.dmarz.xyz/builder"
SESSION_FILE = os.path.join(".flightdeck", "session.json")
MANIFEST_HEADER = ("# Artifact manifest v1 (schema: .flightdeck/artifacts-1.json). Add versions with `fd add`, check with\n"
                   "#   python3 .flightdeck/fd.py check --strict .\n")


# ---- small helpers ------------------------------------------------------------------------------------
def today():
    return datetime.date.today().isoformat()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")[:64] or "project"


def die(msg, code=2):
    print("fd: " + msg, file=sys.stderr)
    sys.exit(code)


def ext_of(path):
    return os.path.splitext(path)[1].lstrip(".").lower()


def under(parent, path):
    parent, path = os.path.realpath(parent), os.path.realpath(path)
    return path == parent or path.startswith(parent + os.sep)


def find_root(start):
    """the nearest folder at or above `start` that holds project.yaml or artifacts.yaml; else `start`"""
    d = os.path.realpath(os.path.expanduser(start))
    cur = d
    while True:
        if any(os.path.isfile(os.path.join(cur, n)) for n in PROJECT_NAMES + ac.MANIFEST_NAMES):
            return cur
        nxt = os.path.dirname(cur)
        if nxt == cur:
            return d
        cur = nxt


class _Dumper(yaml.SafeDumper if yaml else object):
    """PyYAML indents list items under their key (`  - id:`), the way the manifests are written by hand"""
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def _datify(obj, key=None):
    """dates go back to date objects so they dump unquoted (2026-09-24, not '2026-09-24')"""
    if isinstance(obj, dict):
        return {k: _datify(v, k) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_datify(v, key) for v in obj]
    if key in ("date", "created") and isinstance(obj, str) and ac.DATE_RE.match(obj):
        try:
            return datetime.date.fromisoformat(obj)
        except ValueError:
            pass
    return obj


def read_yaml(path):
    """-> (data with dates as strings, header comment lines)"""
    with open(path, encoding="utf8") as f:
        text = f.read()
    header = []
    for line in text.splitlines():
        if line.startswith("#"):
            header.append(line)
        elif line.strip():
            break
    return ac._plain(yaml.safe_load(text)), ("\n".join(header) + "\n") if header else ""


def write_yaml(path, data, header=""):
    body = yaml.dump(_datify(data), Dumper=_Dumper, sort_keys=False, allow_unicode=True, default_flow_style=False, width=120)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf8") as f:
        f.write(header + body)
    os.replace(tmp, path)


def parse_v(s):
    return int(s) if s.isdigit() else (float(s) if s.count(".") == 1 else s)


def now_rfc3339():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def hostname():
    """the short host name, lower-cased (it becomes part of the SLSA builder id URI)"""
    return (socket.gethostname().split(".")[0] or "unknown").lower()


def _git(folder, *args):
    try:
        r = subprocess.run(["git", "-C", folder] + list(args), capture_output=True, text=True, timeout=20)
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def git_commit(folder):
    """HEAD sha, `-dirty` appended when the tree has changes; None outside a repo"""
    sha = _git(folder, "rev-parse", "HEAD")
    if not sha:
        return None
    dirty = _git(folder, "status", "--porcelain")
    return sha + ("-dirty" if dirty else "")


def git_remote_url(folder):
    """origin as an https URL (git@github.com:a/b.git -> https://github.com/a/b), or None"""
    url = _git(folder, "remote", "get-url", "origin")
    if not url:
        return None
    m = re.match(r"^(?:ssh://)?git@([^:/]+)[:/](.+?)(?:\.git)?$", url)
    if m:
        return "https://%s/%s" % (m.group(1), m.group(2))
    return re.sub(r"\.git$", "", url)


def session_default(folder):
    """{harness, session_id} from .flightdeck/session.json (written by the SessionStart hook), else {}"""
    try:
        with open(os.path.join(folder, SESSION_FILE), encoding="utf8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def session_from_env():
    """{harness, session_id, request} of the process running `fd add`, from its own environment: Claude Code sets
    CLAUDE_CODE_SESSION_ID in every command it runs (a subagent's carries its parent's); a session Flight Deck
    launched for another harness may carry FLIGHTDECK_SESSION=<harness>:<id>. Never the shared
    .flightdeck/session.json: it names whichever session STARTED last in the folder, so with two threads open in a
    project one filed the other's work (2026-09-26). request = the promptId of the last message a person typed in
    that session (the request this filing answers), read from its transcript."""
    fs = os.environ.get("FLIGHTDECK_SESSION", "")
    if fs:
        h, _, sid = fs.partition(":") if ":" in fs else ("unknown", "", fs)
        return {"harness": h, "session_id": sid, "request": None}
    cx = os.environ.get("CODEX_THREAD_ID") or os.environ.get("CODEX_SESSION_ID")
    if cx and not os.environ.get("CLAUDE_CODE_SESSION_ID"):
        return {"harness": "codex", "session_id": cx, "request": None}
    sid = os.environ.get("CLAUDE_CODE_SESSION_ID", "")
    if not sid:
        return {}
    return {"harness": "claude", "session_id": sid, "request": request_of(sid)}


def request_of(sid):
    """promptId of the last human prompt in ~/.claude/projects/*/<sid>.jsonl (None when unreadable)"""
    import glob
    paths = glob.glob(os.path.expanduser("~/.claude/projects/*/%s.jsonl" % sid))
    if not paths:
        return None
    last = None
    try:
        with open(paths[0], encoding="utf8", errors="ignore") as f:
            f.seek(max(0, os.path.getsize(paths[0]) - 4_000_000))
            for line in f:
                if '"human"' not in line:
                    continue
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get("type") == "user" and (d.get("origin") or {}).get("kind") == "human" and not d.get("isMeta"):
                    last = d.get("promptId") or d.get("uuid")
    except Exception:
        return None
    return last


def _tail_lines(path, nbytes=4_000_000):
    with open(path, encoding="utf8", errors="ignore") as f:
        f.seek(max(0, os.path.getsize(path) - nbytes))
        return f.readlines()


def model_of(harness, sid):
    """the model the session actually ran, from its own transcript (Claude: the last assistant `message.model`;
    Codex: the last `"model"` in ~/.codex/sessions/**/rollout-*-<id>.jsonl), else None. Agents guess their model id
    wrong (research 10: 3/3 Codex filings said gpt-5), so `fd add` records this instead of trusting --model."""
    import glob
    if not sid:
        return None
    if harness == "claude":
        paths, pat = glob.glob(os.path.expanduser("~/.claude/projects/*/%s.jsonl" % sid)), None
    elif harness == "codex":
        home = os.environ.get("CODEX_HOME") or os.path.expanduser("~/.codex")
        paths, pat = glob.glob(os.path.join(home, "sessions", "*", "*", "*", "rollout-*-%s.jsonl" % sid)), re.compile(r'"model":"([^"]+)"')
    else:
        return None
    if not paths:
        return None
    try:
        lines = _tail_lines(paths[0])
    except OSError:
        return None
    for line in reversed(lines):
        if pat:
            m = pat.search(line)
            if m:
                return m.group(1)
            continue
        if '"assistant"' not in line or '"model"' not in line:
            continue
        try:
            m = ((json.loads(line).get("message") or {}).get("model"))
        except Exception:
            continue
        if m and m != "<synthetic>":
            return m
    return None


# formats keys -> the smallest change that passes (agent-facing refusals name the fix, never --force)
FIX_HINTS = {
    "min_width": "re-render at >= {v}px wide", "max_width": "re-render at <= {v}px wide",
    "min_height": "re-render at >= {v}px tall", "max_height": "re-render at <= {v}px tall",
    "aspect": "re-render at {v}", "ext": "export as one of {v}", "name": "rename the file to match {v}",
    "max_bytes": "compress it under {v} bytes", "video": "re-encode the video as {v} (ffmpeg -c:v ...)",
    "audio": "re-encode the audio as {v} (ffmpeg -c:a ...)",
    "faststart": "re-mux: ffmpeg -i in.mp4 -c copy -movflags +faststart out.mp4",
    "max_fps": "re-encode at <= {v} fps (ffmpeg -r {v})", "max_duration_s": "cut it to <= {v}s",
}


# probe_violations() message -> the formats key it broke
VIOLATION_KEYS = [(r"violates (min_width|max_width|min_height|max_height)", None), (r"^extension ", "ext"), (r"^name ", "name"),
                  (r"max_bytes", "max_bytes"), (r"^aspect ", "aspect"), (r"^video codec", "video"), (r"^audio codec", "audio"),
                  (r"faststart", "faststart"), (r"max_fps", "max_fps"), (r"max_duration_s", "max_duration_s")]


def refusal(src, typ, viol, pol):
    """the `fd add` refusal: which rule failed, the smallest change that passes, and ask-first when the request
    itself conflicts (research 07 §3, 10 fix 4)"""
    fixes = []
    for x in viol:
        key = next(((k or re.search(pat, x).group(1)) for pat, k in VIOLATION_KEYS if re.search(pat, x)), None)
        hint = FIX_HINTS[key].format(v=pol.get(key)) if key else None
        if hint and hint not in fixes:
            fixes.append(hint)
    return ("fd: %s violates formats.%s in project.yaml:\n  %s\nsmallest change that passes: %s.\n"
            "If the request itself asks for this (say a 400px thumbnail), stop and ask the user before substituting." %
            (os.path.basename(src), typ, "\n  ".join(viol), "; ".join(fixes) or "make the file meet the rule above"))


NEEDS_INGREDIENT = ("figure", "film", "dataset", "deck")


def normalise_session(session, harness):
    """`<harness>:<id>`; a bare id gets the harness prefix"""
    if not session:
        return None
    return session if re.match(r"^[a-z0-9_-]+:", session) else "%s:%s" % (harness or "unknown", session)


# ---- in-toto statements (one per version, attestations/<id>-v<N>.intoto.json) ----------------------------
def statement_path(folder, aid, v):
    return os.path.join(folder, ATTEST_DIR, "%s-v%s.intoto.json" % (aid, v))


def bundle_path(folder, aid, v):
    return os.path.join(folder, ATTEST_DIR, "%s-v%s.sigstore.json" % (aid, v))


def build_statement(folder, art, v, lock_entry, prev, host=None):
    """the in-toto Statement v1 + SLSA provenance v1 predicate for one version, from the manifest + lock facts only"""
    harness = v.get("by") or "unknown"
    session = v.get("session")
    commit = v.get("commit")
    ext = {k: val for k, val in (("prompt", v.get("prompt")), ("harness", v.get("by")), ("model", v.get("model"))) if val}
    internal = {k: val for k, val in (("session", session), ("commit", commit)) if val}
    deps = []
    for ing in lock_entry.get("ingredients") or []:
        d = {"uri": ing["uri"]}
        if ing.get("sha256"):
            d["digest"] = {"sha256": ing["sha256"]}
        deps.append(d)
    remote = git_remote_url(folder)
    if remote and commit:
        deps.append({"uri": "git+" + remote, "digest": {"gitCommit": commit.replace("-dirty", "")}})
    if prev and prev[1].get("sha256"):
        deps.append({"uri": prev[0], "digest": {"sha256": prev[1]["sha256"]}, "annotations": {"supersedes": True}})
    builder = {"id": "%s/%s/%s" % (BUILDER_BASE, lock_entry.get("host") or host or hostname(), harness)}
    meta = {}
    if session:
        meta["invocationId"] = session
    if v.get("built_at"):
        meta["startedOn"] = meta["finishedOn"] = v["built_at"]
    return {
        "_type": STATEMENT_TYPE,
        "subject": [{"name": v["path"], "digest": {"sha256": lock_entry["sha256"]}}],
        "predicateType": PREDICATE_TYPE,
        "predicate": {
            "buildDefinition": {"buildType": BUILD_TYPE, "externalParameters": ext, "internalParameters": internal, "resolvedDependencies": deps},
            "runDetails": {"builder": builder, "metadata": meta},
        },
    }


def version_pairs(data, lock):
    """[(artifact, version, key, lock entry, previous (path, entry) or None)] for every version the lock knows"""
    entries = (lock or {}).get("entries") or {}
    out = []
    for a in (data or {}).get("artifacts") or []:
        if not isinstance(a, dict) or not a.get("id"):
            continue
        vs = sorted([x for x in a.get("versions") or [] if isinstance(x, dict) and "v" in x and x.get("path")], key=lambda x: ac._vkey(x.get("v")))
        for i, v in enumerate(vs):
            key = "%s@%s" % (a["id"], v["v"])
            if key not in entries:
                continue
            prev = None
            sup = v.get("supersedes")
            cand = [x for x in vs if str(x.get("v")) == str(sup)] if sup is not None else vs[:i][-1:]
            if cand and "%s@%s" % (a["id"], cand[-1]["v"]) in entries:
                prev = (cand[-1]["path"], entries["%s@%s" % (a["id"], cand[-1]["v"])])
            out.append((a, v, key, entries[key], prev))
    return out


def write_statements(folder, data, lock, selected_keys=None):
    """Write selected statements, or all locked versions for explicit bulk maintenance."""
    written = 0
    for a, v, key, e, prev in version_pairs(data, lock):
        if selected_keys is not None and key not in selected_keys:
            continue
        st = build_statement(folder, a, v, e, prev)
        text = json.dumps(st, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
        sp = statement_path(folder, a["id"], v["v"])
        try:
            with open(sp, encoding="utf8") as f:
                if f.read() == text:
                    continue
        except OSError:
            pass
        os.makedirs(os.path.dirname(sp), exist_ok=True)
        with open(sp + ".tmp", "w", encoding="utf8") as f:
            f.write(text)
        os.replace(sp + ".tmp", sp)
        written += 1
    return written


def check_statements(folder, data, lock):
    """rule 8 -> (errors, notes): a statement whose subject digest differs from the lock is stale (error); a locked
    version without a statement is only noted (projects locked before 1.3 have none; `fd fill` writes them), so
    strict mode does not fail an otherwise clean project"""
    errors, notes = [], []
    for a, v, key, e, prev in version_pairs(data, lock):
        sp = statement_path(folder, a["id"], v["v"])
        rel = os.path.relpath(sp, folder)
        if not os.path.isfile(sp):
            notes.append("attestation: %s has no statement %s (run `fd fill`)" % (key, rel))
            continue
        try:
            with open(sp, encoding="utf8") as f:
                st = json.load(f)
            subj = st["subject"][0]["digest"]["sha256"]
        except Exception as ex:
            errors.append("attestation: %s is not an in-toto statement (%s)" % (rel, ex))
            continue
        if subj != e.get("sha256"):
            errors.append("attestation: %s is stale: subject %s… but the lock says %s… (run `fd fill`)" % (rel, subj[:12], str(e.get("sha256"))[:12]))
    return errors, notes


# ---- project.yaml -------------------------------------------------------------------------------------
def project_path(folder):
    for n in PROJECT_NAMES:
        p = os.path.join(folder, n)
        if os.path.isfile(p):
            return p
    return None


def _project_schema():
    for sp in PROJECT_SCHEMA_PATHS:
        if os.path.isfile(sp):
            with open(sp, encoding="utf8") as f:
                return json.load(f)
    return None


def load_project(folder):
    """-> (data or None, errors, warnings, path or None): rule 1"""
    p = project_path(folder)
    if not p:
        return None, [], [], None
    if yaml is None:
        return None, ["PyYAML is not installed"], [], p
    try:
        data, _ = read_yaml(p)
    except Exception as e:
        return None, ["cannot parse project.yaml: %s" % e], [], p
    errors, warnings = [], []
    if not isinstance(data, dict):
        return None, ["project.yaml is not a mapping"], [], p
    gate = ac.format_gate(data, "project.yaml")
    if gate:
        return data, [gate], [], p
    if data.get("project") != 1:
        errors.append("project.yaml: `project: 1` is required")
    pid = data.get("id")
    if not isinstance(pid, str) or not ac.ID_RE.match(pid):
        errors.append("project.yaml: `id` must be a slug like shielded-lane")
    elif pid != slug(os.path.basename(folder)):
        warnings.append("project.yaml: id `%s` differs from the folder name `%s`" % (pid, os.path.basename(folder)))
    if not isinstance(data.get("name"), str) or not data["name"].strip():
        errors.append("project.yaml: `name` is required")
    sch = _project_schema()
    if jsonschema and sch:
        for e in sorted(jsonschema.Draft202012Validator(sch).iter_errors(data), key=lambda e: list(e.path)):
            where = "/".join(str(x) for x in e.path) or "project"
            msg = "project.yaml schema: %s: %s" % (where, e.message[:160])
            if msg not in errors:
                errors.append(msg)
    return data, errors, warnings, p


def layout_of(proj):
    lay = dict(LAYOUT)
    lay.update({k: v for k, v in ((proj or {}).get("layout") or {}).items() if isinstance(v, str)})
    return lay


# ---- media probes (rule 6) ----------------------------------------------------------------------------
def _header_size(path):
    """width/height from a PNG, JPEG or GIF header, no tools needed"""
    with open(path, "rb") as f:
        head = f.read(32)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", head[16:24])
        if head[:6] in (b"GIF87a", b"GIF89a"):
            return struct.unpack("<HH", head[6:10])
        if head[:2] == b"\xff\xd8":
            f.seek(2)
            while True:
                marker = f.read(2)
                if len(marker) < 2 or marker[0] != 0xFF:
                    return None
                if marker[1] in (0xD8, 0x01) or 0xD0 <= marker[1] <= 0xD7:
                    continue
                (seglen,) = struct.unpack(">H", f.read(2))
                if 0xC0 <= marker[1] <= 0xCF and marker[1] not in (0xC4, 0xC8, 0xCC):        # SOFn
                    _, h, w = struct.unpack(">BHH", f.read(5))
                    return (w, h)
                f.seek(seglen - 2, 1)
    return None


def _svg_size(path):
    with open(path, "r", encoding="utf8", errors="replace") as f:
        head = f.read(4096)
    vb = re.search(r'viewBox=["\']\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)', head)
    if vb:
        return (int(float(vb.group(1))), int(float(vb.group(2))))
    w = re.search(r'\swidth=["\']([\d.]+)(px)?["\']', head)
    h = re.search(r'\sheight=["\']([\d.]+)(px)?["\']', head)
    return (int(float(w.group(1))), int(float(h.group(1)))) if w and h else None


def image_size(path):
    """(width, height) or None: sips on macOS, else identify, else the header parser"""
    if ext_of(path) == "svg":
        return _svg_size(path)
    try:
        if sys.platform == "darwin" and shutil.which("sips"):
            r = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path], capture_output=True, text=True, timeout=30)
            got = dict(re.findall(r"pixel(Width|Height):\s*(\d+)", r.stdout))
            if "Width" in got and "Height" in got:
                return (int(got["Width"]), int(got["Height"]))
        elif shutil.which("identify"):
            r = subprocess.run(["identify", "-format", "%w %h", path + "[0]"], capture_output=True, text=True, timeout=30)
            w, h = r.stdout.split()[:2]
            return (int(w), int(h))
    except Exception:
        pass
    try:
        return _header_size(path)
    except Exception:
        return None


def mp4_faststart(path):
    """True when the top-level `moov` atom precedes `mdat`; None when either is missing"""
    order, pos, total = [], 0, os.path.getsize(path)
    with open(path, "rb") as f:
        while pos + 8 <= total:
            f.seek(pos)
            size, typ = struct.unpack(">I4s", f.read(8))
            hdr = 8
            if size == 1:
                size, hdr = struct.unpack(">Q", f.read(8))[0], 16
            elif size == 0:
                size = total - pos
            order.append(typ.decode("latin1"))
            if size < hdr:
                break
            pos += size
    if "moov" in order and "mdat" in order:
        return order.index("moov") < order.index("mdat")
    return None


def video_info(path):
    """{video, audio, width, height, fps, duration_s, faststart} via ffprobe; {} when ffprobe is missing"""
    if not shutil.which("ffprobe"):
        return {}
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
                           capture_output=True, text=True, timeout=60)
        d = json.loads(r.stdout or "{}")
    except Exception:
        return {}
    out = {"audio": "none"}
    for st in d.get("streams") or []:
        if st.get("codec_type") == "video" and "video" not in out:
            out["video"] = st.get("codec_name")
            out["width"], out["height"] = int(st.get("width") or 0), int(st.get("height") or 0)
            num, _, den = str(st.get("r_frame_rate") or "0/1").partition("/")
            out["fps"] = round(float(num) / float(den or 1), 3) if float(den or 1) else None
        elif st.get("codec_type") == "audio" and out["audio"] == "none":
            out["audio"] = st.get("codec_name")
    if (d.get("format") or {}).get("duration"):
        out["duration_s"] = float(d["format"]["duration"])
    if ext_of(path) in ("mp4", "mov", "m4v"):
        try:
            out["faststart"] = mp4_faststart(path)
        except Exception:
            out["faststart"] = None
    return out


def probe_violations(path, pol):
    """-> (violations, notes) of one file against one `formats` policy"""
    viol, notes, ext = [], [], ext_of(path)
    if pol.get("ext") and ext not in pol["ext"]:
        viol.append("extension .%s not in %s" % (ext, list(pol["ext"])))
    if pol.get("name") and not fnmatch.fnmatch(os.path.basename(path), pol["name"]):
        viol.append("name does not match %s" % pol["name"])
    size = os.path.getsize(path)
    if pol.get("max_bytes") and size > pol["max_bytes"]:
        viol.append("%d bytes > max_bytes %d" % (size, pol["max_bytes"]))
    dims, info = None, {}
    if ext in IMAGE_EXT:
        dims = image_size(path)
    elif ext in VIDEO_EXT:
        info = video_info(path)
        dims = (info["width"], info["height"]) if info.get("width") else None
    wants_dims = any(k in pol for k in ("min_width", "max_width", "min_height", "max_height", "aspect"))
    if wants_dims and not dims:
        notes.append("could not read width/height of %s" % os.path.basename(path))
    if dims:
        w, h = dims
        for key, val in (("min_width", w), ("max_width", w), ("min_height", h), ("max_height", h)):
            if key in pol and (val < pol[key] if key.startswith("min") else val > pol[key]):
                viol.append("%s %d violates %s %d" % (key.split("_")[1], val, key, pol[key]))
        if pol.get("aspect"):
            aw, ah = (int(x) for x in pol["aspect"].split(":"))
            if h and abs(w / h - aw / ah) > 0.02:
                viol.append("aspect %dx%d is not %s" % (w, h, pol["aspect"]))
    if ext in VIDEO_EXT:
        if not info:
            notes.append("ffprobe missing: %s not probed" % os.path.basename(path))
        else:
            if pol.get("video") and info.get("video") != pol["video"]:
                viol.append("video codec %s is not %s" % (info.get("video"), pol["video"]))
            if pol.get("audio") and info.get("audio") != pol["audio"]:
                viol.append("audio codec %s is not %s" % (info.get("audio"), pol["audio"]))
            if pol.get("faststart") and info.get("faststart") is False:
                viol.append("not faststart (moov after mdat); re-mux with -movflags +faststart")
            if pol.get("max_fps") and info.get("fps") and info["fps"] > pol["max_fps"] + 0.01:
                viol.append("fps %s > max_fps %s" % (info["fps"], pol["max_fps"]))
            if pol.get("max_duration_s") and info.get("duration_s", 0) > pol["max_duration_s"]:
                viol.append("duration %.1fs > max_duration_s %s" % (info["duration_s"], pol["max_duration_s"]))
    return viol, notes


# ---- check: rules 1–7 ---------------------------------------------------------------------------------
def manifest_files(folder, data):
    """[(where, artifact, version or None, key, rel, abs)] for every `path` in the manifest"""
    out = []
    for i, a in enumerate((data or {}).get("artifacts") or []):
        if not isinstance(a, dict) or not a.get("id"):
            continue
        where = "artifacts[%d] (%s)" % (i, a["id"])
        if a.get("path"):
            out.append((where, a, None, a["id"], a["path"], ac.expand(folder, a["path"])))
        for j, v in enumerate(a.get("versions") or []):
            if isinstance(v, dict) and v.get("path"):
                out.append(("%s.versions[%d]" % (where, j), a, v, "%s@%s" % (a["id"], v.get("v")), v["path"], ac.expand(folder, v["path"])))
    return out


def unreferenced_files(adir, files):
    """files under artifacts/ (dotfiles skipped) that no manifest path names, directly or by a parent folder inside artifacts/"""
    named = set()
    for _, _, _, _, _, fp in files:
        if fp and under(adir, fp):
            named.add(os.path.realpath(fp))
    out = []
    for root, dirs, names in os.walk(adir):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for n in sorted(names):
            if n.startswith("."):
                continue
            fp = os.path.realpath(os.path.join(root, n))
            if not any(fp == x or fp.startswith(x + os.sep) for x in named):
                out.append(fp)
    return out


def check_folder(folder, strict=False):
    folder, errors, warnings, notes = os.path.realpath(folder), [], [], []
    proj, pe, pw, pp = load_project(folder)                                           # rule 1
    errors += pe
    warnings += pw
    data, me, mw, mp = ac.load_manifest(folder)                                        # rule 2
    errors += me
    warnings += mw
    # a version that is git-ignored here and pinned in the lock can be fetched (`fd pull`): a note, never a --strict error,
    # or every session in a fresh clone is blocked by files it cannot make (agent-dashboard ed46562)
    notes += [w for w in warnings if "pinned in the lock" in w]
    warnings = [w for w in warnings if "pinned in the lock" not in w]
    try:                                                                               # generated exports older than their sources
        import fd_meta
        for stale in fd_meta.stale_exports(folder):
            warnings.append("%s is older than project.yaml/artifacts.yaml: run `fd export`" % stale)
    except ImportError:
        pass
    if not pp:
        notes.append("no project.yaml (`fd adopt` writes a minimal one)")
    if not mp:
        (errors if not pp else notes).append("no artifacts.yaml" + ("" if pp else ": not a project folder"))
    lay = layout_of(proj)
    adir = os.path.join(folder, lay["artifacts"])
    files = manifest_files(folder, data)
    governed = os.path.isdir(adir) or any(fp and under(adir, fp) for *_, fp in files)
    if data and governed:
        for fp in unreferenced_files(adir, files):                                    # rule 3
            warnings.append("unreferenced: %s is not named by any artifact or version" % os.path.relpath(fp, folder))
        for where, a, v, key, rel, fp in files:
            if not fp or not os.path.exists(fp):
                continue
            if not under(adir, fp):                                                   # rule 4
                if a.get("category") in ("content", "model") and os.path.isfile(fp):
                    warnings.append("%s: %s lives outside %s/" % (where, rel, lay["artifacts"]))
                continue
            inside = os.path.relpath(os.path.realpath(fp), os.path.realpath(adir)).split(os.sep)   # rule 5
            if inside[0] != a["id"]:
                errors.append("%s: %s should live in %s/%s/" % (where, rel, lay["artifacts"], a["id"]))
            if v is not None:
                m = VNAME_RE.match(inside[-1])
                if len(inside) != 2 or not m or m.group("stem") != a["id"] or ac._vkey(m.group("v")) != ac._vkey(v.get("v")):
                    errors.append("%s: %s should be %s/%s/%s-v%s.%s" % (where, rel, lay["artifacts"], a["id"], a["id"], v.get("v"), ext_of(rel) or "ext"))
    formats = (proj or {}).get("formats") or {}
    if data and isinstance(formats, dict):                                            # rule 6
        for where, a, v, key, rel, fp in files:
            pol = formats.get(a.get("type"))
            if isinstance(pol, dict) and fp and os.path.isfile(fp):
                viol, nn = probe_violations(fp, pol)
                warnings += ["formats.%s: %s: %s" % (a["type"], rel, x) for x in viol]
                notes += nn
    real = [(key, rel, fp) for _, _, _, key, rel, fp in files if fp and os.path.isfile(fp)]
    if data:                                                                          # rule 7
        lock = ac.load_lock(folder)
        if real and not lock:
            warnings.append("no %s (run `fd fill`)" % ac.LOCK_NAME)
        elif lock:
            entries = lock.get("entries") or {}
            for key, rel, fp in real:
                e, st = entries.get(key), os.stat(fp)
                if not e:
                    warnings.append("lock: %s (%s) is not in %s (run `fd fill`)" % (key, rel, ac.LOCK_NAME))
                elif e.get("size_bytes") != st.st_size or (e.get("mtime") != int(st.st_mtime) and e.get("sha256") != ac._sha256(fp)):
                    warnings.append("lock: %s changed since %s was written (run `fd fill`)" % (rel, ac.LOCK_NAME))
    if data:                                                                          # rule 8
        se, sn = check_statements(folder, data, ac.load_lock(folder))
        errors += se
        notes += sn
    warnings += check_hooks(folder)                                                   # rule 9
    errors += merge_markers(folder)                                                   # rule 10
    for d, kind, name in ((proj, "project", "project.yaml"), (data, "manifest", "artifacts.yaml")):
        need = ac.needs_format(d, kind)
        if need > (1, 0) and (ac.parse_format((d or {}).get("requires")) or (1, 0)) < need:
            notes.append("%s uses format %d.%d keys without `requires: \"%d.%d\"`: `fd upgrade` stamps it" % ((name,) + need + need))
    if strict:
        errors += ["(strict) " + w for w in warnings]
        warnings = []
    n = len((data or {}).get("artifacts") or []) if isinstance(data, dict) else 0
    return {"folder": folder, "project": pp, "manifest": mp, "ok": not errors, "artifacts": n,
            "errors": errors, "warnings": warnings, "notes": notes, "id": (proj or {}).get("id")}


TEMPLATE_OWNED = ("AGENTS.md", "CLAUDE.md", ".flightdeck", ".claude", ".codex", ".cursor", ".agents", ".github", ".pre-commit-config.yaml")


def merge_markers(folder):
    """rule 10: `fd upgrade` leaves conflict markers in template-owned files; committing them breaks hooks and rules"""
    out = []
    for top in TEMPLATE_OWNED:
        base = os.path.join(folder, top)
        paths = [base] if os.path.isfile(base) else [os.path.join(r, f) for r, _, fs in os.walk(base) for f in fs] if os.path.isdir(base) else []
        for fp in paths:
            try:
                with open(fp, encoding="utf8") as f:
                    if any(l.startswith(("<<<<<<< ", ">>>>>>> ")) for l in f):
                        out.append("merge markers in %s: resolve the `fd upgrade` conflict" % os.path.relpath(fp, folder))
            except (OSError, UnicodeDecodeError):
                continue
    return out


HOOK_CONFIGS = (".claude/settings.json", ".codex/hooks.json", ".cursor/hooks.json")


def check_hooks(folder):
    """rule 9: every hook script a harness config names exists, and Claude/Codex hooks do not run relative to cwd
    (a session opened in a subfolder would lose its gates silently: a missing hook is a non-blocking error)"""
    out = []
    for cfg in HOOK_CONFIGS:
        path = os.path.join(folder, cfg)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf8") as f:
                text = f.read()
            json.loads(text)
        except (OSError, ValueError) as e:
            out.append("hooks: %s does not parse (%s): its hooks are off" % (cfg, e))
            continue
        for cmd in re.findall(r'"command"\s*:\s*"((?:[^"\\]|\\.)*)"', text):
            m = re.search(r"\.flightdeck/hooks/([\w.-]+\.py)", cmd)
            if not m:
                continue
            if not os.path.isfile(os.path.join(folder, ".flightdeck", "hooks", m.group(1))):
                out.append("hooks: %s runs .flightdeck/hooks/%s, which is missing (`fd upgrade`)" % (cfg, m.group(1)))
            elif not cfg.startswith(".cursor") and re.match(r"python3?\s+\.flightdeck/", cmd):
                out.append("hooks: %s runs %s relative to cwd; a session opened in a subfolder loses it (`fd upgrade`)" % (cfg, m.group(1)))
    return sorted(set(out))


def refresh_lock(folder, data, selected_keys=None):
    old = ac.load_lock_for_add(folder) if selected_keys is not None else ac.load_lock(folder)
    lock = ac.fill_lock(folder, data, old, host=hostname(), selected_keys=selected_keys)
    lp = ac.write_lock(folder, lock)
    write_statements(folder, data, lock, selected_keys=selected_keys)
    return lp, len(lock["entries"])


# ---- commands -----------------------------------------------------------------------------------------
def cmd_check(a):
    worst = 0
    for folder in a.folders or ["."]:
        folder = os.path.abspath(os.path.expanduser(folder))
        r = check_folder(folder, a.strict)
        if a.json:
            print(json.dumps(r, indent=2))
        else:
            print("%s: %d artifacts, %d errors, %d warnings" % (folder, r["artifacts"], len(r["errors"]), len(r["warnings"])))
            for kind, rows in (("error  ", r["errors"]), ("warning", r["warnings"]), ("note   ", r["notes"])):
                for x in rows:
                    print("  %s %s" % (kind, x))
        worst = max(worst, 0 if r["ok"] else 1)
    return worst


def cmd_fill(a):
    folder = find_root(a.folder)
    data, errors, _, mp = ac.load_manifest(folder)
    if not mp:
        die("no artifacts.yaml in %s" % folder)
    if errors:
        die("fix the manifest first:\n  " + "\n  ".join(errors))
    lp, n = refresh_lock(folder, data)
    print("%s: %d files" % (os.path.relpath(lp, folder), n))
    return 0


def _load_or_new_manifest(folder, proj):
    mp = ac.manifest_path(folder)
    if mp:
        data, header = read_yaml(mp)
        if not isinstance(data, dict) or not isinstance(data.get("artifacts"), list):
            die("%s is not a manifest with an `artifacts` list" % os.path.basename(mp))
        return data, header or MANIFEST_HEADER, mp
    name = (proj or {}).get("name") or os.path.basename(folder)
    return {"manifest": 1, "project": name, "artifacts": []}, MANIFEST_HEADER, os.path.join(folder, "artifacts.yaml")


def next_v(versions):
    return max((ac._vkey(v.get("v"))[0] for v in versions if isinstance(v, dict) and "v" in v), default=0) + 1


def cmd_add(a):
    folder = find_root(a.folder)
    proj = load_project(folder)[0] or {}
    lay = layout_of(proj)
    src = os.path.abspath(os.path.expanduser(a.file))
    if not os.path.isfile(src):
        die("not a file: %s" % a.file)
    if not ac.ID_RE.match(a.id):
        die("--id must be a slug like explainer-film")
    if under(os.path.join(folder, lay["artifacts"]), src) and not a.force:
        # a file already sitting in artifacts/ unreferenced was not made through fd; filing it would claim this
        # session made it (evals t8: Codex did exactly that with a stray file)
        die("fd: %s is already inside %s/ but not in the manifest, so this session did not file it. If you made it "
            "just now, move it to %s/out/ and add it from there. If you did not make it, record it without claiming "
            "authorship: python3 .flightdeck/fd.py adopt . (or ask the user what it is)." %
            (os.path.relpath(src, folder), lay["artifacts"], lay["code"]))
    data, header, mp = _load_or_new_manifest(folder, proj)
    # Do not move the source or change the manifest if historical facts cannot be read.
    ac.load_lock_for_add(folder)
    art = next((x for x in data["artifacts"] if isinstance(x, dict) and x.get("id") == a.id), None)
    if art is None:
        if not (a.type and a.title):
            die("%s is a new artifact: --type and --title are required" % a.id)
        if a.type not in CATEGORY_OF:
            die("--type must be one of %s" % sorted(CATEGORY_OF))
        art = {"id": a.id, "category": CATEGORY_OF[a.type], "type": a.type, "title": a.title}
        data["artifacts"].append(art)
    versions = [v for v in (art.get("versions") or []) if isinstance(v, dict)]
    n = next_v(versions)
    rel = "%s/%s/%s-v%d.%s" % (lay["artifacts"], a.id, a.id, n, ext_of(src) or "bin")
    dest = os.path.join(folder, rel)
    if os.path.exists(dest):
        die("%s exists; versioned files are never overwritten" % rel)
    pol = ((proj.get("formats") or {}).get(art.get("type"))) if isinstance(proj.get("formats"), dict) else None
    if isinstance(pol, dict):
        viol, notes = probe_violations(src, pol)
        for x in notes:
            print("note: " + x)
        if viol and not a.force:
            die(refusal(src, art["type"], viol, pol))
    if art.get("type") in NEEDS_INGREDIENT and not a.ingredient:
        msg = ("a %s needs the script or data it was made from: generate it from a file under %s/ and pass "
               "--ingredient %s/<script> (repeatable)" % (art["type"], lay["code"], lay["code"]))
        if a.strict:
            die("fd: " + msg)
        print("warning: " + msg, file=sys.stderr)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    (shutil.copy2 if a.copy else shutil.move)(src, dest)
    sd = session_from_env()
    by = a.by or sd.get("harness")
    session = normalise_session(a.session or sd.get("session_id"), by)
    request = None if a.session else sd.get("request")
    sid = (session or "").partition(":")[2]
    model = model_of(by, sid)
    if model and a.model and a.model != model:
        print("warning: --model %s disagrees with the session transcript (%s); recording %s" % (a.model, model, model), file=sys.stderr)
    model = model or a.model
    prompt = a.prompt
    if prompt and a.redact_prompt:
        prompt = "sha256:" + hashlib.sha256(prompt.encode("utf8")).hexdigest()
    entry = {"v": n, "date": a.date or today(), "path": rel}
    if not a.date:
        entry["built_at"] = now_rfc3339()
    for k, val in (("note", a.note), ("by", by), ("model", model), ("session", session), ("request", request), ("prompt", prompt),
                   ("ingredients", a.ingredient or None), ("commit", git_commit(folder)), ("public", True if a.public else None)):
        if val:
            entry[k] = val
    art["versions"] = [entry] + versions
    ac.stamp_format(data, "manifest")
    write_yaml(mp, data, header)
    lp, cnt = refresh_lock(folder, data, selected_keys={f"{a.id}@{n}"})
    print("%s v%d -> %s (%s, %s: %d files)" % (a.id, n, rel, os.path.basename(mp), os.path.basename(lp), cnt))
    return 0


def guess_type(rel):
    ext, low = ext_of(rel), rel.lower()
    if ext in ("pdf", "html"):
        return "paper" if ext == "pdf" and "paper" in low else ("deck" if "deck" in os.path.basename(low) else "doc")
    return TYPE_BY_EXT.get(ext, "doc")


TOOLING = [".flightdeck", ".agents/skills/fd-add", ".claude/skills/fd-add", ".claude/settings.json", ".codex/hooks.json", ".cursor/hooks.json"]


def _adopt_tooling(folder):
    """copy the template's checker, skill and hooks into an existing repo without overwriting anything the repo
    already has (a repo with its own .claude/settings.json keeps it and is told to merge the hooks by hand)"""
    tdir = next((os.path.join(d, "base") for d in TEMPLATE_DIRS if os.path.isdir(os.path.join(d, "base"))), None)
    if not tdir:
        die("no base template found")
    copied, kept = [], []
    for rel in TOOLING:
        src, dst = os.path.join(tdir, rel), os.path.join(folder, rel)
        if os.path.islink(src):
            if os.path.lexists(dst): kept.append(rel); continue
            os.makedirs(os.path.dirname(dst), exist_ok=True); os.symlink(os.readlink(src), dst); copied.append(rel); continue
        if os.path.isdir(src):
            for root, dirs, names in os.walk(src):
                for n in names:
                    s_, d_ = os.path.join(root, n), os.path.join(dst, os.path.relpath(root, src), n)
                    if os.path.lexists(d_) and n not in ("fd.py", "artifacts_check.py", "project-1.json", "artifacts-1.json"):
                        kept.append(os.path.relpath(d_, folder)); continue
                    os.makedirs(os.path.dirname(d_), exist_ok=True)
                    if os.path.islink(s_): os.symlink(os.readlink(s_), d_)
                    else: shutil.copy2(s_, d_)
                    copied.append(os.path.relpath(d_, folder))
        else:
            if os.path.lexists(dst): kept.append(rel); continue
            os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst); copied.append(rel)
    gi = os.path.join(folder, ".gitignore")
    want = [".flightdeck/session.json", "AGENTS.local.md"]
    have = open(gi, encoding="utf8").read() if os.path.isfile(gi) else ""
    missing = [w for w in want if w not in have]
    if missing:
        with open(gi, "a", encoding="utf8") as f:
            f.write("\n# Flight Deck tooling (fd adopt --tooling)\n" + "\n".join(missing) + "\n")
    print("tooling: %d file(s) copied, %d kept as they were%s" % (len(copied), len(kept), "" if not kept else " (" + ", ".join(sorted(set(kept))[:6]) + ")"))
    if ".claude/settings.json" in kept:
        print("  note: .claude/settings.json already existed; merge the hooks from the template by hand")


def cmd_adopt(a):
    folder = os.path.realpath(os.path.expanduser(a.folder))
    if a.tooling:
        _adopt_tooling(folder)
    proj, _, _, pp = load_project(folder)
    if not pp:
        pid = slug(os.path.basename(folder))
        proj = {"project": 1, "id": pid, "name": pid.replace("-", " ").title(), "status": "active", "created": today()}
        write_yaml(os.path.join(folder, "project.yaml"), proj, "# Flight Deck project metadata v1 (schema: .flightdeck/project-1.json)\n")
        print("wrote project.yaml (id %s)" % pid)
    lay = layout_of(proj)
    adir = os.path.join(folder, lay["artifacts"])
    data, header, mp = _load_or_new_manifest(folder, proj)
    loose = unreferenced_files(adir, manifest_files(folder, data)) if os.path.isdir(adir) else []
    for fp in loose:
        parts = os.path.relpath(fp, adir).split(os.sep)
        m = VNAME_RE.match(parts[-1])
        aid = parts[0] if len(parts) > 1 and ac.ID_RE.match(parts[0]) else slug(m.group("stem") if m else os.path.splitext(parts[-1])[0])
        art = next((x for x in data["artifacts"] if isinstance(x, dict) and x.get("id") == aid), None)
        if art is None:
            typ = guess_type(fp)
            art = {"id": aid, "category": CATEGORY_OF[typ], "type": typ, "title": aid.replace("-", " ").title()}
            data["artifacts"].append(art)
        versions = [v for v in (art.get("versions") or []) if isinstance(v, dict)]
        canonical = m and parts == [aid, "%s-v%s.%s" % (aid, m.group("v"), m.group("ext"))]
        if canonical and str(parse_v(m.group("v"))) not in {str(v.get("v")) for v in versions}:
            v, rel = parse_v(m.group("v")), os.path.relpath(fp, folder)
        else:
            v = next_v(versions)
            rel = "%s/%s/%s-v%d.%s" % (lay["artifacts"], aid, aid, v, ext_of(fp) or "bin")
            os.makedirs(os.path.dirname(os.path.join(folder, rel)), exist_ok=True)
            shutil.move(fp, os.path.join(folder, rel))
        made = datetime.date.fromtimestamp(os.stat(os.path.join(folder, rel)).st_mtime).isoformat()
        versions.append({"v": v, "date": made, "path": rel, "note": "adopted by fd adopt"})
        art["versions"] = sorted(versions, key=lambda x: ac._vkey(x.get("v")), reverse=True)
        print("adopted %s -> %s v%s" % (os.path.relpath(fp, folder), aid, v))
    if data["artifacts"]:
        write_yaml(mp, data, header)
        refresh_lock(folder, data)
    print("%d file(s) adopted" % len(loose))
    return 0


def _fill_tree(tdir, dest, fills, harness, skip_git=False):
    """copy (or rewrite in place when tdir == dest) every text file, replacing {{key}} placeholders"""
    for root, dirs, names in os.walk(tdir):
        dirs.sort()
        if skip_git and ".git" in dirs:
            dirs.remove(".git")
        for n in names:
            src, to = os.path.join(root, n), os.path.join(dest, os.path.relpath(root, tdir), n)
            os.makedirs(os.path.dirname(to), exist_ok=True)
            if os.path.islink(src):
                # a template symlink (e.g. .claude/skills/fd-add -> ../../.agents/skills/fd-add) stays a symlink
                if src != to:
                    os.symlink(os.readlink(src), to)
                continue
            try:
                with open(src, encoding="utf8") as f:
                    text = f.read()
                for k, v in fills.items():
                    text = text.replace("{{" + k + "}}", v)
                if n in PROJECT_NAMES and harness != "claude":
                    text = text.replace("harness: claude", "harness: " + harness)
                with open(to, "w", encoding="utf8") as f:
                    f.write(text)
                if src != to:
                    shutil.copymode(src, to)
            except UnicodeDecodeError:
                if src != to:
                    shutil.copy2(src, to)


def _fills(name, summary):
    summary = summary or "one line on what this produces"
    # summary_yaml: a quoted scalar, so a summary with ": " or "#" stays valid YAML
    return {"project": name, "id": slug(name), "date": today(), "summary": summary, "summary_yaml": json.dumps(summary)}


def cmd_init(a):
    """a folder cloned from the GitHub template (dmarzzz/cyber-project-template) still carries the
    {{placeholders}}; fill them in place, then refresh the lock. Idempotent: a second run finds nothing to fill."""
    folder = os.path.abspath(os.path.expanduser(a.folder or "."))
    name = (a.name or os.path.basename(folder)).strip()
    if not re.match(r"^[A-Za-z0-9 _-]+$", name):
        die("project name: letters, digits, - _ and spaces")
    if not os.path.isfile(os.path.join(folder, "project.yaml")):
        die("%s has no project.yaml: not a Flight Deck project" % folder)
    _fill_tree(folder, folder, _fills(name, a.summary), a.harness, skip_git=True)
    data, errors, _, mp = ac.load_manifest(folder)
    if mp and not errors:
        refresh_lock(folder, data)
    print("%s: filled as %s (%s)" % (folder, name, slug(name)))
    return 0


def _stamp_template_commit(tdir, dest):
    """record the agent-status commit the template came from (`template.commit`, project.yaml v1.1), the base
    `fd upgrade` diffs against later; a template dir outside git leaves the stamp alone"""
    r = subprocess.run(["git", "-C", tdir, "rev-parse", "--short=12", "HEAD"], capture_output=True, text=True)
    if r.returncode != 0:
        return
    commit = r.stdout.strip()
    py = os.path.join(dest, "project.yaml")
    try:
        with open(py, encoding="utf8") as f:
            lines = f.read().split("\n")
    except OSError:
        return
    for i, line in enumerate(lines):
        if line.startswith("template:") and "commit:" not in line and line.rstrip().endswith("}"):
            body = line.rstrip()
            lines[i] = body[:-1] + ", commit: %s}" % commit
            break
    with open(py, "w", encoding="utf8") as f:
        f.write("\n".join(lines))


def cmd_new(a):
    name = a.name.strip()
    if not name or name.startswith(".") or "/" in name or len(name) > 64 or not re.match(r"^[A-Za-z0-9 _-]+$", name):
        die("project name: letters, digits, - _ and spaces, no slashes")
    tdir = next((os.path.join(d, a.template) for d in TEMPLATE_DIRS if os.path.isdir(os.path.join(d, a.template))), None)
    if not tdir or a.template.startswith(".") or "/" in a.template:
        die("no template named %s" % a.template)
    box = os.environ.get("FD_SANDBOX")                       # evals: log the call, stay inside the box, no GitHub
    if box:
        box = os.path.realpath(box)
        rec = json.dumps({"cwd": os.getcwd(), "name": name, "into": a.into, "github": a.github}) + "\n"
        for d in (box, os.getcwd()):                         # a sandboxed harness may not write the box itself
            try:
                with open(os.path.join(d, "fd-new.log"), "a", encoding="utf8") as f:
                    f.write(rec)
                break
            except OSError:
                continue
        a.github = False
        if not os.path.realpath(os.path.expanduser(a.into)).startswith(box + os.sep):
            a.into = os.getcwd() if os.path.realpath(os.getcwd()).startswith(box + os.sep) else box
    dest = os.path.join(os.path.abspath(os.path.expanduser(a.into)), name)
    if os.path.exists(dest):
        die("%s already exists" % dest)
    _fill_tree(tdir, dest, _fills(name, a.summary), a.harness)
    _stamp_template_commit(tdir, dest)
    git = lambda *args: subprocess.run(["git"] + list(args), cwd=dest, capture_output=True).returncode == 0
    if git("init", "-q"):
        git("add", "-A")
        git("-c", "user.email=flightdeck@local", "-c", "user.name=Flight Deck", "commit", "-q", "-m", "%s: new project from the %s template" % (name, a.template))
    print(dest)
    if a.github:
        # a private repo under the gh login, pushed; the deck's registry picks up the origin as the project's repo link
        repo = "%s/%s" % (a.github_owner, slug(name))
        r = subprocess.run(["gh", "repo", "create", repo, "--private", "--source", dest, "--push", "--description", a.summary or name], capture_output=True, text=True)
        if r.returncode != 0:
            die("gh repo create failed:\n" + (r.stderr or r.stdout).strip())
        print("https://github.com/" + repo)
    return 0


def _session_token():
    """a session Flight Deck launched carries a read-only capability token (docs/SECURITY-CAPS.md, Phase C) as a
    0600 file named by FLIGHTDECK_TOKEN_FILE (or, set by hand, FLIGHTDECK_TOKEN); None outside such a session"""
    t = os.environ.get("FLIGHTDECK_TOKEN", "").strip()
    if t:
        return t
    f = os.environ.get("FLIGHTDECK_TOKEN_FILE", "")
    try:
        with open(f, encoding="utf8") as fh:
            return fh.read().strip() or None
    except OSError:
        return None


def cmd_list(a):
    url = a.deck.rstrip("/") + "/projects"
    req = urllib.request.Request(url)
    tok = _session_token()
    if tok:
        req.add_header("Authorization", "Bearer " + tok)
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            print(json.dumps(json.loads(r.read().decode("utf8")), indent=2))
        return 0
    except urllib.error.HTTPError as e:
        print("%s: HTTP %d%s" % (url, e.code, " (the deck has no /projects route yet)" if e.code == 404 else ""))
    except (urllib.error.URLError, OSError) as e:
        print("no deck answering at %s (%s)" % (a.deck, getattr(e, "reason", e)))
    except ValueError:
        print("%s: not JSON" % url)
    return 1


def _select_versions(folder, data, lock, aid=None, every=False):
    pairs = [p for p in version_pairs(data, lock) if not aid or p[0]["id"] == aid]
    if aid and not pairs:
        die("no locked version of %s (run `fd fill`)" % aid)
    if every:
        return pairs
    latest = {}
    for p in pairs:
        latest[p[0]["id"]] = p                                    # version_pairs yields ascending: the last one wins
    return list(latest.values())


def cmd_attest(a):
    folder = find_root(getattr(a, 'folder_opt', None) or a.folder)
    data, errors, _, mp = ac.load_manifest(folder)
    if not mp:
        die("no artifacts.yaml in %s" % folder)
    lock = ac.load_lock(folder)
    if not lock:
        die("no %s (run `fd fill`)" % ac.LOCK_NAME)
    cosign = shutil.which("cosign")
    if not cosign and not a.dry_run:
        print("fd attest needs cosign: brew install cosign", file=sys.stderr)
        return 3
    targets = _select_versions(folder, data, lock, a.id, a.all)
    if not a.dry_run:
        print("note: keyless signing opens a browser login; the identity (your e-mail) is written to the public Rekor log.")
    rc = 0
    for art, v, key, e, prev in targets:
        sp = statement_path(folder, art["id"], v["v"])
        if not os.path.isfile(sp):
            write_statements(folder, data, lock)
        with open(sp, encoding="utf8") as f:
            st = json.load(f)
        fp = ac.expand(folder, v["path"])
        bp = bundle_path(folder, art["id"], v["v"])
        with tempfile.NamedTemporaryFile("w", suffix=".predicate.json", delete=False, encoding="utf8") as tf:
            json.dump(st["predicate"], tf, sort_keys=True)
            pred = tf.name
        cmd = [cosign or "cosign", "attest-blob", "--predicate", pred, "--type", "slsaprovenance1", "--bundle", bp, fp]
        if a.dry_run:
            print(" ".join(cmd))
            os.unlink(pred)
            continue
        r = subprocess.run(cmd)
        os.unlink(pred)
        if r.returncode != 0:
            rc = 1
            print("%s: cosign failed (%d)" % (key, r.returncode), file=sys.stderr)
        else:
            print("%s: %s" % (key, os.path.relpath(bp, folder)))
    return rc


def cmd_verify(a):
    folder = find_root(getattr(a, 'folder_opt', None) or a.folder)
    data, errors, _, mp = ac.load_manifest(folder)
    if not mp:
        die("no artifacts.yaml in %s" % folder)
    lock = ac.load_lock(folder)
    cosign = shutil.which("cosign")
    pairs = [p for p in version_pairs(data, lock) if not a.id or p[0]["id"] == a.id]
    found, failed = 0, 0
    for art, v, key, e, prev in pairs:
        bp = bundle_path(folder, art["id"], v["v"])
        if not os.path.isfile(bp):
            continue
        found += 1
        if not cosign:
            print("%s: unverified (no cosign)" % key)
            continue
        ident = ["--certificate-identity", a.identity] if a.identity else ["--certificate-identity-regexp", ".*"]
        issuer = ["--certificate-oidc-issuer", a.issuer] if a.issuer else ["--certificate-oidc-issuer-regexp", ".*"]
        cmd = [cosign, "verify-blob-attestation", "--bundle", bp, "--type", "slsaprovenance1"] + ident + issuer + [ac.expand(folder, v["path"])]
        if a.dry_run:
            print(" ".join(cmd))
            continue
        r = subprocess.run(cmd, capture_output=True, text=True)
        ok = r.returncode == 0
        failed += 0 if ok else 1
        print("%s: %s%s" % (key, "pass" if ok else "FAIL", "" if ok else " (" + (r.stderr or r.stdout).strip().splitlines()[-1:][0] + ")" if (r.stderr or r.stdout).strip() else ""))
    if not found:
        print("no bundles under %s/ (run `fd attest`)" % ATTEST_DIR)
    if found and not cosign:
        return 3
    return 1 if failed else 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="fd", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", metavar="command")
    flag = lambda p, name, **kw: p.add_argument(name, **kw)
    p = sub.add_parser("new", help="scaffold a project from a template, git init")
    flag(p, "name"), flag(p, "--template", default="base"), flag(p, "--summary"), flag(p, "--into", default="~", help="parent folder (default ~)")
    p.add_argument("--github", action="store_true", help="also create a private GitHub repo (gh) and push")
    flag(p, "--github-owner", default="dmarzzz")
    flag(p, "--harness", default="claude", choices=["claude", "codex", "nanocodex", "hermes"])
    p.set_defaults(fn=cmd_new)
    p = sub.add_parser("init", help="fill the {{placeholders}} of a folder made from the GitHub template, in place")
    p.add_argument("folder", nargs="?", default=".")
    flag(p, "--name"), flag(p, "--summary"), flag(p, "--harness", default="claude", choices=["claude", "codex", "nanocodex", "hermes"])
    p.set_defaults(fn=cmd_init)
    p = sub.add_parser("check", help="rules 1-7 of docs/PROJECTS.md; exit 1 on errors")
    flag(p, "folders", nargs="*"), flag(p, "--strict", action="store_true", help="warnings fail too (CI)"), flag(p, "--json", action="store_true")
    p.set_defaults(fn=cmd_check)
    p = sub.add_parser("fill", help="write artifacts.lock.json")
    flag(p, "folder", nargs="?", default=".")
    p.set_defaults(fn=cmd_fill)
    p = sub.add_parser("add", help="file the next version of an artifact into artifacts/")
    flag(p, "file"), flag(p, "--id", required=True), flag(p, "--title", help="required for a new id")
    flag(p, "--type", help="required for a new id: " + ", ".join(sorted(CATEGORY_OF)))
    for name in ("--note", "--by", "--model", "--session", "--prompt", "--date"):
        flag(p, name)
    flag(p, "--ingredient", action="append", help="path or url it was made from (repeatable; digested into the lock)")
    flag(p, "--redact-prompt", action="store_true", help="store only sha256:<hex> of the prompt in the manifest")
    for name, h in (("--public", "may go to the CDN"), ("--copy", "copy instead of move"), ("--force", "add even when the file violates `formats` (humans only)"),
                    ("--strict", "refuse a figure/film/dataset/deck with no --ingredient")):
        flag(p, name, action="store_true", help=h)
    flag(p, "--folder", default=".", help="the project (default: nearest project.yaml/artifacts.yaml above cwd)")
    p.set_defaults(fn=cmd_add)
    p = sub.add_parser("adopt", help="manifest entries for unreferenced files under artifacts/")
    flag(p, "folder", nargs="?", default=".")
    p.add_argument("--tooling", action="store_true", help="also copy the template's checker, fd-add skill and hooks (never overwrites)")
    p.set_defaults(fn=cmd_adopt)
    # metadata exports + template upgrade live in their own modules (cockpit/fd_meta.py, cockpit/fd_upgrade.py)
    for _mod in ("fd_meta", "fd_upgrade"):
        try:
            __import__(_mod).add_parser(sub, flag)
        except ImportError:
            pass
    p = sub.add_parser("list", help="projects the local deck knows")
    flag(p, "--deck", default=DECK_URL)
    p.set_defaults(fn=cmd_list)
    p = sub.add_parser("attest", help="sign the in-toto statements keyless with cosign (attestations/*.sigstore.json)")
    flag(p, "--id"), flag(p, "--all", action="store_true", help="every version, not only the latest of each artifact")
    flag(p, "--dry-run", action="store_true", help="print the cosign commands instead of running them")
    p.add_argument("folder", nargs="?", default="."), flag(p, "--folder", dest="folder_opt", help="the same, as a flag")
    p.set_defaults(fn=cmd_attest)
    p = sub.add_parser("verify", help="verify the sigstore bundles with cosign")
    flag(p, "--id"), flag(p, "--identity", help="expected certificate identity (e-mail)"), flag(p, "--issuer", help="expected OIDC issuer")
    flag(p, "--dry-run", action="store_true")
    p.add_argument("folder", nargs="?", default="."), flag(p, "--folder", dest="folder_opt", help="the same, as a flag")
    p.set_defaults(fn=cmd_verify)
    a = ap.parse_args(argv)
    if not a.cmd:
        ap.print_help()
        return 2
    if yaml is None:
        die("PyYAML is not installed (pip install pyyaml)")
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
