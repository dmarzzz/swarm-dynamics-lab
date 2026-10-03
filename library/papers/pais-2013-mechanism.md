---
id: pais-2013-mechanism
type: paper
title: "A Mechanism for Value-Sensitive Decision-Making"
authors: ["Darren Pais", "Patrick M. Hogan", "Thomas Schlegel", "Nigel R. Franks", "Naomi E. Leonard", "James A. R. Marshall"]
year: 2013
venue: "PLoS ONE"
url: "https://doi.org/10.1371/journal.pone.0073216"
doi: "10.1371/journal.pone.0073216"
arxiv: null
cite: "Pais, D., Hogan, P. M., Schlegel, T., Franks, N. R., Leonard, N. E., & Marshall, J. A. R. (2013). A Mechanism for Value-Sensitive Decision-Making. PLoS ONE, 8(9), e73216. https://doi.org/10.1371/journal.pone.0073216"
topics: ["collective-decision", "swarm-intelligence", "sync-consensus"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "138 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Dynamical-systems analysis of the honeybee stop-signal model, in which scout populations committed to two nest sites grow by discovery and waggle-dance recruitment, decay by abandonment, and suppress each other through cross-inhibition. Using timescale separation and bifurcation analysis the authors show the decision is value-sensitive: the cross-inhibition rate sets a value threshold above which deadlock between equal options breaks, sets a Weber-like just-noticeable difference, and tunes the speed-accuracy trade-off.

## Contribution

Extends the deterministic model introduced with the stop-signal experiments [[seeley-2012-stop]] by adding sensory noise and giving a full classification of its bifurcations (pitchfork, saddle-node, hysteresis; the cusp catastrophe in two parameters). It reframes collective choice as maximising the value of the chosen option rather than accuracy, which differs from the drift-diffusion optimality framing of [[marshall-2009-optimal]].

## Key results

- Equal options of value v: below a critical cross-inhibition sigma* the only attractor is deadlock; above it a pitchfork creates two decision attractors. With gamma = rho = v and alpha = 1/v the threshold is sigma* = 4 v^3 / (1 - v^2)^2 (formula as restated in [[reina-2017-model]] eq. 16), so higher-value pairs need less inhibition to break deadlock.
- For unequal options the minimum value difference needed for a unique attractor at the better option grows linearly with mean value, with slope set by cross-inhibition: an analogue of Weber's law (analytic plus numerical).
- Too much cross-inhibition is harmful: a saddle-node bifurcation creates an attractor for the inferior option, so accuracy can fall as inhibition rises.
- Hysteresis appears when the value difference is swept up and down (roughly between -0.5 and +0.5 in their units), which they propose as a diagnostic for this circuit in other systems.
- Stochastic simulations show a speed-accuracy trade-off qualitatively like the drift-diffusion model, but they present evidence that the reduced dynamics are not statistically optimal.
- Three-option simulation: two equal poor sites stay deadlocked until a third better site is discovered and then chosen.

## Methods and models

Mean-field ODEs with Wiener noise for scout fractions Psi_A, Psi_B committed to two sites and Psi_U uncommitted: discovery gamma_i Psi_U, abandonment alpha_i Psi_i, recruitment rho_i Psi_U Psi_i, cross-inhibition sigma Psi_A Psi_B, with rates tied to site value (gamma = rho = v, alpha = 1/v; noise only on value-dependent rates). A decision is a population crossing a quorum threshold. Analysis by singular perturbation (fast convergence to a one-dimensional slow manifold), bifurcation diagrams and stochastic simulation. Matlab simulation code is in the paper's supplementary file S1 (no public repository).

## Limitations and open questions

Infinite-population model: noise is sensory noise only; intrinsic finite-size noise would need a master-equation treatment, which the authors leave out. Analysis is for two options (the N > 2 failure of this parameterisation is shown later in [[reina-2017-model]]). Parameter values are not fitted to swarm data, and the speed-accuracy analysis is described by the authors as preliminary.

## Relevance to us

This model is the reference minimal circuit for value-sensitive collective choice and has been implemented on robots [[reina-2015-design]], [[talamali-2021-when]] and kilobots [[march-pons-2024-honeybee]], and generalised by control theorists [[gray-2018-multiagent]], [[leonard-2024-fast]]. A hackathon experiment can vary cross-inhibition and look for the predicted deadlock threshold, Weber law and hysteresis in a finite agent swarm. Compare the quorum view [[sumpter-2009-quorum]] and the neural-parallels argument [[marshall-2009-optimal]].
