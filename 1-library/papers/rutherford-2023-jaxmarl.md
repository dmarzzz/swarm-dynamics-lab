---
id: rutherford-2023-jaxmarl
type: paper
title: "JaxMARL: Multi-Agent RL Environments and Algorithms in JAX"
authors: ["Alexander Rutherford", "Benjamin Ellis", "Matteo Gallici", "Jonathan Cook", "Andrei Lupu", "Gardar Ingvarsson", "Timon Willi", "Ravi Hammond", "Akbir Khan", "Christian Schroeder de Witt", "et al."]
year: 2023
venue: "arXiv preprint"
url: https://arxiv.org/abs/2311.10090
doi: null
arxiv: '2311.10090'
cite: "Rutherford, A., Ellis, B., Gallici, M., Cook, J., Lupu, A., Ingvarsson, G., Willi, T., Hammond, R., Khan, A., de Witt, C. S., et al. (2023). JaxMARL: Multi-agent RL environments and algorithms in JAX. arXiv:2311.10090."
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "82 (Semantic Scholar, 2026-10-03)"
code: [gh-bold-lab-ai-jaxmarl]
---

## Summary

Library combining GPU-accelerated JAX reimplementations of common MARL environments (including MPE, Overcooked, Hanabi, STORM, and SMAX, a JAX approximation of SMAC that drops the StarCraft II engine) with baseline algorithms. Training pipelines run end-to-end on accelerator.

## Contribution

The first broad JAX MARL environment suite with baselines; the API that later JAX worlds (Craftax-MA, alem) plug into.

## Key results

- JAX pipeline about 14x faster wall clock than existing approaches; up to 12,500x when many training runs are vectorised.
- Introduces SMAX as a GPU-native SMAC replacement.

## Methods and models

JAX environments with a shared multi-agent API; IPPO/MAPPO/QMIX-style baselines.

## Limitations and open questions

Abstract only. Paper catalogued here because the code entry existed without its paper.

## Relevance to us

Bootstrap: default substrate for fast MARL experiments; see [[gh-bold-lab-ai-jaxmarl]], [[gh-baselomari-ma-craftax]], [[tessera-2026-benchmarking]].
