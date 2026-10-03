---
id: waggoner-2012-evaluating
type: paper
title: 'Evaluating Resistance to False-Name Manipulations in Elections'
authors:
- 'Bo Waggoner'
- 'Lirong Xia'
- 'Vincent Conitzer'
year: 2012
venue: 'Proceedings of the AAAI Conference on Artificial Intelligence, 26(1)'
url: https://api.openalex.org/works/doi:10.1609/aaai.v26i1.8266
doi: 10.1609/aaai.v26i1.8266
arxiv: null
cite: 'Waggoner, B., Xia, L., & Conitzer, V. (2012). Evaluating Resistance to False-Name Manipulations in Elections. Proceedings of the AAAI Conference on Artificial Intelligence, 26(1), 1485-1491.'
topics:
- sybil-resistance
- collective-decision
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 'OpenAlex 2026-10-03: 11'
code: []
---

## Summary

When a designer cannot prevent false-name voting but can use limiting methods such as CAPTCHAs to shape how many identities voters obtain, the paper models each voter as drawing a number of identities independently from a distribution influenced by the limiting method. For two alternatives it gives a criterion to compare such distributions and proposes a statistical test for whether an observed election outcome is correct despite possible false-name manipulation.

## Contribution

A statistical, rather than incentive-based, approach to elections under partial Sybil control.

## Key results

- Criterion for comparing identity-count distributions induced by different false-name-limiting methods (abstract).
- A justified statistical test for evaluating the correctness of a two-alternative election outcome (abstract).

## Methods and models

Two alternatives, voters with i.i.d. identity counts, hypothesis testing.

## Limitations and open questions

Abstract-level read. Crossref dates the record 2021 because of the AAAI archive migration; volume 26 is the 2012 conference.

## Relevance to us

Majority votes among agents (for example ensembles voting on an answer) can be audited this way when each operator may run a random number of agents: the question becomes whether the margin exceeds what plausible Sybil counts could produce. Related: [[conitzer-2010-using]], [[buterin-2019-flexible]].
