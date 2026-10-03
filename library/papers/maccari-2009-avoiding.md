---
id: maccari-2009-avoiding
type: paper
title: "Avoiding Eclipse Attacks on Kad/Kademlia: An Identity Based Approach"
authors: [Leonardo Maccari, Matteo Rosi, Romano Fantacci, Luigi Chisci, Luca Maria Aiello, Marco Milanesio]
year: 2009
venue: 2009 IEEE International Conference on Communications (ICC 2009), Dresden, pp. 1-5
url: https://www.dais.unive.it/~maccari/files/bibliography/Fantacci2009Avoiding.pdf
doi: 10.1109/icc.2009.5198772
arxiv: null
cite: "Maccari, L., Rosi, M., Fantacci, R., Chisci, L., Aiello, L. M., & Milanesio, M. (2009). Avoiding Eclipse Attacks on Kad/Kademlia: An Identity Based Approach. In 2009 IEEE International Conference on Communications (ICC 2009), pp. 1-5. IEEE. https://doi.org/10.1109/ICC.2009.5198772"
topics: [sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "12 (Crossref, 2026-10-03)"
code: []
---

## Summary

Author order on the paper is Maccari, Rosi, Fantacci, Chisci, Aiello, Milanesio (Crossref lists Fantacci first). Two parts. First, an OMNeT++ simulation study of eclipse attacks on a single-layer Kad network reproducing Steiner et al.: when the attacker can choose IDs freely and place them before a keyword ID is published, eight attacker IDs capture almost 100% of lookups; for unpredictable file-hash IDs the attack starts after publication and the same eight IDs have little effect unless combined with bucket poisoning (unsolicited pings to nodes in the target's tolerance zone so attacker IDs enter their k-buckets), and even then republication of correct resources by every requester onto ten tolerance-zone nodes keeps the eclipse from becoming total over time (Figure 1). A Sybil-based DoS variant (pointing lookups at a victim) is also simulated and judged hard to stop. Second, a proposed fix: an third-party certification service (CS) issues each node a signed identifier (AuthId) bound to its public key, and an authentication protocol between nodes signs peculiar tokens (AuthXY) so that content publications and messages carry non-repudiable, traceable credentials tying user identity to the keys they publish, which removes free ID choice and makes bucket poisoning attributable. Preliminary simulation of the identity-based scheme reports overhead in node state and CS load; the CS is centralised with distributed variants left as future work. Read: abstract, introduction, Kad background and attack simulations (Section II with Figure 1 discussion), the identity-based proposal (Section III), conclusions; protocol message formats skimmed.

## Contribution

Independent simulation confirmation that eight self-chosen IDs eclipse a predictable Kad key, a nuance that unpredictable keys plus republication blunt the attack, and a certificate-based identity binding for Kademlia as the countermeasure.

## Key results

- Eight attacker IDs, placed in advance: ~100% eclipse of a predictable (keyword) key.
- Post-publication attack on file hashes: weak without bucket poisoning; with poisoning grows over time but never total because of ten-node republication.
- Proposed CS-issued AuthId plus signed tokens; cost is centralisation and CS load.

## Methods and models

OMNeT++ Kad simulation, single-layer overlay, attack scenarios varying ID choice and timing; protocol design for certified identities; preliminary overhead simulation.

## Limitations and open questions

Simulation only; a centralised certification service reintroduces the trusted party DHTs were meant to avoid (the authors acknowledge this); no evaluation of the scheme against Sybils who obtain many certificates; 5-page conference paper.

## Relevance to us

Reinforces the quantitative anchor from [[steiner-2007-exploiting]] (eight identities suffice) and adds the useful observation that unpredictability of the target plus honest redundancy (republication) is itself a partial defence, which transfers to agent networks where targets can be randomised. The certified-identity remedy is the "centralized certification" family in [[urdaneta-2011-survey]] and the same move as [[castro-2002-secure]]. Later live measurements: [[eisenbarth-2022-ethereum]]. Root: [[douceur-2002-sybil]].
