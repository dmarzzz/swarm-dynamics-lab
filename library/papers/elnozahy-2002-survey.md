---
id: elnozahy-2002-survey
type: paper
title: A survey of rollback-recovery protocols in message-passing systems
authors:
- E. N. (Mootaz) Elnozahy
- Lorenzo Alvisi
- Yi-Min Wang
- David B. Johnson
year: 2002
venue: ACM Computing Surveys
url: https://www.cs.cornell.edu/lorenzo/papers/SurveyFinal.pdf
doi: 10.1145/568522.568525
arxiv: null
cite: Elnozahy, E. N. (Mootaz), Alvisi, L., Wang, Y.-M., & Johnson, D. B. (2002).
  A survey of rollback-recovery protocols in message-passing systems. ACM Computing
  Surveys, 34(3), 375-408.
topics:
- fork-merge-security
- llm-agent-swarms
- meta
added_by: dmarz/preflight
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

This survey distinguishes checkpoint-based recovery from protocols that also log nondeterministic events. Recovering a consistent distributed state requires accounting for dependencies across processes and external outputs, rather than restoring each process independently to any convenient snapshot.

## Contribution

Taxonomy of checkpointing, message logging and recovery tradeoffs.

## Key results

Log-based replay requires captured determinants; dependent unrecoverable states create orphan processes.

## Methods and models

Skimmed introduction, system model, recovery examples, log-based section and conclusion.

## Limitations and open questions

Crash recovery and piecewise determinism are not guarantees of semantic correction or reversal of external effects.

## Relevance to us

Classical baseline for [[li-2026-memtx]] and swarm repair.
