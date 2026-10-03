---
id: panayiotou-2026-setting
type: paper
title: "Setting the clock: Evaluating temporal window parameters for coordinated behavior detection"
authors: ["Georgios Panayiotou", "Lorenzo Mannocci", "Maurizio Tesconi"]
year: 2026
venue: "AIDEM Workshop at ECML-PKDD 2026 (arXiv preprint)"
url: https://arxiv.org/abs/2609.21959
doi: null
arxiv: "2609.21959"
cite: "Panayiotou, G., Mannocci, L., & Tesconi, M. (2026). Setting the clock: Evaluating temporal window parameters for coordinated behavior detection. arXiv:2609.21959. Accepted at the AIDEM Workshop, ECML-PKDD 2026."
topics: [swarm-detection]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Coordination networks link users who perform similar actions within shared temporal windows, but window length and stride are usually treated as implementation details. This paper varies both on information-operation campaigns and measures their effect on detecting coordinated communities. Window length determines which coordination patterns are detectable; window stride has negligible effect on precision and recall.

## Contribution

First systematic sensitivity analysis of the time-window parameter that every co-action detector depends on.

## Key results

- Window length changes which coordination patterns are found; stride does not matter for precision and recall (abstract).

## Methods and models

Sweep over window length and stride in a coordination-network pipeline on IO datasets. Details not in the abstract.

## Limitations and open questions

Abstract only; workshop paper. The abstract gives no recommended window values.

## Relevance to us

Any agent-swarm detector built on co-action windows must report a window sweep. Complements [[iannucci-2025-detecting]] (kernel instead of windows) and [[pante-2025-beyond]] (controls).
