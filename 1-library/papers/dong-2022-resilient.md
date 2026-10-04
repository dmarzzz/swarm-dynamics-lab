---
id: dong-2022-resilient
type: paper
title: "Resilient Consensus for Multi-Agent Systems in the Presence of Sybil Attacks"
authors: [Xiaochen Dong, Yiming Wu, Ming Xu, Ning Zheng]
year: 2022
venue: Electronics, vol. 11, no. 5, article 800
url: https://www.mdpi.com/2079-9292/11/5/800/htm
doi: 10.3390/electronics11050800
arxiv: null
cite: "Dong, X., Wu, Y., Xu, M., & Zheng, N. (2022). Resilient Consensus for Multi-Agent Systems in the Presence of Sybil Attacks. Electronics, 11(5), 800. https://doi.org/10.3390/electronics11050800"
topics: [sybil-resistance, sync-consensus, swarm-robotics]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "not checked (OpenAlex budget exhausted 2026-10-03)"
code: []
---

## Summary

Resilient consensus for discrete-time linear multi-agent systems where the attacker is a Sybil: a compromised physical node (the "Sybil parent") fabricates many fake identities ("Sybil children") that all multicast the parent's malicious state to the parent's neighbours. The point of attack is that the whole MSR / W-MSR family of resilient consensus algorithms ([[leblanc-2013-resilient]] and successors) assumes at most F malicious nodes per neighbourhood (F-local) or in total (F-total), and a Sybil can exceed any such F for free. The paper therefore redefines the threat as F-parent-local and F-parent-total (bounds on physical attackers, not identities) and adds a lightweight identity check that needs no trusted authority or radio fingerprinting: each normal node quantises its state to an integer and appends a fresh random decimal label drawn each step from a truncated normal distribution on a per-node interval, so labels never overlap and are used once; Sybil children, having no physical entity, reuse the parent's label, so a receiver that sees the same label on several incoming messages discards the duplicates before running the quantised W-MSR update (the resulting algorithm is called QWL-MSR). Theorems 1 and 2 give graph-robustness conditions (in the (r,s)-robustness sense of the MSR literature) that are necessary and sufficient for quantised resilient consensus almost surely under the F-parent-total and F-parent-local models; the reader proxy stripped the exact robustness parameters, so they are not reproduced here. Simulation with 7 agents, node 4 as Sybil parent with children 4a and 4b holding a constant out-of-range value: plain QW-MSR is dragged outside the safety interval, QWL-MSR converges inside it in 38 steps on the first topology and 19 steps on a 3-robust topology, and fails on reduced (2,1)-robust and merely strongly connected graphs, matching the necessity claim. Read: abstract, introduction, attack model, verification mechanism, theorem statements, simulations, conclusion; proofs skimmed.

## Contribution

Reframes Sybil attacks for the resilient-consensus (MSR) community: bound physical attackers rather than identities, and defeat identity multiplication with a per-message disposable random label embedded in the fractional part of a quantised state, which costs no extra hardware or storage.

## Key results

- F-local / F-total assumptions are invalid under Sybil attacks; F-parent-local / F-parent-total proposed instead (Definitions 6 and 7).
- Random truncated-normal decimal labels per node per step; Sybil children are detected because they share the parent's label (Section 3.1.2).
- Theorems 1 and 2: necessary and sufficient graph robustness for almost-sure quantised resilient consensus under the two parent models.
- 7-agent simulation: QW-MSR fails under a 1-parent attack with two children; QWL-MSR converges in 38 steps (Theorem 1 topology) and 19 steps (3-robust topology); fails when robustness is reduced (Figures 6 to 11).

## Methods and models

Discrete-time linear consensus on directed graphs; probabilistic quantiser; truncated normal label sampling on disjoint per-agent intervals; QWL-MSR (quantised, weighted, labelled MSR); (r,s)-robust graph conditions; numerical simulation only.

## Limitations and open questions

The label defence assumes Sybil children cannot run the label generator themselves, i.e. the fake identities are pure message replicas rather than independently computed forgeries; a parent that generates distinct random labels for each child would defeat it, and the paper does not address that. Also assumes label intervals are pre-assigned per node, which is itself an identity registry. Small simulations (7 agents, one parent); no robots or hardware. The authors concede related defences (fingerprinting, blockchain-based ReCon) exist but argue they are heavier.

## Relevance to us

Highest-relevance item in this batch for the swarm consensus question: it is the explicit bridge between the Byzantine-consensus-in-swarms literature ([[leblanc-2013-resilient]], [[wardega-2023-byzantine]]) and the Sybil literature ([[douceur-2002-sybil]]), and its central observation, that any F-bounded robust aggregation is void if identities are free, applies verbatim to LLM agent swarms that aggregate sub-agent outputs by majority or trimmed mean. The weak point (children cannot forge labels) is exactly where a software agent swarm differs from a radio network, so the physical-layer alternatives ([[gil-2015-guaranteeing]], [[gil-2018-resilient]]) and the audit approach in [[gandhi-2025-roborebound]] are the right comparisons.
