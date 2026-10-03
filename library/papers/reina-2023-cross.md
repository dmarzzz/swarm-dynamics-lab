---
id: reina-2023-cross
type: paper
title: "Cross-inhibition leads to group consensus despite the presence of strongly opinionated minorities and asocial behaviour"
authors: ["Andreagiovanni Reina", "Raina Zakir", "Giulia De Masi", "Eliseo Ferrante"]
year: 2023
venue: "Communications Physics"
url: "https://www.nature.com/articles/s42005-023-01345-3"
doi: "10.1038/s42005-023-01345-3"
arxiv: null
cite: "Reina, A., Zakir, R., De Masi, G., & Ferrante, E. (2023). Cross-inhibition leads to group consensus despite the presence of strongly opinionated minorities and asocial behaviour. Communications Physics, 6(1), 236. https://doi.org/10.1038/s42005-023-01345-3"
topics: ["collective-decision", "swarm-robotics", "sync-consensus"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "22 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Compares cross-inhibition with the voter model (equal options) and the weighted voter model (options of different quality) when the population contains two inflexible, oppositely opinionated minorities (zealots) or individuals who sporadically switch opinion from private information (asocial behaviour). Mean-field models predict, and experiments with swarms of 100 locally interacting robots confirm, that only cross-inhibition reaches a stable majority despite substantial zealotry and asocial switching.

## Contribution

Proposes a functional answer to why inhibitory signals are widespread in natural collective decisions: robustness to stubborn minorities and noise. Extends [[seeley-2012-stop]] and [[pais-2013-mechanism]] to adversarial and noisy populations and complements the uninformed-individual result [[couzin-2011-uninformed]].

## Key results

- Voter and weighted voter models remain undecided under two competing zealot minorities or asocial switching; cross-inhibition reaches a stable majority (mean-field analysis).
- Predictions confirmed with 100 locally interacting robots (experiment; platform details not checked).
- Abstract-level reading only; numbers beyond the abstract were not checked.

## Methods and models

Mean-field ODE models of three opinion rules with zealot fractions and asocial switching rates; robot swarm experiments with 100 robots.

## Limitations and open questions

Abstract-level reading; robot platform and effect sizes not checked.

## Relevance to us

Directly relevant to adversarial robustness of swarms and of LLM agent collectives with stubborn agents. Related: [[zakir-2025-bio]], [[talamali-2021-when]], [[march-pons-2025-non]].
