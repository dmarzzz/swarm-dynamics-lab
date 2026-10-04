#!/usr/bin/env bash
# Move from the flat hackathon layout to the phase layout. Pure renames, no content edits, so file hashes
# recorded in pre-registrations and the artifact lock stay valid.
#
# Idempotent, and it handles stragglers: on a pure old-layout checkout it moves whole directories; after a
# merge of an old-layout branch into the migrated tree it moves each file that arrived at an old path
# (library/..., researchers/<name>/notes/..., tasks/..., experiments/<id>/...) to its new place, `git mv` for
# tracked files and plain `mv` for untracked ones. It never overwrites: if a destination already exists the
# script lists every conflict, moves nothing and exits 1. With nothing left to move it is a no-op.
#
#   scripts/migrate_layout.sh            # move
#   scripts/migrate_layout.sh --dry-run  # list what would move
set -euo pipefail
MIGRATE_SCRIPTS="$(cd "$(dirname "$0")" && pwd)"
cd "$(git rev-parse --show-toplevel)"
DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1
export MIGRATE_DRY=$DRY MIGRATE_SCRIPTS
exec python3 - <<'PY'
import os, subprocess, sys
sys.path.insert(0, os.environ["MIGRATE_SCRIPTS"])
import migrate_common as mc

dry = os.environ.get("MIGRATE_DRY") == "1"
OLD_ROOT_FILES = ("STATUS.md", "PIPELINE.md")


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True)
    if check and r.returncode:
        sys.exit("git %s failed: %s" % (" ".join(args), r.stderr.decode().strip()))
    return r.stdout.decode("utf-8", "surrogateescape")


def ls(*args):
    return [f for f in git("ls-files", "-z", *args).split("\0") if f]


def run(cmd):
    if dry:
        return
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode:
        sys.exit("%s failed: %s" % (" ".join(cmd), r.stderr.decode().strip()))


old_specs = [t for t in mc.OLD_TOPS + OLD_ROOT_FILES if os.path.lexists(t)]
if not old_specs:
    print("already migrated: nothing at an old-layout path")
    sys.exit(0)

tracked = set(ls("--", *old_specs))
untracked = set(ls("-o", "--exclude-standard", "--", *old_specs))
unmerged = set(l.split("\t", 1)[1] for l in git("ls-files", "-u", "--", *old_specs).split("\n") if "\t" in l)
if unmerged:
    print("unmerged paths under the old layout; resolve the merge first:")
    for f in sorted(unmerged):
        print("  " + f)
    sys.exit(1)

# 1. whole directories whose destination does not exist yet (the first-time move, and new top-level areas)
DIRS = []
if os.path.isdir("researchers"):
    for r in sorted(os.listdir("researchers")):
        DIRS.append("researchers/%s/notes" % r)
    DIRS += ["researchers/shadow/factory", "researchers/shadow/qa"]
DIRS += ["library", "surveys", "reviews", "synthesis", "hypotheses", "tooling", "researchers", "tasks", "candidates", "templates"]
if os.path.isdir("experiments"):          # 5-experiments/ usually exists by now (studies), so move its children
    DIRS += ["experiments"] + ["experiments/" + x for x in sorted(os.listdir("experiments")) if os.path.isdir("experiments/" + x)]
moved_dirs = 0
for d in DIRS:
    if not os.path.isdir(d) or os.path.islink(d):
        continue
    dest = mc.remap(d, mc.FORWARD)
    if os.path.lexists(dest):
        continue
    has_tracked = any(f.startswith(d + "/") for f in tracked)
    print("dir   %s -> %s" % (d, dest))
    moved_dirs += 1
    if not dry:
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    run(["git", "mv", d, dest] if has_tracked else ["mv", d, dest])
    if dry:      # pretend: drop its files from the per-file pass
        tracked = {f for f in tracked if not f.startswith(d + "/")}
        untracked = {f for f in untracked if not f.startswith(d + "/")}
if moved_dirs and not dry:
    old_specs = [t for t in mc.OLD_TOPS + OLD_ROOT_FILES if os.path.lexists(t)]
    tracked = set(ls("--", *old_specs)) if old_specs else set()
    untracked = set(ls("-o", "--exclude-standard", "--", *old_specs)) if old_specs else set()

# 2. stragglers, file by file
plan, conflicts = [], []
for f in sorted(tracked | untracked):
    dest = mc.remap(f, mc.FORWARD)
    if dest == f:
        continue
    if os.path.lexists(dest):
        same = os.path.isfile(dest) and os.path.isfile(f) and open(dest, "rb").read() == open(f, "rb").read()
        conflicts.append((f, dest, "identical content" if same else "different content"))
    else:
        plan.append((f, dest, f in tracked))
dests = {}
for f, dest, _ in plan:
    if dest in dests:
        conflicts.append((f, dest, "two old paths map here (also %s)" % dests[dest]))
    dests[dest] = f
if conflicts:
    print("%d conflicts: the destination already exists. Nothing was moved file by file. Resolve by hand:" % len(conflicts))
    for f, dest, why in conflicts:
        print("  CONFLICT %s -> %s (%s)" % (f, dest, why))
    sys.exit(1)
for f, dest, is_tracked in plan:
    print("%s %s -> %s" % ("file " if is_tracked else "file?", f, dest))
    if not dry:
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    run(["git", "mv", "--", f, dest] if is_tracked else ["mv", "--", f, dest])

# 3. drop the old directories if they are now empty; report anything (git-ignored) still sitting there
left = []
if not dry:
    for top in mc.OLD_TOPS:
        if not os.path.isdir(top):
            continue
        for base, dirs, files in os.walk(top, topdown=False):
            visible = [x for x in files if x != ".DS_Store"]
            if visible:
                left += [os.path.join(base, x) for x in visible]
                continue
            for x in files:
                os.remove(os.path.join(base, x))
            try:
                os.rmdir(base)
            except OSError:
                pass
verb = "would move" if dry else "moved"
print("%s %d directories and %d files%s" % (verb, moved_dirs, len(plan), " (dry run)" if dry else ""))
if left:
    print("%d git-ignored files remain under old paths (not moved):" % len(left))
    for x in left[:20]:
        print("  " + x)
if not dry and (moved_dirs or plan):
    print("next: scripts/migrate_all.sh, or python3 scripts/lab.py check")
PY
