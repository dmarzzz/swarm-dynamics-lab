---
id: nitti-2025-collective
type: paper
title: A collective intelligence model for swarm robotics applications
authors:
- Alessandro Nitti
- Marco D. de Tullio
- Ivan Federico
- Giuseppe Carbone
year: 2025
venue: Nature Communications
url: https://www.nature.com/articles/s41467-025-61985-7
doi: 10.1038/s41467-025-61985-7
arxiv: null
cite: Nitti, A., de Tullio, M. D., Federico, I., & Carbone, G. (2025). A collective intelligence model for swarm robotics applications. Nature Communications, 16(1), 6572. https://doi.org/10.1038/s41467-025-61985-7
topics:
- swarm-intelligence
- swarm-robotics
- sync-consensus
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: 20 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Proposes the Swarm Cooperation Model (SCM), an overdamped Langevin equation for M agents that combines a social
"conflict energy" gradient (consensus pull toward others), the gradient of the perceived fitness, and Gaussian noise
whose amplitude self-regulates from the swarm consensus C(t): a global factor sigma(t) is raised in steps when
consensus has stalled for a window tau, and an agent factor lambda_k is larger for low-fitness agents far from the
fitness-weighted centroid. Without memory of best positions, it works on both static and time-varying landscapes.
Against Matlab PSO and multistart interior-point (MIPA), it matches or beats success rate on 22 of 33 low-dimensional
cases with M <= 16 agents, at about ten times more function evaluations, and locates a drifting contaminant with 5
simulated AUVs in a realistic coastal current model.

## Contribution

A recent, high-visibility attempt to make swarm-intelligence optimisers usable as decentralised robot controllers by
merging metaheuristic search with consensus theory (Olfati-Saber style) and CBO ([[pinnau-2017-consensus]]), with
adaptive noise as the key mechanism. Sits between the optimisation literature and swarm robotics.

## Key results

- Measured (6 landscapes: Ackley, Rastrigin, Griewank, Schwefel, others and a fractal surface; 100 replications;
  success = centroid within 0.05 L of the optimum): SCM success >= PSO and MIPA on 22/33 cases with M <= 16 in 2-3 D.
- Measured: SCM needs about one order of magnitude more function evaluations; <FE> significantly higher on 24/33.
- Measured: Ackley 100% success in every dimension tested; worst case is Schwefel (deceptive envelope), where
  gradient-free PSO has an edge.
- Measured: PSO and MIPA success rise monotonically with M; SCM's does not always, which the authors attribute to
  the absence of best-known memory.
- Measured (simulated AUV swarm, 5 agents, 6 km box in the Gulf of Taranto, currents 0.05-0.2 m/s): 86% success over
  100 runs, mean search time 20.8 +/- 3.82 h, mean distance travelled 93.8 +/- 17.3 km per vehicle.
- Claimed: agents only need to exchange position, fitness and its gradient, compatible with acoustic telemetry.

## Methods and models

Dimensionless Langevin model dx = [social gradient + xi * fitness gradient] dt + mu_k(t) dW, with xi set to the
inverse swarm-averaged gradient norm; consensus C from distances to the fitness-weighted centroid; sigma(t) updated
by increments omega every tau if the integral consensus I(C, tau) is steady, capped and reset at sigma_max. Euler-
Maruyama integration (J dt = 0.1), omega = 0.2, sigma0 = 0.05, tau = 60 dt; initial positions from circle packing.
PSO baseline: Matlab particleswarm (inertia 0.4, self 2.4, social 1.3). AUV dynamics from Evans and Nahon models with
PD rudder control; currents from SHYFEM coastal model; passive scalar advection-diffusion with k_H = 0.2 m^2/s.
Code: https://github.com/AleNit/Swarm-Cooperation-Model

## Limitations and open questions

Only low-dimensional landscapes (the robotics use case); performance degrades with dimension. Requires (or
approximates by finite differences) the fitness gradient, which PSO does not. Comparisons are against one PSO
configuration and one gradient method; no CBO, CMA-ES or DE baselines. The AUV test is simulation only and assumes
all-to-all communication. Several hyper-parameters (omega, tau, sigma_max) remain.

## Relevance to us

Concrete template for a hackathon demo that couples a swarm optimiser to embodied agents searching a time-varying
field (source seeking). Its adaptive-noise-from-consensus rule is a measurable control knob. Related:
[[pinnau-2017-consensus]], [[garnier-2007-biological]], swarm-robotics surveys such as [[brambilla-2013-swarm]].
