---
id: build-quota-splitting
type: task
title: Prepare the quota-splitting experiment (agent-budgets hunch B2) on Opus 5.5 to launch-ready
kind: build
status: claimed
priority: p1
owner: dmarz/orbital-orchestrator
for: dmarz
created: 2026-10-04
created_by: dmarz/pipeline
depends_on: []
topics:
- agent-budgets
- sybil-resistance
updated: 2026-10-04T10:48Z
history:
- '2026-10-04T10:47Z released by dmarz/pipeline-quota: paused at 6b9adefa; new owner by the fleet monitor''s assignment: dmarz/orbital-orchestrator (Experiment orchestration session on orbital-one); see researchers/dmarz/notes/quota-splitting/HANDOVER.md'
claimed_at: 2026-10-04T10:48Z
---

## Goal

Design and build hunch B2 of [the agent-budgets note](../researchers/dmarz/notes/agent-budgets-hunches.md) in `researchers/dmarz/notes/quota-splitting/`: when a quota is enforced per identity and an agent can spawn subagents, does an Opus 5.5 agent create more identities than the task needs and take more than its share of a shared pool, and do a lineage quota or a spawn fee remove that? A minimal turn-based instrument with abstract work units; not the general swarm simulator and not a real metering proxy. Hunch-level exploratory study in researcher notes, not a hypothesis (the agent-budgets survey has not passed the gate). Preparation only: this task launches nothing and makes no model inference call. The run itself goes through the private run queue after the fleet monitor's same-researcher check.

## Done when

- [x] Prospective plan and frozen design committed before implementation.
- [x] Code, offline tests and a scripted zero-model-call stage that passes offline. (76 tests; S0 193/193 at code commit fdd2e579, source hash 09c27648)
- [x] Pre-run review per tooling/agent-experiments/RUN-REVIEW.md on main with assignment manifest, call counts, gates, model settings, hard max_calls and the pinned commit. (reviews/chain-001-pre.md)
- [x] Chained launch per researchers/dmarz/notes/pipeline/READY-CHAIN.md with the server as a parameter. (READY.yaml, RUN.md; model ladder per "Providers and models")
- [ ] Run request filed in the private run queue after the fleet monitor's go.
