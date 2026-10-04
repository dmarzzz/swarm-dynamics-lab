---
id: itkin-2026-local
type: paper
title: Local Predictability and Collective Fidelity in LLM-Agent Societies
authors:
- Igor Itkin
year: 2026
venue: arXiv
url: https://export.arxiv.org/api/query?id_list=2609.35813
doi: null
arxiv: '2609.35813'
cite: Igor Itkin. (2026). Local Predictability and Collective Fidelity in LLM-Agent
  Societies. arXiv:2609.35813.
topics:
- llm-agent-swarms
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

This study compares individual prediction and collective forecasting for compact surrogates of LLM societies. Neighbor information helps across sixteen public-data settings, but transfer-dependent collective gains and tests on twenty-four new statements limit earlier claims about the effects of history.

## Contribution

Tests whether surrogates that predict individual LLM agents well also forecast collective outcomes, using 9,455 published trajectories plus new opinion-dynamics runs.

## Key results

- Neighbor information helps in all sixteen public-data settings; twenty-four new statements do not confirm earlier contrasting history effects; Qwen benefits after three observed rounds.

## Methods and models

9,455 published trajectories, held-out collective forecasts, and new opinion-dynamics experiments.

## Limitations and open questions

Individual predictive accuracy is not sufficient for collective fidelity, and available observations and transfer conditions must be controlled.

## Relevance to us

A direct warning for simulation-based work here: individual-level fit does not guarantee collective fidelity, so any surrogate swarm we build needs a collective-level validation step.

## Access provenance

Opened the HTTPS arXiv export record and read its abstract on 2026-10-03. No citation count inferred from an absent or mismatched index record.

## Notes from shadow/sol-1

Read on 2026-10-03 from arXiv HTML (https://arxiv.org/html/2609.35813): sections I to VI, XI, XII and XIII; appendices not read. Depth for this note: skim of methods and results.

- Reanalyses the public [[el-2026-physics]] agent-opinions snapshot (9,600 episodes, 9,455 retained, N = 32, 4 backbones, 60 questions, 14 signed/unsigned graphs) with logistic surrogate policies: interaction-free, global mean, degree-only, graph fields h+ and h-, normalised neighbourhood means, and 1 or 2 history lags. Each surrogate is rolled out autonomously (R = 200 draws per initial state) and scored on magnetisation-trajectory MAE and terminal Wasserstein-1.
- Graph fields lower one-step log loss in all 16 cells (pooled 0.152 nats on held-out questions) and improve collective MAE by 0.0315 [0.0188, 0.0465] on held-out questions, but under joint question-and-graph shift the collective gain is unresolved (0.0238 [-0.0059, 0.0556]). History lags improve local log loss in 15 of 16 cells with no resolved collective gain. Absolute collective errors stay large (Qwen objective MAE about 0.49).
- New trajectories at N = 16, 32, 64, 128 (T = 3) do not show a resolved graph-over-scalar advantage, and 9 of 23 calibratable backend/question pairs had single-class training targets.
- Prospective test on 24 new subjective statements (192 episodes, 46,080 responses, protocol hash-frozen 14 Sep 2026, not third-partyly preregistered): the earlier opposite autonomous history effects for Gemma and Qwen are not confirmed. Qwen gains from history only after three observed rounds, and a simple two-state model fitted to those rounds beats the graph policy.
- Implication: a surrogate that predicts individual updates well can still misforecast the collective; surrogate N-sweeps (the "fit once, sweep N on a laptop" trick of [[itkin-2026-poor]]) need direct collective validation at the target N.
