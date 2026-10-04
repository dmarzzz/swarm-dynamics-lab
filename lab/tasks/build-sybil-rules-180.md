---
id: build-sybil-rules-180
type: task
title: Prepare the 180-owner market experiment (program v5 flagship F) to launch-ready
kind: build
status: claimed
priority: p0
owner: dmarz/flagship-market
for: dmarz
created: 2026-10-04
created_by: dmarz/flagship-market
depends_on: []
topics:
- sybil-resistance
- llm-agent-swarms
claimed_at: 2026-10-04T10:31Z
updated: 2026-10-04T10:31Z
---

## Goal

Build the flagship line "F · Will they Sybil under rules?" of [research program v5](../researchers/dmarz/notes/overnight-program-2026-10-04/SETUP.md) as a launch-ready package in `researchers/dmarz/notes/sybil-rules-180/` (hub experiment `sybil-rules-180`): one connected economy of 180 model-controlled owners in 60 three-owner markets, product-licensed firms, two unregulated warm-up rounds, a checkpoint, and three ten-round rule branches restored from it, followed by the 192-call strategy-cue diagnostic. Model `qwen/qwen3.7-flash` through OpenRouter with the provider pinned, on three servers. Preparation only: this task launches nothing and makes no model call. The run goes through the private run queue after dmarz/fleet-monitor's same-researcher check. Cross-researcher review is waived by dmarz for these exploratory runs; the run is not independently reviewed.

## Done when

- [x] Deterministic economy engine with offline tests: conservation of cash and of capacity in production, reserve and transit; no cross-product transfers; activation and transfer delays; overhead on empty active firms; exact checkpoint save and restore; the focal-owner recombination counterfactual; development fixtures showing affordable other-product expansion and profitable same-product fragmentation.
- [x] Chain S0, P0, Q0, X0, S1, D1 under software gates with hard call caps (main 5,952; qualification at most 552), one coordinator and three workers, an OpenRouter adapter with the frozen request template, and the failure handling of the ready-chain contract.
- [x] Offline rehearsal against a throwaway local hub with a stub model: three workers, the checkpoint fork, a gate failure that stops the chain, the credit-pause path.
- [x] Plan, pre-registration and pre-run review (`reviews/chain-001-pre.md`) on main with the pinned commit and source hash.
- [ ] Run request filed in the private run queue after the fleet monitor's go.
