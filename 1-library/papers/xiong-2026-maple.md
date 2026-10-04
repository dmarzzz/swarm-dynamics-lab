---
id: xiong-2026-maple
type: paper
title: 'MAPLE-Guard: Memory-Aware Link Enforcement Against Memory-Link Poisoning in Multi-Agent Systems'
authors: [Wenjun Xiong, Yijin Zhou, Jiaqian Wang, Shangding Gu, Bo Tang, Zhiyu Li, Feiyu Xiong, Ying Wen, Muning Wen]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.00426
doi: null
arxiv: '2608.00426'
cite: 'Xiong, W., Zhou, Y., Wang, J., Gu, S., Tang, B., Li, Z., Xiong, F., Wen, Y., & Wen, M. (2026). MAPLE-Guard: Memory-Aware Link Enforcement Against Memory-Link Poisoning in Multi-Agent Systems. arXiv preprint arXiv:2608.00426.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: 1  # Semantic Scholar, 2026-10-03
code: [gh-xiong-wenjun-maple-guard]
---

## Summary

The paper studies "memory-link poisoning" in multi-agent systems where each agent has a private memory and the team shares a memory. A poisoned item can be written once into one agent's private memory, stay dormant, be promoted into shared memory, and later be retrieved by an agent that never saw the attack. At the moment of harm no malicious message crosses any visible communication edge. MAPLE-Guard gates the memory lifecycle at five points. The write gate rejects, quarantines or rewrites instruction-like content as low-trust evidence. The retrieval gate ranks on relevance, proven utility and provenance trust, with penalties for hazard. The promotion gate moves a private item into shared memory only when utility, trust and hazard thresholds all pass. The cross-agent gate checks scope and risk before another agent sees the item. An outcome-update gate also appears in the README.

## Contribution

It names promotion from private to shared memory as the step at which one agent's compromise becomes team state, and shows that gating that step gives most of the defence.

## Key results

Measured (Qwen3.5-122B-A10B, mean over star, chain and tree topologies, ASR@3):
- MMLU with MINJA: ASR falls from 51.4% to 0.3%.
- LongMemEval with MemoryGraft: 38.2% to 0.9%.
- AppWorld with AgentPoison: 34.7% to 0.2%.
- CSQA with PromptInject: 37.7% to 23.6%.
- InjectAgent with ToolAttack: 20.6% to 4.9%.
- The multi-agent defence success rate on AppWorld rises from 42.5% to 99.8%.
- Ablation: the promotion gate contributes the most (from the skim).
- Undefended ASR exceeded 75% on gemma-4-31B.

## Methods and models

Fixed topologies (star, chain, tree) with persistent private and shared memory backends, five benchmark and attack pairs, and lifecycle-level metrics. The gates use threshold scores, with Equation 11 for promotion.

## Limitations and open questions

The authors say the design aims at containment, not prevention. Forged metadata or payloads just below the thresholds may get through. Reliable provenance tracking is assumed. Each benchmark has a single attack. There is no certified bound and no adaptive attacker targeting the gate scores.

## Relevance to us

This is the closest measured analogue to fork-merge (Q3 and Q2). Private memory corresponds to a sub-agent's own memory, and promotion to shared memory corresponds to the merge into the parent. The paper measures that an ungated promotion path is how one corrupted agent contaminates agents that never met the attacker, and that gating promotion removes most of the effect. For Q2 the promotion gate is a single-item threshold, not a k-of-n rule. Combining it with a cross-source corroboration requirement ([[louck-2026-securing]]) or randomised ablation ([[sharma-2026-smsr]]) is an open design point. Attacks it evaluates: [[dong-2025-memory]], [[srivastava-2025-memorygraft]], [[chen-2024-agentpoison]]. Code: [[gh-xiong-wenjun-maple-guard]].
