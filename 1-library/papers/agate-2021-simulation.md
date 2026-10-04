---
id: agate-2021-simulation
type: paper
title: "A Simulation Software for the Evaluation of Vulnerabilities in Reputation Management Systems"
authors: [Vincenzo Agate, Alessandra De Paola, Giuseppe Lo Re, Marco Morana]
year: 2021
venue: ACM Transactions on Computer Systems, vol. 37, no. 1-4, article 4, pp. 1-30
url: https://sites.unipa.it/networks/ndslab/pdf/0193.pdf
doi: 10.1145/3458510
arxiv: null
cite: "Agate, V., De Paola, A., Lo Re, G., & Morana, M. (2021). A Simulation Software for the Evaluation of Vulnerabilities in Reputation Management Systems. ACM Transactions on Computer Systems, 37(1-4), Article 4, 1-30. https://doi.org/10.1145/3458510"
topics: [sybil-resistance, swarm-detection]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "8 (Crossref, 2026-10-03)"
code: []
---

## Summary

Presents a simulation platform for stress-testing distributed reputation management systems (RMSs) in multi-agent service networks before deployment. The framework models agents with a true cooperativeness level, service interactions, direct and gossiped feedback, and a taxonomy of attacks: selfish behaviour, slandering and self-promotion, oscillation (alternate good and bad behaviour), collusion, and Sybil attacks (cheap registration lets an agent create many identities, used for whitewashing a bad history or amplifying promotion/slander, Section 2.2.5). Three state-of-the-art RMSs are modelled as case studies, a simple averaging RMS, a Beta-distribution RMS and the Core trust model, and each is run under the attack scenarios with configurable parameters (Table 1). The Sybil experiment (Section 6.1.3, Figure 5): a single malicious agent with true cooperativeness 0.2 is correctly rated ~0.2 by step 50, then begins self-promotion and from step 60 is joined by Sybil accounts arriving at linear, quadratic or cubic replication rates until step 100; in all three RMSs its reputation climbs away from the truth, faster for faster Sybil growth, demonstrating the damage when registration policies do not limit identities. The authors note such countermeasures (registration control, discarding feedback from accounts without real service history) are what would mitigate this and that the simulations deliberately omit them. An open-source release with popular RMSs and attack templates is promised. Read: abstract, introduction, attack taxonomy (Section 2.2), framework architecture overview, Section 6.1 experiments with emphasis on the Sybil case, conclusions; the detailed RMS formalisations skimmed.

## Contribution

A reusable simulator and attack taxonomy for reputation systems, with worked demonstrations that Beta, Core and naive RMSs are all steerable by Sybil-amplified self-promotion when identity creation is free.

## Key results

- Sybil-amplified promotion lifts a 0.2-cooperativeness agent's reputation in all three RMSs; effect scales with the Sybil replication rate (linear < quadratic < cubic).
- Oscillation, slander and collusion attacks likewise characterised per RMS (figures in Sections 6.1.1-6.1.2).
- Platform supports plugging in new RMSs and behaviours.

## Methods and models

Discrete-time agent simulation, parametrised attacker behaviours, three RMS implementations, reputation-vs-truth trajectories as the evaluation metric.

## Limitations and open questions

Synthetic scenarios with hand-set parameters; no quantitative "cost to attacker" model; Sybil defences are discussed but not implemented in the compared RMSs; open-source release status not verified here.

## Relevance to us

Useful as a ready-made harness idea for the swarm-detection and sybil-resistance threads: simulate an agent population with a configurable fraction of coordinated or Sybil agents and measure how fast a reputation or trust signal is captured. The attack taxonomy (whitewashing, promotion, slander, oscillation, collusion, Sybil) is a good checklist for agent-platform reputation design. Related: [[marti-2004-limited]] and [[zhang-2009-promoting]] (older RMS evaluations under whitewashing), [[cheng-2005-sybilproof]] (theory), [[araujo-2011-maximum]] (collusion detection in voting pools). Root: [[douceur-2002-sybil]].
