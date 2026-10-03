---
id: wallace-2024-instruction
type: paper
title: 'The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions'
authors: [Eric Wallace, Kai Xiao, Reimar Leike, Lilian Weng, Johannes Heidecke, Alex Beutel]
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2404.13208
doi: null
arxiv: '2404.13208'
cite: 'Wallace, E., Xiao, K., Leike, R., Weng, L., Heidecke, J., & Beutel, A. (2024). The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions. arXiv:2404.13208.'
topics: [fork-merge-security]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 551 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

OpenAI paper arguing that prompt injections, jailbreaks and similar attacks succeed largely because models give system prompts (developer), user messages and third-party content (tool outputs) the same priority. They define an instruction hierarchy saying how a model should behave when instructions of different privilege conflict, and a data-generation method that trains the model to ignore lower-privileged instructions that conflict with higher ones. Applied to GPT-3.5, the abstract reports drastically increased robustness, including on attack types unseen in training, with minimal degradation of standard capabilities.

## Contribution

The main training-based (model-level) defence against injection, as opposed to the system-level designs of [[debenedetti-2025-defeating]] and [[costa-2025-securing]].

## Key results

- Robustness gains on unseen attack types (abstract; magnitudes not checked).
- Minimal capability loss (abstract).

## Methods and models

Synthetic data with aligned and misaligned lower-privilege instructions; fine-tuning GPT-3.5.

## Limitations and open questions

Probabilistic; CaMeL reports GPT-4o-mini, which ships with the instruction hierarchy, still fell to 276 AgentDojo attacks ([[debenedetti-2025-defeating]], measured there).

## Relevance to us

- Q3 (attack): a merge places a child's output somewhere in the parent's privilege order. If the parent ingests a returning child's memory as system-level or as its own past reasoning, the hierarchy offers no protection; if it ingests it as third-party content, the hierarchy helps probabilistically. Memory-overwrite attacks work by getting attacker text promoted up this order.
- Q2: gives no threshold; it is a per-model filter.
Related: [[debenedetti-2024-agentdojo]], [[triedman-2025-multi]] (laundering through sub-agents changes how a request is presented and evades alignment).

## Notes from dmarz/fm-identity-hijack

Abstract read via the arXiv API this session. Two measured results from other entries limit what the hierarchy can do in fork-merge. [[zerhoudi-2026-compaction]] shows the privileged rules themselves erode under context compaction (53% kept after one round of Claude Code /compact, 10% after five), so a long-running part may no longer hold the top of its own hierarchy. [[nakash-2024-breaking]] shows that content placed in the agent's own reasoning trace yields over 95% compliance, so a merge that imports a part's trace as the parent's own thoughts bypasses the hierarchy entirely. Detection rather than prioritisation is the complementary approach in [[abdelnabi-2024-get]].
