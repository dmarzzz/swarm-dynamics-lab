---
id: fan-2023-altruistic
type: paper
title: 'Altruistic and Profit-oriented: Making Sense of Roles in Web3 Community from Airdrop Perspective'
authors:
- Sizheng Fan
- Tian Min
- Xiao Wu
- Wei Cai
year: 2023
venue: Proceedings of the 2023 CHI Conference on Human Factors in Computing Systems (CHI '23)
url: https://arxiv.org/abs/2303.08457
doi: null
arxiv: '2303.08457'
cite: 'Fan, S., Min, T., Wu, X., & Cai, W. (2023). Altruistic and Profit-oriented: Making Sense of Roles in Web3 Community from Airdrop Perspective. In Proceedings of the 2023 CHI Conference on Human Factors in Computing Systems (CHI ''23), Hamburg, Germany. arXiv:2303.08457.'
topics:
- swarm-detection
- sybil-resistance
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

Data-driven role taxonomy of ParaSwap airdrop recipients. Clustering recipients by post-airdrop behaviour yields roles including speculators, diversified members and an 'airdrop hunter' cluster holding 22.24% of members, who aggregate tokens into one place before staking or providing liquidity. Comparing the pre-airdrop external transfer graph with the PSP token graph, the authors find hunter cliques that slipped past ParaSwap's own filter (at least 50 transactions or a minimum balance, six interactions in six months, and shared-transfer patterns) and describe three styles: organised and planned, cautious, and blatant. They conclude current detection is not sufficient to screen out hunters.

## Contribution

Evidence from a real airdrop that the issuer's published Sybil filter missed coordinated hunter cliques, recoverable after the fact by token-network component analysis.

## Key results

- Hunter cluster is 22.24% of the analysed members.
- Three hunter clique types found that passed ParaSwap's filter.

## Methods and models

Feature clustering of recipients; global network properties (reciprocity, assortativity, attracting components) on PSP token networks; matching components to pre-airdrop transfer graphs.

## Limitations and open questions

Skimmed; detection is retrospective, as the authors acknowledge.

## Relevance to us

A measured failure of an operator's swarm filter, plus post-hoc graph methods that catch what the filter missed. Same group as [[zhou-2024-artemis]]; compare [[luo-2025-toward]].
