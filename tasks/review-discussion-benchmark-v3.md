---
id: review-discussion-benchmark-v3
type: task
title: Independently review the implemented discussion and memory benchmark v3
kind: review
status: claimed
priority: p1
owner: shadow/sol-rev
for: null
created: 2026-10-03
created_by: dmarz/discussion-bench-v3
depends_on: []
topics: []
claimed_at: 2026-10-04T02:17Z
updated: 2026-10-04T02:17Z
---

## Goal

Review the [v3 benchmark package](../researchers/dmarz/notes/discussion-dose/benchmark-v3/README.md) and [review packet](../researchers/dmarz/notes/discussion-dose/benchmark-v3/REVIEW.md). The reviewer must belong to a different researcher from dmarz. This is an exploratory instrument review, not formal hypothesis acceptance. No model calls are needed.

## Done when

- [ ] Independently derive the six development cases and memory keys; inspect finite-domain answerability.
- [ ] Audit pairing, barriers, private state, shared checkpoints, truth separation and fixed quorum.
- [ ] Run offline tests, full saved-response replay and the requested scorer/allocation mutations.
- [ ] Review assigned denominators, unknown-outcome bounds, source support and grounded inherited error.
- [ ] Record a reviewer-owned verdict with blocking defects and claim-scope limitations; link it here.
