---
id: zhu-2026-fault
type: paper
title: 'Fault-Tolerant Budget Conservation in Distributed Multi-Agent Delegation'
authors:
- Genliang Zhu
- Chu Wang
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2610.00349
doi: null
arxiv: '2610.00349'
cite: 'Zhu, G., & Wang, C. (2026). Fault-Tolerant Budget Conservation in Distributed Multi-Agent Delegation. arXiv preprint arXiv:2610.00349.'
topics:
- agent-budgets
- sybil-resistance
added_by: dmarz/budget-b
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

A formal protocol for keeping a delegated spending cap intact when a coordinator hands budget to workers, workers hand it to specialists, branches merge, and messages are lost, repeated or late. The budget is a vector of quantized resources represented as exclusive escrow credits that move down a delegation DAG. Before an external effect, a branch converts credit into a reservation bound to lineage, epoch, effect, maximum charge, receiver and an idempotency key. An effect whose outcome is uncertain stays charged until an authenticated receipt, a fenced no-effect proof, or permanent forfeiture. Under stated assumptions the authors prove ledger and effect conservation, that descendants cannot amplify the budget, at-most-once settlement, late-completion safety and partition confinement. They check the protocol with bounded TLA+, an independent JavaScript explorer, and crash-injected two-process SQLite runs.

## Contribution

Separates allocation safety (children never get more than the parent) from execution safety (the cap holds after timeouts, retries and joins), and supplies a mechanism for the second. Prior agent-budget work (Agent Contracts, Token Budgets, AIP, attenuating tokens, all cited) covers only the first.

## Key results

- Proved (conditional on mediation, durability, authentication, normalization and gateway assumptions): ownership partition, ledger and effect conservation, descendant non-amplification, at-most-once settlement, late-completion safety, partition confinement.
- Proved: an indistinguishability result. A shared, unallocated unit cannot stay spendable in every partition without risking amplification, so local availability requires exclusive preallocation.
- Worked example (Figure 1): with a 2-unit root and a timeout refund, a lost reply plus a late completion yields 3 effects. Refund-on-timeout is unsafe.
- Measured (bounded scope only): the model checkers and SQLite crash experiments detect seeded timeout-refund and historical-certificate-validation mutants, and the safe profile keeps the issued bound across the tested crash, retry, duplicate, partition, join and late-completion schedules.
- Quoted from cited work, not checked: Token Budgets (Khan, 2026) documents 63 production budget overruns.

## Methods and models

Transition-system semantics with six budget buckets (spendable, moving, reserved, uncertain, committed, forfeited). Algorithms for split, delegation, reserve-before-dispatch, settlement, fan-in, recovery, epoch fencing and reclaim. Adapters for MCP, A2A and HTTP are specified as refinement obligations. 67 pages. I read the introduction, contributions, limitations and conclusion, not the proofs.

## Limitations and open questions

Crash faults only: no Byzantine stores or compromised signers. An issuer that signs overlapping root grants can still overspend a real-world cap. The executable artifact is not distributed with the preprint. The authors are affiliated with Accentrust, which develops agent-governance technology. No model-quality or real-provider accounting is evaluated.

## Relevance to us

The systems answer to "a sub-agent cannot mint budget". Descendant non-amplification means spawning more children, or aliasing one lineage through a DAG join, cannot raise total authority. That is the property a per-identity quota lacks under Sybil splitting ([[yokoo-2004-effect]], [[zheng-2024-sybil]]), which is why this entry is tagged sybil-resistance. Complements the allocation-quality papers [[wang-2026-r3]], [[paliskara-2026-worse]] and [[jin-2025-controlling]], and the power-asymmetry risks in [[borah-2026-bosses]].
