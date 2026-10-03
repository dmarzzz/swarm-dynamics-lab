# 2026-10-03 sybil-robotics

## What I did

Ran the scan-papers-sybil-robotics lane. Added 30 paper entries and 3 code entries tagged sybil-resistance, read 4 in full (gil-2015-guaranteeing via notes since sybil-foundations created it first, mallmann-trenn-2021-crowd, wardega-2023-byzantine, strobel-2020-blockchain), and appended notes plus the sybil-resistance tag to leblanc-2013-resilient and strobel-2023-robot. Forward-chased Gil et al. 2017 on Semantic Scholar, backward-chased the four full reads. check: 0 errors; verify: 0 problems.

## What surprised me

- Robotics has three distinct Sybil answers that map cleanly onto agent swarms: physical identity (Wi-Fi fingerprints), trust side channels that let consensus survive a malicious majority (Yemini et al.), and economic scarcity (deposits on a robot-run blockchain). Wardega's accusation-matching protocol is the strongest Byzantine mechanism but explicitly assumes a central identity issuer.
- Sybils do more than add votes: crowd vetting shows spoofed nodes inflate perceived graph robustness, so W-MSR thinks it tolerates an adversary it cannot.
- Only one review (Yan et al. 2025) explicitly bridges swarm-robot security and AI agents. No work found tests these mechanisms on software agents.

## What next

- Survey section idea: "what is the physicality of a software agent" (attestation, stake, compute) as the replacement for radio fingerprints.
- Thin: Byzantine-tolerant best-of-n decisions without ledgers, multi-body colluding attackers, VANET physics-based detection primary papers.
