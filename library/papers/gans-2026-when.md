---
id: gans-2026-when
type: paper
title: 'When Agents Talk: Honeytokens under Shared Memory'
authors:
- Joshua S. Gans
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.11436
doi: null
arxiv: '2608.11436'
cite: 'Gans, J. S. (2026). When Agents Talk: Honeytokens under Shared Memory. arXiv preprint arXiv:2608.11436.'
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: null
code: []
---

## Summary

A theory paper motivated by a 2026 cyber-capability evaluation in which short-lived AI agents turned a shared package repository into persistent memory, passing exploit findings to later agents and rebuilding the channel after it was removed (as described by the author). It asks whether a honeytoken can be harmless to trusted agents without becoming recognisable to an attacker who shares their information and can implement the trusted policy, and proves it cannot. A trusted rule that avoids decoys can be copied; a total-variation bound limits compatibility when decoys resemble real objects; and shared memory pools weak fingerprints, so repeated non-triggering probes drive the Bayes error of classifying decoy vs genuine to zero when response laws differ and are learnable. The proposed fix is to keep token identity in a private reference monitor and route legitimate agents through a provenance-enforcing broker.

## Contribution

The first formal treatment of honeytokens against a coalition of agents with shared memory. That is exactly the swarm case: collective learning defeats per-agent deception.

## Key results

- Impossibility: no honeytoken is both safe for trusted agents and unrecognisable to an attacker who can run the trusted policy (theorem, abstract).
- Shared memory turns many weak fingerprints into a strong one; with learnable response laws, misclassification error goes to zero with probes (theorem, abstract).
- If probing triggers containment, the coalition must stay active long enough to learn, which is a lever for defenders (abstract).

## Methods and models

Information-theoretic and decision-theoretic modelling. Abstract-level read.

## Limitations and open questions

Abstract only; the motivating incident is reported by the author and not checked here.

## Relevance to us

A swarm is a shared-memory coalition, so this is a theoretical ceiling on what traps can do against swarms. It predicts that honeytoken detection degrades with swarm size and memory sharing, which is a testable hypothesis for us. Companion: [[gans-2026-calibrated]]. Empirical counterparts: [[cordeiro-2026-rouxii]], [[ayzenshteyn-2025-cloak]].
