---
id: todo-2009-characterizing
type: paper
title: "Characterizing false-name-proof allocation rules in combinatorial auctions"
authors: [Taiki Todo, Atsushi Iwasaki, Makoto Yokoo, Yuko Sakurai]
year: 2009
venue: Proceedings of the 8th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2009), Budapest, pp. 265-272
url: https://www.ifaamas.org/Proceedings/aamas09/pdf/01_Full%20Papers/04a_23_131_FP_0865.pdf
doi: 10.65109/vbgn7365
arxiv: null
cite: "Todo, T., Iwasaki, A., Yokoo, M., & Sakurai, Y. (2009). Characterizing false-name-proof allocation rules in combinatorial auctions. In Proceedings of the 8th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2009), pp. 265-272. IFAAMAS. https://doi.org/10.65109/vbgn7365"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "0 (Crossref, 2026-10-03; the DOI was registered retroactively by IFAAMAS, Google Scholar counts are higher)"
code: []
---

## Summary

Splits a combinatorial auction mechanism into an allocation rule X and a payment rule p and asks which allocation rules can be made false-name-proof by some payment rule ("FN-implementable"), in the same way that weak-monotonicity (Bikhchandani et al.) characterises strategy-proof-implementable rules. The answer is a second local condition, sub-additivity: for any bidder type and any way of splitting it into k false-name types, the bundle allocated to the true type must be covered by (be a subset of the union of) the bundles the k identities would receive, paired with the appropriate inequality on marginal gains; Figure 1 gives the picture. Theorem 2: a strategy-proof mechanism is false-name-proof iff its allocation rule satisfies the sub-additivity inequality on payments; Theorem 3 (main): an allocation rule is FN-implementable iff it satisfies weak-monotonicity and sub-additivity, and the proof constructs the payment rule. Because sub-additivity is checkable by fixing the other bidders and examining local behaviour, the authors use it to audit existing mechanisms and find that two mechanisms previously believed to be false-name-proof, GM-SMA (Yokoo, Matsutani and Iwasaki, AAMAS 2006) and the Matsuo mechanism, violate sub-additivity and therefore are not false-name-proof. Read: abstract, introduction and contributions, model, Theorems 1-3 with proof outlines, Figure 1, the verification examples, conclusion.

## Contribution

Gives the allocation-rule-level characterisation of false-name-proofness (weak-monotonicity plus sub-additivity), turning Sybil-proofness of an auction into a locally checkable property and exposing two published mechanisms as broken.

## Key results

- Theorem 3: FN-implementable iff weak-monotone and sub-additive.
- Designers can concentrate on allocation rules; a payment rule always exists when both hold.
- GM-SMA and the Matsuo mechanism are not false-name-proof (counterexamples via sub-additivity).

## Methods and models

Quasi-linear combinatorial auctions, private values, false-name manipulation as splitting a type into several identifier types; characterisation proofs; worked counterexamples.

## Limitations and open questions

Characterisation assumes a rich type domain and single-minded style settings for some lemmas; it says which rules can be made false-name-proof, not how efficient they can be (that is [[iwasaki-2010-worst-case]]). Identities costless.

## Relevance to us

The practical test for whether an agent-facing allocation rule can be made Sybil-proof: check weak-monotonicity and sub-additivity. It also corrects the record on [[yokoo-2006-false]] (GM-SMA), which should not be cited as a working false-name-proof mechanism without this caveat. Lineage: [[sakurai-1999-limitation]], [[yokoo-2000-effect]], [[yokoo-2003-characterization]] (the PORF/NSA view at the mechanism level), [[yokoo-2004-effect]]; money-free analogue [[todo-2011-false-name-proof]]. Root: [[douceur-2002-sybil]].
