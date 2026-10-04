#!/usr/bin/env bash
# One-shot move from the flat hackathon layout to the phase layout. Pure renames, no content edits,
# so file hashes recorded in pre-registrations and the artifact lock stay valid.
# Re-run on a fresh checkout of the old layout (for example a lane branch) before merging it.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
[ -d library ] || { echo "already migrated (no library/)"; exit 0; }

mkdir -p lab 5-experiments/studies

# research phases
git mv library 1-library
git mv surveys 2-surveys
git mv reviews 2-surveys/reviews
git mv synthesis 3-synthesis
git mv hypotheses 4-hypotheses
for f in experiments/* experiments/.[!.]*; do [ -e "$f" ] && git mv "$f" 5-experiments/; done
rmdir experiments 2>/dev/null || true
git mv tooling 5-experiments/toolkit

# studies: each researcher's working notes hold the experiment studies
for d in researchers/*/; do
  r=$(basename "$d")
  [ -d "researchers/$r/notes" ] && git mv "researchers/$r/notes" "5-experiments/studies/$r"
  for extra in factory qa; do
    [ -d "researchers/$r/$extra" ] && git mv "researchers/$r/$extra" "5-experiments/studies/$r/$extra"
  done
done

# coordination: task board, agent status, inboxes, intake pipeline, templates
git mv researchers lab/researchers
git mv tasks lab/tasks
git mv candidates lab/candidates
git mv templates lab/templates
git mv STATUS.md lab/STATUS.md
git mv PIPELINE.md lab/PIPELINE.md
echo "moved. next: python3 scripts/lab.py check"
