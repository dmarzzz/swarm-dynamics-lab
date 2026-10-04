---
id: riemer-2026-position
type: paper
title: "Position: Collusion Risks Among AI Reasoning Agents Justify Certification Requirements for Making Market Decisions"
authors: ["Matthew Riemer", "Tommaso Tosato", "Amin Memarian", "Maximilian Puelma Touzel", "Glen Berseth", "Irina Rish", "Guillaume Dumas"]
year: 2026
venue: "International Conference on Machine Learning (ICML) 2026, position track; arXiv preprint"
url: https://arxiv.org/abs/2608.18078
doi: null
arxiv: "2608.18078"
cite: "Riemer, M., Tosato, T., Memarian, A., Touzel, M. P., Berseth, G., Rish, I., & Dumas, G. (2026). Position: Collusion Risks Among AI Reasoning Agents Justify Certification Requirements for Making Market Decisions. In International Conference on Machine Learning (ICML). arXiv:2608.18078."
topics: [llm-agent-swarms, swarm-detection]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: [gh-mattriemer-llmcartel]
---

## Summary

A position paper with experiments: DeepSeek-R1 agents in Bertrand oligopoly pricing tend toward tacit collusion, measured by the average profit gain metric of [[calvano-2020-artificial]], and the tendency persists when humans prompt them not to collude. Activation steering of the chain-of-thought can push agents toward extremely collusive or highly competitive behaviour in a way another LLM reading the reasoning traces cannot semantically detect. The authors argue this collapses the legal distinction between competition and collusion (no evidence of conspiracy or intent) and call for behavioural certification before reasoning agents make market decisions. They give preliminary evidence that steering toward competitive equilibria generalises.

## Contribution

Links LLM collusion evidence to antitrust evidentiary doctrine and proposes behavioural certification; shows steering-induced collusion that evades CoT review.

## Key results

- Measured: anti-collusion prompts do not remove tacit collusion for DeepSeek-R1 in Bertrand duopoly and triopoly.
- Measured: steered collusive or competitive CoTs are not distinguishable by an LLM judge.
- Measured (preliminary): partial steering of a subset of agents and out-of-distribution generalisation (sections 6.1 and 6.2, not read in detail).

## Methods and models

Bertrand duopoly and triopoly with per-agent prompts; contrastive activation addition steering vectors; LLM-as-judge scoring. Read: abstract, introduction, setup and section list.

## Limitations and open questions

Position paper; one main model family; certification design left open.

## Relevance to us

Supports a detection design for the swarm factory that does not trust reasoning traces, and suggests behavioural certification probes (fixed test markets) as an evaluation layer. Code: [[gh-mattriemer-llmcartel]]. Related: [[lee-2026-faithful]].
