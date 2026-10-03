---
id: trianni-2009-self
type: paper
title: "Self-Organizing Sync in a Robotic Swarm: A Dynamical System View"
authors: [Vito Trianni, Stefano Nolfi]
year: 2009
venue: IEEE Transactions on Evolutionary Computation
url: https://api.openalex.org/works/doi:10.1109/tevc.2009.2015577
doi: 10.1109/tevc.2009.2015577
arxiv: null
cite: "Trianni, V., & Nolfi, S. (2009). Self-organizing sync in a robotic swarm: A dynamical system view. IEEE Transactions on Evolutionary Computation, 13(4), 722-741."
topics: [sync-consensus, swarm-robotics]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "74 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Studies self-organised synchronisation in a swarm of robots that each have an individual periodic behaviour.
Instead of hand-designing a coupling law, the authors evolve neural controllers with artificial evolution, which
discovers minimal synchronisation strategies that exploit the dynamical coupling between robots and their
environment. They then analyse the evolved controllers as dynamical systems, which explains the mechanism and
predicts how synchronisation scales with group size.

## Contribution

An early swarm-robotics demonstration that synchrony can be learned rather than designed, and that the learned
strategy can be reverse-engineered with dynamical-systems tools; a precursor to learned-controller work in the
marl-emergence topic.

## Key results

- Abstract-level: evolved minimal sync strategies; dynamical-systems analysis predicts scalability with group size.

## Methods and models

Evolutionary robotics: neural controllers synthesised by artificial evolution, analysed as dynamical systems.
Full text not read (IEEE blocked automated access; abstract from OpenAlex).

## Limitations and open questions

Platform, group sizes and whether real robots were used are unverified.

## Relevance to us

Precedent for "learn a sync rule, then explain it" projects; compare with hand-designed pulse coupling
([[mirollo-1990-synchronization]], [[quinn-2025-decentralised]]).
