---
id: bialek-2014-social
type: paper
title: 'Social interactions dominate speed control in poising natural flocks near criticality'
authors: ['William Bialek', 'Andrea Cavagna', 'Irene Giardina', 'Thierry Mora', 'Oliver Pohl', 'Edmondo Silvestri', 'Massimiliano Viale', 'Aleksandra M. Walczak']
year: 2014
venue: 'Proceedings of the National Academy of Sciences'
url: https://arxiv.org/abs/1307.5563
doi: 10.1073/pnas.1324045111
arxiv: '1307.5563'
cite: 'Bialek, W., Cavagna, A., Giardina, I., Mora, T., Pohl, O., Silvestri, E., Viale, M., & Walczak, A. M. (2014). Social interactions dominate speed control in poising natural flocks near criticality. Proceedings of the National Academy of Sciences, 111(20), 7212–7217.'
topics: [criticality-measurement, collective-motion]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: '203 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Extends maximum entropy modelling of starling flocks from directions to full velocities. Models
constrained by local neighbour correlations and the variance of speeds give parameter-free predictions of how
speed correlations spread through the flock. The inferred parameters lie in the critical regime, which is
why speed fluctuations show scale-free correlations even though speed is a "stiff" mode.

## Contribution

Shows that criticality in flocks is not just a Goldstone-mode artefact of broken rotational
symmetry: the speed sector, which has no such symmetry, is also inferred to be critical.

## Key results

- Maximum entropy speed model predictions of correlation spread agree well with flock data (claimed in abstract).
- Fitted parameters sit in the critical regime; criticality lets the flock achieve long-range correlation with limited speed fluctuations.

## Methods and models

Maximum entropy on STARFLAG 3D velocity data; model equivalent to a ferromagnet with a soft
constraint on speed; arXiv preprint titled "Social interactions dominate speed control in driving natural flocks
toward criticality" (1307.5563).

## Limitations and open questions

Equilibrium inference on snapshots; abstract-level read.

## Relevance to us

Key evidence that the critical signature is not trivially explained by symmetry breaking; when
our simulated swarms have variable speed, test speed correlations too. See [[cavagna-2010-scale]] and
[[bialek-2012-statistical]].
