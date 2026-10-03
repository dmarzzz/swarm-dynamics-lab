---
id: boyd-2006-randomized
type: paper
title: Randomized gossip algorithms
authors: [Stephen Boyd, Arpita Ghosh, Balaji Prabhakar, Devavrat Shah]
year: 2006
venue: IEEE Transactions on Information Theory
url: https://doi.org/10.1109/tit.2006.874516
doi: 10.1109/tit.2006.874516
arxiv: null
cite: "Boyd, S., Ghosh, A., Prabhakar, B., & Shah, D. (2006). Randomized gossip algorithms. IEEE Transactions on Information Theory, 52(6), 2508-2530."
topics: [sync-consensus]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "2518 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Analyses gossip algorithms, in which a node wakes up and averages with one randomly chosen neighbour, for
computing averages on arbitrary, changing networks (sensor, peer-to-peer, ad hoc). The averaging time is governed
by the second largest eigenvalue of a doubly stochastic matrix describing the algorithm; finding the fastest gossip
algorithm is a semidefinite program, which the authors solve in a distributed way with a subgradient method. Via
the link to random-walk mixing times they derive scaling of gossip on geometric random graphs (wireless sensor
networks) and on preferential-connectivity Internet graphs.

## Contribution

The standard reference for asynchronous, pairwise consensus; extends [[xiao-2004-fast]] to randomised
asynchronous updates, which is how real radios exchange messages.

## Key results

- Abstract: averaging time set by the second largest eigenvalue; optimal design is an SDP solvable by a
  distributed subgradient method; scaling results for geometric random graphs and preferential-connectivity
  graphs (specific rates not read).

## Methods and models

Markov chain mixing, spectral graph theory, convex optimisation. Abstract from OpenAlex.

## Limitations and open questions

Assumes a doubly stochastic averaging structure and i.i.d. random wake-ups; the specific scaling rates were not
read here, so whether gossip is fast enough on a sparse drone network has to be checked in the full text.

## Relevance to us

The model of choice for drone or robot swarms that talk over lossy, pairwise radio links; compare with the
"stochastic coupling" results for swarmalators summarised in [[sar-2026-interplay]].
