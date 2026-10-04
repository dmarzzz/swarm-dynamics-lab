---
id: amayuelas-2024-multiagent
type: paper
title: 'MultiAgent Collaboration Attack: Investigating Adversarial Attacks in Large Language Model Collaborations via Debate'
authors:
- Alfonso Amayuelas
- Xianjun Yang
- Antonis Antoniades
- Wenyue Hua
- Liangming Pan
- William Wang
year: 2024
venue: arXiv preprint (Semantic Scholar lists EMNLP 2024)
url: https://arxiv.org/abs/2406.14711
doi: null
arxiv: '2406.14711'
cite: 'Amayuelas, A., Yang, X., Antoniades, A., Hua, W., Pan, L., & Wang, W. (2024). MultiAgent Collaboration Attack: Investigating Adversarial Attacks in Large Language Model Collaborations via Debate. arXiv preprint arXiv:2406.14711.'
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 77 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Evaluates a network of LLMs collaborating through debate when one participant is an adversary. Introduces metrics for adversary effectiveness based on system accuracy and model agreement, finds that a model's persuasive ability largely determines how much it can sway others, explores inference-time methods for generating more compelling arguments, and tests prompt-based mitigation as a defence.

## Contribution

An early controlled measurement of a single adversarial agent steering multi-agent debate.

## Key results

- Reported in abstract: persuasiveness is the key factor in adversarial influence; prompt-based mitigation is evaluated (effect size not checked).

## Methods and models

Multi-agent debate among LLMs with one adversarial agent; accuracy and agreement metrics.

## Limitations and open questions

Abstract only. A single adversary; how influence scales when the adversary controls several debate seats (the Sybil case) is not stated in the abstract.

## Relevance to us

Debate and voting are the default aggregation in LLM swarms. If one persuasive agent can shift a debate, a principal that controls several seats can shift it further, so seat allocation needs Sybil resistance. Compare [[huang-2024-resilience]], [[ju-2024-flooding]] and the epistemic view in [[bara-2026-epistemic]].
