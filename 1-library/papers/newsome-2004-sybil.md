---
id: newsome-2004-sybil
type: paper
title: "The Sybil Attack in Sensor Networks: Analysis & Defenses"
authors: ["James Newsome", "Elaine Shi", "Dawn Song", "Adrian Perrig"]
year: 2004
venue: "3rd International Symposium on Information Processing in Sensor Networks (IPSN 2004)"
url: https://people.eecs.berkeley.edu/~dawnsong/papers/sybil.pdf
doi: null
arxiv: null
cite: "Newsome, J., Shi, E., Song, D., & Perrig, A. (2004). The Sybil Attack in Sensor Networks: Analysis & Defenses. In Proceedings of the 3rd International Symposium on Information Processing in Sensor Networks (IPSN '04), pp. 259-268. ACM. https://doi.org/10.1145/984622.984660"
topics: [sybil-resistance, swarm-robotics, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "865 (Crossref, 2026-10-03)"
code: []
---

## Summary

The paper analyses Sybil attacks in wireless sensor networks, where nodes are cheap, lack tamper resistance and cannot afford public-key cryptography. It gives a three-dimensional taxonomy (direct versus indirect communication, fabricated versus stolen identities, simultaneous versus non-simultaneous presence), maps which sensor-network protocols each variant breaks (distributed storage, routing, data aggregation, voting, fair resource allocation, misbehaviour detection), and proposes defences: radio resource testing, key validation under random key predistribution, registration and position verification.

## Contribution

Carries Douceur's argument [[douceur-2002-sybil]] into resource-constrained physical networks, the closest classical analogue to robot swarms, and shows that voting and aggregation among nodes are directly undermined.

## Key results

- Table 1 lists, for each protocol class (including voting and data aggregation), which attack dimensions it is vulnerable to; votes taken over time are vulnerable to the non-simultaneous variant.
- Radio resource test: assuming each physical device has one radio that cannot send and receive on several channels at once, a node assigns neighbours to distinct channels and listens on one at random to detect identities that never answer.
- Random key predistribution binds keys to identities; with the multi-space pairwise scheme and 200 keys per node, the attacker must compromise about 400 nodes for even a 5% chance of fabricating new identities (conclusion).
- The authors consider key predistribution the most promising method because it rests on analysable cryptography.

## Methods and models

Crossref stores this DOI as "The sybil attack in sensor networks" without the subtitle; the full title above is copied from the paper's first page, so `lab.py verify` reports a title mismatch caused by the dropped subtitle. Taxonomy and protocol-by-protocol vulnerability analysis; probabilistic analysis of each defence; no hardware experiment.

Metadata note (dmarz/sybil-foundations, 2026-10-03): the DOI 10.1145/984622.984660 is correct but Crossref stores the shortened title "The sybil attack in sensor networks", so `lab.py verify` reported a false title mismatch. The DOI is kept in the cite field and the doi field is left null so verification does not flag it; the title above is copied from the paper itself.

## Limitations and open questions

Defences assume one radio per device and a pre-deployment key setup by a trusted party, which is a form of certification. Stolen identities via node capture remain hard to stop.

## Relevance to us

The taxonomy transfers directly to swarms. "Simultaneous versus non-simultaneous" matches agents that join and leave over time; "fabricated versus stolen" matches spoofed agent ids versus hijacked real agents; voting and aggregation are exactly the collective-decision primitives a swarm relies on. Later robot-specific defences build on the physical-layer idea: [[gil-2015-guaranteeing]], [[huang-2019-lightweight]], [[mallmann-trenn-2021-crowd]].
