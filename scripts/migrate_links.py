#!/usr/bin/env python3
"""Repair relative markdown links after scripts/migrate_layout.sh.

For every broken relative link, work out what it pointed at in the old layout, map that target to its new
path, and rewrite the link if the new target exists. Files whose sha256 is recorded anywhere in the repo
(pre-registrations, evidence metadata, the artifact lock) are left byte-identical and only reported.

    python3 scripts/migrate_links.py            # dry run
    python3 scripts/migrate_links.py --write
"""
import hashlib, os, re, subprocess, sys
from collections import Counter

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
os.chdir(ROOT)

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
SKIP_DIRS = ("artifacts/", "attestations/", "dashboard/", "agentops/")
LINK = re.compile(r'(\]\()([^)\s]+?)((?:\s+"[^"]*")?\))')


def remap(path, table):
    for pat, rep in table:
        new, n = re.subn(pat, rep, path)
        if n:
            return new
    return path


def tracked(*globs):
    out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard", *globs], capture_output=True, text=True).stdout
    return [f for f in out.split("\n") if f and os.path.isfile(f)]


def recorded_digests():
    hexes = set()
    pat = re.compile(rb"\b[0-9a-f]{64}\b")
    for f in tracked():
        if f.endswith((".png", ".jpg", ".jpeg", ".webp", ".mp4", ".gif", ".pdf", ".npz", ".npy", ".woff2", ".zip", ".gz")):
            continue
        try:
            with open(f, "rb") as fh:
                hexes.update(m.decode() for m in pat.findall(fh.read()))
        except OSError:
            pass
    return hexes


def main():
    write = "--write" in sys.argv
    pinned = recorded_digests()
    fixed, held, left = Counter(), Counter(), Counter()
    for f in tracked("*.md"):
        if f.startswith(SKIP_DIRS):
            continue
        raw = open(f, "rb").read()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        old_self = remap(f, INVERSE)
        here, old_here = os.path.dirname(f), os.path.dirname(old_self)
        n_fix = 0

        def sub(m):
            nonlocal n_fix
            target = m.group(2)
            path, sep, frag = target.partition("#")
            if not path or re.match(r"^[a-z][a-z0-9+.-]*:", path) or path.startswith(("<", "/")):
                return m.group(0)
            if os.path.exists(os.path.normpath(os.path.join(here, path))):
                return m.group(0)
            old_target = os.path.normpath(os.path.join(old_here, path))
            if old_target.startswith(".."):
                return m.group(0)
            new_target = remap(old_target, FORWARD)
            if not os.path.exists(new_target):
                left[f] += 1
                return m.group(0)
            rel = os.path.relpath(new_target, here or ".")
            if path.endswith("/"):
                rel += "/"
            n_fix += 1
            return m.group(1) + rel + sep + frag + m.group(3)

        new_text = LINK.sub(sub, text)
        if not n_fix:
            continue
        if hashlib.sha256(raw).hexdigest() in pinned:
            held[f] = n_fix
            continue
        fixed[f] = n_fix
        if write:
            with open(f, "w", encoding="utf-8", newline="") as fh:
                fh.write(new_text)
    print(f"{'rewrote' if write else 'would rewrite'} {sum(fixed.values())} links in {len(fixed)} files")
    print(f"held back {sum(held.values())} links in {len(held)} hash-recorded files (left byte-identical)")
    print(f"{sum(left.values())} links in {len(left)} files were already broken before the move")
    if "--list-held" in sys.argv:
        for f, n in sorted(held.items()):
            print(f"  held {n:4d}  {f}")


if __name__ == "__main__":
    main()
