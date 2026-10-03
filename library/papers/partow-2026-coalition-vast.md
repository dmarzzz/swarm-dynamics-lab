---
id: partow-2026-coalition-vast
type: paper
title: "COALITION-VAST: Auditable Multi-Agent Alignment Under Byzantine Governance"
authors: [Soraya Partow, Satyaki Nan]
year: 2026
venue: 2026 International Conference on Intelligent Multimedia, Networking, and Security (IMNS), pp. 1-6
url: https://ieeexplore.ieee.org/document/11655305
doi: 10.1109/imns67862.2026.11655305
arxiv: null
cite: "Partow, S., & Nan, S. (2026). COALITION-VAST: Auditable Multi-Agent Alignment Under Byzantine Governance. In 2026 International Conference on Intelligent Multimedia, Networking, and Security (IMNS), pp. 1-6. IEEE. https://doi.org/10.1109/IMNS67862.2026.11655305"
topics: [sybil-resistance, llm-agent-swarms, fork-merge-security]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (Crossref, 2026-10-03)"
code: []
---

## Summary

Short IEEE conference paper extending the authors' VAST / VAST-Blockchain line (single-agent compliance and deployment integrity) to multi-agent ecosystems, where the failure modes are coalition deviation, governance capture and rushed rule changes. COALITION-VAST models agent coordination as a coalition game coupled to on-chain evolution of the rules, keeps each agent bound to locked machine-checkable constraints, and adds trust-driven targeted auditing so that detection probability adapts to behaviour rather than being a fixed parameter. The abstract claims: derived conditions under which adaptive detection plus enforceable penalties make profitable coalition deviation unattractive; with BFT consensus and supermajority rule updates, Byzantine validators alone cannot finalise unauthorised constraint changes, and Sybil governance attempts are in the threat model; a prototype simulation across healthcare resource allocation, autonomous swarms and multi-stakeholder finance shows mean alignment 0.90 vs 0.69 baseline (+30% relative), a 98% reduction in undetected coalition deviation, and 2.8-3.4 s latency per coordinated decision; an evolutionary analysis shows compliance is stable when expected audit penalty exceeds deviation gain; and a "governance gate" for high-stakes updates based on evidence commitment, delay and independent review. Abstract only (IEEE Xplore, paywalled, no OA copy); the alignment metric, simulation setup and how Sybil governance attempts are modelled are not visible.

## Contribution

Frames multi-agent alignment as a governance problem with Byzantine validators and Sybil voters, and proposes adaptive auditing plus on-chain supermajority rule changes as the enforcement layer.

## Key results

- Alignment score 0.90 vs 0.69 (+30% relative), 98% fewer undetected coalition deviations, 2.8-3.4 s per decision (abstract; metric definitions unknown).
- Claimed theorem-style conditions: deviation unprofitable when expected penalty exceeds gain; Byzantine validators cannot finalise unauthorised updates under BFT plus supermajority.

## Methods and models

Coalition game plus on-chain rule evolution, trust-weighted targeted audits, BFT consensus with supermajority governance, evolutionary game analysis, prototype simulation in three domains. Details not read.

## Limitations and open questions

Abstract-level, 6-page venue paper with no citations yet; the "alignment" score is undefined from the abstract; Sybil resistance for governance votes appears to rest on the validator set and supermajority, which does not by itself stop one operator from fielding many agent voters unless validator admission is Sybil-resistant. Treat the numbers as unverified until the paper is read.

## Relevance to us

A 2026 data point that LLM-era multi-agent alignment work is reaching for Byzantine and Sybil vocabulary and audit-based deterrence, which lines up with the accountability layer in [[lin-2026-treacherous]] and the collusion framing in [[motwani-2024-secret]] and [[hammond-2025-multi]]. Classic underpinnings: [[lamport-1982-byzantine]], [[castro-1999-practical]], [[douceur-2002-sybil]].
