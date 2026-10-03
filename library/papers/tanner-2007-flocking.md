---
id: tanner-2007-flocking
type: paper
title: Flocking in Fixed and Switching Networks
authors: [Herbert G. Tanner, Ali Jadbabaie, George J. Pappas]
year: 2007
venue: IEEE Transactions on Automatic Control
url: https://api.openalex.org/works/doi:10.1109/tac.2007.895948
doi: 10.1109/tac.2007.895948
arxiv: null
cite: "Tanner, H. G., Jadbabaie, A., & Pappas, G. J. (2007). Flocking in fixed and switching networks. IEEE Transactions on Automatic Control, 52(5), 863-868."
topics: [sync-consensus, collective-motion]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "1438 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Analyses mobile agents that align velocities and stabilise inter-agent distances using decentralised
nearest-neighbour rules, over networks that may switch arbitrarily (no dwell time between switches). Switching
introduces discontinuities into the control laws, handled with nonsmooth analysis. Main result: regardless of
switching, velocities converge to a common vector and inter-agent distances stabilise, as long as the network
remains connected at all times.

## Contribution

Rigorous flocking (alignment plus cohesion/separation) under arbitrary switching, extending the alignment-only
result of [[jadbabaie-2003-coordination]].

## Key results

- Abstract: convergence to common velocity and stable spacing under arbitrary switching if the graph stays
  connected at all times.

## Methods and models

Velocity-alignment plus distance-stabilising control laws, nonsmooth analysis for the switching-induced
discontinuities. Abstract from OpenAlex. The 2003 CDC precursors ("Stable flocking of mobile agents", parts I
and II) were seen in the Crossref search.

## Limitations and open questions

Assumes connectivity at all times, which motion can break; connectivity-preserving control is a separate line.

## Relevance to us

Cite when claiming flocking is provably stable under link switching; pairs with
[[olfati-saber-2006-flocking]] and [[cucker-2007-emergent]].
