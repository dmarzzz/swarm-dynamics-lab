---
id: papageorgiou-2024-compromise
type: paper
title: "Compromise or choose: shared movement decisions in wild vulturine guineafowl"
authors: ["Danai Papageorgiou", "Brendah Nyaguthii", "Damien R. Farine"]
year: 2024
venue: "Communications Biology"
url: "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10787764/fullTextXML"
doi: "10.1038/s42003-024-05782-w"
arxiv: null
cite: "Papageorgiou, D., Nyaguthii, B., & Farine, D. R. (2024). Compromise or choose: shared movement decisions in wild vulturine guineafowl. Communications Biology, 7(1), 95. https://doi.org/10.1038/s42003-024-05782-w"
topics: ["collective-decision", "collective-motion"]
added_by: dmarz/collective-decision-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "29 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

High-resolution (1 Hz) GPS tracking of nearly all adults in two wild vulturine guineafowl groups in Kenya, analysed with the pull/anchor method of [[strandburg-peshkin-2015-shared]]. All individuals could initiate movements, but leadership is graded: males are followed more often, and dominance has no effect within sex. When two initiators pull in different directions, followers average the directions if the angle between them is small and pick one (the majority) if it is large, the compromise-to-choose transition predicted by the [[couzin-2005-effective]] model and seen in baboons.

## Contribution

First replication of the baboon compromise-or-choose result in a second, distantly related species in the wild, supporting the claim that a common mechanism governs movement decisions across taxa. It also separates sex from dominance as the source of influence.

## Key results

- 502,253 leader-follower dyadic cases from two groups; all members could pull others.
- In two-initiator events with one male and one female initiator, the male succeeded with probability 0.543 (group 1) and 0.553 (group 2), about a 10 per cent advantage; permutation tests show no dominance effect within sex.
- Two-initiator events were about 17 to 18 per cent of all events.
- Compromise-to-choose transition: group 1 from 78 to 130 degrees, group 2 at about 117 degrees, against 72 to 96 degrees in baboons.
- When choosing, followers go with the majority; reaching an 80 per cent follow probability needed a larger majority than in baboons (about a third of group 1, a quarter of group 2), suggesting coarser discrimination.

## Methods and models

Solar GPS tags recording 1 Hz every fourth day 06:00 to 19:00; dyadic pull/anchor classification from changes in inter-individual distance; permutation tests (1000) for dominance and sex effects; directional analysis of follower headings against the angle between two initiators; spatial clustering to count initiators per direction. Groups of 13 to 65 adults in the species.

## Limitations and open questions

Two groups only, with fewer data for group 2, so the transition angle and its group-size dependence are uncertain (the authors decline to test the predicted group-size effect). Initiation is inferred from movement, not intent.

## Relevance to us

Field numbers (transition angles, majority thresholds) to calibrate an informed-agent movement model like [[couzin-2005-effective]] or [[leonard-2012-decision]], and evidence for the geometry of decision bifurcations in [[sridhar-2021-geometry]]. Related: [[strandburg-peshkin-2015-shared]], [[sueur-2012-from]].
