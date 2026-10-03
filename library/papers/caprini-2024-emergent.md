---
id: caprini-2024-emergent
type: paper
title: "Emergent memory from tapping collisions in active granular matter"
authors: ["Lorenzo Caprini", "Anton Ldov", "Rahul Kumar Gupta", "Hendrik Ellenberg", "René Wittmann", "Hartmut Löwen", "Christian Scholz"]
year: 2024
venue: "Communications Physics"
url: https://arxiv.org/abs/2310.19566
doi: "10.1038/s42005-024-01540-w"
arxiv: "2310.19566"
cite: "Caprini, L., Ldov, A., Gupta, R. K., Ellenberg, H., Wittmann, R., Löwen, H., & Scholz, C. (2024). Emergent memory from tapping collisions in active granular matter. Communications Physics, 7(1), 52."
topics: ["active-matter", "swarm-robotics"]
added_by: dmarz/active-matter-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "40 (OpenAlex, 2026-10-03)"
code: []  # library ids of code that implements this paper
---

## Summary

Experiment with 3D-printed vibration-driven robots ("vibrobots") on a shaken plate: a large passive tracer (legs
symmetric, so no self-propulsion; radius twice that of the bath particles) is immersed in a bath of small active
vibrobots at packing fractions up to about 0.3. Because the bath particles are inertial and self-propelled, a particle
that hits the tracer bounces back, then returns and hits it again, several times and from nearly the same direction,
while frictional torques align it around the tracer. These "tapping collisions" give the tracer an emergent persistent,
active-like motion with memory. The authors propose a generalized active Einstein relation that links tracer
fluctuations, dissipation and the bath-induced persistence, and show the memory can be tuned by bath density and
motility.

## Contribution

Particle-resolved experimental evidence that inertia plus activity changes how an active bath drives a passive body,
beyond the effective-temperature picture. Experimental companion to the inertial active matter theory in
[[lowen-2020-inertial]], from the same Düsseldorf group as [[scholz-2018-rotating]].

## Key results

- Measured: tracer trajectories become persistent at short times and diffusive only at long times once active
  particles are added; the equilibrium (φ = 0) tracer is a plain underdamped Brownian particle.
- Measured: number of recollisions per tapping event and contact duration have broad distributions (fitted as
  e^(−x/a) x^b) at φ = 0.075.
- Measured: tracer kinetic energy grows with φ (scaling argument K_t − D_tΓ_t ~ φ); the velocity autocorrelation has two
  decay regimes for φ > 0, a short one set by the tracer's own inertia M/Γ_t and a long, bath-induced one.
- Measured: the emergent persistence time first increases with φ and is counteracted at φ ≳ 0.3 by simultaneous
  collisions from opposite sides, i.e. memory is non-monotonic in density.
- Theory: an "active" Einstein relation including rotational dynamics reproduces the measured effective translational
  and rotational diffusivities.

## Methods and models

Vibrobots with tilted elastic legs on a 300 mm plate driven by an electromagnetic shaker; tracer 30 mm in diameter with
thick symmetric legs; sub-pixel tracking of all particles. Model: underdamped Langevin tracer with an active-like
(Ornstein–Uhlenbeck) force from the bath. Read abstract, introduction, results and parts of Methods of
arXiv:2310.19566v1; no code or data link found in the text.

## Limitations and open questions

Single tracer size ratio (R = 2r) and a single bath type; quasi-2D plate with walls; theory is phenomenological for the
bath force. Generalisation to many tracers or to deformable objects is not tested.

## Relevance to us

For a robot swarm pushing an object (collective transport) or for mixed active/passive robot groups, inertial
recollisions create correlated pushes, so a passive payload can acquire directed, persistent motion from an
undirected swarm. Density tunes this memory, with an optimum. Related: [[lowen-2020-inertial]],
[[scholz-2018-rotating]], [[deblais-2018-boundaries]], [[giraldobarreto-2025-active]].
