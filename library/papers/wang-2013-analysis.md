---
id: wang-2013-analysis
type: paper
title: "Analysis on perfect location spoofing attacks using beamforming"
authors: [Ting Wang, Yaling Yang]
year: 2013
venue: 2013 Proceedings IEEE INFOCOM, Turin, pp. 2778-2786
url: https://ieeexplore.ieee.org/document/6567087
doi: 10.1109/infcom.2013.6567087
arxiv: null
cite: "Wang, T., & Yang, Y. (2013). Analysis on perfect location spoofing attacks using beamforming. In 2013 Proceedings IEEE INFOCOM, pp. 2778-2786. IEEE. https://doi.org/10.1109/INFCOM.2013.6567087"
topics: [sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "27 (Crossref, 2026-10-03)"
code: []
---

## Summary

The attacker's-side answer to RSS-based location verification. Most work either detects location spoofing or designs robust localisation; this paper shows that in many deployments a "perfect location spoofing" (PLS) attack, in which a transmitter with a smart antenna array shapes its radiation pattern so that every anchor measures exactly the RSS it would see from a chosen fake position, remains undetectable even against robust localisers and detectors. PLS is formulated as a nonlinear feasibility problem in antenna-array pattern synthesis (find array weights producing the target gain toward each anchor given the attacker's real position); since the problem is intractable in general it is solved by semidefinite relaxation plus a heuristic local search. Simulations show the approach works and yield design advice for defenders, chiefly about anchor deployment (more anchors, placed to surround the attacker, make PLS infeasible). Abstract only (IEEE Xplore, paywalled; no OA copy via Unpaywall). The array sizes, anchor counts and feasibility regions reported in the simulations are not visible from the abstract; the first author's VT dissertation ("Wireless Network Physical Layer Security with Smart Antenna", 2013) expands on it.

## Contribution

Formalises when RSS-fingerprint location verification can be defeated exactly by beamforming, turning "signal strength is hard to forge" into a quantitative condition on attacker antenna count versus anchor geometry.

## Key results

- PLS feasibility cast as a pattern-synthesis problem, solved via SDR + local search.
- Simulation: perfect spoofing is feasible in many anchor layouts; anchor deployment is the defender's lever (abstract; numbers not visible).

## Methods and models

Smart antenna array model, RSS path-loss model at anchors, nonlinear feasibility program, semidefinite relaxation, heuristic search; simulation only.

## Limitations and open questions

Abstract-level read; assumes the attacker knows anchor positions and channel model; multipath-rich indoor channels and full CSI or AoA signatures (as in SecureArray) are harder to spoof than scalar RSS, which the abstract does not address.

## Relevance to us

Important caveat for the whole physical-layer identity family: scalar RSS fingerprints ([[sheng-2008-detecting]], [[yang-2013-detection]]) are forgeable by an adversary with an antenna array, so Sybil defences built on them need either richer signatures ([[liu-2014-practical]], [[xiong-2013-securearray]], [[gil-2015-guaranteeing]]) or anchor geometry the attacker cannot satisfy. The general lesson transfers: any behavioural fingerprint used to separate one operator's agents is only as strong as the cost of synthesising it. Taxonomy: [[urdaneta-2011-survey]] (its critique of network-characteristic defences).
