---
id: conitzer-2006-computing
type: paper
title: Computing the Optimal Strategy to Commit to
authors:
- Vincent Conitzer
- Tuomas Sandholm
year: 2006
venue: Proceedings of the 7th ACM Conference on Electronic Commerce (EC 2006), 82-90
url: https://users.cs.duke.edu/~conitzer/commitEC06.pdf
doi: 10.1145/1134707.1134717
arxiv: null
cite: Conitzer, V., & Sandholm, T. (2006). Computing the optimal strategy to commit to. In Proceedings of the 7th ACM Conference on Electronic Commerce (pp. 82-90). ACM.
topics:
- fork-merge-security
- collective-decision
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: 219 (Crossref, 2026-10-03)
code: []
---

## Summary

Gives algorithms and hardness results for the leader's optimal commitment in normal-form and Bayesian games. For two players, the optimal mixed strategy to commit to is computed by one linear program per follower action. With three or more players, or a Bayesian game with several follower types, the problem is NP-hard. The authors note that deployed software agents commit by their code. I read the abstract, introduction and results table.

## Contribution

The computational basis for Stackelberg security games and audit games ([[blocki-2013-audit]] builds on its multiple-LP method).

## Key results

- Two-player normal form, mixed commitment: polynomial (one LP per follower pure strategy).
- Bayesian game with multiple follower types: NP-hard.
- Commitment to a mixed strategy never hurts the leader under mild assumptions (cited from von Stengel and Zamir).

## Methods and models

Linear programming, reductions for hardness.

## Limitations and open questions

Exact optimisation; no robustness to wrong payoff estimates.

## Relevance to us

- Q1: a parent facing one known attacker type can compute its optimal randomised reintegration policy cheaply. If it is uncertain which of many attacker types (domains, adversaries) it faces, the exact problem is NP-hard, which is the realistic fork-merge case.
- The remark that code is a commitment device applies directly: a merge policy fixed in the parent's harness is a credible commitment.
Related: [[korzhyk-2011-stackelberg]], [[mazorra-2023-cost]].
