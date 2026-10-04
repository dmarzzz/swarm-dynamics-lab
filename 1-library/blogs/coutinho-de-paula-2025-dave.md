---
id: coutinho-de-paula-2025-dave
type: blog
title: "The Dave Fraud-Proof Algorithm: Triumphing over Sybils with a Laptop and a Small Collateral"
authors: [Gabriel Coutinho de Paula]
year: 2025
url: https://ethresear.ch/t/the-dave-fraud-proof-algorithm/21844
site: ethresear.ch
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: skim
relevance: 5
---

## Summary

Forum post (27 February 2025) summarising Dave, a permissionless fraud-proof algorithm from Cartesi (paper arXiv 2411.05463, co-authors Augusto Teixeira and Diego Nehab). The setting is an optimistic rollup dispute where anyone may post a claim, the honest side ("the hero", possibly many cooperating honest validators acting as one) must defeat an adversary who controls any number of perfectly coordinated Sybil claims, and the adversary can censor transactions for up to one week in total and reorder them. The three goals are security (an attacker must spend impractical resources to beat one honest validator), decentralization (no permission lists or large bonds) and liveness. Dave plays pairwise refutation matches with computation-hash commitments, but makes matches non-eliminatory (a repechage), so the hero can lose a match only through censorship, and amortises the one-week censorship budget over the whole dispute instead of per round. Claimed results: Sybil attacks are exponentially more expensive for the adversary than for the hero, the hero needs constant hardware (a laptop), and delay grows logarithmically in the number of Sybils with a constant an order of magnitude smaller than Cartesi's earlier PRT. A comparison for an attacker burning 1 million ETH lists bond / hero expenses / delay as: OPFP 0.08 ETH / 1,000,000 ETH / 1 week; BoLD 3,600 ETH / 150,000 ETH / 1 week; PRT-1L 1 ETH / 1 ETH / 20 weeks; Dave 3 ETH / 7 ETH / 3 weeks (expenses reimbursed after the dispute).

## Key claims

- Permissionless dispute games face Sybil resource-exhaustion and delay attacks; prior mitigations restrict participation through high bonds.
- In tournament brackets "Sybil eliminates Sybil": adversarial claims must fight each other, so cost and delay grow logarithmically.
- Bond size is decoupled from security in Dave; the bond only refunds the winner. The authors suggest 3 ETH.
- In practice disputes finish in 2 to 5 challenge periods.

## Evidence quality

Summary of a paper with proofs (I read the post's motivation, comparison table, threat model and conclusion, not the full proofs). The comparison numbers are the authors' own estimates. The delay figures differ slightly from the Devcon slides [[coutinho-de-paula-2024-dave]] (2 and 4 weeks there, 1 and 3 weeks here), which I take as different parameter assumptions; not checked against the paper. Replies include questions from Victor Shoup.

## Relevance to us

Dave is the best worked example found of Sybil resistance by protocol structure rather than identity: it does not try to tell honest participants from Sybils, it makes one honest participant with bounded resources win against any number of coordinated copies, with only logarithmic slowdown. That is the property an open agent swarm would want for verifying claims (for example a disputed computation or answer) without admission control. The key design ideas, pairing claims against each other, non-eliminatory matches and amortised timeouts, can be tested in agent debate or verification games where some agents are Sybils of one adversary. Talk version: [[coutinho-de-paula-2024-dave]]. Compare the "one honest operator suffices" integrity argument in [[ethresearch-2026-physical]].
