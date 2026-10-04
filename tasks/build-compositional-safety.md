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
updated: 2026-10-04T04:08Z
history:
- '2026-10-04T04:04Z released by dmarz/patchwork-hypotheses: Simulator, runner and live dashboard shipped; S0 and all four Q0 attempts reconciled. q0-004 failed: 10/24 safe, twelve incomplete, two provider refusals. Worker and uploads finished; sim-dmarz claim released. Resume after requested approved model connection, bounded diagnosis and fresh current-source qualification; P1/S1/S2 remain closed.'
claimed_at: 2026-10-04T04:08Z
---

## Goal

User approved shipping the SEC-54 study plan. Implement the simulator, controls, evaluator, durable execution and reporting; qualify with offline and bounded real-model runs under existing shared authorization. Preserve exploratory status until the formal research gates pass. No claim of completion of the full scaled study before its requirements are met.

## Done when

- [x] Implement simulator invariants and information boundaries; check with a separate replay evaluator and 4,200 reference fixtures (same author, not an external review).
- [x] Ship a frozen, bounded runner with source hashes, failures, accounting and replay.
- [x] Run and reconcile offline qualification and available model qualification; model acceptance failed and remains unresolved.
- [x] Publish results, review status and remaining scale prerequisites.
- [ ] Pass current-source model qualification before the larger pilot; blocked on an approved alternative model connection.

## Coverage note

Deployed to sim-dmarz; all workers stopped and the fleet claim was released after verified uploads. S0: 84/84 scripted completions. Four model qualification attempts and two atomic diagnostics are retained under researchers/dmarz/notes/compositional-safety. Latest q0-004: 10/24 safe, twelve incomplete, two provider refusals. Full post-mortem and summaries are published there; P1/S1/S2 remain closed. Agentops PR 79 fixes the live dashboard loading error. Resume only after reading q0-004-post.md, selecting the requested approved connection and obtaining a fresh server claim.
