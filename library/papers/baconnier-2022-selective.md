---
id: baconnier-2022-selective
type: paper
title: "Selective and collective actuation in active solids"
authors: ["P. Baconnier", "D. Shohat", "C. Hernández López", "C. Coulais", "V. Démery", "G. Düring", "O. Dauchot"]
year: 2022
venue: "Nature Physics"
url: https://arxiv.org/abs/2110.01516
doi: "10.1038/s41567-022-01704-x"
arxiv: "2110.01516"
cite: "Baconnier, P., Shohat, D., López, C. H., Coulais, C., Démery, V., Düring, G., & Dauchot, O. (2022). Selective and collective actuation in active solids. Nature Physics, 18(10), 1234–1239."
topics: [swarm-robotics, active-matter, sync-consensus]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "156 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

An "active solid" is a set of self-propelled units elastically tied to reference positions. The authors build
one from Hexbug toy robots trapped in 3D-printed cylinders at the nodes of a spring lattice pinned at its edges
(triangular, N = 19; kagome, N = 12). Each unit pushes its node along its polarity, and the polarity
self-aligns toward the node's displacement. A single control parameter, the elasto-active feedback
pi = l_e / l_a (elastic deformation per active force over self-alignment length), governs the dynamics. Below
a threshold the lattice freezes in a disordered state; above a second threshold all nodes spontaneously break
chiral symmetry and orbit their rest positions in a synchronised limit cycle ("collective actuation"). The
motion condenses onto a pair of normal modes that are not necessarily the lowest-energy ones (modes 4 and 5 in
the kagome lattice), and they derive a bound that picks out the selected modes from their geometry.

## Contribution

It shows experimentally and theoretically that elasticity plus self-alignment produces mode-selective
collective oscillation in a mechanically stable solid, a new collective state distinct from flocking in active
fluids. It extends self-aligning active matter to connected robot collectives and is a design principle for
robotic metamaterials; [[ben-zion-2023-morphological]] applies the same self-alignment physics to free robots.

## Key results

- Measured thresholds: triangular pi_FD = 0.800, pi_CA = 1.29; kagome pi_FD = 0.564, pi_CA = 0.600. Between them
  a heterogeneous regime where oscillation survives in the centre and freezing invades layer by layer from
  the pinned edge.
- Measured: dynamics condense on two degenerate modes, extended and locally quasi-orthogonal; for kagome these
  are the 4th and 5th modes.
- Simulated large lattices (triangular up to N = 1141, kagome up to N = 930): collective actuation persists;
  the actuated fraction drops discontinuously at pi_FD and saturates at large N; the selected symmetry class is
  size independent.
- Theory: single unit in a triangle has a circle of marginal fixed points of radius pi/omega0^2 below
  pi_c = omega0^2 and a limit cycle above it, via a global bifurcation of a continuous set of fixed points, not
  a Hopf bifurcation; noise has a sharp threshold D_c above which actuation is lost.

## Methods and models

Overdamped, harmonic, noiseless model: u_i' = pi n_i - M_ij u_j, n_i' = (n_i x u_i') x n_i, with M the dynamical
matrix. Mean-field coarse-graining of displacement U and polarisation m fields; analysis of an N = 7 chain and
of single-unit geometries; numerical simulations. Hexbugs in 3D-printed cylinders linked by springs; tracking
from video. Data/code archived at Zenodo (10.5281/zenodo.6653906).

## Limitations and open questions

Noise is excluded from most of the theory; the transition is mostly characterised numerically for large N;
hardware lattices are small. Open: how this generalises to disordered networks or units with sensing, and
whether mode selection can be programmed for locomotion or function.

## Relevance to us

Shows that a swarm's coupling structure (here an elastic network) can select a collective mode that energy
ranking would not predict. Useful conceptual contrast to consensus and synchronisation on graphs
([[okeeffe-2017-oscillators]], [[fruchart-2021-non]]) and a candidate toy system for "physical
interaction instead of communication" experiments.
