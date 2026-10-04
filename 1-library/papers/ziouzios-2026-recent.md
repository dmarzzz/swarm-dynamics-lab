---
id: ziouzios-2026-recent
type: paper
title: "Recent Progress in Optimising Sustainable Energy Smart Grids Using Swarm Robotics: A Systematic Narrative Review"
authors: [Dimitris Ziouzios, Vayos Karayannis]
year: 2026
venue: Electronics, vol. 15, no. 18, article 4174
url: https://www.mdpi.com/2079-9292/15/18/4174
doi: 10.3390/electronics15184174
arxiv: null
cite: "Ziouzios, D., & Karayannis, V. (2026). Recent Progress in Optimising Sustainable Energy Smart Grids Using Swarm Robotics: A Systematic Narrative Review. Electronics, 15(18), 4174. https://doi.org/10.3390/electronics15184174"
topics: [swarm-robotics, swarm-intelligence, sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: "0 (Crossref, 2026-10-03)"
code: []
---

## Summary

PRISMA-style systematic narrative review of swarm robotics and swarm intelligence applied to smart grids with renewable sources. Searches of Scopus (294), IEEE Xplore (265) and ACM DL (267) in April-June 2025 gave 826 records, 742 after dedup, 84 to full text, 54 included plus 11 hand-searched for a 65-paper corpus (Web of Science was unavailable). Studies are binned into four domains and three evidence levels. Monitoring and inspection dominates (n = 32, with 12 pilot field trials and 2 utility-scale deployments); energy distribution optimisation (n = 21) and fault detection and resilience (n = 12) are almost all lab or simulation; cybersecurity and communication has zero empirical studies, "all conceptual". 41 of 65 studies (63.1%) are lab or simulation only. Headline quantitative claims pulled from primary studies: quantum-inspired PSO scheduling cuts operating cost 9.67% and emissions 13.23%; consensus-based voltage/frequency control gives 66% lower frequency deviation and 56% faster post-fault voltage recovery; hybrid PSO path planning shortens inspection paths 15.5%; consensus convergence proofs hold under packet loss below 10-20%; Byzantine tolerance up to one third compromised agents, all on testbeds under 20 agents. Section 3.4 names four threat models for swarm-grid systems: Sybil attacks (one entity impersonating many swarm agents to inject false readings that look independent, citing Douceur), Byzantine faults (f < n/3, citing Lamport), DoS on inter-agent wireless links, and physical compromise of field robots, with mitigations listed as cryptographic identity management, cross-validation of neighbour readings, and frequency-agile radios; NERC CIP and IEC 62351 do not cover swarm robots. Read: abstract, methods (screening protocol), Table 2, Section 3.4 in full, conclusions; domain sections 3.1-3.3 skimmed.

## Contribution

A maturity map (domain x evidence level) for swarm approaches in grids, whose main message is the gap between lab demonstrations and utility deployment, and an explicit statement that swarm-grid security has no empirical literature at all.

## Key results

- 65-study corpus; 63.1% lab/simulation only; 6 utility-scale studies, all in monitoring/inspection.
- Cybersecurity and communication: 0 empirical, 0 pilot, 0 utility studies (Table 2).
- Sybil, Byzantine, DoS and physical compromise named as the swarm-grid threat models; mitigations stated conceptually only (Section 3.4).
- Numerical gains (9.67% cost, 13.23% emissions, 66% frequency deviation, 15.5% path length) are each from a single primary study, not pooled.

## Methods and models

Two-stage systematic search, PRISMA screening, four-criterion quality assessment, narrative synthesis. No meta-analysis.

## Limitations and open questions

Authors: Web of Science excluded; small corpus; heterogeneous metrics prevent pooling. Mine: "swarm robotics" here mostly means swarm-intelligence optimisers (PSO, ACO) running on grid controllers, with embodied robots mainly in inspection; the Sybil and Byzantine discussion is a restatement of the classic definitions with no grid-specific analysis. MDPI venue; both authors from one group.

## Relevance to us

Marginal for the hackathon. Worth keeping only as evidence that in a safety-critical physical swarm domain the Sybil/Byzantine question is acknowledged ([[douceur-2002-sybil]], [[lamport-1982-byzantine]]) but has zero empirical work, which is a clean "gap" citation for the sybil-resistance survey. Swarm-intelligence background: [[kennedy-1995-particle]], [[dorigo-1996-ant]]. Blockchain-flavoured swarm security is covered better in [[dorigo-2024-blockchain]].
