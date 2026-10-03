---
id: review-discussion-dose
type: task
title: Review SEC-47 discussion dose tasks and exploratory protocol
kind: review
status: open
priority: p1
owner: null
for: null
created: 2026-10-03
created_by: dmarz/discussion-dose
depends_on: []
topics: [fork-merge-security, llm-agent-swarms, collective-decision]
---

## Goal

Review the [exploratory discussion-dose plan](../researchers/dmarz/notes/discussion-dose/README.md), task generator, rendered evidence, independent answer checker, injected counterfactual, all-assigned scoring and architecture. A different researcher should perform this review. This task does not claim the survey or formal hypothesis gate has passed. Formal review records need a formal target before promotion.

## Done when

- [ ] Inspect at least two rendered examples per task family and independently derive the correct and false-world choices.
- [ ] Check task/evaluator leakage, source exposure versus peer propagation, ballot-probe effects, invalid denominators and paired analysis.
- [ ] Run offline tests and deliberately mutate at least one answer, tool allocation and scorer outcome.
- [ ] Decide whether the three templates are adequate for an exploratory pilot; identify what is needed for confirmation and broader task transfer.
- [ ] Record feedback in a reviewer-owned note, then link it from this task without changing hypothesis status.
