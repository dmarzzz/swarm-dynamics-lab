---
id: hein-2015-evolution
type: paper
title: "The evolution of distributed sensing and collective computation in animal populations"
authors: ["Andrew M Hein", "Sara Brin Rosenthal", "George I Hagstrom", "Andrew Berdahl", "Colin J Torney", "Iain D Couzin"]
year: 2015
venue: "eLife"
url: "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4755780/fullTextXML"
doi: "10.7554/elife.10955"
arxiv: null
cite: "Hein, A. M., Rosenthal, S. B., Hagstrom, G. I., Berdahl, A., Torney, C. J., & Couzin, I. D. (2015). The evolution of distributed sensing and collective computation in animal populations. eLife, 4, e10955. https://doi.org/10.7554/elife.10955"
topics: ["collective-decision", "collective-motion", "criticality-measurement", "active-matter"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "89 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Evolutionary agent-based model in which selfish individuals with golden-shiner-like social forces (short-range repulsion, longer-range attraction, no explicit alignment) and a speed response to a local scalar resource cue evolve their baseline speed, cue sensitivity and interaction range in dynamic resource landscapes. Populations evolve sociality, gain about five times the fitness of asocial populations, and settle at trait values that sit just above an abrupt, hysteretic transition between dispersed and cohesive collective states, which lets local groups track moving resource peaks.

## Contribution

Gives an evolutionary explanation for emergent collective sensing of the kind measured in fish by [[berdahl-2013-emergent]]: no individual senses gradients, but slowing in good regions makes neighbour density informative, and social gradient climbing exploits it. It is one of the clearest models where selection places a collective near a transition point, linking collective decision to the criticality literature.

## Key results

- Social populations reach mean fitness about 5 times higher, and coefficient of variation in fitness about 4 times lower, than asocial populations (simulation, N = 500, k = 25 neighbours).
- A single social mutant from the evolved population invades an asocial resident population.
- Collective states as a function of Psi: station-keeping (Psi < 0), cohesive (small Psi), dispersed (large Psi), with first-order-like hysteresis between about 1.6 and 2.95.
- Evolved baseline speed psi0 places populations just above the cohesive-dispersed transition across many environments; the location is predicted analytically from the interaction rules without reference to the environment.
- Social individuals accumulate on a peak at a rate that grows exponentially, N_s about kappa_s1 + exp(kappa_s2 t), versus a constant arrival rate for asocial individuals (analytic, matched to simulation).
- With fast resource depletion (100 individuals deplete a peak in about 5 steps) selection for sociality weakens.

## Methods and models

Equations: social force F_s = -grad sum over k nearest neighbours within l_max of [C_r exp(-d/l_r) - C_a exp(-d/l_a)]; environmental force F_a = [Psi(S(x)) - eta |v|^2] v/|v| with Psi = psi0 - psi1 S; m dv/dt = F_s + F_a plus small heading noise. Resource peaks drift as Brownian motion with drift. Fitness = mean resource experienced; fitness-proportional reproduction with mutation over about 1000-1500 generations. Continuum approximation and stability analysis in the appendix. Parameters C = 1.1, l = 0.13, gamma = 0.01. No code repository stated in the text read.

## Limitations and open questions

Behavioural rules are fixed in form (only three traits evolve); heading does not respond to the cue, by assumption from the shiner data. Results depend on resources not being depleted quickly. The phase-transition analogy is qualitative (hysteresis, nucleation times) and no critical exponents are measured. Not tested against field data beyond qualitative matches.

## Relevance to us

Directly relevant to any hackathon idea about swarms poised near transitions or about distributed sensing without gradient sensors. The model is simple enough to reimplement in a day. Pair with [[berdahl-2013-emergent]] (experiment), [[kao-2014-decision]] (group size and correlated cues), [[sridhar-2021-geometry]] (criticality in individual choice) and [[chase-2025-physics]] (review).
