---
id: mukobi-2023-welfare
type: paper
title: "Welfare Diplomacy: Benchmarking Language Model Cooperation"
authors: [Gabriel Mukobi, Hannah Erlebach, Niklas Lauffer, Lewis Hammond, Alan Chan, Jesse Clifton]
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2310.08901
doi: null
arxiv: '2310.08901'
cite: "Mukobi, G., Erlebach, H., Lauffer, N., Hammond, L., Chan, A., & Clifton, J. (2023). Welfare Diplomacy: Benchmarking language model cooperation. arXiv:2310.08901."
topics: [llm-agent-swarms, marl-emergence, collective-decision]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: [gh-mukobi-welfare-diplomacy]
---

## Summary

Introduces Welfare Diplomacy, a general-sum variant of the zero-sum board game Diplomacy in which powers trade off military conquest against accumulating welfare points, so that cooperation is both measurable and rewarded. Implements the rules in an open-source Diplomacy engine, builds zero-shot prompted language-model agents as baselines, and finds that state-of-the-art models reach high social welfare but are exploitable by exploiter agents.

## Contribution

Argues that most multi-agent benchmarks are zero-sum or purely cooperative and so cannot measure cooperative capability under mixed motives; supplies a mixed-motive LLM benchmark with an explicit exploitability test.

## Key results

- Abstract-level: high welfare for strong LLM baselines; those baselines are exploitable. Exact numbers not read.

## Methods and models

Seven-power Diplomacy, natural-language negotiation, prompted LLM agents, exploiter agents (prompted LLMs and "super exploiters" that switch to an RL policy) from the repo README.

## Limitations and open questions

Read at abstract and README level. Seven fixed players; costly LLM calls.

## Relevance to us

A direct template for "cooperative LLM society plus planted adversary" experiments. Code: [[gh-mukobi-welfare-diplomacy]].
