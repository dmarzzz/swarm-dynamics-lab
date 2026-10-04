---
id: chvykov-2021-low
type: paper
title: "Low rattling: A predictive principle for self-organization in active collectives"
authors: ["Pavel Chvykov", "Thomas A. Berrueta", "Akash Vardhan", "William Savoie", "Alexander Samland", "Todd D. Murphey", "Kurt Wiesenfeld", "Daniel I. Goldman", "Jeremy L. England"]
year: 2021
venue: "Science"
url: https://arxiv.org/abs/2101.00683
doi: "10.1126/science.abc6182"
arxiv: "2101.00683"
cite: "Chvykov, P., Berrueta, T. A., Vardhan, A., Savoie, W., Samland, A., Murphey, T. D., Wiesenfeld, K., Goldman, D. I., & England, J. L. (2021). Low rattling: A predictive principle for self-organization in active collectives. Science, 371(6524), 90–95."
topics: [swarm-robotics, active-matter, criticality-measurement]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "83 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

The paper proposes "rattling" as a nonequilibrium analogue of energy for predicting which configurations a
driven, messy many-body system will spend its time in. Rattling R(q) is the entropy of the distribution of
short-time configuration displacements starting from q, which for a Gaussian approximation is (half) the log
determinant of their covariance. The claim is that the steady-state density follows a Boltzmann-like law,
p_ss(q) proportional to exp(-gamma R(q)), so low-rattling configurations are selected, generalising
thermophoresis (particles collect where diffusivity is low). They test it on "smarticles", three-link robots
that cannot move alone but jostle each other inside a ring, in experiment and simulation. Three smarticles
self-organise into a few ordered collective "dances"; different drive patterns select different dances; a
randomly alternating mixture of two drives selects only the dances common to both; and adding randomness to
the drive melts the order in a quantitatively predicted way.

## Contribution

A general, data-driven predictor of self-organisation in driven collectives that needs only local short
rollouts, and an associated control idea: design the drive pattern to shape the rattling landscape. It is the
theory companion to [[savoie-2019-robot]] and part of the Goldman-lab robophysics line
([[li-2021-programming]], [[ozkan-aydin-2021-collective]]).

## Key results

- Simulation of 15 smarticles (45-D configuration space): ensemble rattling decreases over time after random
  initialisation and the configuration dynamics are well approximated by diffusion, so the rattling law holds.
- Measured (3 smarticles): over 99% of steady-state probability sits in configurations making up 0.1% of the
  accessible states, all low-rattling.
- Measured: two drives give largely non-overlapping steady states; the compound drive A+B selects their
  overlap, and its probabilities are predicted from the constituent distributions (Fig. 3D).
- Measured and derived: increasing the probability of random arm moves flattens the rattling landscape and
  melts the ordered states; a lower bound on rattling from drive entropy predicts this (Fig. 4D).
- Random-transition-rate Markov chain model: state exit rates approximately predict steady-state probability
  (analytic, supplementary).

## Methods and models

Configuration q = (x, y, theta) of each smarticle's middle link relative to the ensemble; drive = periodic arm
angle sequence (alpha1, alpha2) from microcontrollers. Rattling from the covariance C(q) of velocity samples
(q(t) - q(0))/t along short rollouts. Experiments with a confining ring and overhead tracking; simulations of
up to 15 smarticles in a physics engine. Data deposited at Zenodo (10.5281/zenodo.4056700); no code repository
named in the text I read.

## Limitations and open questions

Authors: the relation can fail when energy and rattling landscapes vary on similar scales (strong currents), and
fine-tuned counterexamples exist. I note: the experimental tests use 3 robots, where exhaustive sampling is
possible; the high-dimensional claim rests on simulation. gamma is a fitted system constant. It is untested
on swarms with sensing and decision rules, which is exactly where a hackathon could probe it.

## Relevance to us

A measurable quantity (rattling) we could compute from simulated or tracked swarm trajectories to predict
which collective states persist, and a principled way to choose global drives. Relates to the
criticality/measurement thread ([[sar-2022-dynamics]] for context on collective-state measures) and to
[[baconnier-2022-selective]] and [[ben-zion-2023-morphological]] on robotic active matter.

## Notes from dmarz/swarm-robotics-audit

Checked against the arXiv PDF (2101.00683). Verified 15 smarticles and 45-D space; over 99% of probability in 0.1% of states; Zenodo 10.5281/zenodo.4056700; metadata matches Crossref (Science 371(6524), 90-95). No corrections.
