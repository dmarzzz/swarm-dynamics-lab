---
id: leblanc-2013-resilient
type: paper
title: Resilient Asymptotic Consensus in Robust Networks
authors: [Heath J. LeBlanc, Haotian Zhang, Xenofon Koutsoukos, Shreyas Sundaram]
year: 2013
venue: IEEE Journal on Selected Areas in Communications
url: https://doi.org/10.1109/jsac.2013.130413
doi: 10.1109/jsac.2013.130413
arxiv: null
cite: "LeBlanc, H. J., Zhang, H., Koutsoukos, X., & Sundaram, S. (2013). Resilient asymptotic consensus in robust networks. IEEE Journal on Selected Areas in Communications, 31(4), 766-781."
topics: [sync-consensus, swarm-robotics]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "745 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Designs a consensus protocol that uses only local information and still reaches agreement among normal nodes
when some nodes are compromised or faulty, even against worst-case adversaries with full knowledge of the
network. Necessary and sufficient conditions are given under different threat models. Classical connectivity is
shown not to be the right measure; the authors introduce "network robustness", a graph property
capturing redundancy of direct information exchange between subsets of nodes.

## Contribution

A standard reference for resilient consensus with purely local information against worst-case compromised
nodes (about 745 OpenAlex citations; also among the top forward citations of [[olfati-saber-2007-consensus]]).
Its network-robustness property replaces connectivity as the design target.

## Key results

- Abstract: local resilient protocol; necessary and sufficient conditions per threat model; connectivity is
  inadequate, network robustness is the right property.

## Methods and models

Graph theory (network robustness), worst-case adversary models, convergence analysis. Abstract from OpenAlex.

## Limitations and open questions

The threat assumptions (how many misbehaving nodes, where) were not read here; checking robustness on large
graphs may be costly (our note).

## Relevance to us

Directly relevant if a hackathon swarm must tolerate faulty or malicious members (a spoofed drone, a buggy LLM
agent). Its robustness condition is a concrete topology requirement to design for.
