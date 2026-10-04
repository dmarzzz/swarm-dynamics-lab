#!/usr/bin/env bash
# Bring the working tree fully onto the phase layout, then prove it. Run it after merging an old-layout
# branch (for example origin/main) into the migrated branch. Stops at the first failure. Idempotent: every
# step is a no-op once its work is done, so a second run changes nothing.
#
#   scripts/migrate_all.sh             # migrate, regenerate indexes, run the checks
#   scripts/migrate_all.sh --dry-run   # show what each step would do; writes nothing, runs no checks
#   scripts/migrate_all.sh --checks    # only the checks
#
# Order matters:
#   1 migrate_layout.sh          move files that arrived at old paths (never overwrites; conflicts exit 1)
#   2 migrate_artifact_paths.py  ingredient / source path strings in the manifest, lock and attestations
#   3 migrate_links.py           relative markdown links
#   4 migrate_prose_paths.py     old paths in prose, backticks, frontmatter, default-branch GitHub URLs
#   5 migrate_evidence_relink.py the generated evidence blocks (experiment_evidence.py --write --relink,
#                                applied under the held-file policy; see that script)
#   6 lab.py index               regenerate lab/STATUS.md and 1-library/INDEX.md
# Steps 3-5 run with --include-recorded: files whose sha256 is recorded only in rewritable registries are
# rewritten and the registries updated; files recorded in the research record stay byte-identical
# (scripts/migrate_common.py has the policy).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
MODE="${1:-}"

step() { printf '\n== %s\n' "$*"; }

checks() {
  step "lab.py check";                      python3 scripts/lab.py check
  step "experiment_evidence.py --check";    python3 scripts/experiment_evidence.py --check
  step "fd.py check --strict";              python3 .flightdeck/fd.py check --strict .
  step "toolkit validate.py";               python3 5-experiments/toolkit/agent-experiments/scripts/validate.py
  step "unit tests (the set CI runs)"
  for t in test_experiment_evidence test_experiment_operations test_experiment_theseus test_experiment_closeout test_experiment_iteration; do
    python3 -m unittest discover -s scripts -p "$t.py"
  done
  step "nothing left at an old path";       scripts/migrate_layout.sh --dry-run
  printf '\nall checks passed\n'
}

if [ "$MODE" = "--checks" ]; then checks; exit 0; fi

if [ "$MODE" = "--dry-run" ]; then
  step "1 layout";            scripts/migrate_layout.sh --dry-run
  step "2 artifact paths";    python3 scripts/migrate_artifact_paths.py --dry-run
  step "3 links";             python3 scripts/migrate_links.py --include-recorded
  step "4 prose paths";       python3 scripts/migrate_prose_paths.py --include-recorded
  step "5 evidence blocks";   python3 scripts/migrate_evidence_relink.py --include-recorded
  printf '\ndry run: nothing written. Steps 3-5 are computed against the tree as it is now, not as the earlier steps would leave it.\n'
  exit 0
fi
[ -z "$MODE" ] || { echo "usage: scripts/migrate_all.sh [--dry-run|--checks]" >&2; exit 2; }

if [ -n "$(git ls-files -u | head -1)" ]; then
  echo "unmerged paths in the index: finish the merge (resolve conflicts, git add) before migrating" >&2; exit 1
fi

step "1 layout";            scripts/migrate_layout.sh
step "2 artifact paths";    python3 scripts/migrate_artifact_paths.py
step "3 links";             python3 scripts/migrate_links.py --write --include-recorded
step "4 prose paths";       python3 scripts/migrate_prose_paths.py --write --include-recorded
step "5 evidence blocks";   python3 scripts/migrate_evidence_relink.py --write --include-recorded
step "6 lab.py index";      python3 scripts/lab.py index
checks
