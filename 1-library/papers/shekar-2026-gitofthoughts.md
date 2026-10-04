---
id: shekar-2026-gitofthoughts
type: paper
title: 'GitOfThoughts: Version-Controlled Reasoning and Agent Memory You Can Replay, Diff, and Merge'
authors:
- Pavan C Shekar
- Abhishek H S
- Aswanth Krishnan
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.14470
doi: null
arxiv: '2606.14470'
cite: 'Shekar, P. C., S, A. H., & Krishnan, A. (2026). GitOfThoughts: Version-Controlled Reasoning and Agent Memory You Can Replay, Diff, and Merge. arXiv preprint. arXiv:2606.14470.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

GitOfThoughts stores an agent's reasoning tree as a git repository: each scored thought is a commit, scores are git notes, outcomes are tags, and retrieval is a git log query over the agent's own history, so reasoning and memory can be replayed, diffed, audited and merged between agents. The paper uses it to test, with pre-registered replications, whether cross-problem memory improves accuracy, comparing five memory stores (none, a markdown file, a vector database, a graph, git) on GPQA-Diamond and MATH-500 with two backbone sizes. Read: abstract, introduction and findings list, the test-time architecture section, the summary and the discussion of limitations; the system section was skimmed.

## Contribution

A concrete, low-cost substrate for mergeable and auditable agent memory, together with a careful negative result on what memory transfer actually buys.

## Key results

- Memory from past problems did not reliably improve accuracy on novel problems with any store; one early positive trend for git failed its pre-registered replication (measured).
- Memory helped only when the retrieved case was a near-duplicate of the test problem (cosine similarity above about 0.8); the gain was answer retrieval, not method transfer, and a 4.5 times larger model only steepened that step (measured).
- Git gave auditability, provenance, line-level diffs of reasoning, deterministic replay and mergeable memory at accuracy parity, for about 15 ms per write (measured).
- Self-consistency (sampling several answers and taking the most common) was the only thing that reliably helped on new problems; the GPQA headline of 47.0% versus 33.0% is attributed by the authors to extra compute and MCQ-aware expansion, not to memory (stated).

## Methods and models

Open-weight backbones (two sizes); pre-registered repeats; noise floor estimated from repeated greedy runs (greedy swung 55% to 65% across identical runs on one set).

## Limitations and open questions

Short distilled memory entries only; two open-weight backbones; no adversarial or poisoned memory tested; compute not matched in the headline comparison (stated).

## Relevance to us

Q2 and Q1, defence infrastructure: this is a ready design for merging the memories of separate agents with full provenance. Each returned memory item is a signed, content-addressed commit that the parent can diff, attribute to a specific part, replay, and revert, which turns "un-merge a corrupted child" from a research problem into a git revert, and makes per-item k-of-n attestation straightforward to implement. It also cuts against Q1 hiding, since provenance makes every returned item attributable. The near-duplicate result matters for Q3: if memory mostly works by retrieving near-copies, a returned memory item that closely matches a future query is what will be used, which is exactly how poisoned memory gets triggered. Related: [[liu-2026-towards]], [[ma-2026-catching]], [[zhang-2026-agentworm]].
