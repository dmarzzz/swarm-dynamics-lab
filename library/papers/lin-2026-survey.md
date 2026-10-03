---
id: lin-2026-survey
type: paper
title: 'A Survey on Long-Term Memory Security in LLM Agents: Attacks, Defenses, and Governance Across the Memory Lifecycle'
authors: [Zehao Lin, Xixuan Hao, Renyu Fu, Shaobo Cui, Kai Chen, Chunyu Li, Zhiyu Li, Feiyu Xiong]
year: 2026
venue: EMNLP 2026 (per arXiv comments); arXiv preprint
url: https://arxiv.org/abs/2604.16548
doi: null
arxiv: '2604.16548'
cite: 'Lin, Z., Hao, X., Fu, R., Cui, S., Chen, K., Li, C., Li, Z., & Xiong, F. (2026). A Survey on Long-Term Memory Security in LLM Agents: Attacks, Defenses, and Governance Across the Memory Lifecycle. arXiv preprint arXiv:2604.16548. Accepted to EMNLP 2026.'
topics: [fork-merge-security, meta]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 19  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

A review article on the security of writable, cross-session agent memory. It characterises the threat by three properties, persistence, statefulness and propagation, and organises attacks, defences and their dependencies in a Memory Lifecycle Framework. One axis is six phases (Write, Store, Retrieve, Execute, Share and Propagate, Forget and Rollback). The other is four objectives (Integrity, Confidentiality, Availability, Governance). It proposes Verifiable Memory Governance, a set of five architectural primitives for auditable and recoverable control over memory state. It concludes that memory security cannot be retrofitted at retrieval or execution time alone and must rest on provenance, versioning and policy-aware retention at storage time.

## Contribution

A lifecycle taxonomy that includes "Share and Propagate" and "Forget and Rollback" as phases in their own right.

## Key results

Review article. No new measurements.

## Methods and models

Literature synthesis.

## Limitations and open questions

Abstract only. The coverage and the five primitives were not checked.

## Relevance to us

A review article, catalogued for completeness on all three questions. Its "Share and Propagate" phase is the fork-merge step, and its "Forget and Rollback" phase is the recovery a parent would need after detecting a corrupted merge. Versioned memory with rollback is a defence the primary papers in this lane barely test: if a merge is a versioned commit, a later-detected corrupted merge can be reverted (inferred). Its conclusion that provenance must be bound at storage time agrees with the impossibility arguments in [[sharma-2026-smsr]] and [[louck-2026-securing]]. Other reviews: [[he-2024-emerged]], [[shahriar-2025-survey]], [[torra-2026-memory]].


## Notes from shadow/sol-g74

Issue #74 rerun, 2026-10-03. Source opened: https://arxiv.org/abs/2604.16548 . Read depth in this session: abstract.

Review rediscovered through the forward Agent Smith citation list, then its arXiv abstract opened. The memory lifecycle explicitly includes sharing/propagation and forgetting/rollback. Read depth in this rerun is abstract, not full. This distinguishes admission into a parent memory from later execution-time checks.
