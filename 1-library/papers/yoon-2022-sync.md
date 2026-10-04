---
id: yoon-2022-sync
type: paper
title: "Sync and Swarm: Solvable Model of Nonidentical Swarmalators"
authors: [S. Yoon, K. P. O'Keeffe, J. F. F. Mendes, A. V. Goltsev]
year: 2022
venue: Physical Review Letters
url: https://arxiv.org/abs/2203.10191
doi: 10.1103/physrevlett.129.208002
arxiv: '2203.10191'
cite: "Yoon, S., O'Keeffe, K. P., Mendes, J. F. F., & Goltsev, A. V. (2022). Sync and swarm: Solvable model of nonidentical swarmalators. Physical Review Letters, 129(20), 208002."
topics: [sync-consensus, active-matter, collective-motion]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "64 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Solves exactly the order parameters of a 1D swarmalator model with heterogeneous natural velocities and
frequencies. Swarmalators live on a ring (position x_i) and carry a phase theta_i:
dx_i/dt = v_i + (J/N) sum_j sin(x_j - x_i) cos(theta_j - theta_i), dtheta_i/dt = omega_i + (K/N) sum_j sin(theta_j - theta_i) cos(x_j - x_i),
with v_i and omega_i Lorentzian. In sum/difference coordinates zeta = x + theta, eta = x - theta the model becomes two
linearly coupled Kuramoto models, and a "toroidal" Ott-Antonsen ansatz (a product of two Poisson kernels) closes
the dynamics. Four states appear (async, phase wave, mixed, sync); the authors derive the phase-wave and sync
order parameters in closed form and find a tetracritical point where all four meet.

## Contribution

First exact, Kuramoto-style solution for a population of mobile oscillators with disorder: it carries the
Ott-Antonsen technique [[ott-2008-low]] from fixed oscillators to swarmalators. It turned the swarmalator
field from mostly numerical phenomenology ([[okeeffe-2017-oscillators]]) into a solvable toy model of active
matter, and it is the template for the later 1D papers (forcing, delays, higher-order coupling
[[anwar-2024-collective]], global stability [[okeeffe-2025-global]]).

## Key results

- New order parameters W_+/- = (1/N) sum_j exp(i(x_j +/- theta_j)) = S_+/- exp(i Phi_+/-) measure space-phase order.
  States: async (0,0); phase wave (S,0) or (0,S); mixed (S1,S2) with S1 != S2; sync (S,S) (Figs. 1-2).
- Async loses stability at J_+ = (J+K)/2 = 2(Delta_v + Delta_omega) (eq. 14/20).
- Phase wave: S_+ = sqrt(1 - 2(Delta_v + Delta_omega)/J_+) (eq. 19), the same square-root form as Kuramoto's
  partially locked state.
- Sync: S_+/- = sqrt(1 - 2 Delta_tilde) with Delta_tilde = Delta_v/J + Delta_omega/K; onset at 2(Delta_v/J + Delta_omega/K) = 1 (eqs 22-23).
- The two critical curves meet at J = K = 2(Delta_v + Delta_omega), a tetracritical point; along J = K sync bifurcates
  directly from async, otherwise via the mixed state.
- Measured agreement: theory matches simulations with N = 10^4, RK45, T = 200, averaged over 20 realisations
  (Figs. 2-3). The mixed-state order parameters and the microscopic derivation of sync were not obtained
  analytically (left to the Supplement or future work).
- "Hidden" transition at J = 0: positions drift freely, so the phase model becomes Kuramoto with random
  time-periodic couplings cos((v_j - v_i)t); the theory predicts locking of oscillators to their own
  drift frequency, a claim they describe as novel and untested experimentally.
- Simulations (Supplement) indicate a finite interaction cutoff does not qualitatively change the states.

## Methods and models

Analysis: continuity equation for the density f(v, omega, zeta, eta, t), a product of Poisson kernels with
parameters alpha, beta (eq. 9), residue integration over Lorentzian distributions, plus Kuramoto's
self-consistency argument as an independent microscopic check of S_+. Numerics: RK45 with adaptive step,
N = 10^4. Code: https://github.com/Khev/swarmalators/tree/master/1D/onring/non-identical (cited in the paper).

## Limitations and open questions

- Existence conditions only: stability of phase wave, mixed and sync states is not proved.
- 1D ring with all-to-all coupling; the 2D model of [[okeeffe-2017-oscillators]] remains unsolved.
- Lorentzian disorder is chosen for tractability; Gaussian or bounded distributions need other methods.
- Real-world matches (sperm and vinegar eels on quasi-1D rings, rotating colloids) are qualitative.

## Relevance to us

Gives exact formulas we can use to validate any swarmalator or "sync-plus-motion" simulation before adding
complications, and a clean phase diagram with four states to target in a robot or drone demo
([[barcis-2020-sandsbots]]). The (zeta, eta) trick, mapping a two-variable mobile oscillator onto coupled
Kuramoto models, is reusable for heading-plus-phase agents. Ties to [[okeeffe-2022-collective]] (identical
case) and to [[chandra-2019-continuous]] for higher-dimensional orientation sync.

## Notes from dmarz/sync-consensus-audit

Audit 2026-10-03: metadata, cite string and the key numbers in this entry re-checked against the full text
(arXiv PDF or the hosted PDF at the entry's url); no corrections needed and read_depth full is supported by the
detail in the entry.
