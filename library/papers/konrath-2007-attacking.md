---
id: konrath-2007-attacking
type: paper
title: "Attacking a Swarm with a Band of Liars: evaluating the impact of attacks on BitTorrent"
authors: [Marlom A. Konrath, Marinho P. Barcellos, Rodrigo B. Mansilha]
year: 2007
venue: Seventh IEEE International Conference on Peer-to-Peer Computing (P2P 2007), Galway, pp. 37-44
url: https://ieeexplore.ieee.org/document/4343448
doi: 10.1109/p2p.2007.14
arxiv: null
cite: "Konrath, M. A., Barcellos, M. P., & Mansilha, R. B. (2007). Attacking a Swarm with a Band of Liars: evaluating the impact of attacks on BitTorrent. In Seventh IEEE International Conference on Peer-to-Peer Computing (P2P 2007), pp. 37-44. IEEE. https://doi.org/10.1109/P2P.2007.14"
topics: [sybil-resistance, swarm-detection]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "21 (Crossref, 2026-10-03)"
code: []
---

## Summary

Claims to be the first evaluation of attacks on BitTorrent whose only aim is to harm a swarm (as opposed to selfish free-riding). After presenting state diagrams of peer behaviour, the paper describes two attacks carried out by a band of "liars", peers that misreport piece availability (advertising pieces they do not have) and/or deliver corrupt data, and evaluates their impact on download completion in realistic swarm settings using a discrete-event simulator validated against experiments in a controlled testbed. The abstract reports that the findings "show the seriousness of the problem"; the number of liars, swarm sizes and slowdown figures are not in the abstract. The reference list (via Exa) cites Douceur's Sybil attack, Piatek et al.'s BitTyrant and Jun and Ahamad's free-riding analysis, placing it as the sabotage counterpart to the free-riding papers. Abstract only (IEEE Xplore returned 404 for the document page from this box; Crossref confirms venue and pages, abstract taken from the OpenAlex record via Exa).

## Contribution

Shifts BitTorrent threat analysis from selfishness to deliberate sabotage by coordinated lying peers, with a validated simulator for measuring swarm-level damage.

## Key results

- Two liar-based attacks defined and simulated; qualitative conclusion that modest numbers of coordinated liars noticeably degrade swarms (specific figures not visible).

## Methods and models

Discrete-event BitTorrent simulator validated against a controlled real deployment; attack scenarios with a fraction of malicious peers.

## Limitations and open questions

Abstract-level read; 2007 protocol; later BitTorrent clients added piece hashing and peer banning that blunt corrupt-data attacks. How the liar fraction maps onto identity cost (one attacker, many liar identities) is the Sybil link but is not spelled out in the abstract.

## Relevance to us

Early example of the question swarm-detection cares about from the defender's side: how much damage does a coordinated band of fake participants do to a cooperative population, and can the swarm tell? Belongs with the BitTorrent trio [[piatek-2007-incentives]], [[sirivianos-2007-free]], [[locher-2006-free]] and the defensive-Sybil simulation [[davis-2008-sybil]]. Root: [[douceur-2002-sybil]].
