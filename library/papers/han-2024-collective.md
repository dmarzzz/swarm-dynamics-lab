---
id: han-2024-collective
type: paper
title: "Collective relational inference for learning heterogeneous interactions"
authors: ["Zhichao Han", "Olga Fink", "David S. Kammer"]
year: 2024
venue: "Nature Communications"
url: https://www.nature.com/articles/s41467-024-47098-7
doi: "10.1038/s41467-024-47098-7"
arxiv: null
cite: "Han, Z., Fink, O., & Kammer, D. S. (2024). Collective relational inference for learning heterogeneous interactions. Nature Communications, 15(1), 3191."
topics: [collective-motion, criticality-measurement, meta]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: full
relevance: 3
citations: 6  # (Crossref is-referenced-by-count, 2026-10-03; OpenAlex daily budget exhausted for this IP)
code: []
---
## Summary

Collective Relational Inference (CRI) learns, from trajectories alone, which type of interaction acts on each edge of an interacting system and the force law for each type. Unlike Neural Relational Inference (NRI), which infers edge types independently with a VAE, CRI treats each node and its incoming edges as a subgraph and infers the joint distribution of edge types with a generalised EM algorithm (exact posterior over realisations in the E step, one gradient step on K edge networks in the M step). A variant, Evolving-CRI, handles neighbourhoods that change over time by updating each new edge's posterior while marginalising over co-incident edges. On spring and charge particle benchmarks CRI classifies edge types more accurately than NRI and MPM, learns physically consistent pairwise forces (with the PIG'N'PI decoder), and generalises from 5 to 10 particles with over 99% accuracy versus about 70% for baselines; Evolving-CRI is the only method that works on a 100-particle crystallisation system with distance-limited interactions.

## Contribution

A methodological step for inferring heterogeneous interaction rules (e.g. different follower or leader roles) from trajectory data when neighbourhoods change, which is the situation in moving animal groups. Not itself about animals.

## Key results

- Measured on benchmarks: CRI beats NRI on VAR causal discovery (including VAR-a and VAR-c where NRI fails) and on Netsim fMRI.
- Measured: higher edge-type accuracy and lower pairwise-force MAE than NRI-PIG'N'PI and MPM-PIG'N'PI across Spring N5K2, N10K2, N5K4 and Charge N5K2, especially with 100-1000 training simulations.
- Measured: generalisation N5K2 -> N10K2 above 99% (baselines about 70%).
- Measured: Evolving-CRI succeeds at interpolation and extrapolation on the LJ plus dipole crystallisation simulation where baselines fail.
- Limitation stated: exact E step costs O(N K^|Gamma|), so only sparse neighbourhoods are tractable; a variational version (Var-CRI) is offered.

## Methods and models

Directed graph; node state increment predicted by K edge networks (message passing GNN or PIG'N'PI with Newton's laws); Gaussian likelihood with fixed sigma^2; priors over subgraph realisations learned. Crystallisation: 100 particles, five nearest neighbours each, 10k downsampled steps. Assumes the number of interaction types K and the cutoff radius are known. PyTorch code: https://gitlab.ethz.ch/cmbm-public/toolboxes/cri ; data at ETH Research Collection.

## Limitations and open questions

Only simulated physical systems; no animal or robot trajectories. Requires known K and known neighbourhood definition, which are exactly what is uncertain in animal groups (metric vs topological vs visual). Interaction types fixed in time.

## Relevance to us

A candidate tool to infer heterogeneous roles (leaders, followers, different species) from swarm trajectories, e.g. on datasets like those in [[jadhav-2024-collective]] or [[waldmann-2024-3d]]. Compare with [[gao-2024-learning]] (stochastic equations from bird flocks) and [[hem-2025-learning]] (stochastic force inference on colloids).
