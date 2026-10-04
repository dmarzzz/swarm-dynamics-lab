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
- researchers/vishesh/notes/dissent/rd5/PLAN.md
- researchers/vishesh/notes/dissent/rd5/FAILURE-ANALYSIS.md
- researchers/vishesh/notes/dissent/rd5/IMPROVEMENTS.md
- researchers/vishesh/notes/dissent/rd5/RESEARCH-QUESTIONS.md
- researchers/vishesh/notes/dissent/rd5/analysis/rd4-failure-decomposition.json
- library/papers/hay-2012-selecting.md
- library/papers/tan-2016-honey.md
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
