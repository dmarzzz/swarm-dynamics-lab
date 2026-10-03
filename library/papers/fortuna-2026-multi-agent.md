---
id: fortuna-2026-multi-agent
type: paper
title: Multi-agent Scaling Across Disjunctive and Compensatory Tasks
authors:
- Carolina Fortuna
- Blaz Bertalanic
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.31563
doi: null
arxiv: '2609.31563'
cite: Fortuna, C., & Bertalanic, B. (2026). Multi-agent Scaling Across Disjunctive and Compensatory Tasks. arXiv preprint arXiv:2609.31563.
topics:
- llm-agent-swarms
- collective-decision
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

The paper imports Steiner's (1972) taxonomy of group tasks from social psychology to explain why LLM team scaling depends on the task. Treating independently sampled agents as conditionally independent given the item, plurality voting converges to the model's modal answer and averaging converges to the model's item-level bias as team size grows. Across representative benchmarks, 13 open-weight models and teams of up to 30 agents: on disjunctive tasks (one correct member suffices) the chance that at least one agent is right rises 5-20 points with team size, but plurality voting realises almost none of that potential, as predicted to within 0.5 points; multi-round revision helps, but one peer gives nearly the same gain as 29. On Fermi estimation (compensatory, averaging) shared item-level bias accounts for ~87% of squared error, so averaging cuts error by only ~6%.

## Contribution

A clean theoretical frame (Steiner task types plus conditional independence) for "wisdom of the silicon crowd" failures: correlated errors set the ceiling. Fits with [[bertalanic-2026-ringelmann]] (same authors), [[yang-2026-understanding]] and [[li-2024-more]].

## Key results

- Claimed: pass@N-style potential grows 5-20 points with team size on disjunctive tasks; plurality voting realises almost none of it (model error < 0.5 points).
- Claimed: revision with 1 peer ~ revision with 29 peers.
- Claimed: on Fermi estimation, shared bias explains ~87% of squared error; averaging reduces error ~6%.
- Claimed: mixing model families helps on Fermi estimation but not beyond the strongest member on disjunctive tasks.

## Methods and models

13 open-weight models, teams up to 30, plurality voting, averaging and multi-round revision; analytic large-team limits under conditional independence.

## Limitations and open questions

Abstract-level read. Independence given the item is an assumption that interaction violates; the paper's focus is aggregation rather than dynamics.

## Relevance to us

Useful null model for any swarm aggregation experiment: if agents share a model, expect the large-N limit to be the model's own mode or bias. Related: [[chen-2024-are]], [[kim-2025-towards]].
