---
id: right-dissenter-rd5-design
type: task
title: Plan Right Dissenter repairs and the right to reopen
kind: question
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
claimed_at: 2026-10-04T06:40Z
updated: 2026-10-04T06:50Z
outputs:
- 5-experiments/studies/vishesh/dissent/rd5/PLAN.md
- 5-experiments/studies/vishesh/dissent/rd5/FAILURE-ANALYSIS.md
- 5-experiments/studies/vishesh/dissent/rd5/IMPROVEMENTS.md
- 5-experiments/studies/vishesh/dissent/rd5/RESEARCH-QUESTIONS.md
- 5-experiments/studies/vishesh/dissent/rd5/analysis/rd4-failure-decomposition.json
- 1-library/papers/hay-2012-selecting.md
- 1-library/papers/tan-2016-honey.md
---

## Goal

Use the RD4 post-mortem and saved decision records to explain the observed accuracy gap, prioritize separately testable repairs, and design a bounded next study of repeated uncertainty and future verification capacity. Planning and saved-data analysis only; no native run.

## Done when

- [x] Reconcile every noncorrect checking-arm outcome and each paired difference.
- [x] Publish repair contracts and acceptance criteria without claiming fixes are verified.
- [x] Develop three contrasting scenarios, strong comparators, metrics and a feasible next-stage envelope.
- [x] Link the existing research source map and catalogue any newly read primary sources without duplication.

## Coverage note

Retrospective arithmetic reconciles 288 checking-arm decisions, 26 noncorrect outcomes and every paired correctness difference. Proposed contracts, three-policy design, negative controls, budget envelope and research questions are published under dissent/rd5. Two newly read primary sources were deduplicated and verified against arXiv/Crossref with zero problems. Zero new native calls, no successor experimental implementation and no machine claim.
