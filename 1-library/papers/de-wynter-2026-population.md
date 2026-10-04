---
id: de-wynter-2026-population
type: paper
title: 'Population Physics, Population Problems: Safety and Emergence in LLM Societies'
authors:
- Adrian de Wynter
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.33871
doi: null
arxiv: '2609.33871'
cite: 'de Wynter, A. (2026). Population Physics, Population Problems: Safety and Emergence in LLM Societies. arXiv preprint arXiv:2609.33871.'
topics:
- llm-agent-swarms
- criticality-measurement
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Introduces a framework for measuring self-organisation in LLM social systems and applies it to three systems: a Schelling segregation grid, an AI-agent social network (Moltbook), and a Twitter-like misinformation simulation ("Rogue"). All three show statistically significant self-organisation. Their relaxation dynamics depend on how much environmental information agents have; the open-ended systems (Moltbook, Rogue) show sharp, phase-transition-like dynamics. Population-level pathologies can arise even with safety-tuned or monitored LLMs, driven mainly by the coordinated activity of a subset of the population. Two negative controls, the GovSim commons dilemma and a ChatEval LLM-as-a-judge deliberation, do not show self-organisation. The author argues such signatures could serve as a lightweight, model-agnostic monitoring layer for deployed multi-agent systems.

## Contribution

Proposes self-organisation measures as safety diagnostics for LLM populations and reports phase-transition-like relaxation in real and simulated agent societies. Links to [[de-marzo-2026-collective]] (Moltbook statistics) and [[zomer-2026-unraveling]] (Schelling).

## Key results

- Claimed: significant self-organisation in Schelling, Moltbook and Rogue; none in GovSim or ChatEval.
- Claimed: sharp phase-transition-like relaxation in open-ended systems.
- Claimed: pathologies driven by a coordinated subset even under safety tuning.

## Methods and models

Self-organisation statistics applied to agent-state time series in three environments plus two controls. Specific measures not checked.

## Limitations and open questions

Abstract-level read; single-author preprint; the measure's definition and null model need checking.

## Relevance to us

A candidate measurement layer we could apply to our own swarm runs. Related: [[riedl-2025-emergent]], [[schroeder-2025-how]].
