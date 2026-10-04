#!/usr/bin/env python3
"""Repair relative markdown links after scripts/migrate_layout.sh.

For every broken relative link, work out what it pointed at in the old layout, map that target to its new
path, and rewrite the link if the new target exists. Idempotent: a repaired link resolves, so it is skipped.

Files whose sha256 is recorded somewhere in the repo are handled by the policy in scripts/migrate_common.py:
class (a) (recorded only in rewritable registries) is rewritten with --include-recorded and the registries
are updated to the new digest; class (b) (recorded in the research record) always stays byte-identical.

    python3 scripts/migrate_links.py                                # dry run
    python3 scripts/migrate_links.py --write                        # rewrite files nobody records
    python3 scripts/migrate_links.py --write --include-recorded     # also class (a), registries updated
    python3 scripts/migrate_links.py --list-held                    # print held files and what records them
    python3 scripts/migrate_links.py --only <path-prefix> ...       # restrict to files under a prefix
"""
import os, re, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import migrate_common as mc

os.chdir(mc.ROOT)
SKIP_DIRS = ("artifacts/", "attestations/", "dashboard/", "agentops/")
LINK = re.compile(r'(\]\()([^)\s]+?)((?:\s+"[^"]*")?\))')


def relink(f, text, left=None):
    """-> (new_text, links_fixed)."""
    old_self = mc.remap(f, mc.INVERSE)
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
        new_target = mc.remap(old_target, mc.FORWARD)
        if not os.path.exists(new_target):
            if left is not None:
                left[f] += 1
            return m.group(0)
        rel = os.path.relpath(new_target, here or ".")
        if path.endswith("/"):
            rel += "/"
        n_fix += 1
        return m.group(1) + rel + sep + frag + m.group(3)

    return LINK.sub(sub, text), n_fix


def main():
    argv = sys.argv[1:]
    write, include = "--write" in argv, "--include-recorded" in argv
    only = mc.only_args(argv)
    left, counts, candidates = Counter(), {}, {}
    for f in mc.tracked("*.md"):
        if f.startswith(SKIP_DIRS) or not mc.under(f, only):
            continue
        raw = open(f, "rb").read()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        new_text, n = relink(f, text, left)
        if n:
            counts[f] = n
            candidates[f] = (raw, new_text.encode("utf-8"))
    recorded = mc.Recorded()
    written, held_a, held_b, touched = mc.settle(recorded, candidates, include, write)
    n_links = lambda files: sum(counts[f] for f in files)
    n_a_written = sum(1 for f in written if recorded.classify(f, mc.sha256_bytes(candidates[f][0]))[0] == "a") if not write else None
    print(f"{'rewrote' if write else 'would rewrite'} {n_links(written)} links in {len(written)} files"
          + (f" ({n_a_written} of them class (a), registries updated)" if n_a_written else ""))
    if touched:
        print(f"{'updated' if write else 'would update'} {sum(touched.values())} recorded digests in {len(touched)} registry files")
    print(f"held, class (a) registry-recorded (rewritten with --include-recorded): {n_links(held_a)} links in {len(held_a)} files")
    print(f"held, class (b) recorded in the research record (always byte-identical): {n_links(held_b)} links in {len(held_b)} files")
    print(f"{sum(left.values())} links in {len(left)} files were already broken before the move")
    if "--list-held" in argv:
        for f in sorted(held_a):
            print(f"  held (a) {counts[f]:4d}  {f}  <- {held_a[f][0]}" + (f" (+{len(held_a[f]) - 1})" if len(held_a[f]) > 1 else ""))
        for f in sorted(held_b):
            print(f"  held (b) {counts[f]:4d}  {f}  <- {held_b[f][0]}" + (f" (+{len(held_b[f]) - 1})" if len(held_b[f]) > 1 else ""))


if __name__ == "__main__":
    main()
