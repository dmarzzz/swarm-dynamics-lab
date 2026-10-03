---
id: ceron-2023-diverse
type: paper
title: Diverse behaviors in non-uniform chiral and non-chiral swarmalators
authors: [Steven Ceron, Kevin O'Keeffe, Kirstin Petersen]
year: 2023
venue: Nature Communications
url: https://arxiv.org/abs/2211.06439
doi: 10.1038/s41467-023-36563-4
arxiv: '2211.06439'
cite: "Ceron, S., O'Keeffe, K., & Petersen, K. (2023). Diverse behaviors in non-uniform chiral and non-chiral swarmalators. Nature Communications, 14(1), 940."
topics: [sync-consensus, swarm-robotics, active-matter, collective-motion]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "64 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Extends the 2D swarmalator model of [[okeeffe-2017-oscillators]] with three realistic features: non-identical
natural frequencies (four distributions F1-F4, including two equal and opposite groups), chirality (agents
revolve on circular orbits whose angular position is their phase, v_i = c_i n_i with n_i orthogonal to theta_i),
and local coupling within a radius sigma. A "frequency coupling" phase offset (Q terms) makes counter-revolving
agents interact differently. Parameter sweeps over K in [-1,2] and J in [-1,1] reveal a zoo of states not seen
in the original model: interacting and concentric phase waves, bouncing clusters, static anti-phase,
synchronized expansion, radial oscillation, vortex lattices, revolving clusters. Some states qualitatively
resemble slime mould life stages, sperm vortex arrays, spinning magnetic microrobots and Quincke rollers.

## Contribution

Moves swarmalators from the idealised, globally coupled, identical case toward systems a roboticist could
build (local sensing, manufacturing spread in frequencies, chirality). It is a mapping study of what behaviours
a small, tunable rule set can produce, written from a swarm-robotics design perspective (Petersen lab),
with the argument that a few global parameters switch between very different collective behaviours.

## Key results

- Non-chiral, two opposite frequency groups (F2): two internally synchronised clusters that cannot sync with each
  other produce "bouncing clusters" (periodic attraction and repulsion) at moderate K, J > 0; static anti-phase at
  high K, J = 0; periodic radial expansion and contraction at K > 0, J < 0. With one frequency (F1) and J = -1 the
  synchronised group expands indefinitely.
- The number of concentric splintered phase waves tracks the number of frequency groups (up to three; beyond that
  layering becomes unclear; Supplementary Movie 2).
- Chiral (revolving) agents keep high space-phase order S across much of the (K,J) plane even with little phase
  coupling; vortices form when K < 0, dense revolving clusters when K > 0.
- Local coupling: long range (sigma = 5) gives one sync cluster; intermediate (sigma = 3) multiple clusters with
  little inter-cluster phase correlation; short range (sigma = 0.5) a crystal-like state of length scale ~10 with
  local phase coherence, which melts into a gas-like state with noise and frequency spread (Fig. 7, N = 300,
  500 runs per point).
- Comparisons to real systems are qualitative (snapshots, trajectories, a head-orientation versus angular
  position plot resembling Riedel et al.'s sperm data); the one quantitative comparison (speed and angular
  velocity versus Gardi et al.'s microrobots) is in the Supplement and was not checked here.

## Methods and models

Model eqs (1)-(6): dx_i/dt = v_i + (1/N) sum_j [ (x_j-x_i)/|x_j-x_i| (A + J cos(theta_j - theta_i - Q_x)) - B (x_j-x_i)/|x_j-x_i|^2 ],
dtheta_i/dt = omega_i + (K/N) sum_j sin(theta_j - theta_i - Q_theta)/|x_j-x_i|, A = B = 1, Q_x = (pi/2)|sgn(omega_j) - sgn(omega_i)| and
Q_theta = (pi/4)|sgn(omega_j) - sgn(omega_i)| (non-zero only between counter-revolving agents). Local coupling via step-function cutoffs at sigma. Order parameters
S_+/-, Kuramoto Z, gamma (fraction completing a cycle), beta (separation of the two frequency groups), plus
velocity autocorrelation, g(r) and phase-phase correlation C(r). Simulations in MATLAB, Euler, 500 agents,
dt = 0.1, T = 1000, 10 trials per heat-map cell. Main text and Methods read in full; the 100-page Supplement
was not.

## Limitations and open questions

- Phenomenological: no analytic theory for the new states; boundaries are read from heat maps of S.
- The frequency-coupling offsets are ad hoc and not derived from a physical mechanism.
- Agents can drift out of their circular orbits, so rotating-crystal experiments are not reproduced well
  (the authors say so).
- No robot implementation in this paper; no code link found in the arXiv text.

## Relevance to us

The best catalogue of "what behaviours can I get from a swarmalator rule with local sensing and imperfect
units", which is exactly the hackathon design question for small robots or simulated drones. Pairs with
[[barcis-2020-sandsbots]] (hardware), [[yoon-2022-sync]] (theory), the review [[sar-2026-interplay]] and the
chiral active-matter model [[levis-2019-activity]]. The correlation-function analysis gives measurement tools
for the criticality-measurement topic.

## Notes from dmarz/sync-consensus-audit

Audit 2026-10-03: metadata, cite string and the key numbers in this entry re-checked against the full text
(arXiv PDF or the hosted PDF at the entry's url); no corrections needed and read_depth full is supported by the
detail in the entry.
