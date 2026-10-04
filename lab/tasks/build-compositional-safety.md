---
id: build-compositional-safety
type: task
title: Ship the compositional safety benchmark and qualification
kind: build
status: open
priority: p1
owner: null
for: dmarz
created: 2026-10-03
created_by: dmarz/patchwork-hypotheses
depends_on: []
topics:
- fork-merge-security
- llm-agent-swarms
- swarm-detection
updated: 2026-10-04T04:58Z
history:
- '2026-10-04T04:04Z released by dmarz/patchwork-hypotheses: Simulator, runner and live dashboard shipped; S0 and all four Q0 attempts reconciled. q0-004 failed: 10/24 safe, twelve incomplete, two provider refusals. Worker and uploads finished; sim-dmarz claim released. Resume after requested approved model connection, bounded diagnosis and fresh current-source qualification; P1/S1/S2 remain closed.'
- '2026-10-04T04:58Z released by dmarz/patchwork-hypotheses: q0-005 results, complete raw traces, analysis and post-mortem published. 24 valid,21 safe,2 violations,1 stall; qualification failed unchanged. d0-003 plan published only; user explicitly says DO NOT START. Worker exited, uploads verified, fleet claim released PR146. Resume only on later explicit user instruction; no automatic repair or launch.'
---

## Goal

User approved shipping the SEC-54 study plan. Implement the simulator, controls, evaluator, durable execution and reporting; qualify with offline and bounded real-model runs under existing shared authorization. Preserve exploratory status until the formal research gates pass. No claim of completion of the full scaled study before its requirements are met.

## Done when

- [x] Implement simulator invariants and information boundaries; check with a separate replay evaluator and 4,200 reference fixtures (same author, not an external review).
- [x] Ship a frozen, bounded runner with source hashes, failures, accounting and replay.
- [x] Run and reconcile offline qualification and available model qualification; model acceptance failed and remains unresolved.
- [x] Publish results, review status and remaining scale prerequisites.
- [ ] Pass current-source model qualification before the larger pilot; q0-005 failed, and the user explicitly requested publishing the next plan without starting it.

## Coverage note

The execution-v2 repair is shipped. Latest q0-005 completed 24/24 valid episodes with 21 safe, two approval-reuse violations and one stall; qualification failed under unchanged criteria. All original attempts are retained. Full compressed observations, events, per-episode CSV, summary, hashes, analysis and post-mortem are under 5-experiments/studies/dmarz/compositional-safety/records/q0-005 and reviews/q0-005-post.md. The prospective d0-003 plan is publication only: the user explicitly instructed no next run. P1/S1/S2 remain closed. Worker exited and all 13 hub records/57 artifacts reconciled; exclusive repair claim released through agentops PR 146 at 2026-10-04T04:55:23Z. Resume only after a later explicit user instruction, reading the post-mortem and plan, implementing the proposed manifest with tests, and obtaining a fresh server allocation and admission evidence. Do not automatically resume this open task to launch experiments.
