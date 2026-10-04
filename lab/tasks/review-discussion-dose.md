---
id: review-discussion-dose
type: task
title: Review SEC-47 discussion dose tasks and exploratory protocol
kind: review
status: done
priority: p1
owner: vishesh/codex-independent-reviews
for: null
created: 2026-10-03
created_by: dmarz/discussion-dose
depends_on: []
topics:
- fork-merge-security
- llm-agent-swarms
- collective-decision
claimed_at: 2026-10-04T02:20Z
updated: 2026-10-04T02:26Z
outputs:
- 5-experiments/studies/vishesh/independent-reviews-2026-10-04/discussion-dose.md
---

## Goal

Review the [exploratory discussion-dose plan](../../5-experiments/studies/dmarz/discussion-dose/README.md), task generator, rendered evidence, independent answer checker, injected counterfactual, all-assigned scoring and architecture. A different researcher should perform this review. This task does not claim the survey or formal hypothesis gate has passed. Formal review records need a formal target before promotion.

## Done when

- [x] Inspect at least two rendered examples per task family and independently derive the correct and false-world choices.
- [x] Check task/evaluator leakage, source exposure versus peer propagation, ballot-probe effects, invalid denominators and paired analysis.
- [x] Run offline tests and deliberately mutate at least one answer, tool allocation and scorer outcome.
- [x] Decide whether the three templates are adequate for an exploratory pilot; identify what is needed for confirmation and broader task transfer.
- [x] Record feedback in a reviewer-owned note, then link it from this task without changing hypothesis status.

## Review outcome

Independent retrospective review by vishesh/codex-independent-reviews: [verdict and reproductions](../../5-experiments/studies/vishesh/independent-reviews-2026-10-04/discussion-dose.md). Adequate for the retired engineering pilot; revise before scientific reuse. No new model run or v3 approval.
