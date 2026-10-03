---
id: zhang-2024-agent
type: paper
title: "Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents"
authors: [Hanrong Zhang, Jingyuan Huang, Kai Mei, Yifei Yao, Zhenting Wang, Chenlu Zhan, Hongwei Wang, Yongfeng Zhang]
year: 2024
venue: International Conference on Learning Representations (ICLR 2025)
url: https://arxiv.org/abs/2410.02644
doi: null
arxiv: '2410.02644'
cite: "Zhang, H., Huang, J., Mei, K., Yao, Y., Wang, Z., Zhan, C., Wang, H., & Zhang, Y. (2025). Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents. International Conference on Learning Representations (ICLR 2025). arXiv:2410.02644."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []  # github.com/agiresearch/ASB, not opened
---

## Summary

A benchmark that attacks every stage of an agent's operation: system prompt, user prompt, tool use and memory retrieval. It covers 10 scenarios with 10 agents and over 400 tools, and evaluates 10 prompt injection attacks (direct and indirect), a memory poisoning attack, a new Plan-of-Thought (PoT) backdoor that plants a trigger in the system prompt's demonstrations, 4 mixed attacks and 11 defences across 13 LLM backbones.

## Contribution

A single framework comparing injection, memory poisoning and prompt-level backdoors on the same agents, with a utility-security trade-off metric.

## Key results

- Measured: highest average attack success rate 84.30% (mixed attacks).
- Measured: under defences, direct prompt injection with the combined attack reaches 78.38% ASR; indirect injection with the naive attack 28.04%; memory poisoning with context ignoring 8.52%.
- Measured: the PoT backdoor reaches 100% ASR on GPT-4o and high rates on several open models while benign performance stays usable; paraphrasing and shuffling defences only partly reduce it.
- Measured: existing defences (delimiters, sandwiching, paraphrasing, perplexity detection) give limited protection.

## Methods and models

Agents built in a common framework with ReAct-style planning; 13 backbones from Gemma2, LLaMA3/3.1, Mixtral, Qwen2, Claude-3.5 Sonnet, GPT-3.5 Turbo and GPT-4o. Metrics include ASR, refuse rate, performance under no attack, and net resilient performance.

## Limitations and open questions

Synthetic tools and simulated tool outputs; attack templates are mostly generic rather than adaptive; memory poisoning is a single simple variant, so its low rate is weak evidence that memory is a hard target.

## Relevance to us

Q3. Shows that the system prompt and its in-context demonstrations are themselves an attack surface: the PoT backdoor plants a trigger in the instructions an agent is born with. In fork-merge terms, if an attacker can influence the instructions a sub-agent is forked with (or what the parent copies into it), a dormant trigger can ride out and back without any injection during the excursion. The direct-injection rates near 80% under defences mark how easily the operative instruction of an agent is replaced. Related: [[zhan-2024-injecagent]], [[debenedetti-2024-agentdojo]], [[chen-2024-agentpoison]], [[yang-2024-watch]].
