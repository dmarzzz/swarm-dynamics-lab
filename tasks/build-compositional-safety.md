---
id: build-compositional-safety
type: task
title: Ship the compositional safety benchmark and qualification
kind: build
status: claimed
priority: p1
owner: dmarz/patchwork-hypotheses
for: dmarz
created: 2026-10-03
created_by: dmarz/patchwork-hypotheses
depends_on: []
topics:
- fork-merge-security
- llm-agent-swarms
- swarm-detection
claimed_at: 2026-10-04T02:30Z
updated: 2026-10-04T03:54Z
---

## Goal

User approved shipping the SEC-54 study plan. Implement the simulator, controls, evaluator, durable execution and reporting; qualify with offline and bounded real-model runs under existing shared authorization. Preserve exploratory status until the formal research gates pass. No claim of completion of the full scaled study before its requirements are met.

## Done when

- [ ] Implement and independently check exact simulator invariants and information boundaries.
- [ ] Ship a frozen, bounded runner with source hashes, failures, accounting and replay.
- [ ] Run and reconcile offline qualification and available model qualification.
- [ ] Publish results, review status and remaining scale prerequisites.
