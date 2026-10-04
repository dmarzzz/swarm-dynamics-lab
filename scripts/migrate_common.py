#!/usr/bin/env python3
"""Shared pieces of the phase-layout migration (scripts/migrate_*.py): the path map, the file walk, and the
policy for files whose sha256 is recorded somewhere in the repo.

Held-file policy. A file whose current sha256 appears in another file is "recorded". Where it is recorded
decides what the migration may do with it:

  class (a)  recorded only in rewritable registries (REGISTRIES below: the evidence registry, the artifact
             lock and attestation ingredient digests, generated evidence documents, dashboard exports).
             With --include-recorded the file is rewritten and every registry occurrence of its old digest
             is replaced by the new one, so the registry keeps describing the file that is on disk.
  class (b)  recorded anywhere else: a pre-registration, frozen design, run receipt, launch record,
             *.sha256 file, or any other document. These exist to prove a file was not changed after the
             fact, so the file stays byte-identical, always. A file in both classes is (b). A file with
             the same bytes as a filed artifact (its digest is an artifact entry in the lock) is (b) too.

  snapshot   recorded only by a generated point-in-time export that names its own source commit (SNAPSHOTS
             below). The export says what the tree held at that commit, keyed by the paths of that commit.
             It neither freezes the file nor gets edited: rewriting its digests would make it misdescribe
             the commit it names. Such a file counts as unrecorded unless something else records it.

A registry file whose own sha256 is recorded somewhere is itself frozen and stops counting as a registry.
"""
import hashlib, os, re, subprocess
from collections import defaultdict

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()

# old prefix -> new prefix, most specific first
FORWARD = [
    (r"^researchers/shadow/(factory|qa)(/|$)", r"5-experiments/studies/shadow/\1\2"),
    (r"^researchers/([^/]+)/notes(/|$)", r"5-experiments/studies/\1\2"),
    (r"^researchers(/|$)", r"lab/researchers\1"),
    (r"^tooling(/|$)", r"5-experiments/toolkit\1"),
    (r"^experiments(/|$)", r"5-experiments\1"),
    (r"^reviews(/|$)", r"2-surveys/reviews\1"),
    (r"^library(/|$)", r"1-library\1"),
    (r"^surveys(/|$)", r"2-surveys\1"),
    (r"^synthesis(/|$)", r"3-synthesis\1"),
    (r"^hypotheses(/|$)", r"4-hypotheses\1"),
    (r"^(tasks|candidates|templates|STATUS\.md|PIPELINE\.md)(/|$)", r"lab/\1\2"),
]
# new prefix -> old prefix, most specific first
INVERSE = [
    (r"^5-experiments/studies/shadow/(factory|qa)(/|$)", r"researchers/shadow/\1\2"),
    (r"^5-experiments/studies/([^/]+)(/|$)", r"researchers/\1/notes\2"),
    (r"^5-experiments/toolkit(/|$)", r"tooling\1"),
    (r"^5-experiments(/|$)", r"experiments\1"),
    (r"^2-surveys/reviews(/|$)", r"reviews\1"),
    (r"^1-library(/|$)", r"library\1"),
    (r"^2-surveys(/|$)", r"surveys\1"),
    (r"^3-synthesis(/|$)", r"synthesis\1"),
    (r"^4-hypotheses(/|$)", r"hypotheses\1"),
    (r"^lab/(researchers|tasks|candidates|templates|STATUS\.md|PIPELINE\.md)(/|$)", r"\1\2"),
]
OLD_TOPS = ("library", "surveys", "reviews", "synthesis", "hypotheses", "experiments", "tooling", "researchers",
            "tasks", "candidates", "templates")

BINARY_EXT = (".png", ".jpg", ".jpeg", ".webp", ".mp4", ".mov", ".gif", ".pdf", ".npz", ".npy", ".woff", ".woff2",
              ".ttf", ".otf", ".zip", ".gz", ".tgz", ".bz2", ".xz", ".ico", ".parquet", ".sqlite", ".db", ".pkl",
              ".bin", ".wav", ".mp3", ".webm", ".glb", ".splat", ".ply")

# class (a): files that only register digests and can be brought back in line with the tree
REGISTRIES = (
    re.compile(r"^5-experiments/evidence-metadata\.json$"),
    re.compile(r"^5-experiments/EVIDENCE(-METADATA)?\.md$"),
    re.compile(r"^artifacts\.lock\.json$"),
    re.compile(r"^attestations/"),
    re.compile(r"^dashboard/(public|dist|src/data|data)/.*\.json$"),
)
# generated point-in-time exports (built by a script from a named source commit, old-layout keys)
SNAPSHOTS = (
    re.compile(r"^5-experiments/studies/shadow/narrative/narrative\.json$"),   # build_map.py: provenance.files @ source_commit
)
HEX64 = re.compile(rb"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])")


def remap(path, table):
    for pat, rep in table:
        new, n = re.subn(pat, rep, path)
        if n:
            return new
    return path


def tracked(*globs):
    """Tracked and untracked-but-not-ignored files that exist, repo-relative."""
    out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard", "-z", *globs],
                         capture_output=True, cwd=ROOT).stdout.decode("utf-8", "surrogateescape")
    return [f for f in out.split("\0") if f and os.path.isfile(os.path.join(ROOT, f)) and not os.path.islink(os.path.join(ROOT, f))]


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def is_registry_path(path):
    return any(p.search(path) for p in REGISTRIES)


def is_snapshot_path(path):
    return any(p.search(path) for p in SNAPSHOTS)


class Recorded:
    """Index of every 64-hex digest written in the repo, and which files write it."""

    def __init__(self):
        self.where = defaultdict(set)      # hex -> files that contain it
        for f in tracked():
            if f.lower().endswith(BINARY_EXT) or "/node_modules/" in f or f.startswith("dashboard/node_modules/"):
                continue
            try:
                with open(os.path.join(ROOT, f), "rb") as fh:
                    raw = fh.read()
            except OSError:
                continue
            for h in set(HEX64.findall(raw)):
                self.where[h.decode()].add(f)
        self._frozen_registry = {}
        # digests the artifact lock gives to filed artifacts and prompts. A working file with the same bytes
        # as a filed artifact (`fd add --copy`) shares that digest; replacing it in the lock would corrupt the
        # artifact's own entry and its attestation subject, so such a file is frozen like class (b).
        self.artifact_digests = set()
        try:
            import json
            with open(os.path.join(ROOT, "artifacts.lock.json"), encoding="utf8") as fh:
                for e in (json.load(fh).get("entries") or {}).values():
                    for k in ("sha256", "prompt_sha256"):
                        if isinstance(e, dict) and isinstance(e.get(k), str):
                            self.artifact_digests.add(e[k])
        except (OSError, ValueError):
            pass

    def registry(self, path):
        """True if path is a class (a) registry that is not itself hash-recorded elsewhere."""
        if not is_registry_path(path):
            return False
        if path not in self._frozen_registry:
            try:
                with open(os.path.join(ROOT, path), "rb") as fh:
                    own = sha256_bytes(fh.read())
            except OSError:
                own = None
            self._frozen_registry[path] = bool(self.where.get(own, set()) - {path})
        return not self._frozen_registry[path]

    def classify(self, path, digest):
        """-> (None | 'a' | 'b', sorted recorders). Recorders exclude the file itself."""
        recorders = sorted(r for r in self.where.get(digest, set()) - {path} if not is_snapshot_path(r))
        if not recorders:
            return None, []
        if digest in self.artifact_digests:
            return "b", ["artifacts.lock.json (same bytes as a filed artifact)"]
        if all(self.registry(r) for r in recorders):
            return "a", recorders
        return "b", [r for r in recorders if not self.registry(r)]


def apply_digest_updates(recorded, updates, write):
    """updates: {old_hex: new_hex} for class (a) files that were rewritten. Replace old with new in every
    registry file that holds the old digest. Returns {registry_path: replacements}."""
    touched = defaultdict(int)
    by_file = defaultdict(list)
    for old, new in updates.items():
        if old == new:
            continue
        for r in recorded.where.get(old, ()):
            if recorded.registry(r):
                by_file[r].append((old, new))
    for r, pairs in sorted(by_file.items()):
        p = os.path.join(ROOT, r)
        with open(p, "rb") as fh:
            raw = fh.read()
        new_raw = raw
        for old, new in pairs:
            n = new_raw.count(old.encode())
            if n:
                touched[r] += n
                new_raw = new_raw.replace(old.encode(), new.encode())
        if write and new_raw != raw:
            with open(p, "wb") as fh:
                fh.write(new_raw)
    return dict(touched)


def settle(recorded, candidates, include_recorded, write):
    """Decide what happens to each changed file and apply it.

    candidates: {path: (old_bytes, new_bytes)}. Returns (written, held_a, held_b, registry_touched) where
    written is the list of paths rewritten (or that would be), held_a / held_b map path -> recorders.
    A class (a) file is also held when another file with the same old digest would end up with a different
    new digest: one registry entry cannot describe both."""
    plan, held_a, held_b = {}, {}, {}
    fan = defaultdict(set)
    for path, (old, new) in candidates.items():
        d = sha256_bytes(old)
        cls, recorders = recorded.classify(path, d)
        if cls == "b":
            held_b[path] = recorders
        elif cls == "a" and not include_recorded:
            held_a[path] = recorders
        else:
            plan[path] = (cls, d, sha256_bytes(new), recorders)
            if cls == "a":
                fan[d].add(sha256_bytes(new))
    updates = {}
    for path, (cls, d, nd, recorders) in list(plan.items()):
        if cls == "a":
            if len(fan[d]) > 1:
                held_a[path] = recorders + ["(same digest as another file that would change differently)"]
                del plan[path]
            else:
                updates[d] = nd
    if write:
        for path in plan:
            with open(os.path.join(ROOT, path), "wb") as fh:
                fh.write(candidates[path][1])
    touched = apply_digest_updates(recorded, updates, write)
    return sorted(plan), held_a, held_b, touched


def under(path, prefixes):
    return not prefixes or any(path == p.rstrip("/") or path.startswith(p.rstrip("/") + "/") for p in prefixes)


def only_args(argv):
    """Collect every `--only <path-prefix>` from argv."""
    out = []
    for i, a in enumerate(argv):
        if a == "--only" and i + 1 < len(argv):
            out.append(argv[i + 1])
        elif a.startswith("--only="):
            out.append(a.split("=", 1)[1])
    return out
