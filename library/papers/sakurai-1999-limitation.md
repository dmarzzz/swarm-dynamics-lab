---
id: sakurai-1999-limitation
type: paper
title: "A Limitation of the Generalized Vickrey Auction in Electronic Commerce: Robustness against False-Name Bids"
authors: [Yuko Sakurai, Makoto Yokoo, Shigeo Matsubara]
year: 1999
venue: Proceedings of the Sixteenth National Conference on Artificial Intelligence (AAAI-99), pp. 86-92, AAAI Press
url: https://cdn.aaai.org/AAAI/1999/AAAI99-013.pdf
doi: null
arxiv: null
cite: "Sakurai, Y., Yokoo, M., & Matsubara, S. (1999). A Limitation of the Generalized Vickrey Auction in Electronic Commerce: Robustness against False-Name Bids. In Proceedings of the Sixteenth National Conference on Artificial Intelligence (AAAI-99), pp. 86-92. AAAI Press. https://cdn.aaai.org/AAAI/1999/AAAI99-013.pdf"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "not available (no DOI; AAAI proceedings page gives none; OpenAlex rate-limited at access time)"
code: []
---

## Summary

The paper that introduced "false-name bids" to mechanism design, three years before Douceur named the Sybil attack. In Internet auctions an agent can cheaply submit bids under fictitious identities, which is easier than forming a coalition, and the authors ask whether the generalized Vickrey auction (GVA, the VCG mechanism for multiple units or items), which is incentive compatible and Pareto efficient under truthful single identities, survives this. Example 1 (two units of one item): agent 1 values the units ($6, $6), agent 2 ($3, $5); truthful GVA gives agent 1 both units for $8, utility $4; if agent 1 instead bids ($6, $0) and adds a false-name bid ($6, $0) as "agent 3", each identity wins one unit for $3, so agent 1 gets both units for $6 and utility $6. Theorem 1: GVA is robust to false-name bids when every agent's marginal utility is constant or diminishing (multi-unit case); Theorem 2: robust when items are substitutes. When marginal utility increases or goods are complements (tea and sugar), false-name bids are profitable and GVA is no longer incentive compatible. Theorem 3 (the negative result): under those conditions no single-round sealed-bid auction can simultaneously satisfy individual rationality, Pareto efficiency and incentive compatibility if agents can submit false-name bids. The conclusion suggests giving up Pareto efficiency and designing mechanisms that are only IR plus false-name-proof, which became the Yokoo group's research programme. Read: abstract, introduction, examples, Theorems 1-3 statements and the conclusion; proofs skimmed.

## Contribution

First formalisation of identity multiplication as a strategic manipulation in auctions, with the impossibility result that motivated the entire false-name-proof mechanism design literature.

## Key results

- Numerical example of a profitable false-name bid under increasing marginal utility (utility $4 -> $6).
- Theorems 1-2: GVA is false-name robust under constant/diminishing marginal utility and under substitutes.
- Theorem 3: no single-round sealed-bid mechanism is IR + Pareto efficient + incentive compatible when false-name bids are possible and goods can be complements.

## Methods and models

Standard quasi-linear auction model; GVA (Clarke pivot) payments; worked examples with two agents and two units or two items; impossibility proof by constructing a profitable deviation.

## Limitations and open questions

Sealed-bid single-round only; no cost to creating identities; no randomised or iterative mechanisms considered (later work covers some). The positive side (what false-name-proof mechanisms can achieve) is left to follow-up papers.

## Relevance to us

This is the mechanism-design root of Sybil resistance and belongs in the sybil-resistance survey's seminal list alongside [[douceur-2002-sybil]]: it shows that even a theoretically ideal allocation rule collapses when identities are free, independent of any network or cryptographic setting. Direct descendants in the library: [[yokoo-2004-effect]], [[aziz-2011-false]], [[todo-2013-false]], [[conitzer-2010-using]]; the economics of identity cost in [[kash-2012-optimizing]]. For LLM agent swarms the lesson is that any market or voting among agents where one operator can spawn identities needs a false-name-proof rule, not just a Sybil detector.
