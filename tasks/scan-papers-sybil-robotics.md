---
id: scan-papers-sybil-robotics
type: task
title: 'Catalogue the papers: Sybil and Byzantine agents in robot swarms and networked consensus'
kind: scan
status: claimed
priority: p0
owner: dmarz/sybil-robotics
for: null
created: 2026-10-03
created_by: dmarz/sybil
depends_on: []
topics:
- sybil-resistance
- swarm-robotics
- sync-consensus
claimed_at: 2026-10-03T18:01Z
updated: 2026-10-03T18:01Z
---

## Goal

Sybil and Byzantine robots in swarms: spoof-resilient multi-robot networks (physical-signal fingerprints), resilient consensus (W-MSR and successors), blockchain-coordinated swarms with Byzantine robots, resilient flocking, Byzantine-tolerant collective decision.

## Done when

- [x] At least 15 entries catalogued with topic `sybil-resistance`, including every review article found. (30 papers and 3 code repos created, plus notes and the topic tag appended to 3 existing entries.)
- [x] At least 4 read in full. (gil-2015-guaranteeing, mallmann-trenn-2021-crowd, wardega-2023-byzantine, strobel-2020-blockchain)
- [x] Code linked where it exists. (DBP, ARGoS-Blockchain interface, Toychain)
- [x] Coverage note filled and `python3 scripts/lab.py check` passes (0 errors; `verify` 0 problems).

## Coverage note

Searched by dmarz/sybil-robotics on 2026-10-03.

APIs and queries. OpenAlex works search: "spoof-resilient multi-robot networks", "crowd vetting sybil multi-robot", "resilient multi-robot coverage sybil", "sybil attack robot swarm", "byzantine robots collective decision swarm blockchain", "resilient flocking adversarial", "resilient formation Byzantine robots Pierson Schwager", "resilient flocking Saldana Byzantine", "sybil attack detection VANET survey", "sybil attack UAV swarm", "physicality-based sybil detection", "trust resilience multi-robot Yemini Gil", "Byzantine resilient distributed optimization multi-robot", "resilient consensus survey adversarial networked systems", "adaptive inter-robot trust", "resilience multi-robot physical masquerade", "Sybil attack Douceur", "toychain", "Byzantine fault tolerant collective perception robot swarm", "Sybil detection physical layer drone swarm". arXiv API for abstracts and PDFs. Semantic Scholar: forward citations of Gil et al. 2017 (Autonomous Robots), which surfaced the trust-observation line (Yemini, Cavorsi), Dynamic Crowd Vetting, Prorok's taxonomy, Shoukry's physics-based traffic defence and 2026 IsoRank. Backward chasing from the reference lists of the four full reads (Gil 2015, Mallmann-Trenn 2021, Wardega 2023, Strobel 2020). Web search for UAV/robot Sybil surveys and the Pierson PDF. GitHub API for the three code repos.

Vocabulary covered: Sybil, spoofing, spawning, ghost vehicles (networking/crypto); Byzantine robots, W-MSR, (r,s)-robustness, node injection, resilient consensus/flocking (control); trust observation, crowd vetting, accusations/blocklist (robotics); blockchain meta-controller, deposits, token economy (crypto/mechanism design).

Four lines emerge: (1) physical identity: Wi-Fi fingerprints and backscatter (gil-2015, gil-2018, renganathan-2017, huang-2019, xiao-2009, chulerttiyawong-2023); (2) stochastic trust side channels that beat majority bounds (yemini-2021, yemini-2022, cavorsi-2024, mallmann-trenn-2021, cavorsi-2023, gil-2023 survey); (3) economic scarcity via ledgers (strobel-2018, strobel-2020, strobel-2023, castello-ferrer-2021, keramat-2023, dorigo-2024, pena-queralta-2023, toychain); (4) Byzantine-resilient control that assumes bounded identities (leblanc-2013, saldana-2017, saulnier-2017, wardega-2023, which assumes a central identity issuer). Reviews found and added: gil-2023-physicality, prorok-2021-beyond, liao-2024-survey, wang-2023-resilient, dorigo-2024-blockchain, pena-queralta-2023-blockchain, ceviz-2024-survey, yan-2025-reliability (bridges swarm robots and AI agents).

Found but not added: Gil et al. 2017 Autonomous Robots (journal version of gil-2015, noted inside that entry); Huang et al. arXiv:2012.14227 (extended ScatterID, noted in huang-2019-lightweight); Wardega et al. HoLA Robots arXiv:2301.10704 (centralised plan-deviation attacks, noted in wardega-2019-resilience); Prorok et al. T-RO 2022 special-section introduction (noted in prorok-2021-beyond); VANET Sybil surveys (Hadri et al. 2025, Zhang et al. 2020, Karn and Gupta 2016): abstracts not available through the APIs, so not catalogued; Sagwal et al. WCNC/NOMS 2026 Sybil attack papers, Ishii-group resilient consensus papers, Mitra and Sundaram Byzantine observers, Pacheco et al. federated learning in robot swarms (arXiv:2409.01900), Simionato et al. IROS 2025 inconsistencies in blockchain robot swarms, Krishnamohan blockchain BFT papers, TRIBES UAV framework: seen in listings only, not opened. Bankrupting Sybil and resource-competitive Sybil defences appeared in the citation chase but belong to the p2p lane.

Still thin: Byzantine-tolerant collective decision without blockchains (best-of-n with zealots or stubborn agents; the collective-decision lane may hold these); VANET physics-based Sybil detection (only surveys seen); real-hardware experiments with many colluding physical robots (all physical-layer defences assume one radio per attacker); any work testing these mechanisms on software or LLM agent swarms (none found).
