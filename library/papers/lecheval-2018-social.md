---
id: lecheval-2018-social
type: paper
title: Social conformity and propagation of information in collective U-turns of fish schools
authors: [Valentin Lecheval, Li Jiang, Pierre Tichit, Clément Sire, Charlotte K. Hemelrijk, Guy Theraulaz]
year: 2018
venue: 'Proceedings of the Royal Society B: Biological Sciences'
url: https://europepmc.org/article/MED/29695447
doi: 10.1098/rspb.2018.0251
arxiv: null
cite: 'Lecheval, V., Jiang, L., Tichit, P., Sire, C., Hemelrijk, C. K., & Theraulaz, G. (2018). Social conformity and propagation of information in collective U-turns of fish schools. Proceedings of the Royal Society B: Biological Sciences, 285(1877), 20180251.'
topics: [collective-motion, collective-decision]
added_by: dmarz/collective-motion-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "75 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Groups of rummy-nose tetra (Hemigrammus rhodostomus) of different sizes swim in a ring-shaped tank and
spontaneously reverse direction (collective U-turns). Tracking shows the group slows down before a U-turn,
consistent with predictions that lower speed amplifies heading fluctuations; U-turns are mostly started by
fish at the front, and the new direction spreads front to back at constant pace, like falling dominoes.
The mean time between U-turns rises sharply with group size. An Ising-type spin model with anisotropic,
asymmetric interactions and a nonlinear tendency to follow the local majority (social conformity)
reproduces the dynamics and frequency of U-turns. Read at abstract level (Europe PMC record; full text
returned a server error).

## Contribution

A clean experimental system for spontaneous collective direction changes, with a measured propagation
mechanism (no amplification or damping) and a minimal binary-choice model. It connects collective motion
to collective decision-making via conformity, complementing [[tunstrom-2013-collective]] (state switching)
and [[attanasi-2014-information]] (turning waves in starlings).

## Key results

- Measured: speed drops before collective U-turns; initiators are mostly at the front; information
  propagates front to back without amplification or dampening.
- Measured: mean interval between U-turns increases sharply with group size (exact values not read).
- Model: Ising spin model with anisotropic and asymmetric interactions plus nonlinear majority following
  quantitatively reproduces U-turn dynamics and frequency (claimed in abstract).

## Methods and models

Ring-shaped tank, individual trajectory reconstruction for fish alone and in groups of several sizes;
spin (heading clockwise or anticlockwise) model with conformity nonlinearity (from abstract; parameters
not read).

## Limitations and open questions

- Abstract-level entry; group sizes and fitted parameters not checked.
- The ring tank reduces motion to one dimension, which makes the binary model natural but limits
  generality.

## Relevance to us

A ready-made benchmark for consensus switching in a swarm: measure time between spontaneous reversals
against group size, and test whether agents with conformity rules reproduce the domino-like propagation.
Related: [[crosato-2018-informative]] (information flow in the same species), [[calovi-2014-swarming]],
[[couzin-2005-effective]].
