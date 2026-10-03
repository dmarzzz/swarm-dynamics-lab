---
id: wang-2026-state
type: paper
title: State Contamination in Memory-Augmented LLM Agents
authors: [Yian Wang, Agam Goyal, Yuen Chen, Hari Sundaram]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2605.16746
doi: null
arxiv: '2605.16746'
cite: 'Wang, Y., Goyal, A., Chen, Y., & Sundaram, H. (2026). State Contamination in Memory-Augmented LLM Agents. arXiv:2605.16746.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Names and measures "memory laundering": toxic or adversarial context compressed into memory summaries that pass standard toxicity detectors but still carry hostile framing that shifts later generations. Using paired counterfactual multi-agent rollouts, toxic-origin summaries stay below common detector thresholds yet raise downstream toxicity against matched neutral baselines. A new metric, the sub-threshold propagation gap (SPG), measures behavioural differences conditioned on memory states a deployed monitor would call safe. Raw transcript reuse drives overt downstream toxicity; compressed memory carries hidden sub-threshold influence. Where you sanitise matters: sanitising before summarisation substantially reduces the gap, while cleaning only the finished summary can leave laundered influence in place.

## Contribution

Shows that summarisation, the usual way to compress one agent's experience for another, can hide the influence a monitor is looking for.

## Key results

- Toxic-origin summaries below detector thresholds still raise downstream toxicity (abstract).
- Pre-summary sanitisation reduces SPG; post-summary sanitisation can leave it (abstract).

## Methods and models

Paired counterfactual multi-agent rollouts; transcript, summary and memory-buffer channels compared. Models not checked.

## Limitations and open questions

Abstract-level reading; toxicity is a proxy for adversarial influence, and goal-hijack payloads were not the measured target (as far as the abstract says).

## Relevance to us

The most direct measured analogue of a returning sub-agent handing the parent a summary of what it learned.
- Q3 (attack): an attacker who shapes what a child sees can get influence into the parent through a summary that looks clean.
- Q2 (thresholds): any merge-time filter applied to the child's final summary is the "clean only the completed summary" condition that leaves laundered influence; sanitisation has to happen at the child's raw inputs, which the parent typically cannot see. This argues for the parent receiving raw evidence plus constrained extractions ([[costa-2025-securing]], [[beurer-kellner-2025-design]]) rather than the child's narrative.
Related: [[qinqin-2026-distributed]] (sub-threshold attacks), [[safin-2026-trust]].
