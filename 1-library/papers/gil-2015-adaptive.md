---
id: gil-2015-adaptive
type: paper
title: "Adaptive communication in multi-robot systems using directionality of signal strength"
authors: [Stephanie Gil, Swarun Kumar, Dina Katabi, Daniela Rus]
year: 2015
venue: The International Journal of Robotics Research, vol. 34, no. 7, pp. 946-968
url: https://dspace.mit.edu/handle/1721.1/100520
doi: 10.1177/0278364914567793
arxiv: null
cite: "Gil, S., Kumar, S., Katabi, D., & Rus, D. (2015). Adaptive communication in multi-robot systems using directionality of signal strength. The International Journal of Robotics Research, 34(7), 946-968. https://doi.org/10.1177/0278364914567793"
topics: [swarm-robotics, sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "44 (Crossref, 2026-10-03)"
code: []
---

## Summary

Multi-robot communication-coverage paper: a fixed subset of robots act as mobile routers and must position themselves to serve the communication demands of the remaining client robots in dynamic environments with changing demands. The method builds, for each wireless link, a mapping from the robot's current position to the signal strength it receives along each spatial direction (a synthetic-aperture style directional profile obtained from the robot's own motion), and feeds that into a positional controller that keeps a quadratic structure while adapting to measured wireless conditions. The authors stress that the controller does not need stochastic sampling in counter-productive directions, exact client positions, or a map. Abstract only: the IJRR article is paywalled and the MIT DSpace open copy (CC BY-NC-SA) is behind a human-verification wall from this box, so figures, experimental platform, number of robots and quantitative coverage results were not seen.

## Contribution

Introduces the per-direction signal-strength profile ("spatial fingerprint" of a wireless link, obtained by moving the receiving robot) as a control input for multi-robot coordination; this same primitive is what the group later reuses to detect spoofed identities.

## Key results

- Directional signal-strength profiles can be measured with commodity radios and used in a quadratic positional controller for router placement (abstract; no numbers available).

## Methods and models

Synthetic aperture radar style angle-of-arrival estimation from robot motion over Wi-Fi; coverage-style controller for robotic routers; real-world wireless environments per the abstract. Details not read.

## Limitations and open questions

Abstract-level. Not a security paper; no adversary. Whether directional profiles are stable enough under multipath to serve as identity evidence is exactly the question the follow-up work had to answer.

## Relevance to us

Catalogued as the technical precursor to [[gil-2015-guaranteeing]] and [[gil-2018-resilient]], where the same directional Wi-Fi profiles become physical-layer Sybil detection for robot teams (one transmitter cannot fake many distinct spatial fingerprints). Useful for the sybil-resistance survey's "physical network characteristics" family, which [[urdaneta-2011-survey]] catalogues for P2P and which robotics operationalises here. Coverage-control lineage: [[schwager-2009-decentralized]].
