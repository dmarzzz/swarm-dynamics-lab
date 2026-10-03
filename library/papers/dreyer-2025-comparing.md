---
id: dreyer-2025-comparing
type: paper
title: "Comparing cooperative geometric puzzle solving in ants versus humans"
authors: ["Tabea Dreyer", "Amir Haluts", "Amos Korman", "Nir Gov", "Ehud Fonio", "Ofer Feinerman"]
year: 2025
venue: "Proceedings of the National Academy of Sciences"
url: https://doi.org/10.1073/pnas.2414274121
doi: "10.1073/pnas.2414274121"
arxiv: null
cite: "Dreyer, T., Haluts, A., Korman, A., Gov, N., Fonio, E., & Feinerman, O. (2025). Comparing cooperative geometric puzzle solving in ants versus humans. Proceedings of the National Academy of Sciences, 122(1), e2414274121. https://doi.org/10.1073/pnas.2414274121"
topics: ["collective-decision", "swarm-intelligence", "crowds-and-traffic"]
added_by: dmarz/collective-decision-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "34 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Individuals and groups of longhorn crazy ants (Paratrechina longicornis) and of people were given the same scaled "piano-movers" puzzle: carry a T-shaped load through two narrow slits between three chambers. Ant performance improves with group size because large carrying groups have persistent motion that acts as a short-term collective memory (wall sliding until an opening is found). People solve it better than ants on average, but groups of people do not improve on individuals, and when talking and gestures are banned their performance drops as they fall back on the most obvious moves to reach consensus.

## Contribution

A rare direct cross-species, cross-scale comparison of collective against individual cognition on an identical task. It shows collective benefit depends on how simple the members are: simple agents scale, sophisticated agents need communication to avoid conflicting plans. Extends the cooperative-transport work of [[gelblum-2015-ant]] and [[feinerman-2017-individual]].

## Key results

- Ants: larger groups solve more efficiently (shorter normalised path lengths in configuration space); explained by higher persistence that yields thigmotactic wall sliding (experiment plus simulation).
- People: individuals beat ants on average, though the best ant groups beat the worst human solvers; human groups with full communication (medium n = 22, large n = 21 groups) did not improve on singles, and groups with restricted communication (masks and sunglasses, no speech or gestures; medium n = 28, large n = 20) performed worse.
- Restricted human groups behave more like ants, attempting the most obvious state transitions; with speech, a minority can steer the group to a non-obvious shortcut.

## Methods and models

Puzzle arena with three chambers; load configuration (x, y, theta) partitioned into discrete states for analysis; performance as cumulative distribution of solved attempts against path length and number of attempted state transitions. Ant simulation model based on earlier cooperative-transport models from the Feinerman and Gov groups. I skimmed the main text and did not open the SI; no code repository noted in what I read.

## Limitations and open questions

Single puzzle geometry; group sizes are limited for humans; ant and human groups are compared on different absolute scales. The cognitive interpretation (persistence as memory) is a model-based reading.

## Relevance to us

Strong motivation for a hackathon comparison of "simple" rule-based swarms against LLM-agent groups on the same coordination puzzle, with and without communication. Related: [[gelblum-2015-ant]], [[feinerman-2017-individual]], [[becker-2017-network]], [[tump-2024-cognitive]].
