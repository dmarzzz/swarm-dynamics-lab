---
id: heins-2024-collective
type: paper
title: "Collective behavior from surprise minimization"
authors: ["Conor Heins", "Beren Millidge", "Lancelot Da Costa", "Richard P. Mann", "Karl J. Friston", "Iain D. Couzin"]
year: 2024
venue: "Proceedings of the National Academy of Sciences"
url: https://arxiv.org/html/2307.14804
doi: "10.1073/pnas.2320239121"
arxiv: "2307.14804"
cite: "Heins, C., Millidge, B., Da Costa, L., Mann, R. P., Friston, K. J., & Couzin, I. D. (2024). Collective behavior from surprise minimization. Proceedings of the National Academy of Sciences, 121(17), e2320239121."
topics: [collective-motion, collective-decision]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "55 (OpenAlex W4394874494, 2026-10-03)"
code: []
---
## Summary

Agents are modelled as active-inference (free-energy minimising) Bayesian filters rather than self-propelled particles with social forces. Each agent tracks a hidden state, the average distance to neighbours in each of several visual sectors, with a generative model whose drift relaxes that distance to a preferred value, and it changes its heading by gradient descent on variational free energy. The resulting action update is a precision-weighted sum of prediction errors times sector vectors pointing at the neighbours, which reproduces attraction and repulsion (sign set by whether the sensed distance is larger or smaller than expected) without explicit rules; alignment can be derived if the agent also models the angle to neighbours. Simulations show polarised, milling and disordered states controlled by the agents' beliefs about sensory noise (precision and smoothness), reproduce the Couzin et al. 2005 informed-minority result, and show that letting agents learn the smoothness parameter online makes groups respond more strongly and more proportionally to perturbations.

## Contribution

Gives a principled, inference-based account of social forces, where interaction weights become precisions with a probabilistic meaning, and proposes fitting generative models to tracking data ("computational phenotyping") instead of fitting force maps. A conceptual bridge between neuroscience-style models and collective motion.

## Key results

- Claimed/derived: social forces are free-energy gradients; the switch from attraction to repulsion happens where the prediction error changes sign (at the preferred distance x*).
- Simulation: increasing sensory precision amplitude or smoothness moves groups from polarised to milling; milling is stable over a wide parameter range, unlike the classic three-zone model; too high or too low precision fragments groups.
- Simulation: collective accuracy to reach a target rises with the informed fraction and is maximised at intermediate social precision (and intermediate target precision).
- Simulation: online learning of sensory smoothness increases group turning response to a perturbation of 1-25 of 50 agents and its dynamic range.

## Methods and models

Generalised filtering in generalised coordinates of motion (3 orders for hidden states, 2 for observations), Laplace-approximated free energy, sector-wise distance observations within an interaction radius, Euler-Maruyama integration of positions. Derivations in SI Appendices A-E. Code (JAX and Julia): https://github.com/conorheins/collective_motion_actinf .

## Limitations and open questions

Pure simulation; no fitting to real trajectories yet (the model inversion is proposed as future work). Many parameters (precisions, smoothness, sector geometry) with unclear biological counterparts. Speed is constant and only heading is controlled. The perturbation and accuracy results are qualitative matches to earlier SPP results rather than new empirical predictions.

## Relevance to us

A candidate "cognitive agent" baseline that could be compared head to head with SPP rules on real data. Related cognitive-model papers: [[salahshour-2025-allocentric]] (ring attractors), [[sayin-2025-behavioral]] (locusts do not align). Related method critique: [[gao-2024-learning]] (data-driven inference recovers a Vicsek-like law for pigeons).

## Notes from dmarz/collective-motion-recent-audit

Audited against arxiv.org/html/2307.14804: N = 50 agents, informed-fraction accuracy result and online learning of sensory smoothness confirmed; cite (121(17), e2320239121) confirmed. No corrections. citations replaced with the OpenAlex cited_by_count (2026-10-03) in place of the Crossref count.
