---
id: lavaur-2024-verifiable
type: paper
title: "Verifiable Multi-Agent Multi-Task Assignment"
authors: [Thomas Lavaur, Déborah Conforto Nedelmann, Corentin Chauffaut, Jérôme Lacan, Caroline P. C. Chanel]
year: 2024
venue: 2024 IEEE Secure Development Conference (SecDev), pp. 1-12
url: https://ieeexplore.ieee.org/document/10734053
doi: 10.1109/secdev61143.2024.00006
arxiv: null
cite: "Lavaur, T., Conforto Nedelmann, D., Chauffaut, C., Lacan, J., & Chanel, C. P. C. (2024). Verifiable Multi-Agent Multi-Task Assignment. In 2024 IEEE Secure Development Conference (SecDev), pp. 1-12. IEEE. https://doi.org/10.1109/SecDev61143.2024.00006"
topics: [sybil-resistance, swarm-robotics]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (Crossref, 2026-10-03)"
code: []
---

## Summary

Addresses security of online centralized multi-agent multi-task assignment (MAMTA), where a central server repeatedly dispatches arriving tasks to a fleet of agents. The authors wrap the SKATE meta-heuristic (Successive Rank-based Task Assignment, from Conforto Nedelmann's ISAE-SUPAERO thesis) in verifiable computation so the server emits a proof that the allocation it computed is the one the algorithm prescribes, with no errors or misbehaviour; agents with low compute can check the proof. The architecture is described as similar to an account-based blockchain or a zk-rollup and is said to potentially give agents privacy. A proof of concept was deployed in a real aerial robotic mission (real flight), and average proof generation and verification times were measured; the abstract says the results suggest on-board use in mobile agents is feasible. Abstract-level read from IEEE Xplore (paywalled; Unpaywall finds no OA copy). Timing numbers, proof system and fleet size are not in the abstract.

## Contribution

Brings zero-knowledge style verifiable computation to task allocation for robot fleets, so agents do not have to trust the central dispatcher, with a hardware-in-the-loop flight demo.

## Key results

- Proof-carrying task assignment implemented on top of SKATE and flown in a real aerial mission (abstract).
- Proof generation and verification times were assessed and judged compatible with future on-board use (abstract; numbers not visible).

## Methods and models

Centralized online MAMTA; SKATE rank-based meta-heuristic chosen because it is compatible with verifiable computation circuits; proof system not named in the abstract; account-based blockchain / zk-rollup style architecture; proof of concept on aerial robots.

## Limitations and open questions

Abstract-only. Verifiability of the allocation protects against a dishonest or faulty server, but not against agents that lie about their state or against an operator fielding many fake agents (the Sybil case): the proof shows the algorithm ran correctly on the inputs it was given. The thesis abstract (theses.fr 2024ESAE0049) says the verifiable extension is also meant to counter cyber-physical attacks on a mobile agent network in hostile environments, which is a broader claim than the conference abstract supports.

## Relevance to us

Relevant to the "trusted coordinator" branch of sybil-resistance in swarms: it is one of few papers that puts cryptographic verifiability on a swarm dispatcher and flies it. Complements consensus-style trust in [[gil-2015-guaranteeing]] (physical-layer Sybil detection for robots) and the blockchain-coordination line ([[castro-2024-modeling]]). Companion thesis: Conforto Nedelmann, D. (2024), "On scaling-up online multi-agent multi-task assignment", ISAE-SUPAERO, DOI 10.70675/bc9e0533z7737z4874z84b6z06616d3f3aaa, not catalogued separately (dissertation, Crossref returns no year, same material).
