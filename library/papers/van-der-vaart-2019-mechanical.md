---
id: van-der-vaart-2019-mechanical
type: paper
title: 'Mechanical spectroscopy of insect swarms'
authors: ['Kasper van der Vaart', 'Michael Sinhuber', 'Andrew M. Reynolds', 'Nicholas T. Ouellette']
year: 2019
venue: 'Science Advances'
url: https://europepmc.org/article/PMC/PMC6719412
doi: 10.1126/sciadv.aaw9305
arxiv: null
cite: 'van der Vaart, K., Sinhuber, M., Reynolds, A. M., & Ouellette, N. T. (2019). Mechanical spectroscopy of insect swarms. Science Advances, 5(7), eaaw9305.'
topics: [criticality-measurement, collective-motion]
added_by: dmarz/criticality-measurement-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: '47 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Treats a laboratory midge swarm as a material and measures its response to controlled perturbation. Mating
swarms of Chironomus riparius form over a visual marker; the authors oscillate the marker sinusoidally and
track the swarm. The swarm follows at the drive frequency with reduced amplitude and a phase lag, and the
response propagates through the swarm like a shear wave, from which they extract storage and loss moduli. The
swarm is strongly damped, both viscously and inertially, the opposite of the near-lossless information
propagation reported for bird flocks.

## Contribution

One of the few direct-perturbation (response function) measurements of a natural collective, as opposed to
inferring susceptibility from fluctuations. Fills the gap flagged in the scan's coverage note, next to
[[chatterjee-2025-maximal]] and [[gelblum-2015-ant]].

## Key results

- Swarm centre-of-mass amplitude is linear in marker amplitude at fixed frequency (linear response regime) (measured).
- Storage modulus G' is negative and scales quadratically with frequency, implying an effective inertia; loss modulus G'' increases with frequency (measured).
- Shear-wave speed increases linearly with driving frequency and is of the order of midge flight speeds (measured).
- A stochastic swarm model with an oscillating centre of attraction reproduces negative G' and increasing G'' (simulation).

## Methods and models

Laboratory swarms tracked in 3D with multiple cameras; swarm marker on a linear stage oscillated at
controlled frequency and amplitude (for example amplitude 84 mm); slabs of the swarm fit to A(z) sin(omega t -
phi); constitutive model with inertial term (standard viscoelastic models cannot give negative G'); comparison
with a Reynolds-type stochastic model.

## Limitations and open questions

Laboratory swarms of one species; the visual marker cue is an external field acting on all individuals, not a
local perturbation; relation to the near-critical swarm claims of [[attanasi-2014-finite]] is discussed only
qualitatively.

## Relevance to us

Template for measuring response, not just fluctuations, in a robot swarm: drive a beacon sinusoidally and
measure G' and G''. Lets us test the fluctuation-dissipation issues raised in [[ferretti-2025-out]]. Related:
[[sinhuber-2017-phase]], [[ouellette-2022-physics]].
