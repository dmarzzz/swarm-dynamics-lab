---
id: integrate-run-closeout-cycle
type: task
title: Integrate automatic run closeout and approved next-run planning
kind: build
status: done
priority: p1
owner: vishesh/codex-pi-review
for: vishesh
created: 2026-10-04
created_by: vishesh/codex-pi-review
depends_on: []
topics: []
claimed_at: 2026-10-04T07:50Z
updated: 2026-10-04T08:03Z
outputs:
- tooling/agent-experiments/RUN-REVIEW.md
- tooling/agent-experiments/RUN-QUALITY.md
- scripts/experiment_ops/closeout.py
- scripts/experiment_ops/iteration.py
---

## Goal

Implement the owner-requested completion loop: automatic evidence-based post-mortem handoff, next-session run-quality assessment and concrete successor plan, owner approval of the update before provisioning/dispatch. Preserve cumulative budgets, historical outcomes and study-specific admission. Tooling and offline tests only; no new experimental execution.

## Done when

- [x] Add recoverable automatic completion records to supported shared run paths.
- [x] Define run-quality assessment and next-run sample/scenario/data planning with owner approval.
- [x] Expose next-session handoff and bind successor approval to the reviewed proposal.
- [x] Test terminal, interruption, recovery, stale approval and privacy boundaries; publish accurate adapter limits.
