---
id: blocki-2013-audit
type: paper
title: Audit Games
authors:
- Jeremiah Blocki
- Nicolas Christin
- Anupam Datta
- Ariel D. Procaccia
- Arunesh Sinha
year: 2013
venue: arXiv preprint; IJCAI 2013 version (pages not checked)
url: https://arxiv.org/abs/1303.0356
doi: null
arxiv: '1303.0356'
cite: Blocki, J., Christin, N., Datta, A., Procaccia, A. D., & Sinha, A. (2013). Audit Games. arXiv:1303.0356 (IJCAI 2013).
topics:
- fork-merge-security
- collective-decision
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Extends the security-game model with a punishment rate: a defender (auditor) chooses which of n targets to audit with one resource and a punishment level x, which is costly to the defender. The adversary picks a target as a best response. Computing the Stackelberg equilibrium has non-convex quadratic constraints; the paper gives an additive FPTAS. Motivated by hospital audits of record access. I read the introduction, model and algorithm overview.

## Contribution

Joins Becker's crime-and-punishment trade-off ([[becker-1968-crime]]) with committed randomised auditing, and makes it computable.

## Key results

- Additive FPTAS for the optimal audit probabilities plus punishment rate (proved).
- Argues the Stackelberg concept fits audits because audit mechanisms should be secure when published, the security-through-obscurity principle.

## Methods and models

Stackelberg audit game, multiple-LP method of [[conitzer-2006-computing]], approximation scheme.

## Limitations and open questions

One audit resource; rational adversary; fixed deterministic punishment.

## Relevance to us

- Q1: a direct template for pre-merge auditing of children, with the extra lever of penalty on a child caught returning corrupted (for example, discarding its whole branch). Penalty and audit probability trade off, but see [[gans-2026-when-does]] for why this substitution breaks when the agent can learn or erase the evidence.
Related: [[blocki-2015-audit]], [[avenhaus-2002-inspection]].
