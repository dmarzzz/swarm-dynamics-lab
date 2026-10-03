---
id: chechulin-2024-detection
title: 'From Detection to Dissection: Unraveling Bot Characteristics in the VKontakte
  Social Network'
authors:
- Andrey Chechulin
- Maxim Kolomeets
year: 2024
venue: 2024 16th International Conference on COMmunication Systems & NETworkS (COMSNETS),
  159-164
url: https://doi.org/10.1109/COMSNETS59351.2024.10427530
doi: 10.1109/COMSNETS59351.2024.10427530
arxiv: null
cite: 'Chechulin, A., & Kolomeets, M. (2024). From Detection to Dissection: Unraveling
  Bot Characteristics in the VKontakte Social Network. 2024 16th International Conference
  on COMmunication Systems & NETworkS (COMSNETS), 159-164. https://doi.org/10.1109/COMSNETS59351.2024.10427530.'
topics:
- swarm-detection
read_depth: abstract
relevance: 4
type: paper
added_by: shadow/sol-w1
accessed: '2026-10-03'
citations: null
code: []
---

## Summary

Chechulin and Kolomeets build a VKontakte bot-characterization dataset using controlled attacks on honeypot accounts. They study bot cost, quality, speed, and users' ability to distinguish bots, then apply conventional classifiers to graph, text, and statistical features. The abstract claims successful detection under class imbalance and identification of many bot networks, but supplies no numerical accuracy. Its focus extends from binary detection to forensic characterization of attackers' capabilities.

## Contribution

Pairs controlled collection of bot interactions with economic/behavioral characterization to inform countermeasure selection and botnet forensics.

## Key results

- Abstract claims effective detection on class-imbalanced data and identification of a majority of bot networks.
- No sample counts, precision/recall, or user-study effect sizes were accessible.
- Cost, quality, and speed are proposed characterization dimensions, not quantified here.

## Methods and models

Read the complete IEEE Xplore abstract and conference metadata via the DOI. Collection uses controlled attacks against honeypot accounts; a Turing-test-style assessment measures user discrimination. Classifiers use interaction-graph, text, and distributional features. Exact classifier types and purchase/collection procedure were not inspected. Conference dates are January 3-7, 2024, Bengaluru; full text required sign-in or purchase.

## Limitations and open questions

Honeypot-exposed bot services may not represent all organic or strategic bot populations. Accuracy language in the abstract is qualitative and should not become an invented number. Details of human testing, label ground truth, and evaluation splits require full text. No attack was performed or dataset/code run.

## Relevance to us

A non-Twitter platform example and a reminder to characterize operator resources alongside detection scores. Compare large descriptive Twitter aggregates in [[ng-2025-global]] and staged botnet collection in [[wicherski-2011-automated]].
