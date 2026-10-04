---
id: fix-discussion-review-findings
type: task
title: Address Vishesh's discussion-dose review in the v3 successor
kind: build
status: claimed
priority: p1
owner: dmarz/discussion-bench-v3
for: dmarz
created: 2026-10-03
created_by: dmarz/discussion-bench-v3
depends_on: []
topics: []
claimed_at: 2026-10-04T02:28Z
updated: 2026-10-04T02:28Z
---

## Goal

Implement the user-requested repairs from Vishesh's [retrospective review](../researchers/vishesh/notes/independent-reviews-2026-10-04/discussion-dose.md) in the current v3 successor. Preserve retired v1/v2 code/results and the independent review record. No model run or deployment is requested.

## Done when

- [ ] Validate every observed row against its assignment before analysis; preserve wholly absent worlds and bounds.
- [ ] Validate the full allocation before dispatch and reject changes to the frozen evidence partition.
- [ ] Expose correct-but-unsupported, wrong-but-unsupported, grounded inherited errors and required-key coverage separately.
- [ ] Verify matched private work, exact starting checkpoints, initial contamination and clean diagnostics.
- [ ] Run regression/mutation checks and saved-response replay; publish a finding-to-evidence response without claiming independent approval.
