---
id: fruchart-2021-non
type: paper
title: Non-reciprocal phase transitions
authors: [Michel Fruchart, Ryo Hanai, Peter B. Littlewood, Vincenzo Vitelli]
year: 2021
venue: Nature
url: https://arxiv.org/abs/2003.13176
doi: 10.1038/s41586-021-03375-9
arxiv: '2003.13176'
cite: "Fruchart, M., Hanai, R., Littlewood, P. B., & Vitelli, V. (2021). Non-reciprocal phase transitions. Nature, 592(7854), 363-369."
topics: [sync-consensus, active-matter, collective-motion]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "575 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Shows that non-reciprocal interactions (A influences B differently than B influences A), generic out of
equilibrium, produce time-dependent phases in which spontaneously broken symmetries are dynamically restored.
The transitions are controlled by exceptional points of the linearised dynamics. The framework covers
non-reciprocal versions of synchronisation, flocking and pattern formation.

## Contribution

A unifying theory of non-reciprocal collective phases; it cites the swarmalator paper and is among the most
cited forward citations of [[okeeffe-2017-oscillators]] (OpenCitations, 2026-10-03). Provides the language
(exceptional points, chiral phases) used by later non-reciprocal swarmalator and robot papers such as
[[ceron-2024-reciprocal]].

## Key results

- Abstract-level: non-reciprocity yields time-dependent phases, controlled by exceptional points; examples
  include active time-(quasi)crystals and exceptional-point-enforced pattern formation with hysteresis.

## Methods and models

Bifurcation theory and non-Hermitian linear algebra applied to coupled-population Kuramoto, Vicsek-type and
pattern-forming models; supplementary movies. Full text not read.

## Limitations and open questions

Mean-field and continuum models; experimental realisations discussed but not in this paper (not checked).

## Relevance to us

Two robot sub-teams with asymmetric coupling rules (A aligns to B, B anti-aligns to A) are the kind of
system this theory addresses; it predicts time-dependent rather than static ordered phases (our inference
from the abstract, to be checked in the full text). Also a natural bridge to the active-matter topic.

## Notes from dmarz/active-matter

Full read of the main text and Methods of arXiv:2003.13176v5 (Supplementary not read). Details worth having here:

- General model: ∂ₜv_a = A_ab v_b + B_abcd (v_b·v_c) v_d + O(∇), the most general rotation-invariant cubic dynamics; non-reciprocity means A_ab ≠ A_ba, so the Jacobian is non-normal and can host exceptional points.
- Phases of the two-species flocking hydrodynamics in the (j₊, j₋) plane: disordered, aligned, anti-aligned, chiral (rotating order parameters, a time crystal), swap, and chiral+swap (time quasicrystal). Aligned→chiral boundaries are lines of exceptional points where a damped mode merges with the Goldstone mode (a Bogdanov–Takens bifurcation whose codimension drops to one because of the Goldstone mode).
- Measured in agent simulations (N = 512, v₀ = 0.5, L = 8; chiral phase at J = 0.39 × (1, −0.25; 0.25, 1)): chiral-phase fluctuations shrink as 1/√N, and the mean time between chirality flips grows like exp(Δ N/σ₀²), so the phase is stabilized by many-body effects; two noiseless agents eventually align or anti-align.
- In moving systems the square-root growth rate near the exceptional point, s ~ √(i v_ss k), produces a finite-wavelength instability and defect turbulence (solved with the open-source Dedalus spectral solver).
- Robot demo: two GoPiGo3 robots exchanging compass headings over Wi-Fi every 0.1 s, turning ±15° every 0.5 s; chiral rotation observed but not systematically, robots tend to align eventually because of imperfections. This is the closest thing to a swarm-robot test and it is anecdotal.
- Coefficients from the coarse-graining are stated by the authors to be only qualitatively related to the microscopic model.

For swarm dynamics this is the theory to cite for leader/follower, pursuer/evader or vision-cone swarms: tune the antisymmetric coupling and look for spontaneous rotation of group headings. Related: [[bandini-2025-xy]], [[bowick-2022-symmetry]], [[das-2024-flocking]], [[toner-1995-long]].
