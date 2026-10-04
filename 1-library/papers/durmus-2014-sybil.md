---
id: durmus-2014-sybil
type: paper
title: "Sybil-Resistant Meta Strategies for the Forwarder's Dilemma"
authors: [Yunus Durmus, Andreas Loukas, Ertan Onur, Koen Langendoen]
year: 2014
venue: 2014 IEEE Eighth International Conference on Self-Adaptive and Self-Organizing Systems (SASO), London, pp. 90-99
url: https://open.metu.edu.tr/handle/11511/41279
doi: 10.1109/saso.2014.21
arxiv: null
cite: "Durmus, Y., Loukas, A., Onur, E., & Langendoen, K. (2014). Sybil-Resistant Meta Strategies for the Forwarder's Dilemma. In 2014 IEEE Eighth International Conference on Self-Adaptive and Self-Organizing Systems (SASO), pp. 90-99. IEEE. https://doi.org/10.1109/saso.2014.21"
topics: [sybil-resistance, swarm-intelligence]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (Crossref, 2026-10-03)"
code: []
---

## Summary

Addresses the forwarder's dilemma in wireless ad hoc networks: every node benefits when neighbours relay its packets, but relaying costs energy and bandwidth, so selfish defection can collapse the network. The authors note that prior incentive and enforcement schemes assume homogeneous nodes and reliable identities, whereas in ad hoc networks identity is "fuzzy": a free rider can forge multiple identities (Sybil) to hide a history of defection, and the wireless medium itself is noisy (collisions, interference, asymmetric links), so a node cannot be sure whether a neighbour defected or a packet was simply lost. Drawing on evolutionary game theory and multi-agent systems, they adapt two meta strategies, Win Stay Lose Shift and Stochastic Imitate Best Strategy, so that they do not require strict identity information and depend only on a node's own observations. Nodes monitor neighbourhood traffic by two-hop overhearing and decide locally whether to cooperate or defect. The abstract claims that nodes discover and adopt the best strategy in their locality and protect themselves against free riders who mount Sybil attacks by rotating identities. Abstract read from the METU open-access record (the handle page; the IEEE body is paywalled and the repository shows 0 downloads of a deposited PDF, so the full text was not reached). Specific simulation numbers and the exact modifications to WSLS and imitation are therefore not recorded here.

## Contribution

Reframes Sybil resistance for cooperation enforcement: instead of trying to pin behaviour to identities (reputation, credit, or watchdog schemes that a cheap identity change defeats), use identity-free, locally adaptive strategies from evolutionary game theory that only condition on the node's own recent payoff and what it overhears, so there is nothing for a Sybil identity swap to launder.

## Key results

- Modified Win Stay Lose Shift and Stochastic Imitate Best Strategy let nodes converge on the locally best strategy and resist exploitation by identity-changing free riders (abstract claim; magnitudes not available at this read depth).
- Two-hop overhearing is the only monitoring primitive required; no identity infrastructure.

## Methods and models

Evolutionary game theory meta strategies (WSLS, stochastic imitation) on a wireless ad hoc forwarding game with heterogeneous node capabilities, noisy observations, and Sybil-capable free riders. Evaluation method (simulation setup, topology, noise model) not visible from the abstract.

## Limitations and open questions

Abstract-only read. Unclear how the scheme performs when a large fraction of neighbours are Sybil clones of one attacker (the classic failure mode for local imitation, since imitation of the "best" neighbour can be gamed by a majority of fake neighbours). Also unclear how quickly WSLS recovers after a burst of channel noise versus real defection. Network reciprocity results from this era are usually on static grids; mobility is not mentioned in the abstract.

## Relevance to us

A rare paper that designs for Sybil resistance by making the decision rule identity-free rather than by making identities expensive. That is a different axis from [[douceur-2002-sybil]] (identities need a trusted authority or resource cost) and from reputation schemes ([[cheng-2005-sybilproof]]). For agent swarms where member identity is cheap and churn is high, a WSLS-style local rule that conditions on realised outcomes rather than on who said what is a candidate baseline for our own cooperation and defection experiments. Compare the review of open-MAS attacks in [[bijani-2014-review]].
