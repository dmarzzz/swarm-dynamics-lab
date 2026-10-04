---
id: sha-2026-stochastic
type: paper
title: 'Stochastic Dynamics of Human-Bot Interactions on Social Platforms: A Three-Population
  SDE Model'
authors:
- Zihan Sha
- Wenhao Cui
year: 2026
venue: 2026 International Conference on Generative Artificial Intelligence and Information
  Security (GAIIS)
url: https://doi.org/10.1109/gaiis69281.2026.11519274
doi: 10.1109/gaiis69281.2026.11519274
arxiv: null
cite: 'Zihan Sha; Wenhao Cui. (2026). Stochastic Dynamics of Human-Bot Interactions
  on Social Platforms: A Three-Population SDE Model. 2026 International Conference
  on Generative Artificial Intelligence and Information Security (GAIIS), 764-769.
  https://doi.org/10.1109/gaiis69281.2026.11519274'
topics:
- swarm-detection
- sync-consensus
added_by: shadow/sol-w7
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Sha and Cui model humans, bots, and detectors as interacting noisy populations rather than a static classification problem. Their abstract calibrates population proportions to TwiBot-22, then reports Monte Carlo outcomes for user attrition and detector tradeoffs. These are simulated futures under the model, not measured month-long losses on a deployed platform.

## Contribution

A stochastic three-population perspective coupling attack injection, human retention, and detector upkeep.

## Key results

- The abstract uses 860,057 humans and 139,943 bots from TwiBot-22 proportions and reports 1,000 Monte Carlo simulations.
- It reports an 11% simulated probability of losing one-third of humans within a month and 22% greater retention under balanced detector policies.
- The abstract claims its qualitative conclusions survive parameter changes of 20%; calibration uncertainty was not independently evaluated.

## Methods and models

Lotka-Volterra-style dynamics with multiplicative Itô noise. Humans leave under harassment, attackers inject bots, and detector effectiveness decays without upkeep. Abstract and beginning of introduction only; equations and solver details were not read.

## Limitations and open questions

Dataset class proportions do not validate causal transition rates or the time unit. Model-based percentages are not observed platform prevalence or attrition. Numerical methods, realistic false-positive costs, and empirical dynamical validation remain unchecked.

## Relevance to us

A possible baseline for population-level costs of bot control, rather than a detector of common operators or communication links. Compare [[zhang-2026-botevo]] for account classification.
