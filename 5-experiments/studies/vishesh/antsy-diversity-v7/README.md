# Antsy v7: worker diversity

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-methods; source `5114250e` ([registry](../../../evidence-metadata.json), [rubric](../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — Repaired native pilot shows competence mismatch and quorum coverage loss; it does not establish a diversity benefit. Basis: 100/100 valid OCR calls, but best Tesseract worker1/19 correct fails the per-family gate while RapidOCR R0 is11/19. S1 unrun; small dependent qualification outcomes only.
- **sample_size_summary:** Repaired qualification:20/20 paired receipts,19 scorable,100/100 valid OCR calls,220 policy outcomes; S1 unrun. Parent interrupted after10 recorded receipts,30 valid/20 invalid calls plus uncertain partial work. Vendor independence unknown.
<!-- experiment-evidence:end -->

Exploratory tool-worker study, not an LLM experiment or accepted hypothesis.

- [Prospective plan](PLAN.md)
- [Authoritative setup record](SETUP.md)
- [Parent final assessment](../antsy-receipt-v6/RESULTS.md)


Current result: **qualification failed; S1 not run.** The repaired run completed100/100 valid OCR calls on20 receipts. RapidOCR R0 got11/19 scorable totals correct; the best Tesseract variant got1/19, failing the minimum per-family competence gate. [Results and visual evidence](RESULTS.md) · [post-mortem](reviews/S0-repair-post.md) · [reusable diversity protocol](DIVERSITY-PROTOCOL.md).

[Prospective lessons from Dmarz’s recent experiments](../antsy-targeted-v8/DESIGN-TRANSFER.md) inform the next design without changing this cohort or authorizing a new run.

## External study-review proposals — 2026-10-04

[Recommendation dispositions and next-step acceptance checks](../antsy-targeted-v8/EXTERNAL-REVIEW-PROPOSALS.md). These reconcile the external review with newer evidence; they are proposals, not completed fixes or changes to frozen runs. Use the latest owning post-mortem and current diagnostic authority before acting.
