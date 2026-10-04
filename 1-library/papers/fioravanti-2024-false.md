---
id: fioravanti-2024-false
type: paper
title: "False-name-proof and strategy-proof voting rules under separable preferences"
authors: [Federico Fioravanti, Jordi Massó]
year: 2024
venue: Theory and Decision, vol. 97, no. 2, pp. 391-408
url: https://link.springer.com/content/pdf/10.1007/s11238-023-09973-5.pdf
doi: 10.1007/s11238-023-09973-5
arxiv: null
cite: "Fioravanti, F., & Massó, J. (2024). False-name-proof and strategy-proof voting rules under separable preferences. Theory and Decision, 97(2), 391-408. https://doi.org/10.1007/s11238-023-09973-5"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "not checked (OpenAlex budget exhausted 2026-10-03)"
code: []
---

## Summary

Social-choice characterisation of voting rules that survive Sybil voting. Setting: a society chooses a subset from a set of objects (candidates, binary issues) and voters have separable preferences (adding an object improves a set iff the object is good on its own), the domain for which Barberà, Sonnenschein and Zhou (1991) showed strategy-proof, onto rules are exactly "voting by committees" and the neutral ones "voting by quota". A rule is false-name-proof if no voter gains by repeating her own vote under extra identities, and strongly false-name-proof if no voter gains by casting several different votes. Theorem 1: the rules that are false-name-proof, strategy-proof and onto are exactly voting by quota where each object is chosen if it gets at least one vote (quota 1, any voter can impose it) or only if it gets a unanimous vote (quota n, any voter can veto it). Corollary 1 shows strong false-name-proofness gives the same class here. Auxiliary results: any false-name-proof, strategy-proof, onto rule is automatically anonymous (voter names cannot matter, Proposition 3), such rules also satisfy participation (Proposition 6), and in any domain strongly false-name-proof plus anonymity plus participation implies strategy-proofness (Proposition 8), with Example 1 showing the weak version does not. The final remark is blunt: the two incentive requirements together only leave "extreme forms of unanimity" that are unappealing for large electorates. Motivated by online polls, MOOC admissions, rating systems and auctions where identities are unverified. Read abstract, introduction, result overview and final remark; proofs and the independence examples in Section 3 skimmed.

## Contribution

Shows that even on a well-behaved restricted domain (separable preferences) where many strategy-proof rules exist, adding Sybil-resistance collapses the admissible rules to unanimity-or-veto quotas, strengthening the negative message of Conitzer (2008) and Bu (2013) for unrestricted domains.

## Key results

- Theorem 1: false-name-proof + strategy-proof + onto on separable preferences = voting by quota with quota in {1, n} per object.
- Corollary 1: same class under strong false-name-proofness.
- Proposition 3: false-name-proof + strategy-proof + onto implies anonymous.
- Proposition 8: strongly false-name-proof + anonymous + participation implies strategy-proof (any domain); fails for weak false-name-proofness (Example 1).

## Methods and models

Axiomatic social choice; variable electorates (rules defined for every finite voter set); separable preference domain; deterministic rules. No experiments.

## Limitations and open questions

Deterministic rules only (randomised rules, as in Conitzer 2008, can do somewhat better). Identity creation is free and unbounded; no cost-of-identity or verification model, so the result is the worst case. The authors do not discuss approximate or Bayesian relaxations.

## Relevance to us

Hard limit for any collective-decision layer in an open agent swarm: if agents can vote and spawn identities, the only incentive-compatible aggregations are "anyone can impose" or "anyone can veto", neither of which is a sensible consensus rule, so swarm voting must rely on identity cost, admission control or proof of personhood rather than on the rule itself. Companion to the auction-side false-name results ([[yokoo-2004-effect]], [[yokoo-2007-making]], [[gafni-2023-optimal]], [[conitzer-2010-using]], [[todo-2013-false]]) and to the mechanism survey [[pan-2024-sybil]].
