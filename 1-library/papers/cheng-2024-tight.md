---
id: cheng-2024-tight
type: paper
title: "Tight incentive analysis of Sybil attacks against the market equilibrium of resource exchange over general networks"
authors: [Yukun Cheng, Xiaotie Deng, Yuhao Li, Xiang Yan]
year: 2024
venue: Games and Economic Behavior, vol. 148, pp. 566-610 (preliminary version EC 2022)
url: http://yuhao.li/papers/ec2022_bt_incentive_ratio.pdf
doi: 10.1016/j.geb.2024.10.009
arxiv: null
cite: "Cheng, Y., Deng, X., Li, Y., & Yan, X. (2024). Tight incentive analysis of Sybil attacks against the market equilibrium of resource exchange over general networks. Games and Economic Behavior, 148, 566-610. https://doi.org/10.1016/j.geb.2024.10.009"
topics: [sybil-resistance, sync-consensus]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "54 (Crossref, 2026-10-03)"
code: []
---

## Summary

Studies the BitTorrent-style proportional response protocol on a resource exchange network: an undirected graph G = (V, E) where each peer v owns a divisible resource w_v, uploads to neighbours in proportion to what it received from them last round, and has utility equal to total resource received. Wu and Zhang (STOC 2007) showed these dynamics converge to a market equilibrium characterised by a "bottleneck decomposition" of the graph. Earlier work by the same group showed no agent gains at equilibrium by cutting edges or misreporting its resource amount, but Chen et al. 2017 showed the protocol is not truthful under Sybil attacks, where an agent splits its endowment across fictitious identities it controls. Using the incentive ratio (maximum utility achievable by a Sybil attack divided by truthful utility), prior results gave bounds of at most two on trees, cliques and cycles. This paper settles the general case: Theorem 1.2, the incentive ratio of proportional response against Sybil attacks over general networks is exactly two. The lower bound comes from an explicit example (Example 2.10); the upper bound is a staged argument over the bottleneck decomposition, splitting on whether the attacker is a B-class or C-class vertex and bounding how its utility changes as fictitious identities are inserted (Lemmas 3.2-3.7). Read from the EC 2022 submission PDF on the author's site: abstract, introduction, model and problem statement, structure of the proof; detailed lemmas skimmed. The GEB version is 45 pages and paywalled; its abstract matches.

## Contribution

Closes the open problem on Sybil manipulation of proportional response / tit-for-tat resource exchange with a tight constant: a Sybil attacker can at most double its equilibrium utility, on any network.

## Key results

- Incentive ratio against Sybil attacks is exactly 2 on general graphs (Theorem 1.2); matching lower bound by example.
- Protocol remains strategyproof against weight cheating and edge deletion (prior results, cited), so Sybils are the only known profitable manipulation.
- Proof technique: bottleneck decomposition of the equilibrium plus a case split on vertex class.

## Methods and models

Linear exchange economy on a graph; proportional response dynamics x_vu(t+1) = w_v * x_uv(t) / sum_k x_kv(t); market equilibrium (clearance, budget, individual optimality); Sybil attack as splitting w_v among controlled copies that follow the protocol; incentive ratio as in Chen et al. 2011/2012.

## Limitations and open questions

Bound is on utility gain from a single strategic agent; it says nothing about welfare loss to others or about coordinated Sybils by several agents. Model is BitTorrent-era bandwidth exchange; identities are costless. Whether a factor-2 gain is "acceptable" is left to the designer.

## Relevance to us

A clean quantitative statement of how much Sybils buy in a decentralised reciprocity protocol, useful for the sybil-resistance survey's mechanism-design section: the harm is bounded (2x) rather than unbounded, which contrasts with the systemic crash in [[kash-2012-optimizing]] and the impossibility in [[sakurai-1999-limitation]]. Pairs with [[cheng-2005-sybilproof]] on Sybilproof reputation and the P2P reciprocity context in [[levine-2006-survey]]. Root: [[douceur-2002-sybil]].
