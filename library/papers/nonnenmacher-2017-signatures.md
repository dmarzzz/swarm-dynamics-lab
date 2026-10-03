---
id: nonnenmacher-2017-signatures
type: paper
title: 'Signatures of criticality arise from random subsampling in simple population models'
authors: ['Marcel Nonnenmacher', 'Christian Behrens', 'Philipp Berens', 'Matthias Bethge', 'Jakob H. Macke']
year: 2017
venue: 'PLOS Computational Biology'
url: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005718
doi: 10.1371/journal.pcbi.1005718
arxiv: null
cite: 'Nonnenmacher, M., Behrens, C., Berens, P., Bethge, M., & Macke, J. H. (2017). Signatures of criticality arise from random subsampling in simple population models. PLOS Computational Biology, 13(10), e1005718.'
topics: [criticality-measurement]
added_by: dmarz/criticality-measurement-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: '53 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Diverging specific heat of fitted maximum entropy models has been read as evidence that neural populations sit
at a critical point. The authors link this signature to ordinary population statistics and show that specific
heat diverges whenever average correlation strength does not depend on population size, which is automatically
true when correlated data are randomly subsampled. Higher firing rates and correlations produce stronger
signatures, consistent with experiments, so the signature does not indicate an optimised code.

## Contribution

A clean null result against the heat-capacity diagnostic used in [[mora-2011-biological]]: it is explained by
mean rate and mean correlation alone. Complements the latent-variable critiques of [[schwab-2014-zipfs]] and
[[morrell-2021-latent]].

## Key results

- Specific heat diverges with N whenever mean pairwise correlation is N-independent (analytic, claimed in abstract).
- Random subsampling guarantees this condition, whatever the origin of correlations (analytic).
- Feed-forward population model reproduces experimental specific-heat curves; rates and correlations set their shape (simulation).

## Methods and models

Analytically tractable homogeneous models, simulations of a feed-forward population model (retina-like), and
efficient maximum entropy fitting (K-pairwise models) for large populations.

## Limitations and open questions

Abstract-level read; focused on neural spike trains, but the argument applies to any subsampled population
with correlated inputs.

## Relevance to us

Before using heat capacity of a fitted model as a swarm criticality signature, check whether it follows from mean
correlation alone. Related: [[kloucek-2023-biases]], [[levina-2022-tackling]], [[touboul-2017-power]].
