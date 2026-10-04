---
id: tan-2023-botpercent
type: paper
title: 'BotPercent: Estimating Bot Populations in Twitter Communities'
authors:
- Zhaoxuan Tan
- Shangbin Feng
- Melanie Sclar
- Herun Wan
- Minnan Luo
- Yejin Choi
- Yulia Tsvetkov
year: 2023
venue: 'Findings of the Association for Computational Linguistics: EMNLP 2023'
url: https://arxiv.org/abs/2302.00381
doi: 10.18653/v1/2023.findings-emnlp.954
arxiv: '2302.00381'
cite: 'Tan, Z., Feng, S., Sclar, M., Wan, H., Luo, M., Choi, Y., & Tsvetkov, Y. (2023). BotPercent: Estimating Bot Populations in Twitter Communities. In Findings of the Association for Computational Linguistics: EMNLP 2023, pp. 14295-14312. https://doi.org/10.18653/v1/2023.findings-emnlp.954'
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 16 (Crossref, 2026-10-03)
code: []
---

## Summary

Reframes bot detection as estimating the fraction of bots in a community rather than labelling individual accounts. BotPercent combines several bot datasets and feature-, text- and graph-based detectors with confidence calibration across models, and the authors report it gives less biased community-level estimates under balanced and imbalanced settings. Applied to partisan-news audiences and political communities, it finds bot rates vary a lot across space and time.

## Contribution

Treats prevalence estimation as its own calibrated task, which is the right target for 'how many agents are in this swarm' questions.

## Key results

- Community-level estimation with cross-model confidence calibration; state-of-the-art on community-level benchmarks in their tests (abstract).
- Bot presence is heterogeneous across communities and over time (abstract).

## Methods and models

Ensemble of feature, text and graph detectors trained on amalgamated TwiBot and Botometer-repository datasets, calibrated per community. Code: github.com/TamSiuhin/BotPercent (not opened). Abstract-level read.

## Limitations and open questions

Still inherits the training-label issues documented by [[hays-2023-simplistic]]; calibration helps only if the target community resembles the calibration data.

## Relevance to us

Closest existing method to a calibrated 'swarm share' estimator for a population. Same group as [[feng-2024-what]]; uses [[data-twibot22-2022]]. Contrast the threshold-counting critique in [[gallwitz-2022-investigating]].
