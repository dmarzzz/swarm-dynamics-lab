---
id: zhang-2026-botevo
type: paper
title: 'BotEvo: LLM-Driven social bot detection via behavioral evolution modeling
  and cross-modal fusion'
authors:
- Yuxin Zhang
- Kai Qiao
- Shuhao Shi
- Jiaxin Liu
- Zihao Liu
- Jian Chen
- Lei Li
- Bin Yan
year: 2026
venue: Journal of King Saud University Computer and Information Sciences
url: https://doi.org/10.1007/s44443-026-00814-3
doi: 10.1007/s44443-026-00814-3
arxiv: null
cite: 'Yuxin Zhang; Kai Qiao; Shuhao Shi; Jiaxin Liu; Zihao Liu; Jian Chen; Lei Li;
  Bin Yan. (2026). BotEvo: LLM-Driven social bot detection via behavioral evolution
  modeling and cross-modal fusion. Journal of King Saud University Computer and Information
  Sciences, 38(6), article 460. https://doi.org/10.1007/s44443-026-00814-3'
topics:
- swarm-detection
- sybil-resistance
added_by: shadow/sol-w7
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

BotEvo combines temporal post behavior, text-pattern consistency, sentiment signals, and account attributes without requiring the social graph. The paper reports strong classification on BotSim and mixed TwiBot-20/SDAR benchmarks, using tree-based implicit fusion and risk-conditioned thresholds. Its strongest features differ sharply across datasets, cautioning against assuming one invariant signature of LLM agents.

## Contribution

A graph-agnostic detection framework with temporal weighting, nonlinear multi-view fusion, and adaptive decision thresholds.

## Key results

- Reported F1 is 96.46% on BotSim and 89.30% on TwiBot-20/SDAR, compared with 14 baselines.
- BotSim accuracy is 96.81%; its F1 exceeds BotDMM by 3.48 points. The mixed-dataset F1 advantage is 1.07 points.
- SHAP identifies text logits as dominant on BotSim and verified-account status as dominant on the mixed dataset; these are dataset-specific evidence, not operator attribution.

## Methods and models

Post-level text, sentiment and behavior features are weighted and aggregated into user representations, fused via tree-based implicit gating, then classified with threshold optimization. Read introduction, framework overview, result discussions and conclusion, not all equations or experimental tables. Main runs use five seeds; ablations use fewer.

## Limitations and open questions

Benchmarks may miss newer adversarial strategies. The mixed benchmark is a supplementary three-class setting rather than a clean out-of-distribution test. Account metadata and template-heavy generated text can supply shortcuts. No code was run, and coordinated-swarm or common-operator labels are not established.

## Relevance to us

Direct detector baseline if our traces contain post sequences but no network topology. Compare [[rossi-2024-bots]] for a broader detection bibliography and [[greenblatt-2026-brief]] for actual artifact-mediated cooperation.
