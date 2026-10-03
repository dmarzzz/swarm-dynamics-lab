---
id: sargeant-2013-modelling
type: paper
title: "Modelling malicious entities in a robotic swarm"
authors: [Ian Sargeant, Allan Tomlinson]
year: 2013
venue: 2013 IEEE/AIAA 32nd Digital Avionics Systems Conference (DASC), East Syracuse, NY (session 7B1)
url: https://ieeexplore.ieee.org/document/6719716
doi: 10.1109/dasc.2013.6719716
arxiv: null
cite: "Sargeant, I., & Tomlinson, A. (2013). Modelling malicious entities in a robotic swarm. In 2013 IEEE/AIAA 32nd Digital Avionics Systems Conference (DASC). IEEE. https://doi.org/10.1109/DASC.2013.6719716"
topics: [swarm-robotics, sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "7 (Crossref, 2026-10-03)"
code: []
---

## Summary

Royal Holloway ISG follow-on to Higgins, Tomlinson and Martin's 2009 threat taxonomy ([[higgins-2009-threats]]), presented at an avionics venue because of UAV-swarm interest. The IEEE Xplore abstract is an outline: overview of a swarm, why swarm security matters, generic models for swarms, potential malicious attacks against a swarm, and current work on enhancing the models. The programme is to build formal generic models of a robotic swarm (entities, communication, emergent behaviour) in which malicious entities can be represented explicitly, so that attacks can be reasoned about rather than listed. The authors' later companion paper (Sargeant and Tomlinson, "Maliciously Manipulating a Robotic Swarm", ESCS 2016, which was readable) fills in the content of that programme: a hostile-environment assumption, swarm characteristics (autonomy, decentralisation, local sensing, emergence), an adversary who can plant malicious swarm entities or masquerade as legitimate ones to operate covertly, and a mapping of classic threats (masquerade, system penetration, authorisation violation, planting, eavesdropping, modification in transit, denial of service) onto swarm elements, noting that authorisation violation only arises if a group hierarchy exists in practice. Identity multiplication is implicit in the "planting malicious swarm entities" and "masquerade" threats rather than named as Sybil. Abstract only for the 2013 paper (IEEE paywalled); detail above is from the 2016 companion, not catalogued separately (no DOI, small venue).

## Contribution

Starts the formal-modelling branch of swarm-robotics security: represent the adversary as entities inside the swarm model so that masquerade and planting attacks can be analysed against emergent behaviour.

## Key results

- Conceptual: generic swarm model with explicit malicious entities; threat mapping (masquerade, planting, DoS, etc.) onto swarm elements (2016 companion).
- No experiments or quantitative results in either paper.

## Methods and models

Conceptual modelling and threat analysis in the style of the group's 2009 paper; no simulation.

## Limitations and open questions

Abstract-level read of the 2013 paper; conceptual only; the Sybil case (one adversary, many planted identities) is not analysed quantitatively, and the models were never, as far as the library knows, instantiated in simulation by these authors.

## Relevance to us

Bridges the 2009 taxonomy to later quantitative swarm-security work; mainly a citation to show that "planting many malicious entities" has been recognised as the core swarm threat since the early 2010s. Quantitative successors: [[gil-2015-guaranteeing]], [[renganathan-2022-spoof]], [[strobel-2018-managing]]; broader survey [[neupane-2024-security]]. Root: [[douceur-2002-sybil]].
