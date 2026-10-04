---
id: ravindran-2026-portable
type: paper
title: 'Portable Agent Memory: A Protocol for Cryptographically-Verified Memory Transfer Across Heterogeneous AI Agents'
authors: [Santhosh Kumar Ravindran]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2605.11032
doi: null
arxiv: '2605.11032'
cite: 'Ravindran, S. K. (2026). Portable Agent Memory: A Protocol for Cryptographically-Verified Memory Transfer Across Heterogeneous AI Agents. arXiv preprint arXiv:2605.11032.'
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 5  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

The paper proposes an open protocol and reference implementation for moving an agent's persistent memory between different runtimes and models. Memory has five components (episodic, semantic, procedural, working state and identity preferences), stored as content-addressed entries linked in a Merkle-DAG provenance graph for tamper evidence. Capability-based access control allows scoped disclosure of memory segments. An "injection-resistant rehydration protocol" adapts recalled content to the target model while mitigating indirect prompt injection. Serialisation is JSON-first with optional CBOR. Reported (abstract): a Python SDK with 54 passing tests and memory transfer between GPT-4, Claude, Gemini and Llama. Apache 2.0.

## Contribution

A concrete wire format for moving memory between agents with provenance, which can serve as a merge payload format.

## Key results

- Engineering artefact. Cross-model transfer is demonstrated and 54 tests pass (abstract).
- No adversarial evaluation of the injection-resistant rehydration is reported in the abstract.

## Methods and models

Merkle-DAG, capabilities, JSON or CBOR. Single author. 8 pages.

## Limitations and open questions

A Merkle-DAG gives tamper evidence after signing but cannot tell whether content was honest when it was written. A compromised sub-agent produces validly hashed poison. The claim of injection resistance is unevaluated in the abstract.

## Relevance to us

For Q3 and Q2 this is the closest existing artefact to a fork-merge protocol. It separates memory into typed components (episodic, semantic, procedural, identity), which suggests a merge rule could treat them differently. The identity and preference component is where "become the attacker's agent" would live, and a parent could refuse to merge that component from any sub-agent at all (inferred design point). Its provenance DAG gives the writer-identity bookkeeping that k-of-n corroboration ([[louck-2026-securing]]) needs, while [[zhan-2026-when]] shows that losing such metadata at consolidation is the default failure.
