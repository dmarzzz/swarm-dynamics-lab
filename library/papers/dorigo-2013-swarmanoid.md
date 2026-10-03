---
id: dorigo-2013-swarmanoid
type: paper
title: "Swarmanoid: A Novel Concept for the Study of Heterogeneous Robotic Swarms"
authors: ["Marco Dorigo", "Dario Floreano", "Luca Maria Gambardella", "Francesco Mondada", "Stefano Nolfi", "Tarek Baaboura", "Mauro Birattari", "Michael Bonani", "Manuele Brambilla", "Arne Brutschy", "et al."]
year: 2013
venue: "IEEE Robotics & Automation Magazine"
url: https://doi.org/10.1109/mra.2013.2252996
doi: "10.1109/mra.2013.2252996"
arxiv: null
cite: "Dorigo, M., Floreano, D., Gambardella, L. M., Mondada, F., Nolfi, S., Baaboura, T., Birattari, M., Bonani, M., Brambilla, M., Brutschy, A., et al. (2013). Swarmanoid: A Novel Concept for the Study of Heterogeneous Robotic Swarms. IEEE Robotics & Automation Magazine, 20(4), 60–71."
topics: ["swarm-robotics"]
added_by: dmarz/swarm-robotics-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "415 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

Reports the Swarmanoid project (2006-2010), which argued that swarm robotics was held back by the insistence
on identical robots and built a heterogeneous swarm of three robot types: foot-bots (ground), hand-bots
(climbing and grasping) and eye-bots (flying, ceiling-attaching). According to [[dorigo-2021-swarm]], the
three types collaborated on a search-and-retrieval task. The paper has 37 authors.

## Contribution

The canonical heterogeneous-swarm demonstration and the source of the foot-bot and eye-bot platforms that
ARGoS ([[pinciroli-2012-argos]]) models.

## Key results

- Position argument (abstract): heterogeneity is needed for swarms to reach real-world complexity.
- Demonstration of a three-type heterogeneous swarm (details from [[dorigo-2021-swarm]]; the paper's own
  numbers were not checked).

## Methods and models

Hardware and system paper: three custom robot types with shared communication (not checked in detail).

## Limitations and open questions

Abstract-level entry; the full text (ULB repository) was not read in this session. Heterogeneity remains
under-studied, as [[dorigo-2021-swarm]] notes eight years later.

## Relevance to us

Cite for heterogeneous swarms. It fills the gap the scan noted, and pairs with
[[ferrante-2015-evolution]] on task specialisation and [[mathews-2017-mergeable]] on robots that physically
combine.
