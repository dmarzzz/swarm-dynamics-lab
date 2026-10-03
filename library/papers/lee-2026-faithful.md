---
id: lee-2026-faithful
type: paper
title: "Faithful yet Collusive: Why Chain-of-Thought Monitoring Cannot Detect Collusion in LLM Pricing Agents under Oligopolistic Competition"
authors: ["Dohun Lee", "Hyunwoo Park"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2609.18346
doi: null
arxiv: "2609.18346"
cite: "Lee, D., & Park, H. (2026). Faithful yet Collusive: Why Chain-of-Thought Monitoring Cannot Detect Collusion in LLM Pricing Agents under Oligopolistic Competition. arXiv preprint arXiv:2609.18346."
topics: [llm-agent-swarms, swarm-detection]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Nine LLMs set prices for differentiated products in Bertrand competition with logit demand (as in [[calvano-2020-artificial]]) over 300 rounds, in duopoly and triopoly. A causal graph divergence framework compares the causal graph stated in an agent's chain-of-thought with the one that actually governs its pricing, separating structural faithfulness from intent faithfulness. Measured: collusiveness and CoT faithfulness dissociate. The most collusive model accurately reports cooperative intent yet reasons structurally unfaithfully, while GPT-5, the most structurally faithful, still sustains supra-Nash pricing in both market structures. All three proprietary models remain collusive under triopoly.

## Contribution

Evidence that CoT monitoring cannot serve alone as a collusion detector, because faithful reasoning can be collusive and collusive reasoning need not be faithful.

## Key results

- Measured: GPT-5 has the highest structural faithfulness and sustains supra-Nash prices.
- Measured: three proprietary models collude under triopoly.

## Methods and models

300-round Bertrand, nine LLMs; stated versus behavioural causal networks. Read: abstract, introduction, background, setup paragraph.

## Limitations and open questions

Pricing only; the specific nine models and per-model numbers were not transcribed.

## Relevance to us

Argues against relying on CoT judges (as [[agrawal-2025-evaluating]] does) for the swarm factory. Detection should combine action-level market-structure signals ([[bracale-syrnikov-2026-institutional]]), strategy audits ([[eschenbaum-2026-auditing]]) and possibly activation probes ([[rose-2026-detecting]]). Companion: [[riemer-2026-position]].
