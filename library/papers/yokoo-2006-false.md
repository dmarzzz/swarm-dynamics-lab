---
id: yokoo-2006-false
type: paper
title: "False-name-proof combinatorial auction protocol: Groves Mechanism with SubModular Approximation"
authors: [Makoto Yokoo, Toshihiro Matsutani, Atsushi Iwasaki]
year: 2006
venue: Proceedings of the Fifth International Joint Conference on Autonomous Agents and Multiagent Systems (AAMAS '06), Hakodate, pp. 1135-1142
url: https://dl.acm.org/doi/10.1145/1160633.1160840
doi: 10.1145/1160633.1160840
arxiv: null
cite: "Yokoo, M., Matsutani, T., & Iwasaki, A. (2006). False-name-proof combinatorial auction protocol: Groves Mechanism with SubModular Approximation. In Proceedings of the Fifth International Joint Conference on Autonomous Agents and Multiagent Systems (AAMAS '06), pp. 1135-1142. ACM. https://doi.org/10.1145/1160633.1160840"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "7 (Crossref, 2026-10-03)"
code: []
---

## Summary

Proposes the Groves Mechanism with SubModular Approximation (GM-SMA), a combinatorial auction protocol the authors say is the first to satisfy three properties at once: (1) false-name-proofness (no bidder gains by splitting its bid across fictitious identities), (2) every winner is part of a Pareto efficient allocation, and (3) whenever a Pareto efficient allocation is reached the outcome is in the core and robust to collusion among losers. The construction keeps VCG/Groves payments for winners but, when computing a bidder's payment, replaces the other bidders' true valuations with a submodular approximation, which is what removes the incentive to use false names (complementarities are the source of profitable false-name bids per Sakurai, Yokoo and Matsubara 1999). Simulations reported in the abstract show GM-SMA yields higher social surplus and seller revenue than earlier false-name-proof protocols as long as the submodular approximation is close to the true valuations. Abstract only (ACM DL abstract via Exa and mirror pages; the PDF is paywalled and Unpaywall has no OA copy). Simulation parameters, surplus numbers and the formal definition of the approximation are not visible.

## Contribution

A constructive answer to the 1999 impossibility result: give up full Pareto efficiency in general but keep VCG-style payments, and show a concrete mechanism that is false-name-proof while remaining efficient whenever valuations are close to submodular.

## Key results

- GM-SMA is false-name-proof, winner-Pareto-efficient and core/loser-collusion robust (abstract; conditions on the approximation apply).
- Better surplus and revenue than prior false-name-proof protocols in simulation when the approximation is accurate (abstract; no numbers).

## Methods and models

Combinatorial auction with quasi-linear bidders; Groves payments; submodular approximation of others' valuations; simulation comparison (details not read).

## Limitations and open questions

Abstract-only. Guarantees degrade as valuations depart from submodular; computing the approximation and winner determination is itself hard in general. Zero identity cost assumed, as in the whole false-name literature.

## Relevance to us

Part of the mechanism-design branch of sybil-resistance: shows what positive results look like once identities are free. Follows [[sakurai-1999-limitation]] and [[yokoo-2004-effect]]; broader context in [[conitzer-2010-using]], voting analogue in [[aziz-2011-false]], matching in [[todo-2013-false]]. For agent swarms, the design question "which allocation or voting rule stays truthful when one operator can spawn bidders" is exactly this.
