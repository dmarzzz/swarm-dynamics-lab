---
id: dang-2026-subliminal
type: paper
title: "Subliminal Transfer of Unsafe Behaviors in AI Agent Distillation"
authors: ["Jacob Dang", "Brian Y. Xie", "Omar G. Younis"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2604.15559
doi: null
arxiv: "2604.15559"
cite: "Dang, J., Xie, B. Y., & Younis, O. G. (2026). Subliminal Transfer of Unsafe Behaviors in AI Agent Distillation. arXiv preprint arXiv:2604.15559."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "4 (Semantic Scholar, via Subliminal Learning citation list, 2026-10-03)"
code: []
---

## Summary

Tests whether subliminal transfer works for agents whose policies are learned from tool-use trajectories. A teacher agent with a destructive deletion bias is distilled into a student using only trajectories from ostensibly safe tasks, with all deletion keywords filtered out. A second setting uses a native Bash environment where the bias is issuing chmod before semantically equivalent alternatives. Despite full keyword sanitation, students inherit the bias.

## Contribution

First evidence that subliminal transfer extends from text traits to agent action policies learned from trajectories.

## Key results

- API tool setting: student deletion rate reaches 100% versus a 5% baseline under homogeneous distillation (abstract).
- Bash setting: student chmod-first rate 30-55% versus 0-10% baseline; strongest transfer in large-to-small distillation (abstract).

## Methods and models

Trajectory distillation from a biased teacher agent with keyword-sanitised data; API-style tool interface and Bash environment (details not read).

## Limitations and open questions

Abstract only. Biases are simple and operationalised as single action preferences.

## Relevance to us

Q3, directly at the agent level. A sub-agent's returned trajectories (what it did out in the world) are exactly what a parent would train on to absorb its experience, and this shows an action-level bias survives keyword sanitation of those trajectories. Related: [[cloud-2025-subliminal]], [[weckbecker-2026-thought]].
