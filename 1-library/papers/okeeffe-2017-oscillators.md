---
id: okeeffe-2017-oscillators
type: paper
title: Oscillators that sync and swarm
authors: [Kevin P. O'Keeffe, Hyunsuk Hong, Steven H. Strogatz]
year: 2017
venue: Nature Communications
url: https://arxiv.org/abs/1701.05670
doi: 10.1038/s41467-017-01190-3
arxiv: '1701.05670'
cite: "O'Keeffe, K. P., Hong, H., & Strogatz, S. H. (2017). Oscillators that sync and swarm. Nature Communications, 8(1), 1504."
topics: [sync-consensus, collective-motion, active-matter]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "372 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

The paper that founded the swarmalator field. Studies of synchronisation treat oscillators that do not move;
studies of swarming treat agents whose internal state does not matter. The authors couple the two: each agent
has a position x_i in the plane and a phase theta_i, spatial attraction is modulated by phase similarity and
phase coupling is modulated by distance. A minimal instance (power-law kernels, Kuramoto sine coupling) with
two parameters (J for phase-dependent attraction, K for phase coupling) settles into five collective states:
static sync, static async, static phase wave, splintered phase wave and active phase wave. They compute the
radii of the stationary states analytically for a linear attraction kernel, locate the async instability
numerically (K_c roughly -1.2 J), and show the states survive noise, frequency disorder, 3D motion and
Vicsek-style alignment.

## Contribution

Defines "swarmalators" (agents whose spatial and phase dynamics are bidirectionally coupled) and supplies the
reference model that almost every later paper in this subfield modifies. Earlier mobile-oscillator work
(Frasca 2008, Fujiwara 2011, Uriu 2013) let position affect phase but not the reverse; Tanaka's chemotactic
oscillators (2007) and Igoshin's myxobacteria model (2001) had two-way coupling but were system-specific. This
paper gives the minimal, generic version and a vocabulary (static/active/splintered phase waves) that the
later solvable 1D models [[okeeffe-2022-collective]], [[yoon-2022-sync]] and reviews [[sar-2022-dynamics]],
[[sar-2026-interplay]] build on.

## Key results

- Model (eqs 3-4): dx_i/dt = v_i + (1/N) sum_j [ (x_j-x_i)/|x_j-x_i| (A + J cos(theta_j-theta_i)) - B (x_j-x_i)/|x_j-x_i|^2 ];
  dtheta_i/dt = omega_i + (K/N) sum_j sin(theta_j-theta_i)/|x_j-x_i|. With identical units, A=B=1, the system has two
  parameters (J in [-1,1], K).
- Five states found numerically in the (J,K) plane (Fig. 1, N=1000, dt=0.1): static sync for K>0 (all J);
  static async for K<0 and J below a wedge; static phase wave at K=0, J>0; splintered phase wave just below K=0
  (disconnected clusters that "quiver"); active phase wave for more negative K (counter-rotating shear flow,
  similar to double milling in swarms and sperm vortex arrays).
- Analytic (linear attraction kernel, measured against simulation in Fig. 3): R_sync = (1+J)^(-1/2) in 2D and
  (1+J)^(-1/3) in 3D; R_async = 1; static phase-wave annulus radii R_1, R_2 in closed form (eqs 10-11).
- Order parameters: W_plus/minus = S exp(i Psi) = (1/N) sum_j exp(i(phi_j +/- theta_j)), where phi is the spatial
  angle; S measures space-phase correlation. A second parameter gamma (fraction of agents completing a full
  cycle) separates splintered from active phase waves.
- Async instability: linearising the continuity equation, the critical mode is the first phase harmonic;
  numerics on the integral eigenproblem give K_c ~ -1.2 J (eq 18). The authors state openly that the sign of the
  leading eigenvalue below K_c could not be pinned down (values ~1e-6), so async is "weakly stable, neutral or
  weakly unstable"; they lean to weakly unstable. This is a numerical claim, not a proof.
- Robustness (simulated): phase noise kills the splintered state for D_theta above ~1e-3; Lorentzian frequency
  disorder turns phase waves into active phase waves and async into "active async"; more disorder shifts K_c
  toward zero (Fig. 8, N=500, 10 realisations). Adding Vicsek alignment with noise D_beta produces mobile
  (translating) versions of the same states (Fig. 10, N=300).

## Methods and models

ODE simulations with scipy odeint and Heun's method, N = 300 to 1000, dt 0.01 to 0.1, T up to 5000, initial
positions uniform in a box of side 2 and phases uniform in [-pi, pi]. Continuum (density) description
rho(x, theta, t) with stationary solutions derived following Fetecau/Kolokolnikov aggregation-model techniques;
stability via Fourier expansion in theta and in spatial angle, eigenvalues from Gaussian quadrature with up to
1600 grid points. Supplementary notes cover other kernels (a linear attraction kernel gives extra
"non-stationary phase waves"), 1D and 3D motion. The authors' later swarmalator code is public at
https://github.com/Khev/swarmalators (referenced in [[yoon-2022-sync]]); not checked whether it includes this
paper's 2D scripts.

## Limitations and open questions

- No alignment-phase coupling: agents have no heading in the base model, so it describes aggregation plus
  sync, not flocking plus sync. The authors flag the full position-orientation-phase problem as the main open
  direction.
- Async stability is unresolved analytically.
- All-to-all coupling with 1/r weights; local coupling and chirality were added later by [[ceron-2023-diverse]].
- Real-world matches (magnetic colloid asters, sperm vortices, tree frogs) are qualitative analogies, not fits.
- Number of clusters in the splintered state is not explained.

## Relevance to us

Core reference for any hackathon project that couples an internal clock or phase to motion: drone light shows,
robot swarms that time-share a channel, or "rhythm-aware" flocking. It supplies an off-the-shelf model with
five known states and order parameters S and gamma that we can reuse as measurement tools. Robot
implementations exist ([[barcis-2020-sandsbots]]). Solvable 1D versions ([[okeeffe-2022-collective]],
[[yoon-2022-sync]], [[okeeffe-2025-global]]) give analytic baselines to test simulations against. Connects to
the Kuramoto literature ([[acebron-2005-kuramoto]], [[strogatz-2000-kuramoto]]) and to chiral active matter
([[levis-2019-activity]]).

## Notes from dmarz/sync-consensus-audit

Audit 2026-10-03: metadata, cite string and the key numbers in this entry re-checked against the full text
(arXiv PDF or the hosted PDF at the entry's url); no corrections needed and read_depth full is supported by the
detail in the entry.
