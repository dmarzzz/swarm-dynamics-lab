---
id: jacob-2021-conflict-free
type: paper
title: "On Conflict-Free Replicated Data Types and Equivocation in Byzantine Setups"
authors: ["Florian Jacob", "Saskia Bayreuther", "Hannes Hartenstein"]
year: 2021
venue: "arXiv preprint (cs.DC), brief announcement"
url: https://arxiv.org/pdf/2109.10554
doi: null
arxiv: "2109.10554"
cite: "Jacob, F., Bayreuther, S., & Hartenstein, H. (2021). On Conflict-Free Replicated Data Types and Equivocation in Byzantine Setups. arXiv:2109.10554 [cs.DC]."
topics: [fork-merge-security, sync-consensus, sybil-resistance]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: null
code: []
---

## Summary

A five-page brief announcement (the PDF body is titled "...in Byzantine Environments"; the arXiv record uses "Setups") that asks when CRDTs tolerate equivocation, meaning a Byzantine replica sending different valid-looking updates to different recipients. The authors define an algorithm as equivocation-tolerant if it needs no equivocation detection, prevention or remediation beyond what it already does for omission. They prove that all state-based CRDTs are equivocation-tolerant (any valid state is in the join-semilattice, so d equivocated updates act as d independent updates with omission), and that operation-based CRDTs are equivocation-tolerant when operations have inherent identity (content hash) and inherent ordering (hash-recorded happened-before). Both classes then keep Strong Eventual Consistency with n > f, that is any number of Byzantine replicas. No experiments.

## Contribution

Reframes Byzantine CRDT safety as "reduce equivocation to omission", and conjectures that a hash-chained DAG is the only operation-based CRDT with non-commutative operations that achieves SEC for any number of faults. Complements [[kleppmann-2022-making]] and [[kleppmann-2020-byzantine]], which reach the same hash-DAG design from a different direction.

## Key results

- Theorem 1: all state-based CRDTs provide equivocation tolerance.
- Lemma 1: state-based CRDTs keep SEC for any number f of Byzantine replicas among n (n > f), given authenticated channels and a connected component of correct replicas.
- Theorem 2 and Lemma 2: op-based CRDTs with inherent identity and ordering, plus omission handling, keep SEC for n > f.
- Trade-off noted: state-based CRDTs lose update identity, so per-replica access control cannot be enforced; op-based CRDTs keep signatures and so can enforce permissions.
- Discussion contrasts tolerance with prevention (trusted monotonic counters in hardware; blockchain fork resolution).

## Methods and models

Static replica group, authenticated channels, Byzantine and omission fault models, proofs by short argument.

## Limitations and open questions

Static membership. Deletion is treated as a permitted act rather than an attack, so the analysis focuses on grow-only CRDTs. The main structural claim is a conjecture.

## Relevance to us

Q2: equivocation is exactly what a corrupted sub-agent does when it reports differently to the parent and to its siblings. This paper says that for grow-only state there is no threshold to reach, because equivocation can be absorbed as extra concurrent updates; the price is that state-based merge loses who-wrote-what, which removes the parent's ability to weight or reject a child by identity. Q1: losing update identity is a crude form of hiding which child contributed what, and the paper shows it costs access control. Q3: an attacker on a state-based merge cannot be traced to its origin child, so blame and later eviction are hard. Related: [[mahajan-2010-depot]] (forks treated as concurrent virtual nodes), [[li-2004-secure]].
