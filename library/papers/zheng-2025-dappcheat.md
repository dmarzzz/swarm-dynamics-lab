---
id: zheng-2025-dappcheat
type: paper
title: "DAppCheat: Detecting Cheating Robots for DApps on Multiple Blockchains"
authors: [Peilin Zheng, Xiapu Luo, Weilin Zheng, Zibin Zheng]
year: 2025
venue: IEEE Transactions on Services Computing, vol. 18, no. 5, pp. 2687-2700
url: https://ieeexplore.ieee.org/document/11119786/
doi: 10.1109/tsc.2025.3596896
arxiv: null
cite: "Zheng, P., Luo, X., Zheng, W., & Zheng, Z. (2025). DAppCheat: Detecting Cheating Robots for DApps on Multiple Blockchains. IEEE Transactions on Services Computing, 18(5), 2687-2700. https://doi.org/10.1109/tsc.2025.3596896"
topics: [sybil-resistance, swarm-detection]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "1 (Crossref, 2026-10-03)"
code: []
---

## Summary

First systematic study of "robots" (bot-controlled Sybil accounts) used to inflate decentralised application (DApp) activity: fake unique-active-wallet counts to climb rankings on trackers like DAppRadar, attract users, and mislead investors. The authors collect and release a multi-chain DApp-user dataset of 4,857 DApps and 99,758,959 user accounts across Ethereum, EOSIO, TRON and BSC. Because an abusing operator funds and drives many anonymous accounts, they propose a general "parent account" mechanism that works across chains with different account models to link anonymous accounts that were created or funded from the same source, exposing collusion. To avoid false positives from exchanges (which create many accounts legitimately) and whales (which move large volume), they define a creating-account weight and a used-DApp-volume weight that discount those entities. The abstract reports "extensive experimental results" showing effectiveness but gives no precision, recall or prevalence figures; the IEEE body is paywalled, no open copy was found, so this entry rests on the abstract and the first paragraphs of the introduction (DAppRadar: more than 5,000 DApps, 17.2 million daily unique active wallets as of October 2024).

## Contribution

A cross-chain account-linking heuristic (parent accounts) plus weighting to down-rank exchanges and whales, applied to detect Sybil-inflated DApp usage, and the accompanying public dataset. Extends the Ethereum-specific address clustering line to EOSIO and TRON account models.

## Key results

- Dataset: 4,857 DApps, 99,758,959 users, four chains (abstract).
- Parent-account mechanism finds anonymous user collusion across differing account systems (abstract; method details and numbers not visible).
- Weights for creating accounts and used-DApp volume reduce exchange and whale confounding (abstract).

## Methods and models

On-chain account creation and funding graph; parent-account attribution per chain; weighted scoring; evaluation presumably against labelled robot DApps (not visible at this read depth).

## Limitations and open questions

Abstract only. Ground truth for "cheating robot" is the hard part and the abstract does not say how labels were obtained. Parent-account linking will miss operators who fund Sybils through mixers or exchanges, and the exchange discount could be gamed by routing Sybil funding through exchange withdrawals. Static dataset snapshot (2024); adaptive attackers not considered as far as the abstract shows.

## Relevance to us

Detection-side Sybil work on exactly the economic setting where fake "agents" (bots) inflate collective activity signals. The parent-account idea is the same move as Ethereum address clustering ([[victor-2020-address]]) and airdrop-hunter detection ([[harrigan-2018-airdrops]], [[messias-2023-airdrops]]): find the common controller through funding provenance. For detecting coordinated agent swarms, provenance-of-resources (who paid for the compute or the API key) is probably a stronger signal than behaviour alone, and this paper is a worked example at 100M-account scale. Mechanism-design counterparts: [[pan-2024-sybil]], [[zheng-2024-sybil]].
