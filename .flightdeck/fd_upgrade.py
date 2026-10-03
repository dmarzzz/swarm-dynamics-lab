#!/usr/bin/env python3
"""fd_upgrade — re-apply the template a project was scaffolded from, after the template changed (Copier's algorithm).

  fd upgrade [folder] [--template base] [--dry-run] [--force] [--repo ~/agent-status] [--to <ref>]

The project's `template.commit` (stamped here; `project.yaml` v1.1) is the agent-status commit its files came from.
For every template-owned file we render the template at that commit (OLD) and at the target (NEW) with the same
{{placeholders}} the scaffold used, then per file:

  project file == NEW               nothing to do
  project file missing              add NEW
  project never changed it (== OLD) take NEW
  template did not change (OLD==NEW) keep the project's version
  both changed                      `git merge-file` project OLD NEW; conflict markers stay in the file, reported
  template dropped it               keep the project's file (reported)

`src/ artifacts/ data/ notes/` (the layout dirs), `project.yaml`, `artifacts.yaml` and the lock are never touched:
they are the project's, the template only seeds them. Without a recorded `template.commit` there is no OLD, so a
file the project changed is only overwritten with --force (the diff is shown); unchanged and missing files are
still updated. The stamp is written after a successful pass.
"""
import difflib
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fd  # noqa: E402

PROTECTED_FILES = ("project.yaml", "project.yml", "artifacts.yaml", "artifacts.yml", "artifacts.lock.json")


class GitSource:
    """template files as they were at a commit of the agent-status repo"""
    def __init__(self, repo, name="base"):
        self.repo, self.sub = os.path.realpath(os.path.expanduser(repo)), "templates/%s" % name

    def _git(self, *args):
        r = subprocess.run(["git", "-C", self.repo] + list(args), capture_output=True)
        return r.returncode, r.stdout

    def head(self, ref="HEAD"):
        rc, out = self._git("rev-parse", ref)
        if rc != 0:
            fd.die("%s: cannot resolve %s in %s" % (self.sub, ref, self.repo))
        return out.decode().strip()

    def files(self, ref):
        rc, out = self._git("ls-tree", "-r", "--name-only", ref, self.sub)
        if rc != 0:
            return None
        pre = self.sub + "/"
        return sorted(l[len(pre):] for l in out.decode().splitlines() if l.startswith(pre))

    def read(self, ref, rel):
        rc, out = self._git("show", "%s:%s/%s" % (ref, self.sub, rel))
        return out if rc == 0 else None


class DirSource:
    """tests: {ref: directory}; `head()` is the ref named "HEAD" or the last one given"""
    def __init__(self, refs):
        self.refs = dict(refs)

    def head(self, ref="HEAD"):
        return ref if ref in self.refs else list(self.refs)[-1]

    def files(self, ref):
        root = self.refs.get(ref)
        if not root:
            return None
        out = []
        for base, dirs, names in os.walk(root):
            dirs[:] = sorted(d for d in dirs if d != ".git")
            for n in names:
                out.append(os.path.relpath(os.path.join(base, n), root).replace(os.sep, "/"))
        return sorted(out)

    def read(self, ref, rel):
        p = os.path.join(self.refs.get(ref, "/nonexistent"), rel)
        try:
            with open(p, "rb") as f:
                return f.read()
        except OSError:
            return None


def render(raw, fills):
    """the scaffold's fill, on one file's bytes; binary files pass through"""
    if raw is None:
        return None
    try:
        text = raw.decode("utf8")
    except UnicodeDecodeError:
        return raw
    for k, v in fills.items():
        text = text.replace("{{" + k + "}}", v)
    return text.encode("utf8")


def _fills_of(proj):
    return {"project": proj.get("name") or proj.get("id") or "", "id": proj.get("id") or "", "date": str(proj.get("created") or fd.today()),
            "summary": proj.get("summary") or "one line on what this produces"}


def _protected(rel, layout):
    if rel in PROTECTED_FILES:
        return True
    top = rel.split("/", 1)[0]
    return top in {layout[k].strip("/").split("/")[0] for k in ("code", "artifacts", "data", "notes")}


def _merge(cur, old, new, labels):
    """git merge-file -p; -> (merged bytes, conflicts)"""
    d = tempfile.mkdtemp(prefix="fd-upgrade-")
    try:
        paths = []
        for name, blob in (("current", cur), ("old", old), ("new", new)):
            p = os.path.join(d, name)
            with open(p, "wb") as f:
                f.write(blob)
            paths.append(p)
        r = subprocess.run(["git", "merge-file", "-p", "-L", labels[0], "-L", labels[1], "-L", labels[2]] + paths, capture_output=True)
        if r.returncode < 0:
            return None, -1
        return r.stdout, r.returncode
    finally:
        shutil.rmtree(d, ignore_errors=True)


# Data migrations for the files the template only seeds (project.yaml, artifacts.yaml): ordered, idempotent, kept
# forever so a project that skipped several formats still upgrades (OpenTelemetry schema files / Copier _migrations;
# research 08 §3.5). Ops: ("rename", "a.b", "a.c") moves a key; ("default", "a.b", value) sets it when absent;
# ("stamp",) writes `requires` from the keys the file uses. The lock is rewritten by `fd fill` in the newest format.
MIGRATIONS = [
    {"to": "1.2", "file": "project", "ops": [("stamp",)]},
    {"to": "1.2", "file": "manifest", "ops": [("stamp",)]},
]


def _dig(d, path, create=False):
    *parents, leaf = path.split(".")
    for k in parents:
        if not isinstance(d.get(k), dict):
            if not create:
                return None, leaf
            d[k] = {}
        d = d[k]
    return d, leaf


def migrate(data, kind):
    """apply every migration for `kind` in order; -> list of what changed (empty when already current)"""
    done = []
    for m in MIGRATIONS:
        if m["file"] != kind:
            continue
        for op in m["ops"]:
            if op[0] == "stamp":
                if fd.ac.stamp_format(data, kind):
                    done.append("%s: requires %s" % (m["to"], data["requires"]))
            elif op[0] == "rename":
                src, key = _dig(data, op[1])
                if src is not None and key in src:
                    dst, nkey = _dig(data, op[2], create=True)
                    if nkey not in dst:
                        dst[nkey] = src.pop(key)
                        done.append("%s: %s -> %s" % (m["to"], op[1], op[2]))
            elif op[0] == "default":
                dst, key = _dig(data, op[1], create=True)
                if key not in dst:
                    dst[key] = op[2]
                    done.append("%s: %s = %r" % (m["to"], op[1], op[2]))
    return done


def migrate_folder(folder, dry_run=False, out=print):
    """run MIGRATIONS on project.yaml and artifacts.yaml; -> number of changes"""
    n = 0
    for kind, path in (("project", fd.project_path(folder)), ("manifest", fd.ac.manifest_path(folder))):
        if not path:
            continue
        data, header = fd.read_yaml(path)
        if not isinstance(data, dict):
            continue
        done = migrate(data, kind)
        for what in done:
            out("  %-40s migrated (%s)" % (os.path.basename(path), what))
        if done and not dry_run:
            fd.write_yaml(path, data, header)
        n += len(done)
    return n


def upgrade(folder, source, to="HEAD", dry_run=False, force=False, template="base", out=print):
    """-> {"from", "to", "actions": [(rel, action)], "conflicts": n, "skipped": n}"""
    folder = os.path.realpath(folder)
    pp = fd.project_path(folder)
    if not pp:
        fd.die("%s has no project.yaml" % folder)
    proj, header = fd.read_yaml(pp)
    stamp = proj.get("template") or {}
    base = stamp.get("commit")
    target = source.head(to)
    layout = fd.layout_of(proj)
    fills = _fills_of(proj)
    new_files = source.files(target)
    if new_files is None:
        fd.die("no template files at %s" % target)
    old_files = source.files(base) if base else None
    if base and old_files is None:
        out("template.commit %s is not in the repo: treating the base as unknown" % base[:12])
        base, old_files = None, None
    if base and base == target:
        out("already at %s" % target[:12])
        migrate_folder(folder, dry_run, out)
        return {"from": base, "to": target, "actions": [], "conflicts": 0, "skipped": 0}
    labels = ("project", "template %s" % (base or "?")[:7], "template %s" % target[:7])
    actions, conflicts, skipped = [], 0, 0
    for rel in sorted(set(new_files) | set(old_files or [])):
        if _protected(rel, layout):
            continue
        new = render(source.read(target, rel), fills) if rel in new_files else None
        old = render(source.read(base, rel), fills) if (old_files and rel in old_files) else None
        dst = os.path.join(folder, rel)
        cur = None
        if os.path.isfile(dst):
            with open(dst, "rb") as f:
                cur = f.read()
        if new is None:
            actions.append((rel, "template dropped it; kept"))
            continue
        if cur == new:
            actions.append((rel, "unchanged"))
            continue
        if cur is None:
            actions.append((rel, "added"))
            _write(dst, new, dry_run)
            continue
        if old is None:
            if force:
                actions.append((rel, "overwritten (--force, no recorded base)"))
                _write(dst, new, dry_run)
            else:
                actions.append((rel, "skipped: changed by the project and no recorded base (--force overwrites)"))
                skipped += 1
                for line in list(difflib.unified_diff(cur.decode("utf8", "replace").splitlines(), new.decode("utf8", "replace").splitlines(), "project/" + rel, "template/" + rel, lineterm=""))[:40]:
                    out("    " + line)
            continue
        if cur == old:
            actions.append((rel, "updated"))
            _write(dst, new, dry_run)
            continue
        if old == new:
            actions.append((rel, "kept local change"))
            continue
        merged, n = _merge(cur, old, new, labels)
        if merged is None:
            actions.append((rel, "merge failed; kept"))
            skipped += 1
            continue
        if n == 0:
            actions.append((rel, "merged"))
        else:
            actions.append((rel, "merged with %d conflict(s): resolve the <<<<<<< markers" % n))
            conflicts += n
        _write(dst, merged, dry_run)
    for rel, what in actions:
        if what != "unchanged":
            out("  %-40s %s" % (rel, what))
    migrate_folder(folder, dry_run, out)
    if not dry_run and not skipped:                      # a skipped file keeps the old base so a --force re-run still has it
        proj["template"] = dict(stamp, name=stamp.get("name") or template, commit=target)
        proj["template"].setdefault("source", "~/agent-status/templates/%s" % template)
        fd.write_yaml(pp, proj, header)
    out("%s%s -> %s: %d changed, %d conflict(s), %d skipped" % ("(dry run) " if dry_run else "", (base or "no base")[:12], target[:12],
        sum(1 for _, w in actions if w not in ("unchanged", "kept local change") and not w.startswith("skipped") and not w.startswith("template dropped")), conflicts, skipped))
    return {"from": base, "to": target, "actions": actions, "conflicts": conflicts, "skipped": skipped}


def _write(dst, blob, dry_run):
    if dry_run:
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    tmp = dst + ".tmp"
    with open(tmp, "wb") as f:
        f.write(blob)
    os.replace(tmp, dst)


def default_repo():
    """the agent-status checkout this fd.py lives in (cockpit/..), else ~/agent-status"""
    for cand in (os.path.join(HERE, ".."), os.path.expanduser("~/agent-status")):
        if os.path.isdir(os.path.join(cand, ".git")) and os.path.isdir(os.path.join(cand, "templates")):
            return os.path.realpath(cand)
    return os.path.expanduser("~/agent-status")


def cmd_upgrade(a):
    folder = fd.find_root(a.folder)
    src = GitSource(a.repo or default_repo(), a.template)
    r = upgrade(folder, src, to=a.to, dry_run=a.dry_run, force=a.force, template=a.template)
    return 1 if r["conflicts"] or r["skipped"] else 0


def add_parser(sub, flag):
    p = sub.add_parser("upgrade", help="re-apply the template (3-way from the recorded template.commit); stamps template.commit")
    flag(p, "folder", nargs="?", default=".")
    flag(p, "--template", default="base"), flag(p, "--repo", help="agent-status checkout (default: this one)"), flag(p, "--to", default="HEAD", help="template ref (default HEAD)")
    flag(p, "--dry-run", action="store_true"), flag(p, "--force", action="store_true", help="overwrite project-changed files when no base is recorded")
    p.set_defaults(fn=cmd_upgrade)
