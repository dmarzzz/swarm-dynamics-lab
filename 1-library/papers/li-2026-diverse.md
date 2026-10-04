---
id: li-2026-diverse
type: paper
title: 'Diverse Evidence, Better Forecasts: Multi-Agent Deliberation Under Information Asymmetry'
authors: [Yuante Li, Yicheng Tao, Kate Zhang, Taozhi Wang, Gefei Gu, Yaxin Zhou]
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2607.01661
doi: null
arxiv: '2607.01661'
cite: 'Li, Y., Tao, Y., Zhang, K., Wang, T., Gu, G., & Zhou, Y. (2026). Diverse Evidence, Better Forecasts: Multi-Agent Deliberation Under Information Asymmetry. arXiv:2607.01661.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

When all agents in a forecasting deliberation receive identical evidence, deliberation collapses into herding and multi-agent systems do little better than one agent. The authors partition evidence into a shared public set and disjoint private subsets, argue theoretically that this lowers inter-agent error correlation, and build InfoDelphi (evidence routing, rationale-based iterative deliberation, confidence-weighted aggregation). On PolyGym, 375 binary questions from real prediction markets, it beats the strongest single- and multi-agent baselines by 12 to 18% in Brier score and 4 to 8 points in accuracy; removing the information asymmetry removes most of the gain.

## Contribution

Evidence distribution (not model diversity) as a decorrelation lever, measured on a ground-truth forecasting task.

## Key results

- Brier improvement 12 to 18% over baselines; ablating asymmetry removes most gains (reported).

## Methods and models

LLM deliberation framework on PolyGym. Abstract-level read; models and N not read.

## Limitations and open questions

Abstract only; a method paper, N not swept as far as the abstract says.

## Relevance to us

Bears on the evidence-distributed N_eff gap: splitting evidence is a second lever beside cross-family mixing. Closest prior with [[zhang-2026-silo]] and [[li-2025-systematic]] for a sharded-evidence board experiment.
