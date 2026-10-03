---
id: green-2007-provenance
type: paper
title: Provenance Semirings
authors:
- Todd J. Green
- Grigoris Karvounarakis
- Val Tannen
year: 2007
venue: PODS 2007
url: https://www.cs.ucdavis.edu/~green/papers/pods07.pdf
doi: 10.1145/1265530.1265535
arxiv: null
cite: Green, T. J., Karvounarakis, G., & Tannen, V. (2007). Provenance Semirings.
  Proceedings of PODS, 31-40.
topics:
- llm-agent-swarms
- fork-merge-security
- meta
added_by: dmarz/preflight
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Green and colleagues represent relational-query provenance algebraically. Input annotations combine through query operations, preserving information about derivations that ordinary output values omit. The paper unifies several database semantics and extends the construction to recursive queries.

## Contribution

A compositional language for derivation provenance.

## Key results

Polynomial annotations support positive relational algebra; formal power series extend the treatment to Datalog.

## Methods and models

Skimmed abstract, introduction, worked examples, main construction and conclusion; proofs not fully checked.

## Limitations and open questions

Applies to specified query operations. It does not infer semantic dependence inside an LLM.

## Relevance to us

Useful formal baseline beside [[ouyang-2026-memlineage]].
