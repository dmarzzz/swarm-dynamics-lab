---
id: das-2024-flocking
type: paper
title: "Flocking by Turning Away"
authors: ["Suchismita Das", "Matteo Ciarchi", "Ziqi Zhou", "Jing Yan", "Jie Zhang", "Ricard Alert"]
year: 2024
venue: "Physical Review X"
url: https://arxiv.org/abs/2401.17153
doi: "10.1103/physrevx.14.031008"
arxiv: "2401.17153"
cite: "Das, S., Ciarchi, M., Zhou, Z., Yan, J., Zhang, J., & Alert, R. (2024). Flocking by Turning Away. Physical Review X, 14(3), 031008."
topics: [collective-motion, active-matter]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 35  # (Crossref is-referenced-by-count, 2026-10-03; OpenAlex daily budget exhausted for this IP)
code: []
---
## Summary

Shows that polar flocking can emerge from interactions that turn agents away from each other rather than align them. Combining simulations, kinetic theory and experiments with self-propelled Janus colloids that repel more strongly at the front than the rear, the authors find a stable polar state in which each particle compromises between turning away from left and right neighbours. Unlike alignment, turn-away flocking needs particle repulsion; at high density it produces flocking Wigner crystals rather than motility-induced phase separation.

## Contribution

Bridges aligning and non-aligning active matter and offers a mechanism for cell flocking despite contact inhibition of locomotion.

## Key results

- Simulation/theory/experiment (abstract): polar order from turn-away torques plus repulsion; flocking Wigner crystals at high concentration.

## Methods and models

Agent-based simulations, kinetic theory, experiments with Janus colloids (details not read).

## Limitations and open questions

Abstract only. Mapping to animals is speculative.

## Relevance to us

A counterexample to "alignment is needed for flocking", alongside [[sayin-2025-behavioral]] and [[salahshour-2025-allocentric]]. Interaction inference on similar colloids: [[hem-2025-learning]].

## Notes from dmarz/active-matter

Full read of arXiv:2401.17153v2 (main text and start of Appendix A). Points beyond the abstract:

- Experiment: 3 µm silica Janus particles (35 nm Ti + 20 nm SiO₂ cap) sedimented between ITO coverslips 120 µm apart, AC field 10 V at 30 kHz. Flocking is classified by time-averaged polar order ⟨P⟩ ≥ 0.5 (high magnification) or PIV correlation length (low magnification); the experimental phase boundary in (area fraction, v₀) matches simulations and two theories.
- Model: ABPs with dipolar repulsion F ∝ (d_h + d_t)² e^(−r/λ)/r⁴ and a torque Γ_ij ∝ (d_h² − d_t²) e^(−r/λ)/r⁴ n̂_j × r̂_ij that turns each particle away from its neighbour (λ = 120 µm). The torque couples orientation to the other particle's position, so it is intrinsically non-reciprocal (Γ_ij ≠ −Γ_ji). Flipping the sign (d_t² > d_h², turn-toward) reproduces the earlier active phase separation result.
- Simulations: N = 2500 up to 70,225; polar order still appears at large N; at higher density flocks become "active Wigner crystals" (hexatic then crystalline), with monocrystals at higher activity. Crystallization is not needed for flocking; N = 40,000 runs show classic polar bands.
- Theory 1 (BBGKY): growth rate of polarity a = ρτ₀/(2πξ_r) − D_r, where τ₀ is an integral of the torque against the measured pair distribution g(r, φ, θ); four symmetry-breaking conditions on g are needed and are satisfied in simulations. Theory 2 (Boltzmann scattering): torques alone give θ_out = −θ_in (no net alignment); repulsion pushes particles apart before they finish turning, so |θ_out| < |θ_in| and the pair gains forward momentum. Repulsion is necessary.
- Mechanism of stability: each particle compromises between turning away from left and right neighbours.
- Turn-away torques suppress MIPS (particles reorient away from clusters), so these flocks reach higher density and speed without the flock-freezing seen in Quincke rollers.
- Speculative outlook stated by the authors: contact inhibition of locomotion in cells, and robust swarming of robots through disordered environments with stuck agents.

For the hackathon: a collision-avoidance rule ("turn away from neighbours") plus short-range repulsion is enough for a robot swarm to flock, which is cheaper than explicit heading communication. Related: [[fily-2012-athermal]], [[cates-2015-motility]], [[baconnier-2025-self]], [[fruchart-2021-non]], [[caprini-2023-flocking]].
