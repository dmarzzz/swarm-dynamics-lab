---
id: kuhn-2018-privacy
type: paper
title: On Privacy Notions in Anonymous Communication
authors: [Christiane Kuhn, Martin Beck, Stefan Schiffner, Eduard Jorswieck, Thorsten Strufe]
year: 2018
venue: arXiv preprint; published in Proceedings on Privacy Enhancing Technologies 2019(2)
url: https://arxiv.org/abs/1812.05638
doi: 10.2478/popets-2019-0022
arxiv: '1812.05638'
cite: Kuhn, C., Beck, M., Schiffner, S., Jorswieck, E., & Strufe, T. (2019). On Privacy Notions in Anonymous Communication. Proceedings on Privacy Enhancing Technologies, 2019(2), 105-125.
topics: [fork-merge-security]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 55 (Semantic Scholar citing-paper listing of Loopix shows this entry with 55, 2026-10-03)
code: []
---

## Summary

Kuhn and colleagues unify the formal privacy notions used across analysis frameworks for anonymous communication networks. They define notions as combinations of building blocks, prove for every pair whether one is strictly stronger, and give a complete hierarchy. Practical assumptions such as protocol model or user corruption are added as options. They claim to capture the notions and assumptions of all existing analytical frameworks and to resolve inconsistencies between them.

## Contribution

A common, game-based hierarchy of anonymity notions, so that systems with ad hoc goals can be compared.

## Key results

- Complete hierarchy of privacy notions for anonymous communication with strictness proofs (abstract).
- Corruption and protocol-model assumptions expressed as options to notions.

## Methods and models

Indistinguishability games; not read beyond the abstract.

## Limitations and open questions

Only the abstract was read.

## Relevance to us

Q1 and survey work. When we write the fork-merge survey we need a precise statement of what "hiding which sub-agent returns" means; this hierarchy lets us pick the exact notion (for example sender unobservability versus sender-message unlinkability) and compare designs like [[piotrowska-2017-loopix]] and [[boneh-2020-single]] on the same scale. Informal glossary: [[pfitzmann-2010-terminology]]; bounds: [[das-2018-anonymity]].
