---
id: mora-2016-local
type: paper
title: 'Local equilibrium in bird flocks'
authors: ['Thierry Mora', 'Aleksandra M. Walczak', 'Lorenzo Del Castello', 'Francesco Ginelli', 'Stefania Melillo', 'Leonardo Parisi', 'Massimiliano Viale', 'Andrea Cavagna', 'Irene Giardina']
year: 2016
venue: 'Nature Physics'
url: https://arxiv.org/abs/1511.01958
doi: 10.1038/nphys3846
arxiv: '1511.01958'
cite: 'Mora, T., Walczak, A. M., Del Castello, L., Ginelli, F., Melillo, S., Parisi, L., Viale, M., Cavagna, A., & Giardina, I. (2016). Local equilibrium in bird flocks. Nature Physics, 12(12), 1153–1157.'
topics: [criticality-measurement, collective-motion, active-matter]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: '123 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Develops a dynamical maximum entropy inference method that handles changes in the interaction network
and slow sampling, and applies it to starling flocks. Alignment between birds is much faster than neighbour
rearrangement, so equilibrium inference with a fixed network gives results consistent with dynamical inference:
flock orientations are in local quasi-equilibrium.

## Contribution

Justifies applying equilibrium statistical mechanics (and hence critical-point analyses) to an
active system, at least over the interaction length scale.

## Key results

- Local alignment timescale much shorter than network rearrangement timescale (inferred from data).
- Equilibrium and dynamical inference of coupling strength and range agree.

## Methods and models

Dynamical maximum entropy on consecutive frames of 3D starling velocities. arXiv 1511.01958.

## Limitations and open questions

Abstract-level read.

## Relevance to us

Tells us when equilibrium-style criticality measures on swarm snapshots are defensible; check the
timescale separation in our own swarms. Related: [[bialek-2012-statistical]].
