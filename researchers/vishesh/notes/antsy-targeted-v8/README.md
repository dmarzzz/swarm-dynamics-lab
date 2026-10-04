# Antsy v8: verify the field, not the vote

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-methods; source `f76f0248` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — Corrected extraction improves the primary reader on reused development receipts; fresh qualification and checker benefit remain untested. Basis: Two parser defects corrected after inspecting development failures. Replaying the same observations yields 13 rather than 11 correct primary totals of 19 scorable receipts; weak-checker fallback adds an error and is rejected.
- **sample_size_summary:** 20 reused receipts, 19 scorable; 100 saved OCR observations replayed twice, not 40 independent receipts. Zero new native calls. Fresh Q0 and held-out S1 unrun.
<!-- experiment-evidence:end -->

Exploratory study. **Fresh Q0 stopped on a checker timeout: 6 calls started, 5 valid, 1 timed out, 34 unstarted; only2/20 complete pairs. Qualification is incomplete.**

- [Native Q0 post-mortem and next decision](reviews/Q0-attempt-1-post.md)
- [Complete assignment plot](results/Q0-attempt-1/closeout.png) and [audited results](results/Q0-attempt-1/audit.json)
- [Public native run](https://swarm-live.pages.dev/#/r/antsy-targeted-v8%2FQ0-attempt-1)

- [Latest readiness review and exact dispatch blocker](reviews/Q0-readiness-review.md)
- [Next native Q0 plan](NATIVE-Q0.md) and [pre-run assessment](reviews/Q0-pre.md)
- [Results: primary improved on used data; Tesseract checker rejected](RESULTS.md)
- [Prospective plan](PLAN.md) and [current amendment](AMENDMENT-01.md)
- [Authoritative setup and next gates](SETUP.md)
- [Tested field/policy prototype](src/fields.py) and [EasyOCR output adapter](src/adapter.py)

The frozen Q0 ran on the existing team fleet after verified admission and runtime staging. The checker exceeded its45-second cold-call limit on train62. The two completed pairs were correct for both readers, but there is no estimate of correction benefit or error independence. Saved-data audits reproduce all five retained outputs. Artifacts are backed up, the host is released, and no retry or S1 was launched. The next changed execution plan requires owner approval.

## Design transfer — 2026-10-04

[Lessons from Dmarz’s recent studies](DESIGN-TRANSFER.md): specific controls, measurements and next-design options. Prospective only; current run contracts and approval status are unchanged.
