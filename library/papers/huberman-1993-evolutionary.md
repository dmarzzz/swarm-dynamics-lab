---
id: huberman-1993-evolutionary
type: paper
title: "Evolutionary games and computer simulations"
authors: ["Bernardo A. Huberman", "Natalie S. Glance"]
year: 1993
venue: "Proceedings of the National Academy of Sciences"
url: https://arxiv.org/abs/chao-dyn/9307017
doi: 10.1073/pnas.90.16.7716
arxiv: "chao-dyn/9307017"
cite: "Huberman, B. A., & Glance, N. S. (1993). Evolutionary games and computer simulations. Proceedings of the National Academy of Sciences, 90(16), 7716-7718."
topics: [meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: full
relevance: 3
citations: "620 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Re-runs Nowak and May's spatial Prisoner's Dilemma (99 x 99 lattice, single defector in a sea of cooperators, fixed boundaries) with synchronous updating, which reproduces the famous persistent kaleidoscope of cooperators and defectors, and with asynchronous updating (at most one player updated per microstep, rest of the system frozen), which drives the lattice to all-defection within about a hundred generations whenever at least one defector is present.

## Contribution

The classic demonstration that a simulation artefact (a global clock implied by synchronous updating) can produce a headline scientific result. Argues that unless a real global clock exists, simulations of social or biological systems should use continuous, asynchronous updating.

## Key results

- Synchronous: symmetric persistent patterns at generation 217, matching Nowak and May's figure.
- Asynchronous with the same initial condition: fixed all-defect state within about 100 generations; always converges to defection if at least one defector starts.
- With asynchronous updating on delayed scores, asymptotic cooperation increases with the delay, and long delays (several generations) lengthen initial transients.

## Methods and models

Cellular-automaton Prisoner's Dilemma; asynchronous version uses microsteps sized so that a whole-lattice update takes the same average time as one synchronous generation; each player is replaced by the highest-scoring player in its neighbourhood.

## Limitations and open questions

Three-page note with one figure; no statistics over seeds; Only one payoff setting and one asynchronous scheme are shown. The claim that nature lacks global clocks is argued, not measured.

## Relevance to us

Cited by [[radax-2010-timing]] as the founding result on update artefacts. For our swarm and LLM-swarm sims it is the cautionary example to put next to every emergent-cooperation or emergent-coordination claim: check the result under asynchronous or randomised scheduling before believing it.
