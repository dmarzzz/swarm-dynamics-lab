---
id: cresci-2020-decade
type: paper
title: A Decade of Social Bot Detection
authors:
- Stefano Cresci
year: 2020
venue: Communications of the ACM
url: https://arxiv.org/abs/2007.03604
doi: 10.1145/3409116
arxiv: '2007.03604'
cite: Cresci, S. (2020). A decade of social bot detection. Communications of the ACM, 63(10), 72-83. https://doi.org/10.1145/3409116
topics:
- swarm-detection
- sybil-resistance
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 285 (Crossref, 2026-10-03)
code: []
---

## Summary

A review of social bot detection from about 2010 to 2020 built on a longitudinal analysis of the literature. It traces the shift from per-account supervised classifiers to group-level methods that look for coordinated behaviour, argues that evolving bots keep defeating static detectors, and proposes adversarial and proactive detection as the way to stop losing the arms race.

## Contribution

The standard review of the pre-LLM bot detection field and the clearest statement of the move from individual-account to collective (coordination-based) detection.

## Key results

- Longitudinal analysis of the bot-detection literature over a decade (abstract).
- Identifies the trend from feature-based supervised account classifiers to unsupervised group-based detectors exploiting collective behaviour.
- Recommends adversarial detection: anticipate future bot designs rather than react to observed ones.

## Methods and models

Literature review with bibliometric analysis. Abstract-level read.

## Limitations and open questions

Pre-LLM. Review rather than new measurement; built mostly on Twitter studies.

## Relevance to us

The 'detect the group, not the agent' turn is the core idea for detecting LLM agent swarms, whose individual outputs may be indistinguishable. Follow-ups: [[cresci-2017-paradigm]], [[mannocci-2024-detection]], [[cresci-2023-demystifying]].
