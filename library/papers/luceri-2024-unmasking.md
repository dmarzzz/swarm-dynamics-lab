---
id: luceri-2024-unmasking
type: paper
title: 'Unmasking the Web of Deceit: Uncovering Coordinated Activity to Expose Information Operations on Twitter'
authors:
- Luca Luceri
- Valeria Pantè
- Keith Burghardt
- Emilio Ferrara
year: 2024
venue: Proceedings of the ACM Web Conference 2024 (WWW)
url: https://arxiv.org/abs/2310.09884
doi: 10.1145/3589334.3645529
arxiv: '2310.09884'
cite: 'Luceri, L., Pantè, V., Burghardt, K., & Ferrara, E. (2024). Unmasking the Web of Deceit: Uncovering Coordinated Activity to Expose Information Operations on Twitter. In Proceedings of the ACM Web Conference 2024 (pp. 2530–2541). ACM.'
topics:
- swarm-detection
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 58 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Builds similarity networks from several behavioural traces of accounts and asks which network properties identify the drivers of state-backed information operations. On 49 million tweets from six countries with verified IOs, the authors find standard edge-filtering does not consistently find IO drivers; node pruning (by centrality) works better, especially when several behavioural indicators are fused. A supervised classifier on a vector representation of the fused similarity network reaches precision above 0.95.

## Contribution

Moves coordination detection from hand-set edge thresholds to node pruning and fused multi-trace networks, and shows the result generalises across campaigns from several countries.

## Key results

- Dataset: 49 million tweets, six countries, multiple verified IOs (abstract).
- Traditional network filtering does not consistently find IO drivers across campaigns (abstract).
- Node pruning on fused networks outperforms; supervised model precision above 0.95 for classifying IO drivers and forecasting their temporal engagement (abstract).

## Methods and models

Per-trace user similarity networks (co-retweet, co-URL, co-hashtag, fast retweet, text similarity, following [[pacheco-2021-uncovering]]), fused into one network; eigenvector-centrality node pruning; a classifier on the fused-network representation. Ground truth from X's takedown releases.

## Limitations and open questions

Only the abstract read. Ground truth is X's attribution, which is itself the output of an unknown detector. Precision is reported; recall and base rate in the wild are not in the abstract.

## Relevance to us

The current reference pipeline from the USC HUMANS lab, reused in [[pante-2025-beyond]], [[cinus-2025-exposing]], [[luceri-2026-coordinated]] and [[minici-2025-iohunter]]. For agent swarms it gives the multi-trace fusion step; whether node pruning still finds an LLM swarm with no hub structure is untested.

## Notes from dmarz/sd-bots

Folded in by dmarz/sd-merge from the duplicate entry `luceri-2023-unmasking` (added_by dmarz/sd-bots, accessed 2026-10-03, read_depth abstract, relevance 4). Same source (same arXiv id and DOI); the kept id uses the year of the published version given in cite.

- Frontmatter `year` in the folded entry: 2023
- Frontmatter `venue` in the folded entry: Proceedings of the ACM Web Conference 2024 (WWW '24)
- Frontmatter `cite` in the folded entry: 'Luceri, L., Pantè, V., Burghardt, K., & Ferrara, E. (2024). Unmasking the Web of Deceit: Uncovering Coordinated Activity to Expose Information Operations on Twitter. In Proceedings of the ACM Web Conference 2024 (WWW ''24), pp. 2530-2541. https://doi.org/10.1145/3589334.3645529'
- Frontmatter `citations` in the folded entry: 28 (Crossref, 2026-10-03)

### Summary

Using 49 million tweets from six countries with verified state information operations, the authors show standard network filtering does not consistently find IO drivers across campaigns. A node-pruning framework that fuses several behavioural similarity networks works better, and a supervised model on a vector representation of the fused network classifies IO drivers with precision above 0.95 and forecasts their future participation.

### Contribution

Moves coordination detection from single-trace networks to a fused multi-trace network with a supervised layer, evaluated across many state campaigns.

### Key results

- 49M tweets, six countries, multiple verified IOs.
- Precision above 0.95 for classifying IO drivers globally (abstract).
- Traditional network filtering does not consistently find IO drivers across campaigns.

### Methods and models

Similarity networks per behavioural indicator, fused network, node pruning, supervised classifier on network embeddings. Abstract-level read.

### Limitations and open questions

Ground truth comes from Twitter's IO takedown releases, which reflect what Twitter found; evaluation is on pre-LLM campaigns.

### Relevance to us

Template for detecting an operator's swarm from multiple weak shared-behaviour signals. Negative control lesson: [[pante-2025-beyond]]. Applied to 2024 elections in [[minici-2024-uncovering]] and [[cinus-2025-exposing]].
