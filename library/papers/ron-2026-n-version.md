---
id: ron-2026-n-version
type: paper
title: N-Version Programming with Coding Agents
authors:
- Javier Ron
- Benoit Baudry
- Martin Monperrus
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2606.20158
doi: null
arxiv: '2606.20158'
cite: 'Ron, J., Baudry, B., & Monperrus, M. (2026). N-Version Programming with Coding Agents. arXiv preprint arXiv:2606.20158.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Replicates the Knight-Leveson experiment [[knight-1986-experimental]] with AI coding agents in place of students. Five agent harnesses (Claude Code, Codex, Gemini, Cursor, OpenCode), 23 models and three languages (Python, Rust, Pascal) gave 69 [harness, model, language] triples; 48 passed the 200-case acceptance screen and were run on one million random inputs against the reference. Independence is rejected decisively: 429 inputs caused coincident failures versus 115.36 expected, and every per-language slice also rejects. Failure clusters cross agent and language boundaries. Majority-vote triples still help: mean failures drop from 387.44 for single versions to 130.99 for triples, and 11,844 triples show zero failures.

## Contribution

Shows that the 1986 common-mode result carries over to LLM agents, and that harness, model and language diversity do not by themselves produce behavioural diversity, while voting still gives a useful but sub-independent gain.

## Key results

- Measured: 48 of 69 configurations admitted (70 percent); 27 of 48 failure-free; worst version fails 10,469 of 10^6.
- Measured: pooled coincident failures 429 observed vs 115.36 expected; per-language z from 80.7 to 253.3.
- Measured: among 146 cross-language pairs with defined correlation, 81 have perfect co-failure (phi = 1); among cross-agent pairs with defined correlation, 87 of 158 are perfect.
- Measured (authors' root cause analysis): many co-failures trace to hard or ambiguous parts of the specification.
- Measured: three-version majority units cut mean failures by about a factor of 3.

## Methods and models

Knight-Leveson z statistic, pairwise Pearson correlation of binary failure vectors, stratification by language and agent, manual root-cause analysis per launch-interceptor condition, exhaustive enumeration of three-version voting units. Sections on RQ4 and RQ5 were skimmed.

## Limitations and open questions

One specification, natural (non-adversarial) failures. Pairs where one version never fails have undefined correlation and drop out, so the correlation distribution describes only failing versions.

## Relevance to us

Q2. Direct evidence for sub-agents built on LLMs: diversity in tooling and model gives some decorrelation, but failures concentrate on the same hard inputs. For fork-merge, the analogue of a hard or ambiguous spec region is the part of the explored domain that the attacker controls, which every explorer sees. A k-of-n merge still reduces risk by a constant factor rather than exponentially in k. See [[nogueira-2026-systematic]] and [[kim-2025-correlated]].
