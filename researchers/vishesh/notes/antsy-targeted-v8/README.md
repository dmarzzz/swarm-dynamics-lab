# Antsy v8: verify the field, not the vote

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-methods; source snapshots shown per cohort ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

**Antsy v8: development replay cohort** (`antsy-targeted-v8`)
Source: `f76f0248`.

- **evidence_confidence:** **1/4** — Corrected extraction improves the primary reader on reused development receipts; this cohort does not establish fresh qualification or checker benefit. Basis: Two parser defects corrected after inspecting development failures. Replaying the same observations yields 13 rather than 11 correct primary totals of 19 scorable receipts; weak-checker fallback adds an error and is rejected.
- **sample_size_summary:** Development only:20 reused receipts,19 scorable;100 saved OCR observations replayed twice,not40 independent receipts. Zero new calls in this cohort. Fresh native Q0 is assessed separately.

**Antsy v8: fresh Q0 runtime qualification** (`antsy-targeted-v8-q0`)
Source: `023fe193`.

- **evidence_confidence:** **1/4** — The frozen checker failed its execution deadline; fresh competence and complementary correction remain unestablished. Basis: Six starts produced five valid outputs and one45-second timeout. Two completed pairs were correct; the third is partial and17never started. Same-author saved-output audit verifies retained decisions, not population safety or error independence.
- **sample_size_summary:** 20 paired receipts assigned;2complete,1partial,17unstarted.40OCR calls assigned;6started,5valid,1timeout,34unstarted. Conditional rescue and error correlation are not estimable; no S1.

**Antsy v8: D1 cold-reader latency diagnostic** (`antsy-targeted-v8-d1`)
Source: `6a997edf`.

- **evidence_confidence:** **1/4** — The larger reused receipt required46.25s and still produced an abstention; OCR occupied36.63s. Current cold45s eligibility remains unmet. Basis: Three started calls all returned valid phase-complete outputs; first slow-call stop left three repetitions unstarted. Saved raw outputs and phases replay and hash-match. This bounded same-author diagnostic supports local latency interpretation, not efficacy, error independence or population inference.
- **sample_size_summary:** 3distinct reused receipts observed once;6calls planned,3valid,3unstarted,0execution failures. No second repetitions, fresh qualification or S1; zero new charges.
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


## Offline repair prepared

[Execution repair v1](execution-repair-v1/README.md) adds durable phases and private timeout streams, with13passing offline fault tests. The [concrete six-call D1 proposal](execution-repair-v1/PLAN.md) awaits owner approval. This is not a native rerun or a claim that the checker is faster.


## Latest: D1 latency diagnostic completed

[D1 post-mortem](reviews/D1-latency-attempt-1-post.md):3valid calls,3unstarted after the larger receipt took46.25s. Its36.63s OCR phase dominated;the resulting candidate still abstained. The45s requirement was not relaxed;qualification remains closed. Full traces retained;no new charges;host released. [Native phase plot](results/D1-latency-attempt-1/final_frame.png).
