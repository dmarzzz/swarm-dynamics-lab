---
id: gal-2022-emergence
type: paper
title: "The emergence of a collective sensory response threshold in ant colonies"
authors: ["Asaf Gal", "Daniel J. C. Kronauer"]
year: 2022
venue: "Proceedings of the National Academy of Sciences"
url: https://doi.org/10.1073/pnas.2123076119
doi: "10.1073/pnas.2123076119"
arxiv: null
cite: "Gal, A., & Kronauer, D. J. C. (2022). The emergence of a collective sensory response threshold in ant colonies. Proceedings of the National Academy of Sciences, 119(23), e2123076119. https://doi.org/10.1073/pnas.2123076119"
topics: ["collective-decision", "criticality-measurement"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "37 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Colonies of the clonal raider ant Ooceraea biroi on a temperature-controlled arena collectively evacuate their nest when a 15-minute step increase in ground temperature is large enough. The probability of a full colony response follows a sigmoidal, psychometric-like curve with a threshold near 34 degrees C for 36-ant colonies, individual responses are strongly correlated, and the collective threshold rises with colony size. A two-stage binary (spin-like) network model with heterogeneous individual thresholds and excitatory versus inhibitory social interactions that scale differently with group size reproduces the size dependence.

## Contribution

Establishes a clean experimental paradigm for a group-level sensory threshold, and shows that the threshold is not an objective estimate of the stimulus (as wisdom-of-crowds pooling would predict) nor a detection limit that falls with group size, but a decision integrating the external stimulus with the colony's internal state (its size). It brings the excitation-inhibition logic of neural circuits, also central to [[seeley-2012-stop]] and [[pais-2013-mechanism]], into a measurable ant system.

## Key results

- Collectivity at 33 degrees C (3 colonies x 24 perturbations): bimodal colony response distributions and mean pairwise correlation of individual binary responses 0.424 (shuffle test P < 10^-5).
- At 40 degrees C: mean pairwise correlation 0.558 for response latency and 0.628 for response direction (both P < 10^-5).
- Threshold for a full response (at least 90 per cent of ants outside the nest for at least 30 s), 10 colonies of 36 workers plus 18 larvae: theta = 34.12 degrees C, 95 per cent CI 33.3 to 34.8 degrees C (logistic regression; 8 of 150 events excluded for not being settled).
- Colonies of 10 to 200 ants (3 replicates per size): larger colonies have significantly higher collective thresholds; robust to the quorum and duration used to define a response.
- Two timescales: a fast individual response (1 to 3 min) with colony state widely distributed around one half, then a social-feedback phase (5 to 10 min) that drives the colony to all-in or all-out.
- Model: separatrix m_c = J_r / (J_p + J_r); the threshold increases with N only if inhibition scales more strongly with N than excitation (alpha_r > alpha_p in h = N^alpha_p J_p m - N^alpha_r J_r (1 - m)). This scaling is a model inference, motivated by global pheromone versus saturating contact interactions, not measured.

## Methods and models

10 x 10 cm plaster-of-Paris arena on four thermoelectric zones under PID control, heated confining frame at 45 to 50 degrees C, closed-loop moisture control via image brightness; baseline 26 degrees C; 15-min perturbations every 2 h in random order between 29 and 43 degrees C. Age-matched clonal workers (line B, stock STC6) with larvae at 2:1; individual colour tags and tracking at 10 fps with anTraX (ref. 42 of the paper). Data, simulation code and analysis scripts: Zenodo https://doi.org/10.5281/zenodo.6569620. Model: P(sigma_i = 1) = 1 / (1 + exp(-beta h_i)), first stage h_i = T - theta_i with theta_i drawn from a normal distribution, second stage all-to-all social input; asynchronous simulation.

## Limitations and open questions

One species with an unusual queenless, clonal biology; the size-dependent threshold might be adaptive (larger colonies pay more to evacuate) but this is a hypothesis. The model ignores space and the identity of the excitatory and inhibitory signals is unknown. Only heat as stimulus.

## Relevance to us

A ready-made protocol for measuring a swarm-level threshold and its scaling with N in simulation or robots: perturb, record the fraction responding, fit a logistic curve, repeat across N. The two-timescale signature (individual then social) is a measurable prediction for any agent swarm. Related: [[sumpter-2009-quorum]], [[hartnett-2016-heterogeneous]], [[goldstein-2024-how]], [[chase-2025-physics]], [[kao-2014-decision]].

## Notes from dmarz/collective-decision-audit

Audited 2026-10-03: opened the full text and checked title, authors, year, venue, volume/pages (against Crossref) and every number in Key results against the paper. No errors found; read_depth full is consistent with the methods detail.
