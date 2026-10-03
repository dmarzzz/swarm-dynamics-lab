---
id: wu-2024-system
type: paper
title: 'System-Level Defense against Indirect Prompt Injection Attacks: An Information Flow Control Perspective'
authors: [Fangzhou Wu, Ethan Cecchetti, Chaowei Xiao]
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2409.19091
doi: null
arxiv: '2409.19091'
cite: 'Wu, F., Cecchetti, E., & Xiao, C. (2024). System-Level Defense against Indirect Prompt Injection Attacks: An Information Flow Control Perspective. arXiv:2409.19091.'
topics: [fork-merge-security]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 109 (Semantic Scholar, 2026-10-03)
code: []  # github.com/fzwark/Secure_LLM_System, not opened
---

## Summary

Proposes the f-secure LLM system: an information-flow-control defence that disaggregates an LLM system into a context-aware pipeline with dynamically generated, structured executable plans, and a security monitor that filters untrusted input out of the planning process. Formal models of existing LLM systems and of the f-secure design support analysis of security guarantees; case studies and benchmarks are reported (abstract) to show robust security with preserved functionality and efficiency.

## Contribution

One of the first system-level IFC defences for agents. The later Fides paper [[costa-2025-securing]] notes that f-secure has a formal proof of non-compromise but that its practical realisation allows insecure implicit flows to taint plans (a claim made there, not checked by me).

## Key results

- Formal model plus non-compromise argument (abstract).
- Benchmark results claimed robust (abstract; numbers not read).

## Methods and models

Planner isolated from untrusted data; executable plans; monitor filtering untrusted content from planning.

## Limitations and open questions

Abstract-level reading; implicit flows per [[costa-2025-securing]].

## Relevance to us

- Q2/Q3: a design template for keeping a returning child's content out of the parent's planner while still using it as data. The planner-isolation idea is the minimum condition for a merge that cannot rewrite the parent's goals.
Related: [[debenedetti-2025-defeating]], [[willison-2023-dual]].
