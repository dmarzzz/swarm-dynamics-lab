#!/usr/bin/env python3
"""artifacts_check — validate a project folder's artifacts.yaml against docs/ARTIFACTS.md (manifest v1).

  python3 artifacts_check.py <folder> [<folder> ...]   exit 1 on any error; warnings still pass
  python3 artifacts_check.py --strict <folder>          warnings fail too (CI)
  python3 artifacts_check.py --json <folder>            machine-readable {ok, errors, warnings, manifest}
  python3 artifacts_check.py --fill <folder>            write artifacts.lock.json: sha256 / size / mime / media
                                                        probes (ffprobe, pdfinfo) for every file the manifest names
  python3 artifacts_check.py --install-ci <folder>      copy the schemas, this checker, fd.py, a GitHub Action and a
                                                        pre-commit hook into the repo (.flightdeck/, .github/)

The manifest is human-written (docs/ARTIFACTS.md); the schema (schemas/artifacts-1.json) is enforced when
`jsonschema` is importable, the structural rules below always. Machine facts never go into the manifest:
they live in artifacts.lock.json next to it, keyed by artifact id and "id@version".
Also imported by the deck server (load_manifest / check_manifest), so keep it stdlib + PyYAML (+ optional jsonschema).
"""
import hashlib
import json
import mimetypes
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from datetime import date

try:
    import yaml
except ImportError:                     # the deck degrades to "no manifest" rather than dying
    yaml = None
try:
    import jsonschema
except ImportError:
    jsonschema = None

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATHS = (os.path.join(HERE, "..", "schemas", "artifacts-1.json"), os.path.join(HERE, "artifacts-1.json"))
LOCK_NAME = "artifacts.lock.json"
# the newest fd format this checker reads. Bump the minor whenever fd starts writing a key a checker of the previous
# minor would reject (the schemas are closed), and teach needs_format() to spot it. 1.0 = the template of 2026-09-24;
# 1.1 = identity + relations + template stamp (09-24); 1.2 = versions[].request, project `agent_branches`,
# serving.cdn "private"/"off", launch.setup/resume/archive/ports (research 08 §3.5, ROADMAP R13-14).
FORMAT = (1, 2)


def parse_format(v):
    m = re.match(r"^(\d+)\.(\d+)$", str(v or ""))
    return (int(m.group(1)), int(m.group(2))) if m else None


def format_gate(data, name):
    """an error when `data` says it needs a newer checker than this one, else None. Callers stop there instead of
    reporting the newer keys as schema violations."""
    need = parse_format((data or {}).get("requires")) if isinstance(data, dict) else None
    if need and need > FORMAT:
        return ("%s requires fd format %d.%d; this checker reads up to %d.%d: run `fd upgrade` (or update .flightdeck/ "
                "from the template)" % ((name,) + need + FORMAT))
    return None


def needs_format(data, kind):
    """the format a manifest ("manifest") or project.yaml ("project") needs, from the keys it uses"""
    if not isinstance(data, dict):
        return (1, 0)
    if kind == "manifest":
        vs = [v for a in data.get("artifacts") or [] if isinstance(a, dict) for v in a.get("versions") or [] if isinstance(v, dict)]
        return (1, 2) if any("request" in v for v in vs) else (1, 0)
    serving = data.get("serving") if isinstance(data.get("serving"), dict) else {}
    launch = data.get("launch") if isinstance(data.get("launch"), dict) else {}
    newer = "agent_branches" in data or serving.get("cdn") in ("private", "off") or any(k in launch for k in ("setup", "resume", "archive", "ports"))
    return (1, 2) if newer else (1, 0)


def stamp_format(data, kind):
    """set `requires` to what the keys need (never lower an existing one); True when it changed"""
    need, have = needs_format(data, kind), parse_format(data.get("requires"))
    if need > (1, 0) and (not have or need > have):
        data["requires"] = "%d.%d" % need
        return True
    return False


def _schema():
    for sp in SCHEMA_PATHS:
        if os.path.isfile(sp):
            with open(sp, encoding="utf8") as f:
                return json.load(f)
    return None


def _plain(obj):
    """YAML parses 2026-09-19 into a date; the schema and the deck want strings"""
    if isinstance(obj, dict):
        return {k: _plain(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_plain(v) for v in obj]
    if isinstance(obj, date):
        return obj.isoformat()
    return obj


def schema_errors(data):
    """schema violations as strings (empty when jsonschema or the schema file is missing)"""
    sch = _schema()
    if not (jsonschema and sch):
        return []
    out = []
    for e in sorted(jsonschema.Draft202012Validator(sch).iter_errors(_plain(data)), key=lambda e: list(e.path)):
        where = "/".join(str(x) for x in e.path) or "manifest"
        msg = e.message
        if e.validator == "anyOf":
            msg = "needs url, path or versions" if "artifacts" in where else msg
        out.append(f"{where}: {msg[:160]}")
    return out

CATEGORIES = {
    "deployment": {"site", "service", "app", "api"},
    "codebase": {"repo", "package", "library"},
    "content": {"spec", "paper", "thread", "film", "figure", "deck", "doc", "post", "dataset"},
    "model": {"model", "notebook"},
}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL_RE = re.compile(r"^https?://\S+$")
VERSIONED_NAME_RE = re.compile(r"-v\d+(\.\d+)*\.[A-Za-z0-9]+$|^versions/v\d+(\.\d+)*_\d{4}-\d{2}-\d{2}/")
MANIFEST_NAMES = ("artifacts.yaml", "artifacts.yml")


def manifest_path(folder):
    for n in MANIFEST_NAMES:
        p = os.path.join(folder, n)
        if os.path.isfile(p):
            return p
    return None


def expand(folder, p):
    if not isinstance(p, str):
        return None
    if p.startswith("~/"):
        return os.path.expanduser(p)
    if os.path.isabs(p):
        return p
    return os.path.normpath(os.path.join(folder, p))


def _vkey(v):
    """sortable version: '2.5.1' -> (2,5,1); 6 -> (6,)"""
    parts = re.findall(r"\d+", str(v))
    return tuple(int(x) for x in parts) if parts else (-1,)


def check_manifest(folder, data):
    """-> (errors, warnings). `data` is the parsed YAML."""
    errors, warnings = [], []
    if not isinstance(data, dict):
        return ["manifest is not a mapping"], []
    if data.get("manifest") != 1:
        errors.append("`manifest: 1` is required")
    if not isinstance(data.get("project"), str) or not data["project"].strip():
        errors.append("`project` (the human name) is required")
    for f in data.get("folders") or []:
        fp = expand(folder, f)
        if not fp or not os.path.isdir(fp):
            warnings.append(f"folders: {f} is not a folder here")
    arts = data.get("artifacts")
    if not isinstance(arts, list) or not arts:
        errors.append("`artifacts` must be a non-empty list")
        return errors, warnings
    ids = set()
    for i, a in enumerate(arts):
        where = f"artifacts[{i}]"
        if not isinstance(a, dict):
            errors.append(f"{where}: not a mapping")
            continue
        aid = a.get("id")
        where = f"artifacts[{i}] ({aid})" if aid else where
        if not isinstance(aid, str) or not ID_RE.match(aid):
            errors.append(f"{where}: `id` must be a slug like explainer-film")
        elif aid in ids:
            errors.append(f"{where}: duplicate id")
        ids.add(aid)
        cat, typ = a.get("category"), a.get("type")
        if cat not in CATEGORIES:
            errors.append(f"{where}: category must be one of {sorted(CATEGORIES)}")
        elif typ not in CATEGORIES[cat]:
            errors.append(f"{where}: type `{typ}` is not a {cat} type ({sorted(CATEGORIES[cat])})")
        if not isinstance(a.get("title"), str) or not a["title"].strip():
            errors.append(f"{where}: `title` is required")
        has_url, has_path, versions = a.get("url"), a.get("path"), a.get("versions")
        if not (has_url or has_path or versions):
            errors.append(f"{where}: needs `url`, `path` or `versions`")
        if has_url and not URL_RE.match(str(has_url)):
            errors.append(f"{where}: url must start with http(s)://")
        if has_path:
            fp = expand(folder, has_path)
            if not fp or not os.path.exists(fp):
                errors.append(f"{where}: path does not exist: {has_path}")
        if cat == "deployment" and not a.get("source"):
            warnings.append(f"{where}: a deployment should name its `source` folder or repo")
        if versions is not None:
            if not isinstance(versions, list) or not versions:
                errors.append(f"{where}: `versions` must be a non-empty list")
            else:
                seen, keys = set(), []
                for j, v in enumerate(versions):
                    vw = f"{where}.versions[{j}]"
                    if not isinstance(v, dict):
                        errors.append(f"{vw}: not a mapping")
                        continue
                    if "v" not in v:
                        errors.append(f"{vw}: `v` is required")
                    else:
                        vs = str(v["v"])
                        if vs in seen:
                            errors.append(f"{vw}: duplicate version {vs}")
                        seen.add(vs)
                        keys.append(_vkey(vs))
                    d = v.get("date")
                    if not isinstance(d, (str, date)) or not DATE_RE.match(str(d)):
                        errors.append(f"{vw}: `date` must be YYYY-MM-DD")
                    if not (v.get("path") or v.get("url")):
                        errors.append(f"{vw}: needs `path` or `url`")
                    if v.get("url") and not URL_RE.match(str(v["url"])):
                        errors.append(f"{vw}: url must start with http(s)://")
                    if v.get("path"):
                        fp = expand(folder, v["path"])
                        if not fp or not os.path.exists(fp):
                            errors.append(f"{vw}: path does not exist: {v['path']}")
                        elif not VERSIONED_NAME_RE.search(str(v["path"])):
                            warnings.append(f"{vw}: {v['path']} does not carry its version in its name")
                if keys != sorted(keys, reverse=True):
                    errors.append(f"{where}: versions must be newest first")
    return errors, warnings


def load_manifest(folder):
    """-> (data or None, errors, warnings, path or None); dates come back as strings"""
    p = manifest_path(folder)
    if not p:
        return None, [], [], None
    if yaml is None:
        return None, ["PyYAML is not installed"], [], p
    try:
        with open(p, encoding="utf8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return None, [f"cannot parse {os.path.basename(p)}: {e}"], [], p
    data = _plain(data)
    gate = format_gate(data, os.path.basename(p))
    if gate:
        return data, [gate], [], p
    errors, warnings = check_manifest(folder, data)
    for e in schema_errors(data):
        if e not in errors:
            errors.append("schema: " + e)
    return data, errors, warnings, p


# ---- the lock file: machine facts about every file the manifest names ---------------------------------
def _sha256(path, limit=None):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _probe(path, mime):
    """duration/width/height for video, pages for PDF, via ffprobe / pdfinfo when present"""
    out = {}
    try:
        if mime.startswith("video/") and shutil.which("ffprobe"):
            r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration",
                                "-of", "json", path], capture_output=True, text=True, timeout=30)
            d = json.loads(r.stdout or "{}")
            st = (d.get("streams") or [{}])[0]
            if st.get("width"):
                out["width"], out["height"] = int(st["width"]), int(st["height"])
            if (d.get("format") or {}).get("duration"):
                out["duration_s"] = round(float(d["format"]["duration"]), 2)
        elif mime == "application/pdf" and shutil.which("pdfinfo"):
            r = subprocess.run(["pdfinfo", path], capture_output=True, text=True, timeout=30)
            for line in r.stdout.splitlines():
                if line.startswith("Pages:"):
                    out["pages"] = int(line.split()[1])
    except Exception:
        pass
    return out


def file_facts(path):
    st = os.stat(path)
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    facts = {"path": path, "size_bytes": st.st_size, "mtime": int(st.st_mtime), "mime": mime, "sha256": _sha256(path)}
    media = _probe(path, mime)
    if media:
        facts["media"] = media
    return facts


def ingredient_facts(folder, items, prev=None):
    """the manifest's short ingredient strings -> lock objects {uri, sha256, size} (+ mtime for the cache): a local file
    (relative to the project) is digested, a URL or a missing path stays undigested (sha256 null)"""
    cache = {x.get("uri"): x for x in (prev or []) if isinstance(x, dict)}
    out = []
    for it in items or []:
        uri = it.get("uri") if isinstance(it, dict) else str(it)
        if not uri:
            continue
        obj = {"uri": uri, "sha256": None, "size": None}
        fp = None if URL_RE.match(uri) else expand(folder, uri)
        if fp and os.path.isfile(fp):
            st = os.stat(fp)
            c = cache.get(uri)
            if c and c.get("size") == st.st_size and c.get("mtime") == int(st.st_mtime) and c.get("sha256"):
                obj.update(sha256=c["sha256"], size=st.st_size, mtime=int(st.st_mtime))
            else:
                obj.update(sha256=_sha256(fp), size=st.st_size, mtime=int(st.st_mtime))
        out.append(obj)
    return out


def prompt_digest(prompt):
    """sha256 hex of the prompt text; a prompt already stored as `sha256:<hex>` (redacted) yields that hex"""
    if not prompt:
        return None
    if isinstance(prompt, str) and prompt.startswith("sha256:") and len(prompt) == 71:
        return prompt[7:]
    return hashlib.sha256(str(prompt).encode("utf8")).hexdigest()


def fill_lock(folder, data, old=None, host=None):
    """-> lock dict. Facts are recomputed only when size or mtime changed (sha256 of a 200 MB film is not free).
    Version entries also carry provenance facts derived from the manifest: `ingredients` as digested objects,
    `prompt_sha256`, and `host` (the machine that first locked that version; the SLSA builder id uses it)."""
    old_entries = (old or {}).get("entries") or {}
    entries = {}
    host = host or (socket.gethostname().split(".")[0] or "unknown").lower()

    def one(key, rel, v=None):
        fp = expand(folder, rel)
        if not fp or not os.path.isfile(fp):
            return
        try:
            st = os.stat(fp)
        except OSError:
            return
        prev = old_entries.get(key)
        if prev and prev.get("size_bytes") == st.st_size and prev.get("mtime") == int(st.st_mtime) and prev.get("sha256"):
            facts = dict(prev, path=rel)
        else:
            facts = file_facts(fp)
            facts["path"] = rel
            if prev and prev.get("host"):
                facts["host"] = prev["host"]
        if v is not None:
            facts["host"] = facts.get("host") or host
            if v.get("ingredients"):
                facts["ingredients"] = ingredient_facts(folder, v["ingredients"], (prev or {}).get("ingredients"))
            else:
                facts.pop("ingredients", None)
            ph = prompt_digest(v.get("prompt"))
            if ph:
                facts["prompt_sha256"] = ph
            else:
                facts.pop("prompt_sha256", None)
        entries[key] = facts
    for a in data.get("artifacts") or []:
        if not isinstance(a, dict) or not a.get("id"):
            continue
        if a.get("path"):
            one(a["id"], a["path"])
        for v in a.get("versions") or []:
            if isinstance(v, dict) and v.get("path") and "v" in v:
                one(f"{a['id']}@{v['v']}", v["path"], v)
    return {"lock": 1, "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "project": data.get("project"), "entries": entries}


def load_lock(folder):
    p = os.path.join(folder, LOCK_NAME)
    try:
        with open(p, encoding="utf8") as f:
            return json.load(f)
    except Exception:
        return None


def write_lock(folder, lock):
    p = os.path.join(folder, LOCK_NAME)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf8") as f:
        json.dump(lock, f, indent=1, sort_keys=True)
        f.write("\n")
    os.replace(tmp, p)
    return p


def install_ci(folder):
    """copy the schema + this checker + a workflow + a pre-commit config into a repo (nothing committed)"""
    tpl = os.path.join(HERE, "..", "docs", "templates")
    fd = os.path.join(folder, ".flightdeck")
    os.makedirs(fd, exist_ok=True)
    os.makedirs(os.path.join(folder, ".github", "workflows"), exist_ok=True)
    written = []
    project_schema = next((p for p in (os.path.join(HERE, "..", "schemas", "project-1.json"), os.path.join(HERE, "project-1.json")) if os.path.isfile(p)), None)
    for src, dst in ((SCHEMA_PATHS[0], os.path.join(fd, "artifacts-1.json")),
                     (os.path.abspath(__file__), os.path.join(fd, "artifacts_check.py")),
                     (os.path.join(HERE, "fd.py"), os.path.join(fd, "fd.py")),                   # the project tool (docs/PROJECTS.md)
                     (project_schema, os.path.join(fd, "project-1.json")),
                     (os.path.join(tpl, "artifacts-check.yml"), os.path.join(folder, ".github", "workflows", "artifacts-check.yml"))):
        if not src or not os.path.isfile(src):
            continue
        shutil.copyfile(src, dst)
        written.append(os.path.relpath(dst, folder))
    pc = os.path.join(folder, ".pre-commit-config.yaml")
    hook = open(os.path.join(tpl, "pre-commit-artifacts.yaml"), encoding="utf8").read()
    if os.path.exists(pc):
        cur = open(pc, encoding="utf8").read()
        if "artifacts-check" not in cur:
            with open(pc, "a", encoding="utf8") as f:
                f.write("\n" + hook.split("repos:", 1)[1] if cur.strip().startswith("repos:") else "\n" + hook)
            written.append(".pre-commit-config.yaml (appended)")
    else:
        with open(pc, "w", encoding="utf8") as f:
            f.write(hook)
        written.append(".pre-commit-config.yaml")
    return written


def main(argv):
    as_json = "--json" in argv
    strict = "--strict" in argv
    fill = "--fill" in argv
    folders = [a for a in argv if not a.startswith("--")] or ["."]
    worst = 0
    if "--install-ci" in argv:
        for folder in folders:
            folder = os.path.abspath(os.path.expanduser(folder))
            for w in install_ci(folder):
                print(f"{folder}: wrote {w}")
        return 0
    for folder in folders:
        folder = os.path.abspath(os.path.expanduser(folder))
        data, errors, warnings, p = load_manifest(folder)
        if fill and data and not errors:
            lock = fill_lock(folder, data, load_lock(folder))
            lp = write_lock(folder, lock)
            if not as_json:
                print(f"{folder}: {os.path.basename(lp)}, {len(lock['entries'])} files hashed")
        if strict:
            errors = errors + [f"(strict) {w}" for w in warnings]
            warnings = []
        if as_json:
            print(json.dumps({"folder": folder, "manifest": p, "ok": not errors and p is not None,
                              "errors": errors, "warnings": warnings, "project": (data or {}).get("project")}, indent=2))
        else:
            if not p:
                print(f"{folder}: no artifacts.yaml")
                worst = max(worst, 1)
                continue
            n = len((data or {}).get("artifacts") or []) if isinstance(data, dict) else 0
            print(f"{folder}: {os.path.basename(p)}, {n} artifacts, {len(errors)} errors, {len(warnings)} warnings")
            for e in errors:
                print(f"  error   {e}")
            for w in warnings:
                print(f"  warning {w}")
        if errors or not p:
            worst = 1
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
