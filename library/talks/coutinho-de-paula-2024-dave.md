---
id: coutinho-de-paula-2024-dave
type: talk
title: "The Dave fraud-proof algorithm — triumphing over Sybils with a laptop and a small collateral"
authors: [Gabriel Coutinho de Paula, Augusto Teixeira]
year: 2024
url: https://app.devcon.org/schedule/C7ZFH3
venue: Devcon 7 SEA (Bangkok), 13 November 2024, Stage 5; video https://www.youtube.com/watch?v=dI_3neyXVl0; slides https://drive.google.com/file/d/1ulLAN8HrVwwBhQFbRhpx3KGT14CNJ0nZ/view
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: skim
relevance: 4
---

## Summary

25-minute Devcon talk introducing the Dave fraud-proof algorithm. I read the session abstract and the full slide deck; I did not watch the video, so no timestamps are given. The abstract states that current fraud-proof algorithms are susceptible to Sybil attacks that hurt security, decentralization and settlement liveness, and that Dave admits no realistic Sybil attack able to exhaust defenders' resources or cause significant delay, even with minimal bonds. The slides frame the goals as: anyone can validate with a laptop and little ETH, one honest validator ("Willie") can defeat a nation-state, and disputes finish without long delays. Threat model: the L1 works but the adversary can censor for one week and control transaction order. The slides walk from pairwise refutation games (bisection over Merkleized computation hashes, chess clocks) to BoLD's parallel multiparty game (fast but can overwhelm the honest player unless bonds are high) to PRT brackets ("Sybil eliminates Sybil", logarithmic cost and delay but paying the one-week censorship every round, (7d + 2h) × log2(Sybils)) to Dave, which amortises censorship over the whole dispute (7d + 2h × log2(Sybils)) using non-eliminatory repechage matches with hit points, so the honest claim can lose at most seven one-day matches to censorship. Comparison slide for a 1 million ETH Sybil attack (bond / expenses / delay): OP 0.08 ETH / 1,000,000 ETH / 2 weeks; BoLD 3,600 ETH / 150,000 ETH / 2 weeks; PRT-1L 1 ETH / 1 ETH / 20 weeks; Dave 3 ETH / 7 ETH / 4 weeks.

## Relevance to us

The talk is the most compact presentation of a Sybil-tolerant (rather than Sybil-excluding) protocol: a single honest agent with constant resources wins against any number of coordinated adversarial copies, at logarithmic cost in delay. The bracket-plus-repechage structure is a candidate mechanism for adjudicating disputed claims among LLM agents when some agents are Sybils of one adversary, and the hit-point idea bounds what censorship (an adversary delaying honest messages) can achieve. Written version with slightly different delay figures: [[coutinho-de-paula-2025-dave]].
