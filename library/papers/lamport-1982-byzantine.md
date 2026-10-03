---
id: lamport-1982-byzantine
type: paper
title: The Byzantine Generals Problem
authors:
- Leslie Lamport
- Robert Shostak
- Marshall Pease
year: 1982
venue: ACM Transactions on Programming Languages and Systems
url: https://lamport.azurewebsites.net/pubs/byz.pdf
doi: 10.1145/357172.357176
arxiv: null
cite: 'Lamport, L., Shostak, R., & Pease, M. (1982). The Byzantine Generals Problem. ACM Transactions on Programming Languages and Systems, 4(3), 382-401.'
topics:
- fork-merge-security
- sync-consensus
- sybil-resistance
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: 4517 (Crossref, 2026-10-03)
code: []
---

## Summary

Defines the Byzantine Generals Problem: a commander sends an order to n - 1 lieutenants, some of whom (possibly including the commander) are traitors who can send conflicting messages; all loyal lieutenants must obey the same order (IC1) and, if the commander is loyal, obey his order (IC2). With oral (unauthenticated) messages the problem is solvable if and only if more than two-thirds of the generals are loyal, so m traitors need at least 3m + 1 generals; three generals cannot tolerate one traitor. With unforgeable signed messages (algorithm SM(m)) it is solvable for any number of traitors. Extensions handle incomplete communication graphs (3m-regular graphs for OM(m, p); connectivity of loyal generals for SM). Section 6 argues that majority voting over redundant processors is reliable only if all non-faulty processors first agree on the same inputs.

## Contribution

The founding threshold result for agreement under arbitrary faults: n >= 3m + 1 without authentication, unbounded with signatures, and message paths of length m + 1 are required.

## Key results

- Proved: no oral-message solution with 3m or fewer generals tolerates m traitors.
- Proved: OM(m) works for n >= 3m + 1; SM(m) works for any n with signed messages.
- Proved: OM(m, p) works on p-regular graphs with p >= 3m.
- Argued: replicated computation with voting needs interactive consistency on inputs; redundant inputs alone cannot achieve reliability.
- Argued: with median as the combining function, outputs stay within the range of values the input unit provides.

## Methods and models

Recursive oral-message algorithm, signed-message algorithm, impossibility by reduction to the three-general case. Assumptions A1 to A4: reliable delivery, known sender, detectable absence of messages, unforgeable signatures.

## Limitations and open questions

Counts faulty processes and assumes they are a bounded minority, independent of each other's failure causes; the algorithms are expensive in messages.

## Relevance to us

Q2, as the base answer. If the parent treats returning sub-agents as generals that must agree on what to merge, and they communicate by unauthenticated text, it needs at least 3f + 1 of them to tolerate f corrupted ones. With authenticated messages (each part signs what it observed at fork time and on return) the bound relaxes, which suggests signing sub-agent observations before they can be rewritten. Section 6 maps onto the fork-merge threat: voting is useless if a faulty input source (a hostile domain) feeds different or poisoned data to the replicas, which is exactly the shared-input corruption measured for LLMs in [[liu-2026-consensus]] and [[alavi-2025-more]]. Graph versions: [[leblanc-2013-resilient]], [[lee-2026-robust]]. Practical asynchronous form: [[castro-1999-practical]].

## Notes from dmarz/preflight

2026-10-03: Re-opened the primary author PDF, problem definition and message assumptions. The oral-message theorem bounds the number of arbitrarily behaving traitors; it does not require independent random failures. Coordinated traitors are within that model. Common-cause compromise can violate the fault-count bound, but correlation alone is not a counterexample while the bound and protocol assumptions hold. Nor does agreement certify factual truth. Applying the theorem to free-text agent reports requires a specified protocol and correctness condition; plain majority voting is not that protocol. See synthesis/pre-experiment-research.md for the resulting scope restriction.
