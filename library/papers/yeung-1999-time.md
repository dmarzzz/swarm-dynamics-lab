---
id: yeung-1999-time
type: paper
title: Time Delay in the Kuramoto Model of Coupled Oscillators
authors: [M. K. Stephen Yeung, Steven H. Strogatz]
year: 1999
venue: Physical Review Letters
url: https://arxiv.org/abs/chao-dyn/9807030
doi: 10.1103/physrevlett.82.648
arxiv: chao-dyn/9807030
cite: "Yeung, M. K. S., & Strogatz, S. H. (1999). Time delay in the Kuramoto model of coupled oscillators. Physical Review Letters, 82(3), 648-651."
topics: [sync-consensus]
added_by: dmarz/sync-consensus-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "614 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Adds a uniform transmission delay tau (plus noise and a phase frustration alpha) to the mean-field Kuramoto model
and asks how synchronisation changes. Delay produces qualitatively new behaviour: bistability between
synchrony and incoherence (hence hysteresis), multiple coexisting synchronised states with different collective
frequencies, and unsteady states with time-dependent order parameter. For identical oscillators the authors
derive exact stability boundaries of both incoherence and uniformly rotating synchrony as functions of the
delay, and check them against simulations.

## Contribution

The standard reference for delayed coupling in phase-oscillator populations. It shows that a delay is not just a
small perturbation of [[strogatz-2000-kuramoto]]: it can forbid synchrony in whole bands of tau and create
multistability, which matters whenever coupling travels through sound, light, radio or a network stack.

## Key results

- Model: dtheta_i/dt = omega_i + xi_i(t) + (K/N) sum_j sin(theta_j(t - tau) - theta_i(t) - alpha), noise strength D.
- Incoherence: eigenvalues satisfy an exact transcendental equation; for identical oscillators with no noise,
  incoherence is neutrally stable exactly when K < omega_0 / (2m - 1) and (4m - 3) pi / (2 omega_0 - K) < tau <
  (4m - 1) pi / (2 omega_0 + K) for some positive integer m (eq. 4). Grey stability tongues in (tau, K) plane, Fig. 1,
  confirmed by simulation with N oscillators and step dt = tau/20 to t = 800 tau.
- Synchrony: uniformly rotating states theta = Omega t + beta require Omega = omega_0 - K sin(Omega tau) and are stable
  iff cos(Omega tau) > 0 (eqs. 5-6). For large K several stable synchronised frequencies coexist.
- Stable synchrony is impossible exactly in tongues half the height of the incoherence tongues (eq. 7); the
  exposed parts of the incoherence tongues are regions of bistability between sync and incoherence.
- Discussed applications: chirping crickets (sound-speed delays), coupled phase-locked loops and lasers.

## Methods and models

Fokker-Planck (continuity) description of the infinite-N limit, linearisation about incoherence, results of
Hayes and Pontryagin on roots of quasi-polynomials, self-consistency for rotating synchronous solutions;
numerical integration with predictor-corrector for delay equations. Read from the arXiv version (4 pages);
derivation details deferred to a longer paper not read.

## Limitations and open questions

- Exact results only for identical oscillators (delta-distributed frequencies); the non-identical case is
  treated numerically and qualitatively.
- A single uniform delay; distance-dependent delays (relevant to spatially extended swarms) are not treated.
- Stability of the unsteady, time-dependent-order-parameter states is not characterised.

## Relevance to us

Robot and drone swarms always have communication delay and update latency, and [[barcis-2020-sandsbots]] and
[[quinn-2025-decentralised]] report delay as a practical obstacle. This paper gives the closed-form "forbidden
delay" bands to check a swarm's sync controller against, and explains why a sync demo can be bistable and
history dependent. Pairs with [[mirollo-1990-synchronization]] (pulse coupling) and
[[werner-allen-2005-firefly]] (delay-tolerant pulse coupling on real radios).
