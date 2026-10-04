---
id: fish-2025-econevals
type: paper
title: "EconEvals: Benchmarks and Litmus Tests for Economic Decision-Making by LLM Agents"
authors: ["Sara Fish", "Julia Shephard", "Minkai Li", "Ran I. Shorrer", "Yannai A. Gonczarowski"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2503.18825
doi: null
arxiv: "2503.18825"
cite: "Fish, S., Shephard, J., Li, M., Shorrer, R. I., & Gonczarowski, Y. A. (2025). EconEvals: Benchmarks and Litmus Tests for Economic Decision-Making by LLM Agents. arXiv preprint arXiv:2503.18825."
topics: [agent-budgets, llm-agent-swarms]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

From the authors of [[fish-2024-algorithmic]]: benchmarks derived from procurement, scheduling and pricing that test whether an LLM learns an unknown environment in context, plus "litmus tests" that score an LLM's trade-off between conflicting objectives (litmus score), the coherence of its choices (reliability score) and its competence when the objective is single and well specified (competency score). Applied across frontier LLMs to track capability and tendency changes over time.

## Contribution

A measurement framework that separates what an LLM economic agent can do from what it tends to do.

## Key results

- Reported (abstract): framework validated for self-consistency, robustness and generalisability; specific numbers not in the abstract.

## Methods and models

Abstract read only.

## Limitations and open questions

Single-agent decision tasks; collusion is not the focus. Abstract only.

## Relevance to us

The competency-versus-tendency split is useful for the swarm factory: before attributing supra-competitive outcomes to collusion we should check that firms can compute the competitive best response (as [[deshpande-2026-strategic]] does against Nash and best-response opponents).
