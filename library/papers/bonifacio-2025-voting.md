---
id: bonifacio-2025-voting
type: paper
title: "On voting rules satisfying false-name-proofness and participation"
authors: [Agustín G. Bonifacio, Federico Fioravanti]
year: 2025
venue: "arXiv preprint (econ.TH); also SSRN working paper 6438674 (2026)"
url: https://arxiv.org/abs/2503.02740
doi: null
arxiv: "2503.02740"
cite: "Bonifacio, A. G., & Fioravanti, F. (2025). On voting rules satisfying false-name-proofness and participation. arXiv:2503.02740."
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

Social-choice theory for online voting where identities cannot be verified. Two manipulations: casting duplicate votes under several identities (false-name-proofness rules this out; "strong" false-name-proofness also forbids gaining from several different votes) and gaining by abstaining (participation rules this out, i.e. no no-show paradox). Results with a variable electorate: (1) on any preference domain, false-name-proofness plus participation imply anonymity, so the rule cannot treat voters differently; hence on the universal domain no neutral rule satisfies both. (2) When alternatives are subsets of objects (committees, multi-issue referenda) and all preferences over subsets are allowed, no rule is simultaneously onto, object-neutral, tops-only, false-name-proof and participatory, and the five axioms are independent. (3) On separable preferences (an object improves any set iff it is good alone) such rules exist (voting by quota where each object needs at least one vote or unanimity, per Fioravanti and Massó 2024), and the separable domain is maximal: adding any non-separable preference breaks at least one axiom. Skimmed: introduction and conclusion; proofs not checked.

## Contribution

Uses the weaker (duplicate-vote) notion of false-name-proofness and still gets impossibility on rich domains, sharpening when Sybil-immune voting can exist.

## Key results

- FNP + participation implies anonymity (Prop. 2); no neutral rule on the universal domain (Prop. 3).
- Impossibility for onto, tops-only, object-neutral rules over all subset preferences (Thm 1).
- Separable preferences are a maximal domain for possibility (Thm 2).

## Methods and models

Axiomatic social choice with variable electorates.

## Limitations and open questions

Pure theory. The positive rules (each object needs one vote, or unanimity) are extreme, which shows how little room Sybil-immune voting has.

## Relevance to us

If agent swarms can vote in DAOs, polls or governance under cheap identities, this says what is achievable without identity verification: almost nothing neutral on rich preference domains, so practical systems need identity cost (personhood, stake) rather than clever rules. Related: [[conitzer-2010-using]], [[waggoner-2012-evaluating]], [[aziz-2011-false]], [[mazorra-2023-cost]], [[zheng-2024-sybil]].
