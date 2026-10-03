---
id: wang-2012-quantifying
type: paper
title: 'Quantifying and Tracing Information Cascades in Swarms'
authors: ['X. Rosalind Wang', 'Jennifer M. Miller', 'Joseph T. Lizier', 'Mikhail Prokopenko', 'Louis F. Rossi']
year: 2012
venue: 'PLoS ONE'
url: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0040084
doi: 10.1371/journal.pone.0040084
arxiv: null
cite: 'Wang, X. R., Miller, J. M., Lizier, J. T., Prokopenko, M., & Rossi, L. F. (2012). Quantifying and Tracing Information Cascades in Swarms. PLoS ONE, 7(7), e40084.'
topics: [criticality-measurement, collective-motion]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: '102 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Applies local conditional transfer entropy and active information storage to simulated swarms to
characterise information cascades and collective memory. It shows that cascades propagate as waves through the
swarm, relates individual spatial position to information processing role, and finds that maximal information
transfer tends to follow maximal collective memory.

## Contribution

First direct information-theoretic evidence, in simulation, that information cascades in
swarms travel as waves; introduced transfer entropy to collective motion.

## Key results

- Information cascades occur as waves rippling through simulated swarms (simulation).
- Maximal information transfer follows the stage of maximal collective memory (simulation).
- Cascades of conflicting information can be distinguished from waves of coordinated motion.

## Methods and models

Self-propelled particle swarm simulation (Reynolds-type rules); local conditional transfer entropy
and active information storage computed per agent and time step.

## Limitations and open questions

Simulation only; abstract-level read.

## Relevance to us

Practical blueprint for instrumenting our simulated swarms with information-dynamics measures.
See [[lizier-2008-local]], [[crosato-2018-informative]] and [[lizier-2014-jidt]].
