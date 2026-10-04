---
id: build-sybil-scarcity-xmodel
type: task
title: Prepare sybil-scarcity-xmodel (cross-model replication of sybil-scarcity-opus on identical packets) to launch-ready
kind: build
status: claimed
priority: p0
owner: dmarz/pipeline-scarcity-qwen
for: dmarz
created: 2026-10-04
created_by: dmarz/pipeline-scarcity-qwen
depends_on: []
topics:
- sybil-resistance
- llm-agent-swarms
claimed_at: 2026-10-04T12:29Z
updated: 2026-10-04T12:29Z
---

## Goal

Replicate the strongest result of the night, sybil-scarcity-opus (specialist accuracy 4.2% at one truthful carrier per rare fact against 100% at 81, Opus 5.5), on the identical packets with two pre-registered models, each as its own chain: qwen/qwen3.7-flash (OpenRouter, reasoning disabled) and gpt-6-sol (OpenAI, reasoning effort low). Study directory `researchers/dmarz/notes/sybil-scarcity-xmodel/`. Chosen by dmarz/fleet-monitor under dmarz's instruction to keep experiments running; dmarz did not name it. Preparation only: this task launches nothing and makes no model call.

## Done when

- [x] Code, selftests, offline S0 with byte-identity proof against the parent, manifest, rehearsal (full chain; failed Q0 stops with no S1).
- [x] README, preregistration, setup record, runbook, visualization mapping, READY.yaml and reviews/chain-001-pre.md on main for the Qwen chain.
- [ ] gpt-6-sol path: reference OpenAI adapter, price row, tests and its own pre-run review in a later code commit.
- [ ] Run requests filed in the private run queue after the fleet monitor's go.
