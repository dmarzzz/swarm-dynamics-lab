---
id: gao-2025-heterogeneity
type: paper
title: "Heterogeneity- and homophily-induced vulnerability of a P2P network formation model: the Mana based auto-peering protocol"
authors: [Yu Gao, Carlo Campajola, Nicolò Vallarano, Andreia Sofia Teixeira, Claudio J. Tessone]
year: 2025
venue: Applied Network Science, vol. 10, article 62
url: https://appliednetsci.springeropen.com/articles/10.1007/s41109-025-00740-9
doi: 10.1007/s41109-025-00740-9
arxiv: null
cite: "Gao, Y., Campajola, C., Vallarano, N., Teixeira, A. S., & Tessone, C. J. (2025). Heterogeneity- and homophily-induced vulnerability of a P2P network formation model: the Mana based auto-peering protocol. Applied Network Science, 10, 62. https://doi.org/10.1007/s41109-025-00740-9"
topics: [sybil-resistance, sync-consensus]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: full
relevance: 3
citations: "1 (Crossref, 2026-10-03)"
code: []
---

## Summary

Treats IOTA 2's proposed Mana-based auto-peering protocol as a random network formation model and asks how cheaply an attacker who can split their Mana (reputation stake) across Sybil nodes can partition the resulting P2P graph. Model: N nodes with Zipf-distributed Mana m(i) = K i^-s; node i may peer only with nodes whose Mana is within a factor rho of its own (or within R ranks), and picks k such neighbours, giving a 2k-regular homophilous graph that sits between a 1D lattice and a random regular graph. Attack damage D is the fraction of total Mana cut off (max 1/2); cost x is the Mana needed to control the cheaper endpoint of every cut link. Two full-information strategies (iterated edge-betweenness removal, and a greedy rank-threshold cut) and a blind strategy that only needs the public formation parameters (control all nodes within L ranks of the most-often-cut rank). Simulation on 1000 graphs per parameter set with N=100, R=10, rho=4, k=4: both informed strategies peak at s about 1 with damage per unit cost D/x about 3.5, versus near 0 on a Watts-Strogatz random regular graph of the same degree. The blind strategy reaches 100 percent split success at L=7 (betweenness-informed, E[D/x]=1.75) or L=8 (greedy-informed, E[D/x]=2), both costing about 24 percent of total Mana. Vulnerability is highest for low rho and s in 0.5 to 1, and the formation model is less robust than random rewiring but more robust than a lattice. The authors stress that auto-peering is not currently deployed on IOTA, so the result is a policy warning rather than a live exploit.

## Contribution

Shows quantitatively that a reputation-homophilous peering rule (connect to peers of similar stake) manufactures predictable choke points, so a Sybil attacker who redistributes stake across identities can eclipse the high-Mana core from the rest of the network for roughly a quarter of total stake. Also characterises the auto-peering ensemble as an assortative random graph family bridging lattices and Poisson regular graphs.

## Key results

- Informed attacks: max E[D/x] about 3.5 at s=1 (N=100, rho=4, R=10, k=4), near 0 for the WS baseline (Figure 2).
- Blind attack: 100 percent success at L*=7 (BB) or 8 (BG); cost about 24 percent of total Mana at peak efficiency (Figures 3 and 5).
- Attack efficiency is monotone in rho (worse for small rho) and peaks for intermediate s (Figure 4); N and R have little effect once N is large relative to k (Appendix).
- Lattice baseline splits whenever L >= k; WS baseline almost never splits unless L is of order N.

## Methods and models

Network formation simulated from the IOTA research team's public Go code; Zipf Mana; eligible-neighbour rule m(i)/rho < m(j) < rho m(i) or |i-j| < R; damage and cost as defined above; edge betweenness (Girvan-Newman style) and greedy rank cut; 1000 graphs per setting; comparisons against 1D k-regular lattice and fully rewired Watts-Strogatz.

## Limitations and open questions

Static Mana (no dynamics of accrual or re-peering after a split); N=100 is small; cost counts only Mana and not the number of Sybil identities an attacker must run; the attacker is assumed to know formation parameters and Mana distribution (which the protocol makes public). Not tested against a live network. The question of whether adding randomness (long-range links) restores robustness is suggested but not quantified beyond the WS baseline.

## Relevance to us

Clean, reproducible example of how a reputation or stake signal used for topology formation becomes a Sybil attack surface: splitting one identity's stake into many identities buys choke-point control. Companion to the eclipse literature ([[singh-2006-eclipse]], [[heilman-2015-eclipse]], [[marcus-2018-low-resource]]) and to [[douceur-2002-sybil]]. Relevant to designing peer-selection rules for agent swarms: homophily on a reputation score is exactly the kind of structural predictability an attacker can exploit, and the damage-per-cost metric is a useful template for our own measurements. See also [[keramat-2023-partition]] for IOTA used in a robotics consensus setting.
