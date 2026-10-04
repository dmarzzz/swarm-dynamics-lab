---
id: ghanem-2026-steganalysis
type: paper
title: "Steganalysis of Adaptive Covert Collusion in Tool-Using Agent Populations: A Black-Box, Cross-Principal Approach"
authors: ["Mohamed Chahine Ghanem"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2608.02698
doi: null
arxiv: "2608.02698"
cite: "Ghanem, M. C. (2026). Steganalysis of Adaptive Covert Collusion in Tool-Using Agent Populations: A Black-Box, Cross-Principal Approach. arXiv:2608.02698."
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "2 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Considers populations of tool-using LLM agents from many operators on shared infrastructure, where a few agents may covertly coordinate (rig a market, boost each other in reviews, time a joint data grab). Proposes a black-box, trace-only steganalysis detector combining cross-run mutual information, permutation tests, distribution-shift statistics and timing and tool-call side channels, calibrated to a fixed false-positive budget, and pitted against an adversary that keeps rewriting its encoding. Capacity theory predicts a covert bit-rate below which black-box detection is no better than chance.

## Contribution

States the right threat model (cross-principal, black-box, adaptive) and a theoretical detection-capacity frontier. It reports no measurements yet.

## Key results

- The abstract says the results are "clearly labelled placeholder results pending measurement". No empirical result to cite.
- Flags spreading a payload across sessions as an evasion current methods largely miss (claim).

## Methods and models

Mutual-information estimation across runs, permutation tests, timing and tool-call side channels, red-versus-blue adaptive encoding.

## Limitations and open questions

A proposal with placeholder results; single author; treat as an idea, not evidence.

## Relevance to us

Useful framing for a hackathon experiment (detect covert coordination among agents from traces only, against an adaptive encoder). Measured alternatives: [[tailor-2025-audit]], [[rose-2026-detecting]].
