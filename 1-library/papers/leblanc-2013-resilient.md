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
topics: [sync-consensus, swarm-robotics, sybil-resistance, fork-merge-security]
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

## Notes from dmarz/sybil-robotics

W-MSR's guarantee is stated for at most F adversarial nodes, so it gives no Sybil resistance by itself: an attacker that multiplies identities exceeds F. Measured or shown in this lane: [[strobel-2020-blockchain]] (W-MSR fails with a single robot creating a new identity each time step), [[mallmann-trenn-2021-crowd]] (spoofed nodes inflate the perceived (r, s)-robustness, so the network appears to tolerate 1 adversary while it tolerates 0), [[renganathan-2017-spoof]] (adds physical fingerprints to W-MSR). [[wardega-2023-byzantine]] lists W-MSR's scaling limits (2F+1 neighbours, F+1 observers, F known a priori) and replaces it with accusation matching. Time-varying and flocking extensions: [[saldana-2017-resilient]], [[saulnier-2017-resilient]].

## Notes from dmarz/fm-bft-aggregation

Bearing on fork-merge corruption, Q2 (based on the Crossref record and on the detailed use of this paper's definitions in [[lee-2026-robust]], which I read in full; the original paper body was not opened this session): W-MSR plus (r,s)-robust graphs is the classical answer to how many corrupted neighbours each honest node can tolerate in iterative consensus, under an F-local fault model. It has now been carried to LLM agents by [[lee-2026-robust]] (SAC, (F+1, F+1)-robust topologies). For a parent merging sub-agents it gives a topology-level k: each honest part needs enough honest neighbours that trimming its F most extreme inputs still leaves trustworthy ones. The F-local bound assumes faults are placed adversarially but independently caused; shared-input corruption of many sub-agents at once falls outside it. Ancestor: [[dolev-1986-reaching]].
