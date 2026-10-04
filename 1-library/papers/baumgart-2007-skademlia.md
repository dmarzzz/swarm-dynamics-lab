---
id: baumgart-2007-skademlia
type: paper
title: "S/Kademlia: A practicable approach towards secure key-based routing"
authors: ["Ingmar Baumgart", "Sebastian Mies"]
year: 2007
venue: "2007 International Conference on Parallel and Distributed Systems (ICPADS 2007), IEEE"
url: https://telematics.tm.kit.edu/publications/Files/267/SKademlia_2007.pdf
doi: "10.1109/ICPADS.2007.4447808"
arxiv: null
cite: "Baumgart, I., & Mies, S. (2007). S/Kademlia: A practicable approach towards secure key-based routing. In 2007 International Conference on Parallel and Distributed Systems (ICPADS), IEEE. https://doi.org/10.1109/ICPADS.2007.4447808"
topics: [sybil-resistance]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "175 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

S/Kademlia hardens the Kademlia DHT with three changes: nodeIds are hashes of public keys that must satisfy a static crypto puzzle (so ids cannot be chosen freely) and a dynamic puzzle (so generating many ids costs work), lookups run over d disjoint paths so that one clean path suffices, and a sibling list of size eta*s gives reliable replica sets. Routing-table maintenance only admits signed contacts, and unsolicited contacts are only admitted to buckets whose prefix differs from the node's own by more than chi bits. OverSim simulations with 10,000 nodes show that with 20% adversarial nodes, 99% of lookups still succeed when disjoint paths are used.

## Contribution

A practical, decentralised alternative to the CA-based identity of [[castro-2002-secure]]: it argues that crypto puzzles, although they cannot prevent a Sybil attack (citing [[douceur-2002-sybil]]), are the most effective option without a trusted authority, and pairs them with path diversity to bound damage from the ids an attacker does get.

## Key results

- Lookup success with d disjoint paths and adversarial fraction m is the path-length-weighted probability that at least one of d paths is free of adversaries; disjoint paths and short paths both help.
- Simulation, N=10,000, s=16: increasing d from 1 to 8 with k=16 considerably raises the fraction of successful lookups; the authors recommend d=4..8 with k=8..16. Communication overhead grows linearly in d.
- With 20% adversarial nodes, 99% of lookups succeed with disjoint paths (conclusion).
- Adapting k=2d (smaller buckets) lowers success because average path length grows.
- Supervised signatures (CA-signed keys) are suggested only for the bootstrap phase, when few nodes exist.

## Methods and models

Taxonomy of attacks on Kademlia (eclipse, Sybil, churn, adversarial routing, DoS, storage); design of static and dynamic puzzles with costs O(2^c1 + 2^c2) to create and O(1) to verify; sibling-list proof adapted from the Broose DHT; OverSim simulation of a static, fully stabilised network with adversarial share stepped by 5% up to 90%, no churn.

## Limitations and open questions

No churn in the simulations. Puzzle difficulty is a free parameter with no guidance on how to set it against attacker hardware. Adversaries are assumed to return only colluding nodes on lookup, but routing-table poisoning during bootstrapping is argued away rather than simulated. [[marcus-2018-low-resource]] later shows that Ethereum's Kademlia variant, which kept free key generation, was eclipsable from two IP addresses.

## Relevance to us

S/Kademlia supplies two transferable ingredients for agent overlays. First, make an agent's position in the overlay a function of a costly-to-grind key, so that an attacker cannot place agents next to a chosen target (bounds where identities land, and with the dynamic puzzle, how many). Second, query several disjoint sets of agents and accept the answer from any clean path, which bounds the influence of whatever Sybils got in. Both apply to agent discovery registries and to multi-path retrieval among agents. Related: [[castro-2002-secure]], [[singh-2006-eclipse]], [[gh-ethereum-devp2p]], [[gupta-2020-resource]], [[aspnes-2005-exposing]].
