---
id: paramanick-2024-programming
type: paper
title: "Programming tunable active dynamics in a self-propelled robot"
authors: ["Somnath Paramanick", "Arnab Pal", "Harsh Soni", "Nitin Kumar"]
year: 2024
venue: "The European Physical Journal E"
url: https://arxiv.org/abs/2306.06609
doi: "10.1140/epje/s10189-024-00430-x"
arxiv: "2306.06609"
cite: "Paramanick, S., Pal, A., Soni, H., & Kumar, N. (2024). Programming tunable active dynamics in a self-propelled robot. The European Physical Journal E, 47(5), 34."
topics: ["active-matter", "swarm-robotics"]
added_by: dmarz/active-matter
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "20 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Paramanick and coauthors program a differential-drive wheeled robot so that its two wheel speeds reproduce standard
active-particle models: active Brownian, run-and-tumble, and Brownian dynamics, over wide parameter ranges. Particle
tracking confirms the trajectories match theory, and the dynamics can be switched by light intensity. Read from the abstract on the page in `url`; details beyond the abstract are not checked.

## Contribution

A recipe for turning cheap robots into faithful active particles, enabling table-top tests of active-matter predictions
with robot swarms (cf. [[dmitriev-2025-swarmodroid]], [[scholz-2018-rotating]]).

## Key results

- Measured trajectories agree with predicted active dynamics (abstract).
- Dynamics switchable by an external light signal (abstract).

## Methods and models

Single robot, microcontroller implementation of model equations, video tracking. arXiv:2306.06609; full text not read.

## Limitations and open questions

Single-robot demonstration; collective experiments not reported in abstract.

## Relevance to us

Immediately useful if the hackathon builds physical robots: implement ABP or run-and-tumble on differential drive and
test MIPS or flocking predictions. Related: [[fily-2012-athermal]], [[cates-2015-motility]].
