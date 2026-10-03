---
id: demers-1989-analysis
type: paper
title: Analysis and simulation of a fair queueing algorithm
authors:
- Alan Demers
- Srinivasan Keshav
- Scott Shenker
year: 1989
venue: SIGCOMM 1989
url: https://people.eecs.berkeley.edu/~sylvia/papers/FQ1989.pdf
doi: 10.1145/75246.75248
arxiv: null
cite: Demers, A., Keshav, S., & Shenker, S. (1989). Analysis and simulation of a fair
  queueing algorithm. Symposium proceedings on Communications architectures & protocols,
  1-12.
topics:
- sybil-resistance
- llm-agent-swarms
- sync-consensus
added_by: dmarz/preflight
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Demers and colleagues analyze packet scheduling that separates bandwidth allocation from arrival order and protects traffic from ill-behaved sources. Their discussion explicitly treats the choice of allocation identity as a design problem, including incentives to create additional processes.

## Contribution

Packetized approximation to bit-by-bit fair service.

## Key results

Equal packet counts can allocate unequal bandwidth when sizes differ.

## Methods and models

Skimmed introduction, allocation definitions, algorithm, simulation figures and discussion.

## Limitations and open questions

Packet fairness does not establish semantic usefulness. Per-process allocation invites identity splitting.

## Relevance to us

Attention scheduling needs an identity budget as well as a queue rule; compare [[zhang-2024-cut]].
