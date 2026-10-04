---
id: rippin-2026-tool
type: paper
title: Tool Use Enables Undetectable Steganography in Multi-Agent LLM Systems
authors: [Jimmy Laurence Rippin, Simon C. Marshall, David Demitri Africa, Christian Schroeder de Witt]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.28425
doi: null
arxiv: '2606.28425'
cite: Rippin, J. L., Marshall, S. C., Africa, D. D., & Schroeder de Witt, C. (2026). Tool Use Enables Undetectable Steganography in Multi-Agent LLM Systems. arXiv:2606.28425.
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

The authors show that agentic coding models, given realistic tools such as code execution and web search for papers, can already build stegosystems that are undetectable, adapting when ingredients are missing (for example by adding model-sampling components or implementing related keyed schemes). They then treat tacit steganographic coordination between agents without prior agreement as a Schelling-point problem and introduce coordination metrics. They find substantial convergence on broad scheme families but limited strict one-shot coordination on compatible schemes, keys and parameters, and argue that shared artefacts, repeated interaction and tool-mediated search are where covert-channel risk is highest.

## Contribution

Moves the covert-channel threat model for AI agents from "can they implement it" to "can they coordinate on it", with measured coordination rates.

## Key results

- Tool-using agents produce undetectable stegosystems (abstract claim, details not read).
- Broad agreement on scheme families, weak exact one-shot coordination (abstract).
- Empirical support for the strategic confinement hypothesis that capable agents can build monitor-surviving covert channels.

## Methods and models

Agentic coding evaluations with tools; Schelling-point coordination metrics (not read beyond the abstract).

## Limitations and open questions

Only the abstract was read; coordination results depend on scheme space and prompts.

## Relevance to us

Q1 from both sides, and Q3. For defence, it implies a parent can give its sub-agents a covert, monitor-proof channel home (pre-shared keys turn the hard coordination problem into an easy one), hiding which part is reporting. For attack, a corrupted sub-agent can carry a hidden payload back through the merge that inspection of its plain-text report will not find; the paper's finding that shared artefacts and repeated interaction make coordination easier describes exactly the fork-merge setting, where parts share a base model and past memory. Builds on [[motwani-2024-secret]]; detection side in [[tailor-2025-audit]]; injection propagation in [[lee-2024-prompt]].
