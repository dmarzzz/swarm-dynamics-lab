---
id: johansson-2007-specification
type: paper
title: Specification of the social force pedestrian model by evolutionary adjustment to video tracking data
authors:
- Anders Johansson
- Dirk Helbing
- Pradyumn K. Shukla
year: 2007
venue: Advances in Complex Systems
url: https://arxiv.org/abs/0810.4587
doi: 10.1142/s0219525907001355
arxiv: '0810.4587'
cite: Johansson, A., Helbing, D., & Shukla, P. K. (2007). Specification of the social force pedestrian model by evolutionary adjustment to video tracking data. Advances in Complex Systems, 10(supp02), 271–288. https://doi.org/10.1142/s0219525907001355
topics:
- crowds-and-traffic
- collective-motion
- swarm-intelligence
added_by: dmarz/crowds-and-traffic-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: 422 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex budget exhausted)
code: []
---

## Summary

Calibrates the social force model ([[helbing-1995-social]]) directly against tracked pedestrian trajectories rather than against a fundamental diagram. Pedestrians filmed from above in Budapest (escalator area, shopping mall) and Stuttgart (a crossing experiment) are tracked automatically; for each pedestrian, a 1.5 s social-force simulation is run while all neighbours follow their real tracks, and an evolutionary algorithm searches for the force parameters that minimise the relative position error. Three force specifications are compared; an elliptical, velocity-dependent specification that treats both pedestrians symmetrically fits best.

## Contribution

One of the first trajectory-level calibrations of a microscopic crowd model, establishing the "replay neighbours, simulate one agent" fitness that later data-driven and learned crowd models reuse. It also introduced the "elliptical specification II" of the social force (relative-velocity-dependent ellipses), which is the variant most often used in practice. Sits between the qualitative 1995 model and data-inferred interaction laws such as [[karamouzas-2014-universal]].

## Key results

Measured fitness (negative mean relative distance error after 1.5 s; 0 is perfect):
- No interaction (constant-velocity extrapolation): −0.66.
- Circular force: A = 0.42 ± 0.26, B = 1.65 ± 1.01, anisotropy λ = 0.12 ± 0.07, fitness −0.60.
- Elliptical I (step-size ellipse, [[helbing-1995-social]]): A = 0.11 ± 0.01, B = 1.19 ± 0.45, λ = 0.16 ± 0.04, fitness −0.59.
- Elliptical II (relative-velocity ellipse): A = 0.04 ± 0.01, B = 3.22 ± 0.67, λ = 0.06 ± 0.04, fitness −0.39 (best). With isotropic forces (λ = 1) all specifications fit worse.
- Interpreted: the remaining gap from 0 mainly reflects heterogeneity of individual behaviour; strong front-back anisotropy (small λ) is required by the data.
- The calibrated model is then used for large-scale simulations of evacuations, pilgrimage (Hajj) and urban scenes (illustrative, not validated quantitatively in what I read).

## Methods and models

dv_α/dt = (v_α^0 e_α − v_α)/τ_α + Σ_β f_αβ + Σ_i f_αi + ξ_α, with f_αβ = w(φ_αβ) g(d_αβ), angular weight w = λ + (1 − λ)(1 + cos φ)/2, circular g = A exp[(R_α + R_β − d)/B] d̂, elliptical II semi-minor axis 2b = sqrt((|d| + |d − (v_β − v_α)Δt|)^2 − |(v_β − v_α)Δt|^2). Desired speed set to the maximum tracked speed, goal to the trajectory end point. Fitness averaged over the central 30% of relative errors to drop outliers; simple evolutionary algorithm over (A, B, λ). Head tracking by detecting round moving structures with perspective correction.

## Limitations and open questions

- Short 1.5 s horizon and moderate densities; calibration says little about dense or contact-dominated regimes.
- Large parameter uncertainty for some specifications (for example circular A ± 60%), so parameters are weakly identified.
- I read sections 1–3 and the parameter table; the simulation applications in section 4 were not checked.

## Relevance to us

A ready recipe for fitting any agent-based swarm model to tracked trajectories (robots, animals, humans): replay neighbours, simulate the focal agent, score short-horizon error, optimise. The comparison against a no-interaction baseline (−0.66) is a useful sanity check we should copy. Related: [[moussaid-2009-experimental]] (experiment-based calibration), [[korbmacher-2022-review]] (knowledge-based versus deep-learning prediction).
