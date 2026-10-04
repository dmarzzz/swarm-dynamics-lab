---
id: rauchfleisch-2020-false
type: paper
title: The False positive problem of automatic bot detection in social science research
authors:
- Adrian Rauchfleisch
- Jonas Kaiser
year: 2020
venue: PLOS ONE
url: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0241045
doi: 10.1371/journal.pone.0241045
arxiv: null
cite: Rauchfleisch, A., & Kaiser, J. (2020). The False positive problem of automatic bot detection in social science research. PLOS ONE, 15(10), e0241045. https://doi.org/10.1371/journal.pone.0241045
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 134 (Crossref, 2026-10-03)
code: []
---

## Summary

The authors collected Botometer scores repeatedly over three months for five datasets of verified bots and verified humans (n = 4,134) in English and German. Scores were imprecise, worse in German, and drifted over time, so any fixed threshold produced both false positives and false negatives; they conclude that social-science studies using the tool will miscount humans as bots and vice versa.

## Contribution

Early systematic evidence that a widely used public bot detector is unreliable for prevalence estimates, especially outside English and across time.

## Key results

- n = 4,134 accounts in five labelled datasets (three bot, two human), English and German, scored repeatedly over three months.
- Thresholds, even conservative ones, varied enough over time to flip classifications in both directions (abstract).
- Performance was notably worse on German-language accounts (abstract).

## Methods and models

Repeated Botometer API queries on accounts of known type; analysis of score distributions and threshold stability over time. Read at abstract level only.

## Limitations and open questions

Abstract only; exact error rates not recorded here. Some test accounts may have been in Botometer's training data. The tool and the API have since changed.

## Relevance to us

Score drift over time is a property any deployed agent-swarm detector will share; a measurement campaign needs repeated scoring and a stated threshold. Cited by and extended in [[gallwitz-2022-investigating]]; counter-arguments in [[cresci-2023-demystifying]].
