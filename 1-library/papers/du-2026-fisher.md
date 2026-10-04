---
id: du-2026-fisher
type: paper
title: 'Fisher Information Metric as a model-free measure of proximity to criticality in neural systems'
authors: ['Yuewei Du', 'Alberto Liardi', 'Hardik Rajpal', 'Henrik Jeldtoft Jensen']
year: 2026
venue: 'arXiv'
url: https://arxiv.org/abs/2609.07624
doi: null
arxiv: '2609.07624'
cite: 'Du, Y., Liardi, A., Rajpal, H., & Jensen, H. J. (2026). Fisher Information Metric as a model-free measure of proximity to criticality in neural systems. arXiv preprint arXiv:2609.07624.'
topics: [criticality-measurement]
added_by: dmarz/criticality-measurement-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: '0 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Proposes the Fisher Information Metric (FIM), a generalised susceptibility, as a model-agnostic readout of
how close a system is to criticality. Validated on branching processes, spiking networks and whole-brain models:
the FIM with respect to the control parameter tracks the degree of criticality. When the control parameter is
unknown, they compute the FIM of the observed branching ratio; it peaks where activity growth and decay balance,
and the peak sharpens near criticality, so peak width and height give continuous readouts.

## Contribution

A recent (September 2026) attempt to replace exponent fitting with a susceptibility-like information measure that
does not need the true control parameter. Builds on the Fisher-information view of [[mastromatteo-2011-criticality]]
and the utility measures in [[chen-2025-why]].

## Key results

- FIM of the control parameter tracks criticality across models of increasing biological complexity (simulation, claimed in abstract).
- FIM of the observed branching ratio peaks at balance of growth and decay, sharpening near criticality (simulation, claimed in abstract).

## Methods and models

Branching processes, spiking neuron networks, whole-brain models; FIM estimated from distributions of activity
or of the empirical branching ratio.

## Limitations and open questions

Abstract-level read; new preprint, no independent use yet; neural only.

## Relevance to us

Candidate distance-to-criticality readout for agent or robot swarms with cascade dynamics. Compare with
[[sooter-2025-defining]] and [[wilting-2018-inferring]].
