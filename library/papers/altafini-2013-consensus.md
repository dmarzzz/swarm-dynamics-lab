---
id: altafini-2013-consensus
type: paper
title: Consensus Problems on Networks With Antagonistic Interactions
authors: [Claudio Altafini]
year: 2013
venue: IEEE Transactions on Automatic Control
url: https://api.openalex.org/works/doi:10.1109/tac.2012.2224251
doi: 10.1109/tac.2012.2224251
arxiv: null
cite: "Altafini, C. (2013). Consensus problems on networks with antagonistic interactions. IEEE Transactions on Automatic Control, 58(4), 935-946."
topics: [sync-consensus, collective-decision]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "2137 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Asks whether agreement is possible when some interactions are antagonistic, modelled as negative edge weights.
On signed networks all agents can converge to a value that is the same up to sign ("bipartite consensus"):
two camps reach equal and opposite opinions. Necessary and sufficient conditions are obtained, with strong analogies to monotone systems theory; linear and nonlinear Laplacian
feedback designs are proposed.

## Contribution

Founded the bipartite-consensus literature and brought structural balance into multi-agent control; the
signed-graph extension of [[olfati-saber-2004-consensus]].

## Key results

- Abstract: modulus consensus with opposite signs is achievable on signed networks under necessary and sufficient
  conditions; links to monotone systems.
- The term "structural balance" is not in the abstract; its use here follows the related Crossref hit
  "Dynamics of opinion forming in structurally balanced social networks" (Altafini 2012, PLoS ONE).

## Methods and models

Signed Laplacians, gauge transformations, monotone systems. Abstract from OpenAlex.

## Limitations and open questions

Static signed graphs; what happens when the necessary and sufficient conditions fail was not read here.

## Relevance to us

Models swarms with two teams or adversarial pairs (predator-prey style coupling, competing drone teams) and
polarisation in opinion models ([[proskurnikov-2017-tutorial]]).
