---
id: dias-2023-environmental
type: paper
title: "Environmental memory boosts group formation of clueless individuals"
authors: ["Cristóvão S. Dias", "Manish Trivedi", "Giovanni Volpe", "Nuno A. M. Araújo", "Giorgio Volpe"]
year: 2023
venue: "Nature Communications"
url: https://arxiv.org/abs/2306.00516
doi: "10.1038/s41467-023-43099-0"
arxiv: "2306.00516"
cite: "Dias, C. S., Trivedi, M., Volpe, G., Araújo, N. A. M., & Volpe, G. (2023). Environmental memory boosts group formation of clueless individuals. Nature Communications, 14(1), 7324."
topics: ["active-matter", "swarm-intelligence", "collective-decision", "swarm-robotics"]
added_by: dmarz/active-matter-audit
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "16 (OpenAlex, 2026-10-03)"
code: []  # library ids of code that implements this paper
---

## Summary

Dias, Trivedi, Volpe, Araújo and Volpe show stigmergy without signalling. A few light-driven Janus colloids (surface
coverage 0.5 to 1.6 %) move through a crowd of equally sized passive silica colloids (0 to 75 % coverage). Each
active particle digs a transient open path through the passive crowd; before Brownian motion closes it, other active
particles preferentially follow it, catch up and form groups. The environment therefore stores a short-lived shared
memory that coordinates "clueless" agents with no sensing, signalling or information processing. Group formation is
non-monotonic in crowding: the largest groups appear at intermediate passive density, where paths persist but motion
is not yet caged. Brownian-dynamics simulations reproduce the effect only when active particles feel a steering torque
away from passive ones, and a rate-equation model attributes the boost to enhanced monomer–group and group–group
aggregation.

## Contribution

A clean physical demonstration that stigmergy, usually assumed to require agents that deposit and read cues
(pheromone trails, ant-colony optimisation), can emerge purely from a deformable environment plus an avoidance torque.
It connects active-matter aggregation (MIPS, [[cates-2015-motility]]; living crystals, [[palacci-2013-living]]) to the
swarm-intelligence notion of indirect coordination.

## Key results

- Measured: with no passive particles (ρ_p = 0) and ρ_a = 0.5 % no groups form; with more active particles a few
  (up to about 2) groups form. At intermediate ρ_p (up to 37.5 %) the number of groups rises to about 5 and the largest
  cluster can hold up to about 67 % of grouped particles. Largest-cluster size C_max peaks at intermediate ρ_p for every
  ρ_a, while the total number of groups increases monotonically with ρ_p.
- Measured: the path-revival lifetime τ_ρp (time until a region crossed by one active particle is crossed by another)
  first decreases with ρ_p, opposite to what slower collision-limited motion would predict; this is the signature of
  path reuse.
- Simulated: the experimental trends are reproduced only with an effective torque steering active particles away from
  passive ones, Ω₀ = 72 ± 16 k_BT (fitted two independent ways); without it, aggregation decays monotonically with ρ_p.
  The density of the peak decreases with ρ_a.
- Kinetic model: ċ₁ = −α_mm c₁² − α_mg c₁c_g, ċ_g = (α_mm/2)c₁² − (α_gg/2)c_g². Fitted α_mg and α_gg peak at
  intermediate ρ_p while α_mm stays roughly constant, so groups catalyse their own growth via the shared memory.

## Methods and models

Janus SiO₂ colloids (d = 4.77 µm, about 60 nm carbon cap) in water–2,6-lutidine (0.286 mass fraction) illuminated at
532 nm, speed v ≈ 1.9 µm/s, D_t = 0.0249 µm²/s; quasi-2D samples, 25-minute runs in triplicate. Simulations: underdamped
Langevin dynamics in LAMMPS with matched Péclet number, steric repulsion, short-range attraction between active
particles and an aligning torque away from passive ones; 100 runs per state point. Code and data on request only.
Read the whole arXiv:2306.00516v2 main text and Methods.

## Limitations and open questions

Small numbers of active particles and short observation windows; the steering torque is inferred from fits rather than
measured; short-range attractions between Janus particles help groups persist once formed. Whether the effect survives
for agents without such avoidance torques, or in 3D, is untested.

## Relevance to us

Directly usable for a swarm hackathon: robots moving through a field of movable obstacles (debris, soft terrain,
other passive robots) can coordinate through the traces they leave, with an optimal obstacle density. It is a
physical, communication-free baseline to compare against explicit stigmergy algorithms (ant-colony-style trail
following). Related: [[bauerle-2018-self]], [[lefranc-2025-synthetic]], [[caprini-2024-emergent]],
[[palacci-2013-living]].
