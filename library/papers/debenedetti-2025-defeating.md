---
id: debenedetti-2025-defeating
type: paper
title: 'Defeating Prompt Injections by Design'
authors: [Edoardo Debenedetti, Ilia Shumailov, Tianqi Fan, Jamie Hayes, Nicholas Carlini, Daniel Fabian, Christoph Kern, Chongyang Shi, Andreas Terzis, Florian Tramèr]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2503.18813
doi: null
arxiv: '2503.18813'
cite: 'Debenedetti, E., Shumailov, I., Fan, T., Hayes, J., Carlini, N., Fabian, D., Kern, C., Shi, C., Terzis, A., & Tramèr, F. (2025). Defeating Prompt Injections by Design. arXiv preprint arXiv:2503.18813.'
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

CaMeL is a system-level defence against prompt injection that works even when the underlying model is susceptible. It extracts the control flow and data flow from the trusted user query up front, so that untrusted data retrieved later cannot change the program flow. It attaches capabilities to data values and enforces security policies at tool calls, which prevents private data from leaving through unauthorised flows. Measured (abstract): 77% of AgentDojo tasks solved with provable security, against 84% for an undefended system. Code: github.com/google-research/camel-prompt-injection (not opened).

## Contribution

It brings classic information-flow control and capabilities to LLM agents. Untrusted data is treated as data and never as control.

## Key results

- 77% AgentDojo task success with provable security, against 84% undefended (abstract).

## Methods and models

Dual-model design (planner and quarantined data processor) with a custom interpreter and capability tags. Details not read beyond the abstract.

## Limitations and open questions

Its guarantee is per task, starting from a trusted query. Whether and how it covers persistent memory written in one session and read in another is not addressed in the abstract. [[louck-2026-securing]] reports that a CaMeL/Fides-style capability IFC baseline left memory-laundering ASR at 68%, but that is that paper's reimplementation and has not been checked against the original.

## Relevance to us

For Q3 it marks the boundary of design-based defences. Isolating control from data protects the parent within one task. A fork-merge architecture, however, deliberately turns data a sub-agent gathered into the parent's future context and plans, and that is the step memory laundering exploits. For Q1 and Q2 the capability idea transfers in a different form. Values a sub-agent brings home could carry "from-sub-agent-i, untrusted" capabilities that block them from driving consequential actions without corroboration, which is close to the TMA-NM design in [[louck-2026-securing]]. Seminal context: [[greshake-2023-not]].
