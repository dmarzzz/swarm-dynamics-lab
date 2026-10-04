---
id: deploy-discussion-v3-d1
type: task
title: Deploy and preserve the bounded discussion v3 D1 diagnostic
kind: experiment
status: done
priority: p1
owner: dmarz/discussion-bench-v3
for: dmarz
created: 2026-10-04
created_by: dmarz/discussion-bench-v3
depends_on:
- plan-discussion-v3-successor
topics: []
claimed_at: 2026-10-04T04:18Z
updated: 2026-10-04T05:19Z
outputs:
- researchers/dmarz/notes/discussion-dose/benchmark-v3/RESULTS-D1.md
- researchers/dmarz/notes/discussion-dose/reviews/v3-d1-a1-post.md
- researchers/dmarz/notes/discussion-dose/benchmark-v3/D2-PLAN.md
---

## Goal

The user requested a stronger-model diagnostic as soon as possible. Coordinate with dmarz/cloud-discussion-d1, which owns the public harness and offline repairs, to deploy exactly one frozen v3-d1-a1 batch through the established operator-controlled fleet. The operator owns paid dispatch; the cloud task must not duplicate it.

Use the [committed next-run plan](../researchers/dmarz/notes/discussion-dose/benchmark-v3/NEXT-RUN.md), [Q0 post-mortem](../researchers/dmarz/notes/discussion-dose/reviews/v3-q0-a1-post.md) and [setup runbook](../tooling/agent-experiments/EXPERIMENT-SETUP.md). D1 is 120 paired calls on already-open examples, not fresh qualification. Holdout, D2, Q1 and larger sweeps remain closed.

## Done when

- [x] Verify committed runner, immutable plan and admission receipts against exact saved Q0 actor inputs, with zero retries and durable duplicate-dispatch guards.
- [x] Prepare one dedicated worker and exclusive claim, record account/state verification privately, and preserve all other hosts.
- [x] Rehearse the actual worker path with no paid requests and verify client-independent execution, failures, audit and artifact transport.
- [x] Launch only the fixed D1 allocation; reconcile all assigned calls, cost, validity and development competence measures.
- [x] Audit, preserve and commit the report/post-mortem before any later batch; release and retire only the D1 worker after durable verification.
- [x] Report cloud credential and owner-lifecycle limitations honestly; do not claim unattended cleanup unless it is verified.
