# Post-mortem: s0-local-001

- Experiment / owner / stage / date: sybil-newcomer-sonnet / dmarz / local scripted S0 / 2026-10-04.
- Pre-run assessment: [s0-local-001-pre](s0-local-001-pre.md); code fec657cf6b5d198783b400f1605207c8c338ae72; source hash `a0fa76922ed6000bb07bca6c9d9bbae312b566f4e4cd7271e147c87f75833ed4`; Python 3.12.3 venv with pinned requirements.
- Run IDs: local attempt `s0-local-001` (outputs git-ignored). Reproduce: `python3 src/worker.py --stage S0 --attempt <fresh>`.
- Disposition: advance to fleet S0.

## What ran and what happened

- 198 planned → 198 started → 198 terminal → 198 graded → 198 analyzed; 0 invalid, 0 not started, 0 duplicates.
- 0 model calls, $0.
- Scripted qualification passed in all three shapes (12/12 each; field accuracy, exact packets and abstention all 1.0).
- Selftests 8/8 passed. A discarded pre-commit smoke run of the same command produced the same counts and source hash.
- Expected versus observed: as expected.

## Visualization review

Mapping v1 inherited. Initial, final and 8-frame replay rendered at 1800×1200; the banner reads SONNET only on API stages (S0 shows SCRIPTED, as designed). Final frame matches the scripted counts.

## Experiment-quality assessment

- Engineering check only; no scientific content. Assignments for Q0 and S1 match the parent study exactly (digests in SETUP.md).
- evidence_confidence stays 0 (unrun).

## Failure and repair ledger

| ID / kind | Observed evidence | Suspected or verified cause | Repair / diagnostic | Acceptance check and rerun evidence | Owner / status |
|---|---|---|---|---|---|
| none | — | — | — | — | — |

## Next run

Fleet S0 `s0-001` on sim-dmarz-5 at a revision carrying this post-mortem, per [fleet-s0-001-pre](fleet-s0-001-pre.md). Q0 stays blocked on review or owner waiver.
