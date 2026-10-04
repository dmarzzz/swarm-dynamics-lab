---
id: li-2025-temporal
type: paper
title: "Temporal Neighbor Sequence-based Interpretable Spammer Groups Detection on E-commerce platform"
authors: [Ning Li, Shujuan Ji, Yingtong Dou, Dickson K.W. Chiu, Qi Zhang, Yongquan Liang, Yongshan Wei]
year: 2025
venue: "Information Processing & Management"
url: https://www.sciencedirect.com/science/article/pii/S0306457325001189
doi: 10.1016/j.ipm.2025.104177
arxiv: null
cite: "Li, N., Ji, S., Dou, Y., Chiu, D. K. W., Zhang, Q., Liang, Y., & Wei, Y. (2025). Temporal Neighbor Sequence-based Interpretable Spammer Groups Detection on E-commerce platform. Information Processing & Management, 62(6), 104177. https://doi.org/10.1016/j.ipm.2025.104177"
topics: [swarm-detection]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "5 (Crossref, 2026-10-03)"
code: []
---

## Summary

Proposes TNSGD, a method for finding organised groups of fake reviewers on e-commerce sites. Steps per the abstract: (1) pre-filter to highly suspicious reviewers to shrink the graph; (2) build a co-review temporal network among them (reviewers linked by reviewing the same products, with timing); (3) generate temporal neighbour sequences that capture temporal aggregation and relational features, and use them to form candidate groups; (4) keep candidates that pass group spam indicators and heuristic conditions. Reported gains over baselines: precision and F1 up 4% and 3% on Amazon, and 39% and 31% on Yelp; computational cost cut to 1/85 and 1/7 of baselines (dataset pairing not stated in the abstract). Interpretability: each step has an explicit meaning, plus visualisations of the temporal-spatial and evolutionary structure of detected groups. Only the abstract was read (paywalled).

## Contribution

Group-level (not account-level) detection of coordinated reviewers that exploits fine-grained timing of co-actions, with an interpretable pipeline instead of an end-to-end GNN.

## Key results

- Precision/F1 gains of +4%/+3% (Amazon) and +39%/+31% (Yelp) over baselines (abstract).
- Complexity reduced to 1/85 and 1/7 of baseline cost (abstract).

## Methods and models

Suspicion pre-filter, co-review temporal network, temporal neighbour sequences, group spam indicators with heuristic thresholds. Benchmarks are the standard Amazon and Yelp review-spam datasets (details not read).

## Limitations and open questions

Not assessed beyond the abstract. Heuristic group indicators are typically tuned to known spam campaigns; robustness to adversaries who randomise timing is the obvious question. Yelp gains of 39% suggest the baselines were weak there.

## Relevance to us

Same coordination signal we would use to detect agent swarms (many accounts acting on the same targets in tight time windows), applied to review fraud, a domain where LLM-written reviews make text-based detection weak and timing-based detection more valuable. Compare co-action methods on social media: [[pacheco-2021-uncovering]], [[gh-qut-digital-observatory-coordination-network-toolkit]].
