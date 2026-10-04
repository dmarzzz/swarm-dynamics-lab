# Antsy v8: verify the field, not the vote

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-methods; source `f76f0248` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — Corrected extraction improves the primary reader on reused development receipts; fresh qualification and checker benefit remain untested. Basis: Two parser defects corrected after inspecting development failures. Replaying the same observations yields 13 rather than 11 correct primary totals of 19 scorable receipts; weak-checker fallback adds an error and is rejected.
- **sample_size_summary:** 20 reused receipts, 19 scorable; 100 saved OCR observations replayed twice, not 40 independent receipts. Zero new native calls. Fresh Q0 and held-out S1 unrun.
<!-- experiment-evidence:end -->

Exploratory development and next-study design. **Fresh qualification has not run.**

- [Next native Q0 plan](NATIVE-Q0.md) and [pre-run assessment](reviews/Q0-pre.md)
- [Results: primary improved on used data; Tesseract checker rejected](RESULTS.md)
- [Prospective plan](PLAN.md) and [current amendment](AMENDMENT-01.md)
- [Authoritative setup and next gates](SETUP.md)
- [Tested field/policy prototype](src/fields.py) and [EasyOCR output adapter](src/adapter.py)

Native Q0 runner and operator packet are implemented; 31 offline checks include successful mocked dispatch, first-error stop and duplicate-run refusal. Actual runtime/model staging, exclusive fleet admission and fresh qualification remain pending through the orbital run queue. No old v7 qualification, used-data gain or passing unit test substitutes for fresh Q0.

## Design transfer — 2026-10-04

[Lessons from Dmarz’s recent studies](DESIGN-TRANSFER.md): specific controls, measurements and next-design options. Prospective only; current run contracts and approval status are unchanged.
