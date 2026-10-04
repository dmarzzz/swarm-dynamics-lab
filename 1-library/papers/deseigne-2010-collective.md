---
id: deseigne-2010-collective
type: paper
title: "Collective Motion of Vibrated Polar Disks"
authors: ["Julien Deseigne", "Olivier Dauchot", "Hugues Chaté"]
year: 2010
venue: "Physical Review Letters"
url: https://arxiv.org/abs/1004.1499
doi: "10.1103/physrevlett.105.098001"
arxiv: "1004.1499"
cite: "Deseigne, J., Dauchot, O., & Chaté, H. (2010). Collective Motion of Vibrated Polar Disks. Physical Review Letters, 105(9), 098001."
topics: ["active-matter", "collective-motion", "swarm-robotics"]
added_by: dmarz/active-matter
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "580 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Deseigne, Dauchot and Chaté build the first table-top polar flock of inert objects: 4 mm copper-beryllium disks
with an off-centre tip and a rubber skate on opposite sides, confined between glass plates (gap 2.4 mm) and shaken
vertically at 115 Hz. The two "legs" give each disk a polar axis along which it walks; the disk shape is isotropic,
so any alignment comes from repeated inelastic collisions, not from shape. The vibration strength Γ acts as the
noise knob: lower Γ gives longer persistence. With N = 890 disks (surface fraction about 0.38 in the 20-diameter
region of interest) the polar disks show system-size jets and swirls, a sharply rising mean polar order as Γ
decreases, and giant number fluctuations, while rotationally symmetric control disks never order.

## Contribution

The first well-controlled experiment showing collective motion of non-living, non-communicating particles with
polar (not nematic) order, and the first experimental report of giant number fluctuations in a polar active
system. It is the granular counterpart of the nematic experiment [[narayan-2007-long]] and the reference
physical realisation of Vicsek-class behaviour ([[vicsek-1995-novel]], [[chate-2008-collective]]). Later work on
self-alignment in the same family of vibrated or wheeled bots is reviewed in [[baconnier-2025-self]].

## Key results

- Measured (single particles, 50 disks): typical speed v_typ ≈ 0.025 particle diameters per vibration period,
  varying only 6 % over Γ ∈ [2.7, 3.7]; particles stop near Γ = 2.4. Angular diffusion D_θ falls linearly with
  decreasing Γ; persistence length ξ = π²v_typ/(2D_θ) goes from about 20 diameters at Γ = 3.7 to above 100 at
  Γ = 2.7, versus about 1 for symmetric disks.
- Measured (collective, N = 890): order parameter Ψ = |⟨u_i⟩| fluctuates strongly in time but holds order-one
  plateaus at low Γ; ⟨Ψ⟩ rises sharply as Γ decreases; symmetric disks give no collective motion.
- Measured: number fluctuations Δn ~ n^α with α ≈ 1.45 ± 0.05 over a range of box sizes, levelling off at the system
  size. The authors compare with the predicted 1.6 and argue the exponent should approach it from below as the
  system grows. This is a claim of consistency, not a precise test.
- Observed: a small fraction of particles move against the main flow, so polar versus nematic-with-polar-packets
  order cannot be fully excluded in this small domain.

## Methods and models

Electromagnetic shaker with air-bearing slider, horizontal/vertical vibration ratio < 10⁻², homogeneity better than
1 %; flower-shaped arena of diameter 160 mm whose petals reinject particles from the wall; tracking at 20 Hz with
1728 × 1728 px camera, position resolution 0.1 diameters, orientation 0.05 rad. No simulations, no code. Full read of
arXiv:1004.1499v1 (4-page PRL preprint).

## Limitations and open questions

- Saturated order deep in the ordered phase is not reachable because self-propulsion degrades at low Γ.
- Bounded arena: no periodic boundaries, bands near onset would be broken, and the authors say they cannot separate
  near-transition fluctuations, boundary effects and genuine GNF.
- One density only; the nature of the transition (continuous or discontinuous) is left open.
- The collision statistics that produce alignment are not measured (follow-up work did this).

## Relevance to us

The closest classic experiment to a swarm of simple bots: flocking from collisions alone with no sensing or
communication, and a control (symmetric disks) that isolates the cause. It gives a measurable recipe for our robot
or simulation data: order parameter Ψ versus noise, number-fluctuation exponent in sub-boxes, and persistence length
from the angular diffusion. Related: [[narayan-2007-long]], [[deblais-2018-boundaries]], [[scholz-2018-rotating]],
[[baconnier-2025-self]], [[kumar-2014-flocking]].

## Notes from dmarz/active-matter-audit

Audit 2026-10-03: entry was at abstract depth. I read the full arXiv preprint and rewrote Summary through Relevance
with the measured numbers (N = 890, α ≈ 1.45 ± 0.05 versus predicted 1.6, persistence lengths), raised read_depth to
full, and replaced the Semantic Scholar count with OpenAlex. Metadata confirmed against arXiv and OpenAlex.
