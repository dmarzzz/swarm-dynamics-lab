---
id: kash-2009-manipulating
type: paper
title: "Manipulating Scrip Systems: Sybils and Collusion"
authors: [Ian A. Kash, Eric J. Friedman, Joseph Y. Halpern]
year: 2009
venue: Auctions, Market Mechanisms and Their Applications (AMMA 2009), LNICST vol. 14, pp. 13-24
url: https://arxiv.org/abs/0903.2278
doi: 10.1007/978-3-642-03821-1_4
arxiv: "0903.2278"
cite: "Kash, I. A., Friedman, E. J., & Halpern, J. Y. (2009). Manipulating Scrip Systems: Sybils and Collusion. In Auctions, Market Mechanisms and Their Applications (AMMA 2009), LNICST 14, pp. 13-24. Springer. https://doi.org/10.1007/978-3-642-03821-1_4"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "3 (Crossref, 2026-10-03)"
code: []
---

## Summary

Workshop paper that isolates the Sybil and collusion analysis later folded into the Distributed Computing article ([[kash-2012-optimizing]]). Game-theoretic analyses of P2P systems usually stop at Nash equilibrium, which excludes multi-identity and multi-agent strategic behaviour; this paper examines both in scrip systems. Sybils raise the owner's chance of being chosen to provide service, which generally makes it harder for agents without Sybils to earn scrip and lowers social welfare, yet in certain circumstances (when the designer has set the money supply too low) Sybils can make everyone better off by effectively increasing the supply of work opportunities; collusion (pooling scrip within a group) tends to make all agents better off, not only colluders, unless colluders can relay requests to each other, in which case it behaves like Sybils. The authors read these results as guidance on whether to allow advertising and loans, and argue that existing refinements of Nash equilibrium that address collusion (strong Nash, coalition-proof Nash, k-resilient equilibria) do not adequately capture Sybil and collusion effects in scrip systems because they ignore identity creation and the systemic (money-supply) channel. Read from the arXiv version: abstract, introduction, model recap, Sybil and collusion sections, discussion of solution concepts, conclusion; numerical details skimmed (same simulations as the 2012 paper, n = 1,000 agents).

## Contribution

Earliest quantitative statement of how Sybils and collusion move a scrip economy, including the counterintuitive case where Sybils help, and a critique of equilibrium refinements for ignoring identity multiplication.

## Key results

- Sybils shift the optimal money-supply point and can crash a tuned system; a few Sybils per holder help the holder a lot, more help little.
- Sybils can raise total welfare when the money supply was set too low.
- Collusion is welfare-positive unless colluders can pass requests (then equivalent to Sybils).
- Strong/coalition-proof/k-resilient equilibria do not capture these effects.

## Methods and models

Threshold-strategy scrip model from Friedman, Halpern and Kash (EC 2006), equilibrium analysis plus simulation; see the 2012 journal version for parameters and figures.

## Limitations and open questions

Superseded in detail by [[kash-2012-optimizing]]; same modelling assumptions (single service, uniform volunteer choice, costless identities); workshop length.

## Relevance to us

Cite the 2012 journal version for numbers; this entry matters for its explicit argument that standard equilibrium concepts are the wrong lens for Sybil questions in agent economies, which is also the motivation behind the DSL-strategies framing in [[gafni-2023-optimal]]. Lineage: [[friedman-2006-efficiency]] -> this -> [[kash-2012-optimizing]]. Root: [[douceur-2002-sybil]].
