---
id: qinqin-2026-distributed
type: paper
title: The Distributed Detectability Band Against Marginal-Preserving Attacks
authors: [Zhang Qinqin, Gao Yuze]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2606.10456
doi: null
arxiv: '2606.10456'
cite: 'Qinqin, Z., & Yuze, G. (2026). The Distributed Detectability Band Against Marginal-Preserving Attacks. arXiv:2606.10456.'
topics: [fork-merge-security, criticality-measurement]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: 0 (Semantic Scholar citing list, 2026-10-03)
code: []
---

## Summary

A short theory-plus-simulation paper on distributed sub-threshold sabotage: harm is spread over many steps so that the per-step monitor-score distribution is exactly the benign one, while harm is encoded in temporal correlation (a Gaussian-copula AR(1) construction). Monitors that look at marginal statistics (mean, max, top-k tail, threshold; "Monitor A") are blind by construction: AUC 0.52 at 1% FPR, KS distance to benign 0.013. Sequence monitors that look at correlation (CUSUM, SPRT, HMM likelihood ratio, runs test, autocorrelation, windowed logistic; "Monitor B") reach AUC 0.79 to 0.97 at the same FPR, and stay near 0.95 as harm is spread over more steps. On real traces (Qwen2.5-7B agent scored by a Llama-3.2-3B monitor) Monitor A is again at chance (KS 0.010); a single short episode gives Monitor B only AUC 0.59, rising from 0.68 to 0.98 as the monitored horizon grows. Note: arXiv lists the authors as "Zhang Qinqin, Gao Yuze" with Qinqin indexed as surname; I followed arXiv's indexing for the id.

## Contribution

A formal statement of why per-step threshold monitors cannot catch an attacker that preserves the benign marginal, and of which monitor family can.

## Key results

- Marginal monitors give zero protection against a marginal-preserving attacker (stated as the central message).
- SPRT with known parameters is the likelihood-ratio optimal test within Monitor B.
- Detection on real agents requires accumulating evidence over the deployment horizon.

## Methods and models

Synthetic AR(1) Gaussian traces with tunable benign autocorrelation; Gaussian-copula marginal matching; adaptive red-teamer on synthetic traces only.

## Limitations and open questions

Authors state: synthetic traces; real benign autocorrelation is low and episodes short; the attacker is assumed able to match the marginal exactly, which a real agent in a low-dimensional action space may not manage; harm modelled as a scalar spread uniformly. I read the abstract, real-trace results, limitations and conclusion.

## Relevance to us

- Q2 (thresholds): any merge check that scores each returning child (or each merge event) against a benign distribution and applies a threshold is "Monitor A". An attacker who controls several children, or one child across many merges, can in principle keep each contribution distributed like a benign one. The defence class that survives is sequential testing across contributions (CUSUM or SPRT over merge history).
- Q3 (attack): gives the formal shape of the strongest stealthy attack: preserve the marginal, encode harm in correlation across parts.
Related: [[makins-2026-multi]] and [[hills-2026-distributed]] (empirical versions), [[greenblatt-2023-ai]].
