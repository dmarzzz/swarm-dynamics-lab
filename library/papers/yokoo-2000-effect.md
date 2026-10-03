---
id: yokoo-2000-effect
type: paper
title: "The effect of false-name declarations in mechanism design: towards collective decision making on the Internet"
authors: [Makoto Yokoo, Yuko Sakurai, Shigeo Matsubara]
year: 2000
venue: Proceedings of the 20th IEEE International Conference on Distributed Computing Systems (ICDCS 2000), Taipei, pp. 146-153
url: https://ieeexplore.ieee.org/document/840916
doi: 10.1109/icdcs.2000.840916
arxiv: null
cite: "Yokoo, M., Sakurai, Y., & Matsubara, S. (2000). The effect of false-name declarations in mechanism design: towards collective decision making on the Internet. In Proceedings of the 20th IEEE International Conference on Distributed Computing Systems (ICDCS 2000), pp. 146-153. IEEE. https://doi.org/10.1109/ICDCS.2000.840916"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "22 (Crossref, 2026-10-03)"
code: []
---

## Summary

Generalises the authors' 1999 false-name-bid result from auctions to mechanism design at large, for open dynamic environments such as the Internet where the designer cannot fully identify participants. Contributions per the abstract: a formal model of mechanism design in which agents may make false-name declarations (one agent acting under several identifiers) and may also hide (not participate under some identifiers); a proof that the revelation principle still holds in this model, so attention can be restricted to direct mechanisms where each identifier reports a type truthfully; an impossibility result that when false-name declarations and hiding are possible no auction protocol achieves Pareto efficient allocations in dominant strategies for all cases; and a sufficient condition under which the Clarke (pivotal/VCG) mechanism is robust to false names, namely concavity of the maximal total utility as a function of the set of agents (no complementarities to exploit). Abstract only (IEEE Xplore, paywalled; Crossref carries no year, confirmed April 2000 from the Xplore page). Note this is distinct from the 2004 Games and Economic Behavior paper [[yokoo-2004-effect]] with a nearly identical title that treats combinatorial auctions specifically.

## Contribution

Establishes the false-name mechanism design framework (model, revelation principle, general impossibility, concavity condition for VCG robustness) that the later combinatorial-auction, voting and matching results build on.

## Key results

- Revelation principle holds under false-name declarations and hiding.
- No dominant-strategy Pareto-efficient auction exists in general when false names and hiding are possible.
- Clarke mechanism is false-name-proof when maximal total utility is concave in the agent set.

## Methods and models

Quasi-linear mechanism design with an identifier/agent distinction; dominant-strategy equilibrium; proofs not read.

## Limitations and open questions

Abstract-level read; no quantification; identities costless. The concavity condition is a sufficient condition and the paper's title promise ("collective decision making") is developed later in the voting work of others.

## Relevance to us

Foundational citation for the mechanism-design strand of Sybil resistance: the formal statement that free identities break efficiency in dominant strategies unless valuations lack complementarities. Chain: [[sakurai-1999-limitation]] -> this -> [[yokoo-2003-characterization]] -> [[yokoo-2004-effect]] -> [[yokoo-2006-false]]; voting and matching analogues in [[bachrach-2008-divide]], [[aziz-2011-false]], [[todo-2013-false]]; overview [[conitzer-2010-using]]. Root: [[douceur-2002-sybil]].
