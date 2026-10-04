---
id: dash-2026-untrusted
type: paper
title: 'From Untrusted Input to Trusted Memory: A Systematic Study of Memory Poisoning Attacks in LLM Agents'
authors: [Pritam Dash, Tongyu Ge, Aditi Jain, Tanmay Shah, Zhiwei Shang]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.04329
doi: null
arxiv: '2606.04329'
cite: 'Dash, P., Ge, T., Jain, A., Shah, T., & Shang, Z. (2026). From Untrusted Input to Trusted Memory: A Systematic Study of Memory Poisoning Attacks in LLM Agents. arXiv preprint arXiv:2606.04329.'
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 26  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

The paper is a systematisation of memory poisoning in LLM agents. It identifies four memory write channels and nine structural vulnerabilities across model capabilities, system-prompt design and agent architecture that make those channels exploitable. From these it derives a taxonomy of six classes of memory poisoning attack and releases MPBench, a benchmark for them. Measured (abstract): agents designed to write and retrieve memory more aggressively are more exploitable, and existing prompt-injection defences do not cover memory poisoning.

## Contribution

A taxonomy and benchmark that separate write channels from attack classes.

## Key results

- Aggressive memory writing and retrieval correlate with exploitability (abstract).
- Prompt-injection defences fail to cover memory poisoning (abstract).

## Methods and models

MPBench. Details not read.

## Limitations and open questions

Abstract only. The specific channels and the per-class numbers were not checked.

## Relevance to us

Bears on Q3. Merging a sub-agent is in effect a fifth, bulk write channel into the parent's memory. The finding that more aggressive writers are more exploitable suggests that a parent which merges everything a sub-agent brings back maximises exposure. A selective merge policy is the corresponding control (inferred). The taxonomy is a good checklist for the survey's threat model. Related systematisations: [[lin-2026-survey]], [[torra-2026-memory]].
