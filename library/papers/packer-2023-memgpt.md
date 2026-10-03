---
id: packer-2023-memgpt
type: paper
title: 'MemGPT: Towards LLMs as Operating Systems'
authors: [Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez]
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2310.08560
doi: null
arxiv: '2310.08560'
cite: 'Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I., & Gonzalez, J. E. (2023). MemGPT: Towards LLMs as Operating Systems. arXiv preprint arXiv:2310.08560.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

MemGPT applies operating-system virtual memory to LLM context. The model manages tiers of memory: a fast in-context tier and slow external stores. It moves data between them with function calls and uses interrupts to manage control flow, which gives the appearance of a context larger than the model's window. It is evaluated on analysing documents longer than the context window and on multi-session chat where agents remember, reflect and evolve across long interactions. Code and data were released at memgpt.ai.

## Contribution

It made self-editing, tiered long-term memory a standard agent architecture. The agent writes its own memory through tool calls.

## Key results

- Handles documents larger than the context window and long-term multi-session chat (abstract). Numbers not read.

## Methods and models

Virtual context management with function-call memory operations. Not read beyond the abstract.

## Limitations and open questions

No security analysis. An agent that edits its own memory is exactly the write path that later attacks exploit ([[dong-2025-memory]], [[srivastava-2025-memorygraft]]).

## Relevance to us

This describes the object that gets merged (Q3). In a MemGPT-style design, a sub-agent's state is its core and archival memory, which the agent itself edits. A fork copies these tiers, and a merge has to reconcile them. Because the agent decides what to write, an injection that changes the sub-agent's goals also changes what it chooses to archive, so the merge payload is chosen by the compromised agent. The self-editing core memory (persona and user facts) is also the natural target for the "become the attacker's agent" identity-overwrite attack that dmarz describes. No paper catalogued in this lane measures that attack directly. Compare the memory stream and reflection in [[park-2023-generative]].
