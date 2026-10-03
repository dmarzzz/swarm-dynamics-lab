---
id: kaesberg-2025-voting
type: paper
title: 'Voting or Consensus? Decision-Making in Multi-Agent Debate'
authors: [Lars Benedikt Kaesberg, Jonas Becker, Jan Philip Wahle, Terry Ruas, Bela Gipp]
year: 2025
venue: Findings of ACL 2025 (arXiv preprint)
url: https://arxiv.org/abs/2502.19130
doi: 10.18653/v1/2025.findings-acl.606
arxiv: '2502.19130'
cite: 'Kaesberg, L. B., Becker, J., Wahle, J. P., Ruas, T., & Gipp, B. (2025). Voting or Consensus? Decision-Making in Multi-Agent Debate. Findings of the Association for Computational Linguistics: ACL 2025. arXiv preprint arXiv:2502.19130.'
topics: [llm-agent-swarms, collective-decision]
added_by: shadow/sol-1
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

A one-variable-at-a-time comparison of seven decision protocols (majority voting, unanimity consensus and others) in multi-agent debate, on knowledge and reasoning tasks. Reported: voting protocols improve reasoning-task performance by 13.2% and consensus protocols improve knowledge-task performance by 2.8% relative to other protocols; increasing the number of agents improves performance while more discussion rounds before voting reduce it. Two proposed methods to raise answer diversity, All-Agents Drafting (up to +3.3%) and Collective Improvement (up to +7.4%). Version 4 updated 2026-09-30. Abstract only.

## Contribution

Isolates the aggregation rule as its own variable in debate, complementing [[choi-2025-debate]] (voting explains most debate gains) and [[bertalanic-2026-ringelmann]] (more rounds raise agreement, not accuracy). The "more rounds hurt" finding is a Ringelmann-style result in a different vocabulary.

## Key results

- Reported: voting +13.2% on reasoning, consensus +2.8% on knowledge tasks.
- Reported: performance rises with agent count and falls with discussion rounds before the vote.

## Methods and models

Seven decision protocols, matched discussion parameters, knowledge and reasoning benchmarks. Models and N not read.

## Limitations and open questions

- Abstract-level read.
- Reports accuracy only; no agreement or N_eff measure, so cannot say whether the agent-count gain is independent evidence or correlated sampling.

## Relevance to us

Background for choosing the aggregation rule in any consensus experiment; the rounds-hurt finding is a cheap thing to replicate while measuring agreement alongside accuracy.
