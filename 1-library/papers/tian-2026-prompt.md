---
id: tian-2026-prompt
type: paper
title: "Prompt Optimization Enables Stable Algorithmic Collusion in LLM Agents"
authors: ["Yingtao Tian"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2604.17774
doi: null
arxiv: "2604.17774"
cite: "Tian, Y. (2026). Prompt Optimization Enables Stable Algorithmic Collusion in LLM Agents. arXiv preprint arXiv:2604.17774."
topics: [llm-agent-swarms, agent-budgets]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

LLM agents play duopoly markets while an LLM meta-optimiser iteratively refines a shared strategic guidance prompt. The abstract reports that meta-prompt optimisation lets agents discover stable tacit collusion with better coordination than baseline agents, that the behaviour generalises to held-out markets, and that evolved prompts encode systematic coordination mechanisms through shared strategies.

## Contribution

Shows that optimising a shared prompt, not only hand-crafted prompts, can produce collusion.

## Key results

- Reported (abstract): stable tacit collusion after meta-prompt optimisation, generalising to held-out markets. No numbers in the abstract.

## Methods and models

Meta-learning loop over a shared prompt; abstract read only.

## Limitations and open questions

Abstract only. The guidance is shared across both firms, which is effectively common control.

## Relevance to us

A shared optimised prompt across firms is a soft form of the Sybil-principal condition: one optimiser shapes several firms. Relevant to fork-merge too, since a merged strategy note propagates to all forks. See [[fish-2024-algorithmic]] for the hand-crafted baseline.
