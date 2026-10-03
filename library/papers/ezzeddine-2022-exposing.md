---
id: ezzeddine-2022-exposing
type: paper
title: 'Exposing Influence Campaigns in the Age of LLMs: A Behavioral-Based AI Approach to Detecting State-Sponsored Trolls'
authors:
- Fatima Ezzeddine
- Luca Luceri
- Omran Ayoub
- Ihab Sbeity
- Gianluca Nogara
- Emilio Ferrara
- Silvia Giordano
year: 2022
venue: EPJ Data Science
url: https://arxiv.org/abs/2210.08786
doi: 10.1140/epjds/s13688-023-00423-4
arxiv: '2210.08786'
cite: 'Ezzeddine, F., Ayoub, O., Giordano, S., Nogara, G., Sbeity, I., Ferrara, E., & Luceri, L. (2023). Exposing influence campaigns in the age of LLMs: a behavioral-based AI approach to detecting state-sponsored trolls. EPJ Data Science, 12, 46. https://doi.org/10.1140/epjds/s13688-023-00423-4'
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 19 (Crossref, 2026-10-03)
code: []
---

## Summary

Detects state-sponsored troll accounts from behaviour alone: an LSTM classifies sequences of an account's sharing actions and the feedback they receive, and a 'Troll Score' aggregates classified sequences per account. No text is used, on the argument that LLMs can mimic language but not easily these behavioural sequences. On the 2016 Russian IRA campaign it reaches AUC near 99% on sequences and 91% on accounts.

## Contribution

An explicitly text-free detector motivated by LLM content mimicry.

## Key results

- Sequence-level AUC close to 99%; account-level troll versus organic AUC 91% (abstract).
- Promising generalisation to other information operations (abstract).

## Methods and models

LSTM over action-feedback sequences; Troll Score. Abstract-level read.

## Limitations and open questions

Trained on a pre-LLM human troll farm; an LLM agent could also randomise behaviour, which is untested.

## Relevance to us

Behavioural-sequence modelling is a natural fit for agent swarms whose action loops may be stereotyped. Compare metadata-only [[katyal-2026-account]].
