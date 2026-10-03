---
id: li-2026-state
type: paper
title: State-dependent error correlations shape voting thresholds in committees of AI agents
authors:
- Haifeng Li
- Mo Hai
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2607.23931
doi: null
arxiv: '2607.23931'
cite: 'Li, H., & Hai, M. (2026). State-dependent error correlations shape voting thresholds in committees of AI agents. arXiv preprint arXiv:2607.23931.'
topics:
- fork-merge-security
- collective-decision
- llm-agent-swarms
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Classical voting guarantees for committees assume independent errors, but language-model errors co-occur on the same cases. The authors combine Sah-Stiglitz screening with error dependence that can differ between good and bad cases. In a homogeneous exchangeable Gaussian-copula model, shared errors create a positive asymptotic error floor for majority voting and can change the loss-minimising approval threshold. They estimate a heterogeneous version from 174,384 votes by 28 language models on four binary-screening benchmarks, fit on odd items and predict committee loss on even items.

## Contribution

Turns "LLM errors are correlated" into a committee-design quantity: the voting threshold that minimises loss depends on state-dependent correlation, and majority voting has a non-zero error floor as n grows.

## Key results

- Proved (per abstract): with exchangeable shared errors, majority voting has a positive asymptotic error floor.
- Measured (per abstract): modelling the full dependence matrix raised identity-line R^2 for predicted committee loss from 0.840 (independence) to 0.967.
- Measured (per abstract): cost-sensitive threshold choice under independence cut scaled loss from 60.25 (majority) to 52.50; modelling dependence cut it to 50.77 (gain 1.73, 95 percent bootstrap CI 0.68 to 2.33); total reduction from majority 15.73 percent.

## Methods and models

Sah-Stiglitz screening model, Gaussian copula with state-dependent correlation, held-out prediction on 28 models and four benchmarks. Only the abstract was read.

## Limitations and open questions

Binary screening tasks; natural errors; no adversary.

## Relevance to us

Q2. Gives the formal reason a k-of-n merge rule cannot be pushed to arbitrary safety by raising n when parts share a base model: correlated errors leave an error floor. It also says the right k is not fixed at a majority; it should be set from measured correlation, and correlation may differ on the cases that matter (the "bad" states), which in the fork-merge setting are the attacker-controlled inputs. Related: [[kim-2025-correlated]], [[chen-2026-when]], [[knight-1986-experimental]].
