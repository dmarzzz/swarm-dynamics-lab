---
id: griffin-2024-games
type: paper
title: 'Games for AI Control: Models of Safety Evaluations of AI Deployment Protocols'
authors: [Charlie Griffin, Louis Thomson, Buck Shlegeris, Alessandro Abate]
year: 2024
venue: arXiv preprint (Semantic Scholar lists Proceedings of IASEAI Conference)
url: https://arxiv.org/abs/2409.07985
doi: null
arxiv: '2409.07985'
cite: 'Griffin, C., Thomson, L., Shlegeris, B., & Abate, A. (2024). Games for AI Control: Models of Safety Evaluations of AI Deployment Protocols. arXiv:2409.07985.'
topics: [fork-merge-security, marl-emergence]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 32 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Formalises the red-team exercise of AI control as an AI-Control Game: a multi-objective, partially observable, stochastic game between a protocol designer and an adversary. They give reductions from these games to a special case of zero-sum partially observable stochastic games, so existing solvers can find Pareto-optimal protocols. Applied to trusted monitoring of an untrusted programming assistant (the setting of [[greenblatt-2023-ai]]), they report improvements over the empirical protocols, evaluate new settings, and make explicit the implicit assumptions in earlier control work. Numbers are in the body, which I did not read.

## Contribution

A game-theoretic model in which protocol parameters such as audit allocation can be solved for rather than hand-tuned.

## Key results

- Reductions from multi-objective control games to zero-sum POSGs (abstract).
- Synthesised trusted-monitoring protocols improve on empirical ones (abstract; magnitude not checked).

## Methods and models

Partially observable stochastic games; Pareto-frontier search over safety and usefulness.

## Limitations and open questions

Abstract only on my side. Single untrusted agent; no model of multiple forks or merges.

## Relevance to us

- Q2 (thresholds): the right formal home for a merge protocol is this kind of game, with the parent as protocol designer and the attacker choosing which children to corrupt; extending it to n children and a k-threshold merge looks like an open modelling step (inferred, not checked against later work).
- Q1 (hiding): partial observability of the attacker is explicitly part of the model, so "hide which child returns" can be expressed as restricting the attacker's observation.
Related: [[gardner-challis-2026-when]] (same group, statistical safety case), [[mallen-2024-subversion]].
