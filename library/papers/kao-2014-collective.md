---
id: kao-2014-collective
type: paper
title: "Collective Learning and Optimal Consensus Decisions in Social Animal Groups"
authors: ["Albert B. Kao", "Noam Miller", "Colin Torney", "Andrew Hartnett", "Iain D. Couzin"]
year: 2014
venue: "PLoS Computational Biology"
url: "https://www.ebi.ac.uk/europepmc/webservices/rest/article/MED/25101642?resultType=core&format=json"
doi: "10.1371/journal.pcbi.1003762"
arxiv: null
cite: "Kao, A. B., Miller, N., Torney, C., Hartnett, A., & Couzin, I. D. (2014). Collective Learning and Optimal Consensus Decisions in Social Animal Groups. PLoS Computational Biology, 10(8), e1003762. https://doi.org/10.1371/journal.pcbi.1003762"
topics: ["collective-decision", "marl-emergence"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "107 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Models individuals that learn cue preferences while making consensus decisions as a group. Because consensus decouples each individual's preference from its experienced outcome, learning becomes coupled across group members; collective learners spontaneously detect correlations among members' cues, adjust strategy to group size without knowing it, and approach provably optimal decision accuracy.

## Contribution

Brings learning into collective decision models and connects to multi-agent learning; complements [[kao-2014-decision]].

## Key results

- Collectively learning groups achieve decision accuracy very close to the provable optimum across environments (simulation).
- Abstract-level reading only; numbers beyond the abstract were not checked.

## Methods and models

Agents learn cue preferences from the outcomes of decisions that are made by group consensus; simulation.

## Limitations and open questions

Simple cue environments; no data.

## Relevance to us

Link between collective decision and MARL; a candidate experiment for learned swarm policies. Related: [[miller-2013-both]].
