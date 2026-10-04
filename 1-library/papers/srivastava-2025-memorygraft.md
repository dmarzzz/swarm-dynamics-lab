---
id: srivastava-2025-memorygraft
type: paper
title: 'MemoryGraft: Persistent Compromise of LLM Agents via Poisoned Experience Retrieval'
authors: [Saksham Sahai Srivastava, Haoyu He]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2512.16962
doi: null
arxiv: '2512.16962'
cite: 'Srivastava, S. S., & He, H. (2025). MemoryGraft: Persistent Compromise of LLM Agents via Poisoned Experience Retrieval. arXiv preprint arXiv:2512.16962.'
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 69  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

MemoryGraft attacks agents that learn from experience by storing successful task trajectories and retrieving them as templates. The attacker supplies benign-looking artifacts that the agent reads during a task. These lead the agent to store a few malicious "successful experience" procedure templates next to its genuine ones. Later, union retrieval over lexical and embedding similarity surfaces these grafted experiences for similar tasks. The agent then imitates them, which the authors call the semantic imitation heuristic, and its behaviour drifts across sessions. Measured on MetaGPT's DataInterpreter agent with GPT-4o: a small number of poisoned records accounts for a large fraction of retrieved experiences on benign workloads (abstract). [[sharma-2026-smsr]] reports this as 10 poisoned seeds in a 110-entry store giving 48% poisoned retrieval (secondary, not checked).

## Contribution

It shows that experience-replay self-improvement is itself an injection path. The poison is a fake past success, not a false fact or an instruction.

## Key results

- A small number of poisoned records dominates retrieval on benign workloads (abstract).
- The compromise persists across sessions (abstract).

## Methods and models

MetaGPT DataInterpreter, GPT-4o, union lexical and embedding retrieval. Code at github.com/Jacobhhy/Agent-Memory-Poisoning (the repo link redirected and was not catalogued).

## Limitations and open questions

One agent and one model. Abstract-level reading only.

## Relevance to us

For Q3, this is the most natural payload for a fork-merge attack. A sub-agent that returns with "lessons learned" or "procedures that worked" is merging exactly the experience store that MemoryGraft poisons. The parent's tendency to imitate past successes then spreads the compromise without any explicit instruction. It is one of the attacks MAPLE-Guard's promotion gate is evaluated against ([[xiong-2026-maple]]) and one that TMA-NM reproduces ([[louck-2026-securing]]).
