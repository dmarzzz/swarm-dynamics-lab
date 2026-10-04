---
id: cheng-2005-sybilproof
type: paper
title: 'Sybilproof reputation mechanisms'
authors:
- 'Alice Cheng'
- 'Eric Friedman'
year: 2005
venue: 'Proceedings of the 2005 ACM SIGCOMM workshop on Economics of peer-to-peer systems (P2PECON ''05)'
url: https://api.openalex.org/works/doi:10.1145/1080192.1080202
doi: 10.1145/1080192.1080202
arxiv: null
cite: 'Cheng, A., & Friedman, E. (2005). Sybilproof reputation mechanisms. In Proceedings of the 2005 ACM SIGCOMM Workshop on Economics of Peer-to-Peer Systems (P2PECON ''05), 128-132. ACM.'
topics:
- sybil-resistance
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: 'OpenAlex 2026-10-03: 272'
code: []
---

## Summary

Using a static graph model of reputation, where a peer can create Sybils and fake links among them to raise its own score, the paper formalises Sybilproofness for reputation functions. It proves that no symmetric reputation function (one invariant under relabelling of nodes, such as PageRank-style scores) is Sybilproof. For asymmetric reputations computed relative to a fixed source, it gives a general flow-based reputation function and conditions under which it is Sybilproof.

## Contribution

The foundational impossibility for Sybil-proof reputation: global, symmetric scores cannot resist Sybils; only reputations computed from a trusted viewpoint (flows or paths from a seed) can.

## Key results

- There is no symmetric Sybilproof reputation function.
- An asymmetric flow-based reputation function can be Sybilproof under stated conditions.

## Methods and models

Reputation as a function on a directed weighted trust graph; Sybil strategies add nodes and edges controlled by the attacker; proofs are combinatorial.

## Limitations and open questions

Abstract-level read only; the full text was not available to me. The model is static and does not treat dynamics, costs or collusion between distinct agents.

## Relevance to us

Agent swarms that rank or route by peer endorsement (agent reputation, trust scores for tool calls, peer review among LLM agents) inherit this result: a symmetric score lets an agent mint endorsers. Defences must be anchored at trusted seeds, as in max-flow trust. This is the reputation-side counterpart of [[conitzer-2010-using]] and connects to the social-graph approach in [[ethresearch-2023-collusion]].
