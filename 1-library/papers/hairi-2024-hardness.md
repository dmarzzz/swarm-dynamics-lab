---
id: hairi-2024-hardness
type: paper
title: On the Hardness of Decentralized Multi-Agent Policy Evaluation under Byzantine Attacks
authors:
- Hairi
- Minghong Fang
- Zifan Zhang
- Alvaro Velasquez
- Jia Liu
year: 2024
venue: Proceedings of the 22nd International Symposium on Modeling and Optimization in Mobile, Ad hoc, and Wireless Networks (WiOpt 2024), per arXiv comment
url: https://arxiv.org/abs/2409.12882
doi: null
arxiv: '2409.12882'
cite: Hairi, Fang, M., Zhang, Z., Velasquez, A., & Liu, J. (2024). On the Hardness of Decentralized Multi-Agent Policy Evaluation under Byzantine Attacks. Proceedings of the 22nd International Symposium on Modeling and Optimization in Mobile, Ad hoc, and Wireless Networks (WiOpt 2024), per arXiv comment. arXiv:2409.12882.
topics:
- fork-merge-security
- marl-emergence
- sync-consensus
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Studies fully decentralized multi-agent policy evaluation (consensus-based TD learning of a value function for a fixed policy) where each agent has its own private reward and up to f agents are Byzantine, sending arbitrary and possibly inconsistent parameters to different neighbours (local model poisoning). Proves two impossibility results, then gives a trimmed-mean TD algorithm (BDTD) that achieves the best attainable relaxed goal in the scalar-feature case, and tests it on a 10-agent MPE Simple Spread task with 2 malicious agents. Read: abstract, introduction and contributions, problem formulations, the two impossibility theorems with remarks, the Byzantine model and algorithm description, and the experimental section; proofs not read.

## Contribution

Shows that when honest agents have heterogeneous rewards, Byzantine agents make the natural target (the value of the average reward of the honest agents) unreachable, and characterises exactly how much of the honest population a correct algorithm can still represent.

## Key results

- Proved: with f > 0 Byzantine agents, no algorithm can make honest agents agree on the value function of the uniformly averaged honest reward (Theorem 1).
- Proved: relaxing to a weighted average of honest agents' rewards, no correct algorithm can guarantee more than |N| - f honest agents receive positive weight; that is, the Byzantine agents can always silence f honest agents' contributions in the worst case (Theorem 2). Holds for tabular and linear cases and general graphs.
- With f-trimmed means of neighbours' parameters, honest agents reach consensus (Theorem 3), scalar features assumed.
- Simple Spread, 10 agents, 2 malicious, 10 repetitions: BDTD's Bellman error under the Trim attack was comparable to FedAvg without attack, while Krum, FLTrust and SCCLIP were vulnerable to at least one of the Gaussian, Krum and Trim attacks (measured, Figures 1-2).

## Methods and models

Decentralized projected TD learning with linear features; f-trimmed mean aggregation; attacks Gaussian, Krum, Trim. WiOpt 2024 (per arXiv comment).

## Limitations and open questions

The constructive algorithm needs scalar features; policy evaluation only, not control.

## Relevance to us

Q2: a precise negative threshold for merges of heterogeneous parts. If the parts that return have each learned from different rewards or domains (the reason to fork), and f of them are corrupted, then in the worst case the merged result cannot reflect the true average of the honest parts, and up to f honest parts' contributions can be zeroed out. Corruption therefore costs honest information, not only adds false information: robust aggregation trims the outliers, and a corrupted part can arrange for an honest part's unique contribution to be what gets trimmed. This complements [[lee-2026-fully]] (exact recovery when only channels are corrupted) and [[chen-2022-byzantine-robust]] (near-optimal learning when parts sample the same environment). Related: [[fan-2021-fault-tolerant]], [[yan-2026-when]].
