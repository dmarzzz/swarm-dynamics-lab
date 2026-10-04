---
id: right-dissenter-rd4
type: task
title: Repair and evaluate the Right Dissenter recovery protocol
kind: experiment
status: done
priority: p1
owner: vishesh/codex-decision-models
for: vishesh
created: 2026-10-03
created_by: vishesh/codex-decision-models
depends_on: []
topics:
- dissent
- decision-models
claimed_at: 2026-10-04T04:59Z
updated: 2026-10-04T06:28Z
outputs:
- 5-experiments/studies/vishesh/dissent/rd4/REPORT.md
- 5-experiments/studies/vishesh/dissent/rd4/CLOSEOUT.md
- 5-experiments/studies/vishesh/dissent/rd4/results/combined/summary.json
- artifacts/right-dissenter-rd4-results/right-dissenter-rd4-results-v1.png
- artifacts/right-dissenter-rd4-replay/right-dissenter-rd4-replay-v1.mp4
---

## Goal

Incorporate Dmarz RD-R1/R2/R3 feedback, repair closure invariants, and evaluate a prospective symmetric stop/resume amendment under the existing cumulative cap. Preserve prior results; keep formal confirmation closed.

## Done when

- [x] Publish a prospective plan and feedback response before implementation.
- [x] Repair and regression-check duplicate identity, persistent closure and qualification separation.
- [x] Qualify and run the bounded successor if admission checks pass; retain all outcomes.
- [x] Publish analysis, replay, post-mortems and allocation closeout.

## Coverage note

Completed qualification24/24 and all576fixed S4decisions. Two interrupted segments retained, final continuation completed only unstarted trajectories. Exact saved-data replay, native closure assertions and conservative failure sensitivity published. No net symmetric-gate benefit; independent semantic corpus and explicit native version/expiry/late-verifier strata remain future work. Dmarz allocation released after all artifact hashes matched.
