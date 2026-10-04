---
id: right-dissenter-rd5-run
type: task
title: Run approved Right Dissenter RD5 qualification and conditional pilot
kind: experiment
status: claimed
priority: p1
owner: vishesh/codex-decision-models
for: vishesh
created: 2026-10-04
created_by: vishesh/codex-decision-models
depends_on: []
topics:
- decision-models
- dissent
updated: 2026-10-04T17:38Z
history:
- '2026-10-04T09:00Z released by vishesh/codex-decision-models: Frozen RD5 source deployed, public plan verified, dedicated claim and original-ledger relay ready. Central dispatch request pending; direct-launch exception explicitly requested but unanswered. No worker or new model call. See rd5/RUN-STATUS.md and durable rd5-run/HANDOFF.json. Current relay lease ends around 09:14 UTC; do not reuse stale admission.'
- '2026-10-04T15:32Z released by vishesh/codex-decision-models: One continuation cycle completed through blocked closeout: reconciled expired A1 to 24 unstarted requests and zero RD5 calls; released claim; fixed duplicate-safe A2 activation wrapper; 61 scientific plus 5 activation checks passed; published operational/scientific post-mortem, status figure/readback and confidence0 metadata. Approved Q5/conditional H5 unchanged. Exact blocker is authorized central acknowledgement before fresh allocation/relay; no direct-launch exception inferred.'
claimed_at: 2026-10-04T16:56Z
---

## Goal

Launch the owner-approved frozen Q5-A1 qualification and, only on its gate passing, H5-A1 pilot within the original cumulative cap. Follow the current fleet dispatch workflow and retain the original budget authority.

## Done when

- [ ] Fresh dedicated approved-account allocation, source, public plan and admission checks recorded.
- [ ] Q5 completes and is audited; H5 runs only if qualified.
- [ ] All assigned outcomes and charges reconciled; artifacts verified and scientific post-mortems published.
- [ ] Workers stopped and allocation released, or an exact external blocker recorded.
