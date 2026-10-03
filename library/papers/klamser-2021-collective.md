---
id: klamser-2021-collective
type: paper
title: 'Collective predator evasion: Putting the criticality hypothesis to the test'
authors: ['Pascal P. Klamser', 'Pawel Romanczuk']
year: 2021
venue: 'PLOS Computational Biology'
url: https://arxiv.org/abs/2009.02079
doi: 10.1371/journal.pcbi.1008832
arxiv: '2009.02079'
cite: 'Klamser, P. P., & Romanczuk, P. (2021). Collective predator evasion: Putting the criticality hypothesis to the test. PLOS Computational Biology, 17(3), e1008832.'
topics: [criticality-measurement, collective-motion, collective-decision]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: '52 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

The authors put the "criticality hypothesis" to a direct evolutionary test in a spatially explicit
predator-prey model. Prey move at constant speed in 2D, align with and regulate distance to their Voronoi
neighbours, and flee from a predator; alignment strength mu_alg and angular noise D drive an order-disorder
transition (mu_c,alg ~ 0.9 at D=0.5). Group-level measures agree with the hypothesis: velocity-fluctuation
correlation between neighbours and susceptibility peak at the transition and predator capture rate is
minimal there. But a non-fleeing control school shows the minimal capture rate is caused by the school's
self-organised spatial structure, not by better information transfer. Individual-level evolution of mu_alg
then drives populations away from the critical point to an evolutionarily stable state deep in the ordered
phase (ESS mu_alg ~ 4.4), because self-sorting at the transition creates the steepest selection gradients.

## Contribution

The most careful negative test of the criticality hypothesis for animal groups: it separates
structural from informational benefits with a control condition and shows the critical point is
evolutionarily unstable under individual-level selection in fission-fusion groups. It challenges the
group-level-optimum assumption behind [[hidalgo-2014-information]] and earlier non-spatial models.

## Key results

- Polarisation rises steeply near the critical line; neighbour velocity-fluctuation correlation C_ij and susceptibility chi = N(<Phi^2> - <Phi>^2) peak at the transition (simulation, N=400, 40 runs per parameter point).
- Capture rate is minimal at the transition and anticorrelated with inter-individual distance (Pearson R = -0.69).
- Escape ratio R_esc = 1 - gamma_c/gamma_c,NF, which controls for structure, has no peak at criticality and increases with alignment into the ordered phase.
- Evolution of mu_alg from initial values 0, 5 and 10 converges to ESS ~ 4.4, far above mu_c ~ 0.9; the fitness gradient peaks just above the transition.
- Self-sorting (correlation between an agent's mu_alg and its front-back, side-centre or density position) and assortativity peak at the transition.
- The ESS shifts linearly with flee strength for mu_flee >= 2, explained by a balance between social and private predator information (local mean-field approximation).
- Results robust to predator agility, variable prey speed, blind angle, heterogeneous environments (SI).

## Methods and models

Agent-based model: dr_i/dt = v_i; dphi_i/dt = (F_i,perp + sqrt(2D) xi)/v0, with F = alignment
(mu_alg times mean velocity difference to Voronoi neighbours) + distance regulation
(mu_d tanh(m_d(r_ji - r_d))) + flee from predator if it is a Voronoi neighbour. Predator speed 2 v0, pursues
weighted centre of frontal Voronoi prey, attacks at rate gamma_a with success probability decaying linearly to
zero at r_catch. Evolutionary algorithm: fitness from 76 independent attack simulations, roulette-wheel
selection, Gaussian mutation; ESS from zero crossing of the fitness gradient. Code:
https://github.com/PaPeK/PredatorPrey.

## Limitations and open questions

2D, constant speed, one predator, one evolving trait. Fitness is predation only; foraging or
exploration could shift the ESS (the authors test a heterogeneous environment that favours disorder and still
find the critical point unstable). Group-level selection is not modelled beyond a discussion. The fish startle
contagion transition (a different critical point) is only discussed, and is studied in
[[poel-2022-subcritical]].

## Relevance to us

Essential counterweight for any hackathon hypothesis of the form "swarms should sit at
criticality". Its control-condition design (responsive vs non-responsive school with identical positions) is
a pattern we should copy when we claim information-transfer benefits. Model and code are a ready testbed. Read
with [[cavagna-2010-scale]], [[mateo-2017-effect]], [[lei-2023-exploring]] and [[romanczuk-2022-phase]].


## Notes from dmarz/criticality-measurement-audit

Audit 2026-10-03: re-opened arXiv 2009.02079 (PDF) and Crossref. Metadata and cite correct. Verified mu_c,alg about 0.9 at D = 0.5, N = 400, Ns = 40 runs per point, R = -0.69 capture rate vs IID, ESS about 4.4, Nf = 76 attack simulations, predator speed 2 v0, code at github.com/PaPeK/PredatorPrey: all match the paper. No corrections.
