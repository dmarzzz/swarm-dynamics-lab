---
id: giroux-2024-unmasking
type: paper
title: 'Unmasking Social Bots: How Confident Are We?'
authors:
- James Giroux
- Gangani Ariyarathne
- Alexander C. Nwala
- Cristiano Fanelli
year: 2024
venue: EPJ Data Science
url: https://arxiv.org/abs/2407.13929
doi: 10.1140/epjds/s13688-025-00536-y
arxiv: '2407.13929'
cite: 'Giroux, J., Ariyarathne, G., Nwala, A. C., & Fanelli, C. (2025). Unmasking social bots: how confident are we? EPJ Data Science, 14(1). https://doi.org/10.1140/epjds/s13688-025-00536-y (preprint arXiv:2407.13929, 2024).'
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 1 (Crossref, 2026-10-03)
code: []
---

## Summary

Bot detectors disagree with each other and give no indication of how much to trust a label. The authors add account-level uncertainty quantification to bot detection, so that confident predictions can trigger interventions while uncertain ones prompt caution or more data collection.

## Contribution

Moves bot detection from point labels to calibrated per-account uncertainty, which is what a prevalence estimate needs.

## Key results

- Detectors often disagree on the same account (abstract).
- Proposes account-level uncertainty alongside the bot/human prediction.

## Methods and models

Bot classifiers with uncertainty quantification. Abstract-level read; method details not recorded.

## Limitations and open questions

Uncertainty is only as good as the training distribution; it does not fix label bias ([[hays-2023-simplistic]]).

## Relevance to us

Per-agent uncertainty is a prerequisite for honest swarm-size estimates. Related: [[tan-2023-botpercent]].
