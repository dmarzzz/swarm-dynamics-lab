---
id: build-quota-splitting
type: task
title: Prepare the quota-splitting experiment (agent-budgets hunch B2) on Opus 5.5 to launch-ready
kind: build
status: claimed
priority: p1
owner: dmarz/pipeline-quota
for: dmarz
created: 2026-10-04
created_by: dmarz/pipeline
depends_on: []
topics:
- agent-budgets
- sybil-resistance
claimed_at: 2026-10-04T09:27Z
updated: 2026-10-04T09:27Z
---

## Goal

Design and build hunch B2 of [the agent-budgets note](../researchers/dmarz/notes/agent-budgets-hunches.md) in `researchers/dmarz/notes/quota-splitting/`: when a quota is enforced per identity and an agent can spawn subagents, does an Opus 5.5 agent create more identities than the task needs and take more than its share of a shared pool, and do a lineage quota or a spawn fee remove that? A minimal turn-based instrument with abstract work units; not the general swarm simulator and not a real metering proxy. Hunch-level exploratory study in researcher notes, not a hypothesis (the agent-budgets survey has not passed the gate). Preparation only: this task launches nothing and makes no model inference call. The run itself goes through the private run queue after the fleet monitor's same-researcher check.

## Done when

- [ ] Prospective plan and frozen design committed before implementation.
- [ ] Code, offline tests and a scripted zero-model-call stage that passes offline.
- [ ] Pre-run review per tooling/agent-experiments/RUN-REVIEW.md on main with assignment manifest, call counts, gates, model settings, hard max_calls and the pinned commit.
- [ ] Chained launch per researchers/dmarz/notes/pipeline/READY-CHAIN.md with the server as a parameter.
- [ ] Run request filed in the private run queue after the fleet monitor's go.
