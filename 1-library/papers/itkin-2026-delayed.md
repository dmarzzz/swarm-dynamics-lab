---
id: itkin-2026-delayed
type: paper
title: 'Delayed Verification Destabilizes Multi-Agent LLM Belief: Instability Thresholds and Optimal Corrector Placement'
authors: [Igor Itkin]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2606.27409v1
doi: null
arxiv: '2606.27409'
cite: 'Itkin, I. (2026). Delayed Verification Destabilizes Multi-Agent LLM Belief: Instability Thresholds and Optimal Corrector Placement. arXiv preprint arXiv:2606.27409.'
topics: [llm-agent-swarms, sync-consensus]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: null
code: []
---

## Summary

Models multi-agent belief as delayed consensus on a graph with grounded corrector nodes and faulty nodes injecting a constant bias. The grounded Laplacian gives a closed-form stability bound on correction gain: at verification delay 2 the bound is the inverse golden ratio (about 0.618), at delay 6 about 0.24. Too strong or too late correction makes beliefs oscillate. In LLM debates on signed numeric estimates (five open models, 8 questions), delay 6 produced overshoot in 96 to 100% of debates vs 0 to 4% at delay 1; grounded factual QA showed no such instability.

## Contribution

Shows that correction itself can destabilise a group's belief when it arrives late, and gives a greedy (1-1/e) rule for placing a limited budget of correctors at high-leverage nodes.

## Key results

- Stability threshold kappa_max = 1 at delay 1, about 0.618 at delay 2, about 0.24 at delay 6 (derived).
- Synthetic onset predictions within 1.7% (measured).
- Signed estimation: error amplitude about 4.5 times larger at delay 6 than delay 1 (0.27 vs 0.06), 8 of 8 questions (measured).
- Grounded QA with a moderate verifier reaches about 0.8 convergence; an ungrounded critic flips the majority in 91% of rounds (measured).

## Methods and models

Linear delayed-consensus analysis; nonlinear tanh simulations; LLM debates with Qwen 35B and 14B, Mistral 7B, Phi-4, Gemma 12B. Skimmed via the HTML.

## Limitations and open questions

Symmetric graphs; corrector placement validated only on synthetic data; factual-QA identification weak (interaction p = 0.47).

## Relevance to us

Minor for V4: if a swarm's correction of a false honeypot alarm is delayed, the model predicts oscillation (resource abandoned, retried, abandoned) rather than clean recovery, but only for graded beliefs, not binary "is this a trap" labels. Related: [[abedini-2026-dont]], [[lin-2026-you]].
