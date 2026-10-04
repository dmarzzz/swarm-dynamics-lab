---
id: lowen-2020-inertial
type: paper
title: "Inertial effects of self-propelled particles: From active Brownian to active Langevin motion"
authors: ["Hartmut Löwen"]
year: 2020
venue: "The Journal of Chemical Physics"
url: https://arxiv.org/abs/1910.13953
doi: "10.1063/1.5134455"
arxiv: "1910.13953"
cite: "Löwen, H. (2020). Inertial effects of self-propelled particles: From active Brownian to active Langevin motion. The Journal of Chemical Physics, 152(4), 040901."
topics: ["active-matter", "swarm-robotics", "collective-motion"]
added_by: dmarz/active-matter-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "258 (OpenAlex, 2026-10-03)"
code: []  # library ids of code that implements this paper
---

## Summary

Perspective article arguing that the overdamped active Brownian particle (ABP) model, built for micron-scale swimmers,
is the wrong default for macroscopic self-propelled objects (vibrated granular hoppers, hexbugs, mini-robots) and for
"microflyers" moving in a gas, where mass and moment of inertia matter. Löwen extends the ABP equations to active
Langevin dynamics with translational mass m and moment of inertia J, collects the analytical single-particle results
(mean-square displacement, orientation correlation, the delay between heading and velocity), and summarises what
inertia does to motility-induced phase separation: it pushes MIPS to higher Péclet number, destroys it above a
critical mass, and makes the coexisting dense and dilute phases have different kinetic temperatures.

## Contribution

The standard entry point to inertial (underdamped) active matter, the regime that covers robots and drones. It sits
between the overdamped ABP/MIPS literature ([[fily-2012-athermal]], [[cates-2015-motility]],
[[bechinger-2016-active]]) and robot experiments such as [[deblais-2018-boundaries]] and [[scholz-2018-rotating]],
and names the new timescales (τ = m/γ, τ_r = J/γ_R) that a robot swarm model must include.

## Key results

- Model: m r̈ + γ ṙ = γ v₀ n̂ + f(t), J φ̈ + γ_R φ̇ = M + g(t). Besides the Péclet number there are three
  dimensionless delay numbers built from τ_r, τ, the persistence time and the circling frequency.
- Single particle (analytical, reviewed from the author's earlier papers): the MSD has four regimes (ballistic,
  diffusive, ballistic, diffusive). The long-time diffusivity D_L depends strongly on the moment of inertia J but not
  on the mass. The orientation correlation is a double exponential when J > 0. A positive delay function
  d(t) = ⟨ṙ(t)·n̂(0)⟩ − ⟨ṙ(0)·n̂(t)⟩ shows that heading changes first and velocity follows.
- Measured (vibrated 3D-printed granular particles with different masses and moments of inertia, from Scholz et
  al. 2018): MSD, orientation correlations and the delay function d(t) agree with the active Langevin model once
  parameters are fitted, with no self-aligning torque needed for these particles (unlike hexbugs).
- Collective (simulations cited from Mandal et al.): at area fraction 0.5, MIPS needs higher Péclet number as mass
  grows and vanishes above a critical mass. Head-on pairs bounce back instead of stalling, which breaks up nuclei.
  Coexisting phases have kinetic temperatures that differ by up to a factor of about 100 (cold dense phase, hot gas),
  and the coarsening exponent falls below the overdamped 1/3.
- In non-inertial frames (rotating disk, oscillating plate) fictitious forces appear that have no overdamped analogue.

## Methods and models

Perspective with analytical results for the linear active Langevin model and a review of granular experiments (vibrated
hoppers, 3D-printed particles with added outer or central masses) and simulations. No new data; no code.
Read sections III to VII of arXiv:1910.13953v1 (the inertial parts and perspectives); section II, the recap of
overdamped ABPs, only skimmed.

## Limitations and open questions

- Collective results are summaries of other papers; aligning interactions with inertia, inertial active crystals and
  field theories with inertia are listed as open.
- The linear model ignores the self-aligning torque that couples heading to velocity, which the author notes is needed
  for hexbug-type robots (see [[baconnier-2025-self]]).
- Sensory delay in mini-robots is mentioned as a related memory effect but not modelled.

## Relevance to us

Any physical robot or drone swarm is underdamped, so overdamped ABP intuitions (stall on contact, MIPS at high Pe) can
fail: inertial agents bounce and may not cluster at all. This paper gives the minimal model to simulate and the
dimensionless numbers to report. Related: [[omar-2021-phase]] and [[luo-2025-flocking]] (inertial phase behaviour and
flocking), [[deblais-2018-boundaries]], [[caprini-2024-emergent]], [[baconnier-2025-self]].
