---
id: bai-2025-survey
type: paper
title: "A Survey on Directed Acyclic Graph-Based Blockchain in Smart Mobility"
authors: [Yuhao Bai, Soojin Lee, Seung-Hyun Seo]
year: 2025
venue: Sensors, vol. 25, no. 4, article 1108
url: https://www.mdpi.com/1424-8220/25/4/1108
doi: 10.3390/s25041108
arxiv: null
cite: "Bai, Y., Lee, S., & Seo, S.-H. (2025). A Survey on Directed Acyclic Graph-Based Blockchain in Smart Mobility. Sensors, 25(4), 1108. https://doi.org/10.3390/s25041108"
topics: [sybil-resistance, swarm-robotics]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: "18 (Crossref, 2026-10-03)"
code: []
---

## Summary

PRISMA systematic review of DAG-based distributed ledgers (IOTA Tangle, Hashgraph, Nano and similar, where transactions approve earlier transactions instead of being batched into a linear chain) applied to smart mobility, defined as electric vehicles, robotic systems and drone swarms. Four databases were searched, 1,248 records screened, 47 studies included. The authors argue DAG ledgers suit mobility because of parallel validation, throughput above 1,000 TPS, sub-second latency and feeless microtransactions (EV charging, vehicle-to-infrastructure data, drone coordination). The security section lists parasite-chain, balance, large-weight, censorship, Sybil, double-spending and replay attacks; the Sybil subsection (citing Douceur) notes that in a DAG an adversary with many fake nodes can bias which transactions get approved and, in mobility, tamper with traffic updates, vehicle coordination or toll payments, and points to Blockclique-style resource-committed node selection as the defence; one surveyed IoV data-authentication scheme (Aldweesh et al.) claims Sybil mitigation through DAG immutability. Five research priorities are proposed: standard benchmarks, formal security proofs for DAG protocols, hybrid DAG plus BFT consensus, privacy-preserving cryptography (ZKP, SMPC), and feeless microtransaction optimisation. Read: abstract, structure, the drone-swarm background subsection, the full security-threats section (including the Sybil subsection) and conclusions; the per-application review sections skimmed.

## Contribution

Consolidates the DAG-ledger-for-mobility literature and states its open security problems; the Sybil content is definitional rather than analytical.

## Key results

- 47 included studies from 1,248 screened; reported DAG performance >1,000 TPS and <1 s latency (figures quoted from surveyed work, not measured).
- Seven attack classes relevant to DAG ledgers in mobility; Sybil defence in surveyed systems reduces to costly node admission.
- Five research priorities, two of which are security (formal proofs, hybrid BFT).

## Methods and models

PRISMA search and screening; narrative synthesis; no experiments.

## Limitations and open questions

Drone swarms are a motivating application, not an analysed one; no surveyed study is checked for how its Sybil claim holds up. MDPI Sensors venue. DAG ledgers are a niche in both blockchain and swarm research, so transfer to LLM agent swarms is indirect.

## Relevance to us

Low. Keep as the pointer for "DAG ledgers as a coordination substrate for drone swarms, with Sybil as an acknowledged open problem", next to the swarm-blockchain line [[strobel-2018-managing]], [[strobel-2020-blockchain]], [[dorigo-2024-blockchain]] and the grid-swarm review [[ziouzios-2026-recent]] that reached the same "conceptual only" verdict on security. Root: [[douceur-2002-sybil]].
