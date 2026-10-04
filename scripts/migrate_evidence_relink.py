#!/usr/bin/env python3
"""Relink the generated evidence blocks for the phase layout, under the held-file policy.

`scripts/experiment_evidence.py --write --relink` re-renders the evidence block of every study document so
its registry and rubric links follow the new layout. Run bare, it would also rewrite documents whose sha256
is recorded in the research record. This wrapper asks the same generator for the same output and then
applies the policy in scripts/migrate_common.py:

  * documents nobody records, and class (a) documents with --include-recorded, are written, and each
    class (a) document's digest is updated in the registries that record it
    (5-experiments/evidence-metadata.json `source_sha256`, lock and attestation ingredient digests);
  * class (b) documents stay byte-identical. Their block keeps the pre-move links, which
    `experiment_evidence.py --check` accepts by design (its LEGACY table), so the check still passes.

The registry itself needs no regeneration after this: blocks are rendered from the `studies` rows, which the
digest replacement does not touch, and 5-experiments/EVIDENCE.md is rewritten here if it is stale.

    python3 scripts/migrate_evidence_relink.py                              # dry run
    python3 scripts/migrate_evidence_relink.py --write --include-recorded
    python3 scripts/migrate_evidence_relink.py --only <path-prefix> ...
"""
import json, os, sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import migrate_common as mc
import experiment_evidence as ee

os.chdir(mc.ROOT)


def main():
    argv = sys.argv[1:]
    write, include = "--write" in argv, "--include-recorded" in argv
    only = mc.only_args(argv)
    root = Path(mc.ROOT)
    try:
        data = json.loads(ee.repo_file(root, ee.REGISTRY).read_text(encoding="utf-8"))
        rendered = ee.outputs(root, data, relink=True)
    except (ValueError, OSError) as error:
        print(f"Evidence metadata error: {error}", file=sys.stderr)
        return 1
    candidates = {}
    for path, content in rendered.items():
        if not mc.under(path, only):
            continue
        new = content.encode("utf-8")
        old = (root / path).read_bytes() if (root / path).exists() else b""
        if old != new:
            candidates[path] = (old, new)
    recorded = mc.Recorded()
    written, held_a, held_b, touched = mc.settle(recorded, candidates, include, write)
    print(f"{'relinked' if write else 'would relink'} {len(written)} evidence documents")
    if touched:
        print(f"{'updated' if write else 'would update'} {sum(touched.values())} recorded digests in {len(touched)} registry files")
    print(f"held, class (a) registry-recorded (rewritten with --include-recorded): {len(held_a)} documents")
    print(f"held, class (b) recorded in the research record (block keeps pre-move links): {len(held_b)} documents")
    if "--list-held" in argv:
        for f in sorted(held_a):
            print(f"  held (a)  {f}  <- {held_a[f][0]}")
        for f in sorted(held_b):
            print(f"  held (b)  {f}  <- {held_b[f][0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
