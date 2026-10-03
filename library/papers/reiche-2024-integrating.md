---
id: reiche-2024-integrating
title: Integrating higher-order relations for enhanced twitter bot detection
authors:
- Sebastian Reiche
- Sarel Cohen
- Kirill Simonov
- Tobias Friedrich
year: 2024
venue: Social Network Analysis and Mining 14, 207
url: https://doi.org/10.1007/s13278-024-01372-0
doi: 10.1007/s13278-024-01372-0
arxiv: null
cite: Reiche, S., Cohen, S., Simonov, K., & Friedrich, T. (2024). Integrating higher-order
  relations for enhanced twitter bot detection. Social Network Analysis and Mining,
  14, 207. https://doi.org/10.1007/s13278-024-01372-0.
topics:
- swarm-detection
read_depth: abstract
relevance: 4
type: paper
added_by: shadow/sol-w1
accessed: '2026-10-03'
citations: null
code: []
---

## Summary

The abstract argues that follower graphs miss behavioral coordination and compares retweet, co-retweet, and co-hashtag relations with follower/following links for bot detection. It highlights co-hashtag construction as robust to incomplete data collection and as a way to recover useful relational structure. Quantitative detection improvements are not stated in the accessible abstract, so the result here is a representation proposal with qualitative evaluation claims.

## Contribution

Makes higher-order co-action relations explicit rather than relying only on pairwise follow links to identify social bots.

## Key results

- Retweet, co-retweet, and co-hashtag structures are compared with conventional follow relations.
- Co-hashtag robustness to data-collection flaws is highlighted qualitatively.
- No numerical accuracy, F1, or missing-data robustness value was available in the abstract read.

## Methods and models

Opened the DOI/publisher page, which returned a client challenge; read the complete deposited abstract and bibliographic metadata at https://api.crossref.org/works/10.1007/s13278-024-01372-0. Co-retweet means two users retweeting the same tweet; co-hashtag represents frequent shared hashtag use. Graph architecture, weighting rules, dataset splits, and ablations were not inspected.

## Limitations and open questions

Sharing a hashtag or retweet can arise organically and is not sufficient evidence of common control. Robustness depends on relation-construction thresholds and sampling assumptions, which are inaccessible at abstract depth. Publisher challenge prevented full-text inspection; no implementation or numerical claims were verified.

## Relevance to us

Directly relevant to group-level evidence and comparisons of relation types. Pair with temporal-pattern matching in [[deason-2018-time]] and account-focused representation learning in [[akhtar-2025-botsscl]]. Their evidence should not be conflated with proof of malicious coordination.
