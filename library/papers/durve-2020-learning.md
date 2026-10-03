---
id: durve-2020-learning
type: paper
title: Learning to flock through reinforcement
authors: [Mihir Durve, Fernando Peruani, Antonio Celani]
year: 2020
venue: Physical Review E
url: https://arxiv.org/html/1911.01697
doi: 10.1103/PhysRevE.102.012601
arxiv: '1911.01697'
cite: Durve, M., Peruani, F., & Celani, A. (2020). Learning to flock through reinforcement. Physical Review E, 102(1), 012601.
topics: [marl-emergence, collective-motion]
added_by: dmarz/marl-emergence
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "57 (Crossref is-referenced-by-count, 2026-10-03); 59 (OpenCitations, 2026-10-03)"
code: []
---

## Summary

Constant-speed agents in a 2D periodic box sense only the angle between their own heading and the mean heading
of neighbours within radius R = 1, and choose a turning angle. Each agent runs tabular, myopic Q-learning with a
cost of 1 whenever it loses a neighbour. A single learner placed among Vicsek-rule "teachers" learns the
teachers' own rule, and a population of independent learners with no teachers converges on the same rule: turn
toward the neighbours' mean heading, capped at the maximum turn. Polar order rises as the neighbour-loss rate
falls. The authors read this as evidence that Vicsek-style velocity alignment is the optimal cohesion strategy
when perception is limited to neighbour velocities: "to stay together, steer together".

## Contribution

The cleanest demonstration that a canonical collective-motion rule, Vicsek alignment [[vicsek-1995-novel]], can
emerge from a selfish cohesion objective via multi-agent RL rather than being assumed. It reframes interaction
rules as optimal policies, which links the collective-motion and MARL communities, and it is the starting
point for later physics-style MARL flocking papers ([[brambati-2025-learning]]).

## Key results

- Single learner among N = 200 teachers, theta_max = 3 pi/16: the neighbour-loss rate drops from about 0.5 per
  step (random) to about 0.1 (contact kept 90% of the time), and the learned greedy policy matches the teachers'
  hard-wired rule state by state (measured, 20 training sessions).
- Independent concurrent learners, all starting from zero Q-tables: cost reaches a low steady value within a
  few hundred episodes, roughly independent of group size; with 128 states and 28 actions agents keep all
  neighbours about 97% of the time (measured).
- All agents learn the same policy: across agents, Q(0, a) for the optimal action clusters near 0.1 with a clear
  gap to suboptimal actions (N = 100, Ks = 32, Ka = 7).
- Polar order parameter psi rises toward high order as the neighbour-loss rate falls during training (Fig. 6).
  The claim that alignment is "optimal" is supported only within this observation and action space.

## Methods and models

Positions update r_i(t+1) = r_i(t) + v0 v_i(t) dt with v0 = 0.5, dt = 1, density rho = 2 per unit area, periodic
box. State s_i = signed angle between v_i and P_i, the normalised mean velocity of neighbours within R = 1,
discretised into Ks bins. Action: rotate by one of Ka angles evenly spaced in [-theta_max, theta_max]. Cost
c_i = 1 if n_i(t+1) < n_i(t), else 0. Update Q_i(s,a) <- Q_i(s,a) + alpha [c - Q_i(s,a)] with alpha = 0.005 (no
bootstrapping, i.e. a contextual bandit per step), epsilon-greedy with decaying epsilon, episodes of 1e4 steps.
Teachers follow a discretised Vicsek rule with bounded turning. Read from the arXiv v1 text; the published PRE
version may contain additional material (the PRE abstract mentions a kinetic description) that I did not read.

## Limitations and open questions

The state is a single hand-chosen scalar (relative heading), so the space of possible rules is tiny and
alignment is nearly the only sensible answer; the authors say themselves that metric versus topological
neighbourhoods, neighbour weighting and the choice of state variable should be learned, not fixed. The reward is
a proxy (cohesion) for primary goals such as predator avoidance or foraging. Agents are identical; no noise
sweep or order-disorder transition is reported, so we do not learn whether learned flocks sit near criticality.
No code released.

## Relevance to us

Directly usable as a hackathon baseline: tiny, tabular, reproducible in an afternoon, with a clear physical
observable (polar order). Natural extensions: learn with richer states (positions, topological neighbours),
add noise and measure the order-disorder transition of the learned policy, or reward predator survival instead
of cohesion. Compare with deep-RL swarms [[huttenrauch-2019-deep]], hydrodynamic schooling [[verma-2018-efficient]]
and the mean-field view [[yang-2018-mean]].
