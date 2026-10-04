#!/usr/bin/env python3
"""Rewrite repo paths recorded as ingredients after the phase-layout move (scripts/migrate_layout.sh).

Touches only path strings: `ingredients:` items and `source:` in artifacts.yaml, `"uri"` values in
artifacts.lock.json and attestations/*.intoto.json. Digests, dates, sessions, commits stay as they are.
URLs (commit-pinned permalinks) are left alone.

Absolute paths that point into a checkout of this repo (the main checkout `/Users/<user>/swarm-lab/...`, a
lane worktree `/Users/<user>/swarm-lab-lanes/<lane>/swarm-lab/...`, the same under /home/<user> or /root, and
the renamed `swarm-dynamics-lab`) become repo-relative new-layout paths: the same file, named the way every
other ingredient is, and no home directory in a public manifest. Absolute paths that are not inside a
checkout (/private/tmp/..., /System/...) are left alone and counted.

Why the attestations stay valid: `fd check` (rule 8, check_statements in .flightdeck/fd.py) compares only each
statement's subject digest with the lock entry's sha256 of the artifact file, and neither is touched here.
A statement's resolvedDependencies are the lock's ingredient {uri, sha256} pairs copied verbatim
(build_statement), so rewriting the same uri string in artifacts.yaml, artifacts.lock.json and the statement
keeps all three saying the same thing; a later `fd fill` would write back the identical statement text. The
lock's ingredient cache is keyed by uri, and manifest and lock change together, so it keeps hitting. This
script never changes a digest and never runs `fd fill`.

Idempotent: a path already relative and in the new layout does not match any old prefix or checkout root.

usage: migrate_artifact_paths.py [<repo-root>] [--dry-run]
"""
import glob, os, re, sys
from collections import Counter

HOME = r"(?:/Users/[^/]+|/home/[^/]+|/root)"
# a path segment named exactly like the repo, at any depth below a home directory (main checkout, lane worktrees)
CHECKOUT = re.compile(r"^%s/(?:[^/]+/)*?(?:swarm-lab|swarm-dynamics-lab)/" % HOME)
# a differently suffixed clone directly in a home directory (swarm-lab-2/): accepted only if the file is in the tree
CLONE = re.compile(r"^%s/swarm-(?:dynamics-)?lab[^/]*/" % HOME)
ROOT = "."
REMAINING = Counter()
SIMPLE = (("library/", "1-library/"), ("surveys/", "2-surveys/"), ("reviews/", "2-surveys/reviews/"),
          ("synthesis/", "3-synthesis/"), ("hypotheses/", "4-hypotheses/"), ("experiments/", "5-experiments/"),
          ("tooling/", "5-experiments/toolkit/"), ("tasks/", "lab/tasks/"), ("candidates/", "lab/candidates/"),
          ("templates/", "lab/templates/"))
EXACT = {"STATUS.md": "lab/STATUS.md", "PIPELINE.md": "lab/PIPELINE.md"}
STUDY = re.compile(r"^researchers/([^/]+)/notes(/|$)")
EXTRA = re.compile(r"^researchers/([^/]+)/(factory|qa)(/|$)")


def map_rel(p):
    if p in EXACT:
        return EXACT[p]
    m = STUDY.match(p)
    if m:
        return "5-experiments/studies/%s%s" % (m.group(1), m.group(2)) + p[m.end():]
    m = EXTRA.match(p)
    if m:
        return "5-experiments/studies/%s/%s%s" % (m.group(1), m.group(2), m.group(3)) + p[m.end():]
    if p.startswith("researchers/"):
        return "lab/" + p
    for old, new in SIMPLE:
        if p.startswith(old):
            return new + p[len(old):]
    return p


def map_uri(u):
    if re.match(r"^[a-z][a-z0-9+.-]*://", u):
        return u
    m = CHECKOUT.match(u)
    if m:
        return map_rel(u[m.end():])
    m = CLONE.match(u)
    if m and os.path.exists(os.path.join(ROOT, map_rel(u[m.end():]))):
        return map_rel(u[m.end():])
    if u.startswith("/"):
        REMAINING["/".join(u.split("/")[:3])] += 1
        return u
    return map_rel(u)


def rewrite_yaml(text):
    out, inb, ind, n = [], False, 0, 0
    for line in text.split("\n"):
        m = re.match(r"^(\s*)ingredients:\s*$", line)
        if m:
            inb, ind = True, len(m.group(1))
            out.append(line)
            continue
        if inb:
            m = re.match(r"^(\s*)- (.*)$", line)
            if m and len(m.group(1)) >= ind:
                new = map_uri(m.group(2))
                n += new != m.group(2)
                out.append("%s- %s" % (m.group(1), new))
                continue
            inb = False
        m = re.match(r"^(\s*source: )(\S.*)$", line)
        if m:
            new = map_uri(m.group(2))
            n += new != m.group(2)
            line = m.group(1) + new
        out.append(line)
    return "\n".join(out), n


URI_LINE = re.compile(r'^(\s*"uri": ")([^"\\]*)(",?)$')


def rewrite_json(text):
    out, n = [], 0
    for line in text.split("\n"):
        m = URI_LINE.match(line)
        if m:
            new = map_uri(m.group(2))
            n += new != m.group(2)
            line = m.group(1) + new + m.group(3)
        out.append(line)
    return "\n".join(out), n


def main():
    global ROOT
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = ROOT = args[0] if args else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dry = "--dry-run" in sys.argv
    jobs = [("artifacts.yaml", rewrite_yaml), ("artifacts.lock.json", rewrite_json)]
    jobs += [(os.path.relpath(p, root), rewrite_json) for p in sorted(glob.glob(os.path.join(root, "attestations", "*.intoto.json")))]
    total = files = 0
    for rel, fn in jobs:
        p = os.path.join(root, rel)
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf8", newline="") as f:
            text = f.read()
        new, n = fn(text)
        if n and not dry:
            with open(p, "w", encoding="utf8", newline="") as f:
                f.write(new)
        if n:
            files += 1
            total += n
            if not rel.startswith("attestations/"):
                print("%s: %d paths" % (rel, n))
    print("%d paths %s in %d files%s" % (total, "would be rewritten" if dry else "rewritten", files, " (dry run)" if dry else ""))
    if REMAINING:
        print("%d absolute paths outside any checkout left alone (counted once per file that names them): %s"
              % (sum(REMAINING.values()), ", ".join("%s/ x%d" % kv for kv in sorted(REMAINING.items()))))


if __name__ == "__main__":
    main()
