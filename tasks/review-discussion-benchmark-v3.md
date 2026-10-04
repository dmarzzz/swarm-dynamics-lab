---
id: review-discussion-benchmark-v3
type: task
title: Independently review the implemented discussion and memory benchmark v3
kind: review
status: claimed
priority: p1
owner: vishesh/codex-independent-reviews
for: null
created: 2026-10-03
created_by: dmarz/discussion-bench-v3
depends_on: []
topics: []
claimed_at: 2026-10-04T02:50Z
updated: 2026-10-04T02:50Z
history:
- 2026-10-04T02:50Z user-directed transfer from shadow/sol-rev to vishesh/codex-independent-reviews; user explicitly requested claiming and acting on this design review; preserve prior work and source requirements
---

## Goal

Review the [v3 benchmark package](../researchers/dmarz/notes/discussion-dose/benchmark-v3/README.md) and [review packet](../researchers/dmarz/notes/discussion-dose/benchmark-v3/REVIEW.md). The reviewer must belong to a different researcher from dmarz. This is an exploratory instrument review, not formal hypothesis acceptance. No model calls are needed.

## Done when

- [x] Independently derive the six development cases and memory keys; inspect finite-domain answerability.
- [x] Audit pairing, barriers, private state, shared checkpoints, truth separation and fixed quorum.
- [x] Run offline tests, full saved-response replay and the requested scorer/allocation mutations.
- [x] Review assigned denominators, unknown-outcome bounds, source support and grounded inherited error.
- [x] Record a reviewer-owned verdict with blocking defects and claim-scope limitations; link it here.

## Independent verdict

**PASS for the frozen exploratory instrument**, by vishesh/codex-independent-reviews, 2026-10-04 UTC. [Full independent review](../researchers/vishesh/notes/discussion-benchmark-v3-review/REVIEW.md) and [exact source hashes](../researchers/vishesh/notes/discussion-benchmark-v3-review/source-receipt.json). 89 distinct existing tests passed; 96 cases/636 requests/1,790 events replayed; independent derivations, boundary and mutation checks completed. Source includes d76146b repairs and subsequent operator-launch/reporting amendments. This is not model qualification, a paid launch, hypothesis acceptance or holdout authorization. Browser playback remains unverified; saved replay data and terminal values were checked.
