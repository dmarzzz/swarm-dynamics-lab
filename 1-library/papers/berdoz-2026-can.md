---
id: berdoz-2026-can
type: paper
title: Can AI Agents Agree?
authors:
- Frederic Berdoz
- Leonardo Rugli
- Roger Wattenhofer
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2603.01213
doi: null
arxiv: '2603.01213'
cite: 'Berdoz, F., Rugli, L., & Wattenhofer, R. (2026). Can AI Agents Agree? arXiv preprint arXiv:2603.01213.'
topics:
- fork-merge-security
- llm-agent-swarms
- sync-consensus
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Evaluates LLM agents playing a Byzantine consensus game over scalar values in a synchronous all-to-all simulation, in a no-stake setting where agents have no preference over the final value. Across hundreds of simulations varying model size, group size and Byzantine fraction, valid agreement is unreliable even with no Byzantine agents and gets worse as groups grow. A few Byzantine agents reduce success further. Most failures are loss of liveness (timeouts, stalled convergence) rather than subtle corruption of the agreed value.

## Contribution

A direct test of whether LLM agents can carry out the scalar agreement task that classical approximate agreement solves ([[dolev-1986-reaching]]), finding that they often cannot even without adversaries.

## Key results

- Measured (per abstract): agreement unreliable in benign settings; degrades with group size.
- Measured (per abstract): small numbers of Byzantine agents reduce success further.
- Measured (per abstract): failures dominated by loss of liveness.

## Methods and models

Synchronous all-to-all simulation; scalar values; varied model sizes and Byzantine fractions. Only the abstract was read.

## Limitations and open questions

Abstract-level reading; numbers not checked.

## Relevance to us

Q2. A practical warning: if the parent asks its LLM sub-agents to reach agreement among themselves by conversation before merging, the protocol may stall rather than be subverted, and an attacker gains a denial-of-service lever. Thresholds from classical protocols apply only if the agreement procedure is implemented by code around the agents, not by the agents' own dialogue. Related: [[lee-2026-robust]], [[jo-2025-byzantine]].
