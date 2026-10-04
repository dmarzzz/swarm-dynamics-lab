---
id: fix-discussion-review-findings
type: task
title: Address Vishesh's discussion-dose review in the v3 successor
kind: build
status: done
priority: p1
owner: dmarz/discussion-bench-v3
for: dmarz
created: 2026-10-03
created_by: dmarz/discussion-bench-v3
depends_on: []
topics: []
claimed_at: 2026-10-04T02:28Z
updated: 2026-10-04T02:34Z
outputs:
- researchers/dmarz/notes/discussion-dose/benchmark-v3/VISHESH-REVIEW-RESPONSE.md
- researchers/dmarz/notes/discussion-dose/benchmark-v3/review-fixes-validation.json
---

## Goal

Implement the user-requested repairs from Vishesh's [retrospective review](../researchers/vishesh/notes/independent-reviews-2026-10-04/discussion-dose.md) in the current v3 successor. Preserve retired v1/v2 code/results and the independent review record. No model run or deployment is requested.

## Done when

- [x] Validate every observed row against its assignment before analysis; preserve wholly absent worlds and bounds.
- [x] Validate the full allocation before dispatch and reject changes to the frozen evidence partition.
- [x] Expose correct-but-unsupported, wrong-but-unsupported, grounded inherited errors and required-key coverage separately.
- [x] Verify matched private work, exact starting checkpoints, initial contamination and clean diagnostics.
- [x] Run regression/mutation checks and saved-response replay; publish a finding-to-evidence response without claiming independent approval.
