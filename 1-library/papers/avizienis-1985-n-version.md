---
id: avizienis-1985-n-version
type: paper
title: The N-Version Approach to Fault-Tolerant Software
authors:
- Algirdas Avizienis
year: 1985
venue: IEEE Transactions on Software Engineering
url: https://curtsinger.cs.grinnell.edu/teaching/2019S/CSC395/papers/avizienis.pdf
doi: 10.1109/TSE.1985.231893
arxiv: null
cite: 'Avizienis, A. (1985). The N-Version Approach to Fault-Tolerant Software. IEEE Transactions on Software Engineering, SE-11(12), 1491-1501.'
topics:
- fork-merge-security
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: 735 (Crossref, 2026-10-03)
code: []
---

## Summary

Reviews the N-version approach to tolerating design faults: instead of N identical replicas, which fail together on any design fault, build N versions independently from one specification and vote on their outputs. The paper introduces the vocabulary still used: similar errors (two or more erroneous results within the voter's tolerance), the rule that similar errors outnumbering good results defeat the vote (2 of 3, or 3 of 5), and related faults (attributable to a common cause such as an ambiguous specification, conversation between teams, a shared faulty compiler or manual) versus independent ones. It describes the DEDIX supervisor and testbed and UCLA experiments, including an airport scheduler written from specifications in three languages (OBJ, PDL, English) by 18 programmers.

## Contribution

Names and systematises design diversity as the defence against common-mode design faults, and states its fundamental conjecture: independence of development efforts yields low probability of similar errors.

## Key results

- Definitions: similar errors, related versus independent faults, decision algorithm tolerance.
- Stated conjecture: independent generation of versions will make similar errors at a decision point rare.
- Observed (cited): two entirely different design faults produced a pair of similar errors.

## Methods and models

Notation for multiple computation in time, space and information (for example 1T/NH/NdS for N-version software). Skimmed: abstract, sections I and II, parts of the UCLA experiment description; DEDIX details not read.

## Limitations and open questions

The independence conjecture is the thing [[knight-1986-experimental]] tested and rejected one year later.

## Relevance to us

Q2. Gives the conceptual tool for asking whether a k-of-n merge of LLM sub-agents is meaningful: a corrupted majority is a set of similar errors, and the question is whether the sub-agents' faults are related through a common link. For forks of one model, the common links Avizienis lists (shared specification, shared tools) are all present, plus a shared input domain controlled by the attacker. Also suggests the defence: deliberate diversity of model, prompt, tools and information route between forks. Measurements for LLMs: [[nogueira-2026-systematic]], [[ron-2026-n-version]].
