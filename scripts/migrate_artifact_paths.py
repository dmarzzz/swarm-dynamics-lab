#!/usr/bin/env python3
"""Rewrite repo paths recorded as ingredients after the phase-layout move (scripts/migrate_layout.sh).

Touches only path strings: `ingredients:` items and `source:` in artifacts.yaml, `"uri"` values in
artifacts.lock.json and attestations/*.intoto.json. Digests, dates, sessions, commits stay as they are.
URLs (commit-pinned permalinks) and absolute paths outside the main checkout are left alone.
Idempotent: a path already in the new layout does not match any old prefix.

usage: migrate_artifact_paths.py <repo-root> [--dry-run]
"""
import glob, os, re, sys

ABS_ROOTS = ("/Users/halcyon/swarm-lab/",)          # absolute ingredients recorded from the main checkout
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
    for root in ABS_ROOTS:
        if u.startswith(root):
            return root + map_rel(u[len(root):])
    if u.startswith("/"):
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
    root = sys.argv[1]
    dry = "--dry-run" in sys.argv
    jobs = [("artifacts.yaml", rewrite_yaml), ("artifacts.lock.json", rewrite_json)]
    jobs += [(os.path.relpath(p, root), rewrite_json) for p in sorted(glob.glob(os.path.join(root, "attestations", "*.intoto.json")))]
    total = files = 0
    for rel, fn in jobs:
        p = os.path.join(root, rel)
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
    print("%d paths rewritten in %d files%s" % (total, files, " (dry run)" if dry else ""))


if __name__ == "__main__":
    main()
