---
id: higgins-2009-threats
type: paper
title: "Threats to the Swarm: Security Considerations for Swarm Robotics"
authors: [Fiona Higgins, Allan Tomlinson, Keith M. Martin]
year: 2009
venue: International Journal on Advances in Security, vol. 2, no. 2&3, pp. 288-297 (IARIA)
url: https://www.thinkmind.org/download.php?articleid=sec_v2_n23_2009_14
doi: null
arxiv: null
cite: "Higgins, F., Tomlinson, A., & Martin, K. M. (2009). Threats to the Swarm: Security Considerations for Swarm Robotics. International Journal on Advances in Security, 2(2&3), 288-297."
topics: [swarm-robotics, sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "not available (no DOI; Crossref has no record; OpenAlex rate-limited at access time)"
code: []
---

## Summary

Early (2009) position paper from the Royal Holloway Information Security Group, extended from an ICAS 2009 talk, that claims to be the first attempt to categorise security challenges specific to swarm robotics. Section II contrasts swarms with multi-robot systems (hierarchical C2), mobile sensor networks, MANETs and mobile software agents, and argues the swarm-specific features are (i) diverse and often "exotic" communication channels including implicit communication via stigmergy, (ii) unusual notions of identity (some swarm designs forbid individual identity, others use group identity or broadcast individual IDs), and (iii) adaptive emergent behaviour that an intruder could steer. Section III walks through application domains (space, military, monitoring such as the GUARDIANS fire-fighting swarm and EU-MOP oil-spill project, disaster relief, medical) and the CIA-style security services each would need. Section IV lists nine challenge areas: resource constraints, physical capture and tampering (including a "capture and re-introduction attack" where a modified robot rejoins the swarm, which they call unique to swarm robotics), monitoring and control of a system with no hierarchy, communication security for RF/IR and exotic channels, swarm mobility (which may help authentication by moving toward a peer), entity authentication and identity, key management under join/leave churn, intrusion detection where intrusion is physical insertion of rogue robots and anomalous behaviour is physical and emergent, and "managing learning" (an adversary shapes the environment so the swarm adapts the wrong way, or poisons an anomaly detector's baseline). Figure 1 shows single intruder, multiple intruders and overlapping swarms, and argues that detection gets harder as more foreign robots infiltrate, "particularly if the notion of identity within a swarm is forbidden". No experiments; purely a threat taxonomy. Read in full (10 pages).

## Contribution

First published taxonomy of swarm-robotics security challenges, and the first to state that swarm identity models (none, group, or broadcast individual) are themselves a security design decision with consequences for authentication and intrusion detection.

## Key results

- Three swarm idiosyncrasies that break off-the-shelf security: communication channels, identity concepts, adaptive emergent behaviour (abstract, Section II-E).
- Nine challenge areas in Section IV; the capture-and-reintroduction attack and physical intrusion detection are singled out as swarm-unique.
- Qualitative claim: multiple infiltrators are harder to detect than one, and identity-less swarms make it hardest (Figure 1 discussion).
- Learning as attack surface: anomaly-based intrusion detection can be trained by an adversary who manipulates the environment (Section IV-I).

## Methods and models

Conceptual analysis; comparison with four neighbouring technologies; application case studies drawn from literature (GUARDIANS, EU-MOP, Swarmanoid-era projects). The only prior work they acknowledge on swarm threats is Winfield and Nembrini's hazard analysis.

## Limitations and open questions

No formal model, no numbers, no proposed mechanisms; 2009 so it predates blockchain-based swarm security ([[strobel-2018-managing]]), Wi-Fi fingerprinting ([[gil-2015-guaranteeing]]) and all LLM-agent work. Sybil is not named as such, but the identity section and Figure 1 describe exactly the Sybil-style scenario (many indistinguishable foreign agents). Venue is a low-profile IARIA journal.

## Relevance to us

A good "origin" citation for the sybil-resistance survey's swarm-robotics branch: it frames identity-in-swarms as the open problem that [[gil-2015-guaranteeing]], [[gil-2018-resilient]], [[strobel-2018-managing]], [[strobel-2020-blockchain]] and [[strobel-2023-robot]] later attack, and its "managing learning" point anticipates data-poisoning of adaptive swarms. The multiple-intruder and overlapping-swarm figure maps directly to the swarm-detection question of telling one operator's agents from the host population. Older MAS framing: [[bijani-2014-review]].
