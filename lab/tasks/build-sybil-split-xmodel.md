---
id: build-sybil-split-xmodel
type: task
title: 'Prepare sybil-split-xmodel (cross-model replication of sybil-split-opus: Qwen3.7 Flash and GPT-6 Sol) to launch-ready'
kind: build
status: done
priority: p0
owner: dmarz/pipeline-split-qwen
for: dmarz
created: 2026-10-04
created_by: dmarz/pipeline-split-qwen
depends_on: []
topics:
- sybil-resistance
- llm-agent-swarms
claimed_at: 2026-10-04T12:21Z
updated: 2026-10-04T12:37Z
outputs:
- researchers/dmarz/notes/sybil-split-xmodel/reviews/chain-001-pre.md
---

## Goal

Cross-model replication of sybil-split-opus (finished 2026-10-04, primary +0.41 on Opus 5.5) on byte-identical packets, with a pre-registered set of two models each run as its own complete chain: qwen/qwen3.7-flash via OpenRouter (Alibaba, reasoning disabled) and gpt-6-sol via the OpenAI API (reasoning effort low). Study directory `researchers/dmarz/notes/sybil-split-xmodel/`. dmarz did not name this study; the fleet monitor chose it under his instruction to keep experiments running and ship tonight. Preparation only: this task launches nothing and makes no model call.

## Done when

- [x] Plan and frozen design committed.
- [x] Code, selftests, offline S0 (byte identity with the parent proven), manifest and rehearsal (full chain; failed Q0 stops with no S1) for both models.
- [x] README, preregistration, pre-run review and READY.yaml on main with the pinned commit and source hash.
