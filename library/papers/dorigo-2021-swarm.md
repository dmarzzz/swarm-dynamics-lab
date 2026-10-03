---
id: dorigo-2021-swarm
type: paper
title: "Swarm Robotics: Past, Present, and Future [Point of View]"
authors: ["Marco Dorigo", "Guy Theraulaz", "Vito Trianni"]
year: 2021
venue: "Proceedings of the IEEE"
url: https://iridia.ulb.ac.be/~mdorigo/Published_papers/All_Dorigo_papers/DorTheTri2021pieee.pdf
doi: "10.1109/jproc.2021.3072740"
arxiv: null
cite: "Dorigo, M., Theraulaz, G., & Trianni, V. (2021). Swarm Robotics: Past, Present, and Future [Point of View]. Proceedings of the IEEE, 109(7), 1152–1165."
topics: ["swarm-robotics", "collective-decision", "criticality-measurement"]
added_by: dmarz/swarm-robotics-audit
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "399 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

A perspective by three of the field's founders on two decades of swarm robotics. They trace the history from
stigmergy experiments and the Swarm-bots and Swarmanoid projects to Kilobots and drone swarms, then state
four lessons: robot capabilities limit the tasks swarms can attempt; the micro-macro design problem (program
individuals, get a collective behaviour) is the hardest part; scalability and fault tolerance are not free
and must be designed; and biological inspiration helps but cannot by itself deliver application-specific
engineering. They then list new directions: miniaturisation, heterogeneity, decentralisation versus
hierarchy, swarms poised near phase transitions for adaptability, machine learning, security and human-swarm
interaction. They close with criteria for when a swarm is the right solution at all, and candidate
application domains (precision agriculture, inspection, defence, civil protection, space, entertainment,
nanomedicine).

## Contribution

The most-cited recent field-level perspective from the core European swarm-robotics community. It replaces
[[brambilla-2013-swarm]] as the starting map for open problems, and is the companion to the shorter
[[dorigo-2020-reflections]]. Its explicit statement that "no real-world application of swarm robotics
exists" (as of 2021) is a useful baseline claim for later application-oriented reviews such as
[[kegeleirs-2025-towards]].

## Key results

- Claim (bibliometric, Fig. 1): "swarm robotics" first appears in Google Scholar in 1991 and grows
  substantially only after about 2003; Scopus shows the same trend.
- Claim: Swarm-bots (2001-2005) used up to 20 self-assembling robots and remains "the only example of
  self-organized teams of robots that cooperate to solve a complex task, with the robots in the swarm taking
  different roles over time".
- Claim: ARGoS ([[pinciroli-2012-argos]]) can simulate up to 10 000 robots in real time; research with more
  than 30 e-pucks is complex and costly; they suggest a robot of about 5 cm diameter (between Kilobot and
  e-puck) as the sweet spot for lab swarms.
- Open problems stated: no design methodology gives performance guarantees; benchmarks with adjustable
  complexity (NASA Swarmathon-like) are missing; deep learning is barely used beyond evolved neural
  controllers; security (blockchain, Merkle trees; see [[strobel-2023-robot]]) is in its infancy.
- Section III-D proposes operating robot swarms near a phase transition, so that a few informed individuals
  can switch the collective state, as observed in midges, fish schools and sheep herds.

## Methods and models

A perspective paper with no new experiments. It includes a glossary (stigmergy, self-organisation,
scalability, phase transition, model-free and model-based learning) and draws on about 138 references.
Read in full from the authors' open PDF (CC BY-NC-ND licence).

## Limitations and open questions

A position piece from one research community (IRIDIA, CNRS Toulouse, ISTC-CNR). Robotic active matter and
physics-based swarms ([[li-2019-particle]], [[ben-zion-2023-morphological]]) get only a brief mention under
miniaturisation, and drone-swarm work outside Europe is covered thinly. Application sections are labelled
by the authors as speculative.

## Relevance to us

This is the best citation for "what the field thinks is open": the micro-macro problem, scalability by design,
and the suggestion to exploit near-critical collective states (linking to the criticality-measurement topic
and [[vasarhelyi-2018-optimized]]). Pair with [[hamann-2018-swarm]] for formal models,
[[mathews-2017-mergeable]] and [[zhu-2024-self]] for the decentralisation-versus-hierarchy question, and
[[kolling-2016-human]] for human-swarm interaction.
