---
id: aoki-1982-simulation
type: paper
title: A simulation study on the schooling mechanism in fish.
authors: [Ichiro Aoki]
year: 1982
venue: Nippon Suisan Gakkaishi (Bulletin of the Japanese Society of Scientific Fisheries)
url: https://www.jstage.jst.go.jp/article/suisan1932/48/8/48_8_1081/_article
doi: 10.2331/suisan.48.1081
arxiv: null
cite: 'Aoki, I. (1982). A simulation study on the schooling mechanism in fish. Nippon Suisan Gakkaishi, 48(8), 1081–1088.'
topics: [collective-motion]
added_by: dmarz/collective-motion
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "594 (OpenAlex, 2026-10-03); 475 (Crossref is-referenced-by-count, 2026-10-03); 566 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Early individual-based simulation of fish schooling. Speed and direction of each fish are stochastic
variables, and heading depends on the positions and headings of neighbours through three interactions:
approach, avoidance and parallel orientation. Coherent group movement arises without any individual knowing
the whole school's movement and without a consistent leader. Effective schooling requires both approach
(for aggregation) and parallel orientation (for cohesive movement); varying parameters gives a wide range of
school movement patterns. Read at abstract level on J-STAGE.

## Contribution

Arguably the first published zonal (attraction/repulsion/alignment) model of collective motion, predating
[[reynolds-1987-flocks]]; a direct ancestor of Huth and Wissel (1992, J. Theor. Biol. 156:365-385; not catalogued, full text not reachable) and [[couzin-2002-collective]].

## Key results

- Qualitative: leaderless coherent schooling from local stochastic rules; approach plus parallel orientation
  both needed.

## Methods and models

Stochastic individual-based simulation with three behavioural interactions and random-number-driven
movement.

## Limitations and open questions

Abstract-level read; small groups; no quantitative comparison with data.

## Relevance to us

Historical priority for zonal rules; cite alongside Reynolds when describing boids-like models.
