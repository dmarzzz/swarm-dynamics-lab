---
id: crosato-2018-informative
type: paper
title: 'Informative and misinformative interactions in a school of fish'
authors: ['Emanuele Crosato', 'Li Jiang', 'Valentin Lecheval', 'Joseph T. Lizier', 'X. Rosalind Wang', 'Pierre Tichit', 'Guy Theraulaz', 'Mikhail Prokopenko']
year: 2018
venue: 'Swarm Intelligence'
url: https://arxiv.org/abs/1705.01213
doi: 10.1007/s11721-018-0157-x
arxiv: '1705.01213'
cite: 'Crosato, E., Jiang, L., Lecheval, V., Lizier, J. T., Wang, X. R., Tichit, P., Theraulaz, G., & Prokopenko, M. (2018). Informative and misinformative interactions in a school of fish. Swarm Intelligence, 12(4), 283–305.'
topics: [criticality-measurement, collective-motion]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: '72 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Applies local transfer entropy to tracked groups of five rummy-nose tetras (Hemigrammus
rhodostomus) swimming in a ring-shaped tank, focusing on 455 spontaneous collective U-turns from ten one-hour
trials. Transfer entropy is computed from the relative heading of a source fish to the turning (heading
change) of a destination fish. Information flow peaks during U-turns. Positive local transfer entropy
(informative flow) comes from fish that have already turned about fish that are turning; negative local
transfer entropy (misinformative flow) comes from fish that have not turned yet. Spatial "motifs" show
informative flow to fish behind the source and misinformative flow to fish beside it with opposite heading.

## Contribution

First real-animal demonstration that predictive information flow intensifies during
collective direction changes, and the first use of negative local transfer entropy to identify
misinformative interactions in a collective.

## Key results

- Optimal source-destination lag v = 6 frames = 0.12 s (maximises average transfer entropy), interpretable as an observer-detectable reaction time.
- Embedding parameters k = l = 3, tau = 1 by minimising self-prediction error.
- Incoming transfer entropy averaged over 455 U-turns rises from a negative peak for the first fish to turn to a positive peak for the last; outgoing transfer entropy is positive only for the first turner and negative for the last.
- Information transfer is non-zero even during steady schooling but largest during U-turns.
- Positive transfer entropy is strongest to destinations behind the source and at near-perpendicular relative heading.

## Methods and models

Data: 70 tetras, groups of 5, ring tank (radius 25-35 cm), 50 Hz video tracked with idTracker 2.1;
9.27 million data points. Variables x_n = heading change of destination, y_n = destination heading minus
source heading. Local transfer entropy with a linear-Gaussian estimator (equivalent to Granger causality) from
JIDT ([[lizier-2014-jidt]]), pooled over fish and trials assuming stationarity. Significance of local values by
about 371 million surrogate local values, Benjamini-Hochberg false discovery rate.

## Limitations and open questions

Pairwise transfer entropy only; multivariate (conditional) versions needed to remove redundancy and
capture synergy, which the authors flag. Ring tank restricts behaviour to straight swimming or U-turns.
Five fish only. Gaussian estimator assumes linear dependence. Transfer entropy is observational, not causal.

## Relevance to us

Directly reusable pipeline for measuring information cascades in our swarms during collective
turns, with a proper surrogate test for local values. The informative/misinformative split is a useful lens for
leader/follower and minority-triggered turns ([[syga-2026-minority]]). Related: [[wang-2012-quantifying]],
[[sattari-2022-modes]] (caveats on pairwise transfer entropy), [[attanasi-2014-information]].
