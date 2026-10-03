---
id: celiktemel-2026-group
type: paper
title: Group Selection Promotes Prosocial Prompts in Populations of LLM Agents
authors:
- Luis Celiktemel
- Edward Eichhorn
- Levin Brinkmann
- Robin Schimmelpfennig
- Aron Vallinder
- Yaomin Jiang
- Edward Hughes
- Iyad Rahwan
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.23343
doi: null
arxiv: '2606.23343'
cite: Celiktemel, L., Eichhorn, E., Brinkmann, L., Schimmelpfennig, R., Vallinder, A., Jiang, Y., Hughes, E., & Rahwan, I. (2026). Group Selection Promotes Prosocial Prompts in Populations of LLM Agents. arXiv preprint arXiv:2606.23343.
topics:
- llm-agent-swarms
- marl-emergence
- criticality-measurement
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

LLM agents play a repeated social dilemma and pass their natural-language prompts to the next generation under either individual-level or group-level selection. Under group selection, prompts from high-performing groups are transmitted, prosocial prompts spread and cooperation stabilises; under individual selection, self-interested prompts dominate and populations collapse into collective defection. The gap is robust to prompt ablations, alternative game framings and model swaps. A replicator-mutator model with an empirically estimated transmission kernel reproduces the results and predicts a phase transition at a critical threshold. Preliminary results show GPT-5.4, when told about the selection mechanism, adjusts first-generation donations in anticipation, which other models did not do.

## Contribution

Extends the cultural-evolution line of [[vallinder-2024-cultural]] (shared author) from within-population norm evolution to multilevel selection, and links LLM populations to evolutionary-dynamics theory with an explicit phase transition.

## Key results

- Claimed: group selection sustains cooperation; individual selection leads to collective defection; robust across ablations and models.
- Claimed: replicator-mutator model predicts a phase transition at a critical threshold (value not read).
- Claimed: anticipatory behaviour by GPT-5.4 when informed of the selection rule.

## Methods and models

Repeated social dilemma (game details not read); generational prompt transmission under individual vs group selection; replicator-mutator theory with empirical kernel; several models including GPT-5.4.

## Limitations and open questions

Abstract-level read; group sizes, number of generations and threshold value not checked.

## Relevance to us

A tunable selection-pressure knob with a predicted critical point is an attractive hackathon experiment. Related: [[piatti-2024-cooperate]], [[hammond-2025-multi]].
