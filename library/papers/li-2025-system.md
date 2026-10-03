---
id: li-2025-system
type: paper
title: "System Prompt Poisoning: Persistent Attacks on Large Language Models Beyond User Injection"
authors: [Zongze Li, Jiawei Guo, Haipeng Cai]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2505.06493
doi: null
arxiv: '2505.06493'
cite: "Li, Z., Guo, J., & Cai, H. (2025). System Prompt Poisoning: Persistent Attacks on Large Language Models Beyond User Injection. arXiv:2505.06493."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Introduces system prompt poisoning: an attacker who can alter the system prompt (rather than a single user message) persistently affects every subsequent interaction. Four practical attack strategies are evaluated on generative and reasoning LLMs across mathematics, coding, logical reasoning and NLP tasks.

## Contribution

Frames the system prompt as a persistence channel distinct from per-turn injection.

## Key results

- Reported (abstract): system prompt poisoning is highly feasible without jailbreak techniques and effective across a wide range of tasks.
- Reported (abstract): it remains effective when user prompts use chain-of-thought.
- Reported (abstract): it significantly weakens the benefit of chain-of-thought and retrieval augmentation.

## Methods and models

Four poisoning strategies on generative and reasoning LLMs. Only the abstract was read.

## Limitations and open questions

Assumes write access to the system prompt; abstract-level reading.

## Relevance to us

Q3. In fork-merge the "system prompt" of a sub-agent is whatever the parent hands it at fork plus whatever it rewrites for itself during the excursion. If the excursion can rewrite that standing instruction (for example a self-maintained mission file), the corruption is persistent for every later step and, after merge, for whatever the parent inherits from it. Pairs with the Plan-of-Thought backdoor in [[zhang-2024-agent]] and the cross-session persistence measurements in [[xie-2026-what]].
