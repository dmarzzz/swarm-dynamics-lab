---
id: sayin-2025-behavioral
type: paper
title: The behavioral mechanisms governing collective motion in swarming locusts
authors: [Sercan Sayin, Einat Couzin-Fuchs, Inga Petelski, Yannick Günzel, Mohammad Salahshour, Chi-Yu Lee, Jacob M. Graving, Liang Li, Oliver Deussen, Gregory A. Sword, Iain D. Couzin]
year: 2025
venue: Science
url: https://kops.uni-konstanz.de/bitstreams/3fe07c1e-188e-4f30-a826-525de166089c/download
doi: 10.1126/science.adq7832
arxiv: null
cite: Sayin, S., Couzin-Fuchs, E., Petelski, I., Günzel, Y., Salahshour, M., Lee, C.-Y., Graving, J. M., Li, L., Deussen, O., Sword, G. A., et al. (2025). The behavioral mechanisms governing collective motion in swarming locusts. Science, 387(6737), 995–1000.
topics: [collective-motion, collective-decision]
added_by: dmarz/collective-motion
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "69 (Crossref is-referenced-by-count, 2026-10-03); 62 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Field sensory-deprivation experiments in Kenyan marching bands, plus a panoramic virtual-reality arena in
which untethered juvenile desert locusts interact with holographic virtual conspecifics, test the classical
self-propelled-particle account of locust marching. Vision is necessary and sufficient for coordination.
Alignment of the focal locust depends on the order of the virtual swarm, not its density; locusts do not
use the optomotor (optic-flow) response for social alignment; and they are "pulled" by receding neighbours.
Choice experiments with two targets show a bifurcation from averaging to choosing one, as predicted by a
ring-attractor "vectorial" model in which neighbours' bearings compete as neural activity bumps. A re-analysis
of the [[buhl-2006-disorder]] data finds no density-driven disorder-order transition once group-size
statistics are accounted for. Read in full (main text; supplementary material not read) from the University
of Konstanz repository copy.

## Contribution

A direct experimental challenge to the explicit-alignment assumption at the heart of [[vicsek-1995-novel]]
and [[couzin-2002-collective]], in the very system ([[buhl-2006-disorder]]) that had been the flagship
empirical support for the density-driven transition. Proposes moving from descriptive SPP models to
generative cognitive models of neighbour representation (ring attractor, after Sridhar et al. 2021).

## Key results

- Field (56 bands recorded for direction; reintroduced marked individuals): control (n = 110), anosmic
  (n = 89) and polarized-vision-deprived (n = 54) locusts rejoin the band direction; fully blinded
  (n = 114) move randomly. Vision is necessary and sufficient.
- VR parametric scan over 64 combinations of density (1-64 locusts/m^2) and order (0-1); 421 completed
  trials. Alignment depends strongly on order and not significantly on density (reported via R^2 / adjusted
  R^2 comparisons; exact values in their Fig. 2G and table S2).
- Optic flow: solitarious and gregarious locusts respond similarly (solitarious slightly stronger) to
  moving-dot stimuli (n = 32), but only gregarious locusts align with a virtual swarm (solitarious n = 34,
  gregarious n = 32), so the optomotor response does not mediate social alignment.
- "Pull": a receding ordered band offset 5 cm ahead (n = 21) recovers alignment comparable to full bands;
  a single virtual leader is followed closely; a 2000-locust arena shows the same proximal pursuit.
- Two-target test: follower positions switch from between the targets to one target as lateral separation
  grows (bifurcation; dip test of unimodality), as the ring-attractor model predicts and optic-flow models
  do not. Between two parallel bands, locusts head toward one band (perpendicular to optic flow).
- Re-analysis of Buhl et al. data: order is also independent of density there (their fig. S6).
- Data and scripts deposited on Zenodo (10.5281/zenodo.14353283, 10.5281/zenodo.14355590).

## Methods and models

Field work Feb-Mar 2020, Samburu and Isiolo, Kenya (112 locales). VR: fully panoramic, motion-compensated,
100 Hz projection; virtual bands of 64 animated locusts with real kinematics, periodic boundaries keeping
the focal animal centred, order set by von Mises dispersion. Hierarchical Bayesian model for direction
choice (4000 posterior samples). Theory: neighbours encoded as bumps on a ring-attractor network with local
excitation and long-range inhibition (collective neural consensus); the supplement shows the network model
yields ordered collective motion at swarm scale (fig. S15, not read).

## Limitations and open questions

- Claims about the swarm-scale emergence rest on simulations in the supplement, which I did not read.
- VR removes tactile and cannibalism cues that drive motion in real bands ([[romanczuk-2009-collective]]
  model these); the authors note tactile cues keep blinded animals moving.
- "No density dependence" is a strong claim from a bounded range (1-64 /m^2) and from a re-analysis; it
  invites replication with other species and arenas.
- The neural circuit for neighbour pursuit is not identified.

## Relevance to us

A strong 2025 result that the textbook alignment rule may be the wrong mechanism even where it fits the
macro data. For our hackathon this argues for testing agent rules that are perception- and decision-based
(bearing-only, choose-a-target) against Vicsek alignment, which is also closer to how an LLM or RL agent
would act. Related: [[bastien-2020-model]] (vision-only model), [[heins-2024-collective]] (active
inference agents), [[li-2025-reverse]] (VR reverse engineering in zebrafish).
