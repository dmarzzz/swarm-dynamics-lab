---
id: zerhoudi-2026-compaction
type: paper
title: "The Compaction Cliff in Long-Running AI Agent Memory"
authors: [Saber Zerhoudi, Jelena Mitrovic, Michael Granitzer]
year: 2026
venue: Proceedings of the 35th ACM International Conference on Information and Knowledge Management (CIKM 2026)
url: https://arxiv.org/abs/2608.22752
doi: 10.1145/3799682.3840567
arxiv: '2608.22752'
cite: "Zerhoudi, S., Mitrovic, J., & Granitzer, M. (2026). The Compaction Cliff in Long-Running AI Agent Memory. In Proceedings of the 35th ACM International Conference on Information and Knowledge Management (CIKM 2026). https://doi.org/10.1145/3799682.3840567"
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: null
code: []  # github.com/searchsim-org/cikm26-knowledge-triage, not opened
---

## Summary

When an agent's context fills, runtimes compact it by summarising. The authors measure how many safety rules survive this. On 50 real agent configuration files from a new corpus of 396,934 artifacts in 54,628 GitHub repositories, type-blind compaction (structural truncation, LLMLingua-2, and LLM compactors including Claude Code's /compact on Sonnet 4.6) keeps about half the safety constraints after one round and about a tenth after five. They propose Knowledge Triage: classify each item into one of five types (constraint, procedural, belief, preference, episodic) and route constraints through exact-preservation lanes for compaction, decomposition and retrieval.

## Contribution

A measurement of a non-adversarial erosion channel for an agent's governing rules under the memory operations every long-running agent performs, plus typed operators with per-type guarantees.

## Key results

- Measured: Sonnet 4.6 /compact preserves 53% of safety rules after one 50% compaction round and 10% after five rounds (20 configurations).
- Measured: best type-blind single-round constraint recall is 0.53 at 50% compression, 0.39 at 25%, 0.24 at 10%, across eight strategies and four LLM families.
- Measured: TypeCompact reaches 1.00 / 0.95 / 0.80 at the same ratios and 0.96 over five rounds; loss is bounded by classifier recall.
- Measured: declarative rules ("the patient is allergic to penicillin") are recognised as constraints by an LLM classifier only 62% of the time versus 100% for imperative phrasing; counterfactual SafetyMargin scoring raises this to 90%.
- Measured: decomposition by topic leaves at least one constraint-locality violation in 40% of configurations; replicating constraints into every in-scope partition removes them at 14.5% mean token overhead.
- Measured downstream: on a 200-scenario medical benchmark, TypeCompact beats the Sonnet compactor on pass rate (p = 0.022) and preservation (14.5 points, p = 3.7e-9).
- Authority weighting (system 1.5, developer 1.25, user 1.0, tool 0.75, retrieved 0.6) is a design choice, not a measured security property.

## Methods and models

Corpus scraped via GitHub code search. Constraint survival scored by a key-token test validated against two annotators (kappa 0.92 on preserved vs lost). Compactors: gpt-5.4-nano, gpt-5.4-mini, Sonnet 4.6 via /compact, Opus 4.7, LLMLingua-2, three structural baselines, a reimplementation of MaRS. Behavioural tests on SafetyMed (new), tau-bench retail and airline with paired McNemar tests.

## Limitations and open questions

No adversary: rules are lost by accident, not removed by an attacker. Multi-round decay was run on two of four LLM families. Classifier reference labels partly come from gpt-5.4-mini itself. The authors note the guarantee does not cover inter-agent communication.

## Relevance to us

Q3, the persistence half. dmarz asked whether a hijacked identity survives summarisation. This paper measures the mirror image: the parent-given rules that define a sub-agent's identity do not survive it, falling to 10% after five rounds. A sub-agent on a long excursion is compacted repeatedly, so by return its original constraints may be mostly gone while recent, attacker-supplied content is retained. [[liu-2026-safe]] shows the compressor can also assemble an attacker instruction. Practical bearing on the merge: the parent should re-inject its constraints from its own copy at merge rather than trust the returning part's summary of them, and the authors' remark that "a multi-agent planner that summarizes before delegating inherits the cliff" applies at both fork and merge. Related: [[li-2024-measuring]] (drift without compaction), [[wallace-2024-instruction]] (privilege by source).
