---
id: gorsane-2022-towards
type: paper
title: "Towards a Standardised Performance Evaluation Protocol for Cooperative MARL"
authors: [Rihab Gorsane, Omayma Mahjoub, Ruan de Kock, Roland Dubb, Siddarth Singh, Arnu Pretorius]
year: 2022
venue: Advances in Neural Information Processing Systems 35 (NeurIPS 2022)
url: https://arxiv.org/abs/2209.10485
doi: null
arxiv: '2209.10485'
cite: "Gorsane, R., Mahjoub, O., de Kock, R., Dubb, R., Singh, S., & Pretorius, A. (2022). Towards a standardised performance evaluation protocol for cooperative MARL. In Advances in Neural Information Processing Systems 35 (NeurIPS 2022). arXiv:2209.10485."
topics: [marl-emergence, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

A meta-analysis of evaluation practice in 75 cooperative MARL papers published 2016-2022, finding that most papers evaluate on a single environment (usually SMAC or MPE), use few and unreported seeds, cherry-pick scenarios, report inconsistent metrics, and that reported QMIX results on the same SMAC maps drift across papers. Re-analysing the original SMAC experiments, they argue the community has overfit to SMAC, with most maps at or near 100% win rate by 2021. They propose a standard protocol: report IQM and optimality gap with 95% stratified bootstrap confidence intervals, fixed evaluation intervals and episode counts, multiple environments, and published raw data.

## Contribution

Transfers the single-agent RL evaluation-rigour literature (Henderson, Agarwal et al.) to cooperative MARL and supplies a concrete reporting checklist and annotated dataset of past papers.

## Key results

- 75 papers annotated; SMAC and MPE dominate environment use; most papers use one environment and a small subset of its scenarios.
- Roughly 40% of 2021 papers still lacked any ablation study.
- QMIX performance on the same SMAC map (e.g. MMM2) varies widely across papers (figure 2).
- Recommendation: mean with 95% CI per evaluation point; IQM and optimality gap with stratified bootstrap CIs across tasks; at least several independent runs reported.

## Methods and models

Manual annotation of evaluation methodology (environments, scenarios, seeds, metrics, aggregation, uncertainty reporting) in papers from NeurIPS, ICML, ICLR, AAMAS and others; re-analysis of public SMAC run data.

## Limitations and open questions

Restricted to cooperative MARL; competitive and mixed-motive settings are out of scope. Skimmed, not read in full.

## Relevance to us

Any swarm or Sybil experiment we run on an adopted environment should follow this reporting protocol from day one (seeds, IQM, bootstrap CIs, multiple environments). Pairs with [[ellis-2022-smacv2]] and [[papoudakis-2021-benchmarking]].
