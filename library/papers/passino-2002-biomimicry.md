---
id: passino-2002-biomimicry
type: paper
title: Biomimicry of bacterial foraging for distributed optimization and control
authors: [Kevin M. Passino]
year: 2002
venue: IEEE Control Systems Magazine
url: https://api.openalex.org/works/W2122122715
doi: 10.1109/MCS.2002.1004010
arxiv: null
cite: Passino, K. M. (2002). Biomimicry of bacterial foraging for distributed optimization and control. IEEE Control Systems Magazine, 22(3), 52–67. https://doi.org/10.1109/MCS.2002.1004010
topics: [swarm-intelligence, collective-decision]
added_by: dmarz/swarm-intelligence-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 3082 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Explains the biology and physics of E. coli chemotaxis (run-and-tumble foraging), bacterial swarming and social
foraging, and the cell's control system, then turns them into a distributed optimisation algorithm, bacterial
foraging optimisation (BFO). Demonstrates it on a simple multi-extremum function, relates it to existing optimisers,
and closes with ideas for adaptive and cooperative control of autonomous vehicles.

## Contribution

The founding paper of the bacterial-foraging family, one of the SI families the scan listed as uncatalogued. Unlike
PSO and ACO it comes from the control community and is grounded in a microscopic motility model (run-and-tumble),
the same model active-matter physics uses for bacteria, which makes it a natural bridge to active-matter-style
analysis.

## Key results

- Claimed (abstract): a program emulating social bacterial foraging that minimises a simple multiple-extremum
  function; qualitative relationship to other optimisers. No benchmark numbers in the abstract.

## Methods and models

Chemotaxis (run-and-tumble along a nutrient gradient) and social swarming behaviour turned into a distributed search
program; algorithmic details not read (abstract only, IEEE full text not accessed).

## Limitations and open questions

Unread beyond the abstract. As a metaphor-derived algorithm, BFO falls under the general critique of
[[sorensen-2015-metaheuristics]]; I did not check whether [[kudela-2023-evolutionary]] or
[[vermetten-2024-large]] include it.

## Relevance to us

Relevant if the hackathon studies source-seeking swarms: run-and-tumble plus social signalling is a physically
grounded swarm search, comparable with [[nitti-2025-collective]] (Langevin source seeking) and [[garnier-2007-biological]].
