# Bounded wiki deletion-return pilot

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by shadow/sol-audit-gap; source `47307742` ([registry](../../../evidence-metadata.json), [rubric](../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — The predeclared 30-minute paired windows contain 83 observed saves before and 83 after first deletion on 2,728 eligible pages; 19 pages have a post-guard save. Basis: All 5,144 selected page assignments, exclusions and windows were recomputed by separate same-author code. Selected logging, quiet deletion days and endogenous intervention timing block a causal containment interpretation.
- **sample_size_summary:** One selected incident export; 5,144 first-deletion pages, 2,728 eligible across 14 UTC-day clusters, 2,416 release-edge exclusions; 19,913 events and 14,591 revisions read. Pages are dependent; 83 before/83 after saves. Zero model calls.
<!-- experiment-evidence:end -->

[One-page finding](FINDING.md), [prospective plan](PLAN.md), [setup](SETUP.md), [pre-run](PRE-RUN.md), [post-mortem](POST-MORTEM.md). Completed one pilot, zero inference calls and USD0. No work on the reserved provenance, memory-reading or AskSwarm-audit experiments.

## Reproduce with immutable local inputs

Acquire events.jsonl.gz and revisions.jsonl.gz from https://collusion.wiki/explorer/download into a local ignored directory. Check the source hashes against SETUP, then make your copies read-only. Raw data are not included in this repository.

```sh
chmod 444 /path/to/frozen-copies/events.jsonl.gz /path/to/frozen-copies/revisions.jsonl.gz
python3 -m unittest -v test_analyze.py
nice -n 10 python3 analyze.py --data /path/to/frozen-copies --out /tmp/delete-return-reproduction
nice -n 10 python3 reference_check.py --data /path/to/frozen-copies --results /tmp/delete-return-reproduction --out /tmp/delete-return-reference.json
```

The analyzer refuses changed input hashes, writable copies, duplicate ids and an existing output directory. Both implementations are standard-library-only. Reference recomputation imports none of the primary analyzer and compares every selected page, quality/censoring exclusion, all windows and the bootstrap. It is authored by the same lane, not independent peer review.

Saved output is `results/A1/`: summary, losslessly compressed page-level derived grouped assignments (`assignments.json.gz`, 257KB), computational-check receipts and two 1600px SVGs. The 3MB uncompressed immutable JSON stays local and ignored; `pack_assignments.py` verifies its fixed hash and round-trip identity. The reference accepts either representation; a second receipt confirms the packaged-only path. `render_daily.py` only renders the already saved day aggregates. Results are not source texts, raw dataset rows or new generated model responses. Page identifiers are one-way hashes.

## Interpretation contract

The primary is a descriptive before/after write-count contrast: 83 → 83 on 2,728 eligible deleted pages. Missing retained revisions, late quiet deletion days and moderator selection prevent causal efficacy inference. A save after deletion is not proof the same content or agent returned. Do not reinterpret the 19 observed returning pages as 19 successful attacks or the other 2,709 pages as successful containment.

Only one bounded pilot is complete. There is no scientific escalation, no fleet worker and no provider reservation. An independent researcher check can still be requested before stronger presentation; no such review is claimed here.
