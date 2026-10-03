---
id: cavagna-2019-dynamical
type: paper
title: 'Dynamical Renormalization Group Approach to the Collective Behavior of Swarms'
authors: ['Andrea Cavagna', 'Luca Di Carlo', 'Irene Giardina', 'Luca Grandinetti', 'Tomas S. Grigera', 'Giulia Pisegna']
year: 2019
venue: 'Physical Review Letters'
url: https://arxiv.org/abs/1905.01227
doi: 10.1103/PhysRevLett.123.268001
arxiv: '1905.01227'
cite: 'Cavagna, A., Di Carlo, L., Giardina, I., Grandinetti, L., Grigera, T. S., & Pisegna, G. (2019). Dynamical renormalization group approach to the collective behavior of swarms. Physical Review Letters, 123(26), 268001.'
topics: [criticality-measurement, collective-motion, active-matter]
added_by: dmarz/criticality-measurement-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: '38 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Natural midge swarms show critical slowing down with a dynamical critical exponent z close to 1, while
Vicsek-type and equilibrium dissipative models give z close to 2. The authors run a one-loop dynamical
renormalization group (RG) on a field theory of the Inertial Spin Model (ISM), which couples velocity to a
conserved "spin" (non-dissipative coupling) plus an effective friction. They find a crossover between an
unstable conservative fixed point with z = d/2 and a stable dissipative fixed point with z = 2, governed by a
conservation length scale that grows as friction shrinks. For finite swarms with low friction the conservative
fixed point controls the dynamics, giving z = 3/2 in three dimensions, which simulations of the ISM confirm.

## Contribution

First RG calculation aimed directly at the measured dynamic scaling of wild swarms. It turns the empirical
exponent of [[cavagna-2017-dynamic]] into a constraint on models: purely dissipative alignment dynamics
(Vicsek, model A) cannot reproduce it, inertial or conservative couplings are needed.

## Key results

- One-loop fixed points: conservative z = d/2 (unstable), dissipative z = 2 (stable) (analytic).
- Crossover set by R0 = lambda0/eta0 (transport coefficient over friction); the conservative exponent rules when (xi Lambda)^(d/4) << Lambda R0, i.e. for correlation lengths that are not too large (analytic).
- In d = 3 the conservative point gives z = 3/2, against z of about 1 measured in natural swarms and about 2 in fully dissipative models (comparison with prior experiments).
- ISM simulations on a 3D lattice: z of about 1.5 at low friction (eta-hat = 1, 2) and about 2 at high friction (eta-hat = 4) (simulation, Fig. 2).

## Methods and models

Field theory with order-parameter field psi and conserved generator s (structure of Heisenberg-type models
E and G of Halperin-Hohenberg), plus friction -eta s. Momentum-shell dynamical RG at one loop, flow equations
for coupling f, ratio w and R = lambda/eta. Numerical check: microscopic ISM on a fixed lattice with periodic
boundaries, d psi_i/dt = s_i x psi_i / chi, d s_i/dt = -(eta/chi) s_i + psi_i x J sum n_ij psi_j + noise;
z extracted from the scaling of relaxation time with correlation length.

## Limitations and open questions

One-loop only; the lattice model has no self-propulsion or density fluctuations, so it is a model of
swarm velocity fluctuations, not of the full active system. The gap between z = 3/2 and the measured z of
about 1 remains. Experimental z itself rests on a modest number of swarms.

## Relevance to us

If we measure dynamic scaling in a simulated or robot swarm (relaxation time vs correlation length), this
paper tells us which model class each exponent points to. Read with [[cavagna-2017-dynamic]],
[[attanasi-2014-finite]], [[cavagna-2023-natural]] and [[sinhuber-2017-phase]].
