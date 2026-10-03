---
id: gh-hetu-project-aegean-consensus
type: code
title: 'aegean-consensus: third-party implementation of Aegean quorum consensus for multi-agent LLM reasoning'
repo: hetu-project/aegean-consensus
url: https://github.com/hetu-project/aegean-consensus
authors: [hetu-project (commits by maoaixiao1314)]
year: 2026
language: Python
license: MIT
stars: 3
last_commit: 2026-06-09
topics: [fork-merge-security, sync-consensus, llm-agent-swarms]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

A small repository that implements the protocol from "Reaching Agreement Among Reasoning LLM Agents" (Ruan, Wang, Shi, Li; arXiv 2512.20184), with FastAPI, gRPC, Prometheus and AutoGen integrations. The paper abstract defines a multi-agent refinement problem with correctness guarantees and presents Aegean, a consensus protocol for stochastic reasoning agents with incremental quorum detection and early termination; it reports 1.2 to 20 times lower latency with answer quality within 2.5% on four math benchmarks. The repository README markets the code as "Byzantine fault-tolerant", but the decision engine (`src/aegean/core/decision_engine.py`) documents quorum detection as alpha = ceil(N/2) agreeing agents with a 0.9 similarity threshold for grouping answers, plus a stability horizon of beta rounds.

## What it can do for us

Q2, as a cautionary example: a simple majority quorum tolerates fewer than half of agents being wrong in an uncoordinated way, but it is not a Byzantine quorum (classical BFT needs n >= 3f + 1 with quorums of 2f + 1 when faulty nodes may lie inconsistently [[lamport-1982-byzantine]] [[castro-1999-practical]]). The paper abstract itself claims safety and liveness for stochastic agents, not Byzantine ones; the "Byzantine" label appears only in the third-party README. Any fork-merge design that votes over children's answers should state which fault model its quorum assumes; this repo shows how easily the two get conflated.

## Run notes

Not run. I read the README and grepped the decision engine source for quorum logic.

## Limitations

Three stars, single committer, not by the paper's authors as far as the commit history shows. The README's performance claims are copied from the paper and not reproduced. The similarity-threshold grouping of free-text answers is a second attack surface (an attacker can craft answers that cluster with honest ones) that the README does not discuss.
