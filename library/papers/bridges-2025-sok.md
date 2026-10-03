---
id: bridges-2025-sok
type: paper
title: 'SoK: Honeypots & LLMs, More Than the Sum of Their Parts?'
authors:
- Robert A. Bridges
- Thomas R. Mitchell
- Mauricio Muñoz
- Ted Henriksson
year: 2025
venue: arXiv preprint
url: https://arxiv.org/html/2510.25939
doi: null
arxiv: '2510.25939'
cite: 'Bridges, R. A., Mitchell, T. R., Muñoz, M., & Henriksson, T. (2025). SoK: Honeypots & LLMs, More Than the Sum of Their Parts? arXiv preprint arXiv:2510.25939.'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

A systematisation of LLM-powered honeypots (literature through October 2025, found by a Google Scholar search for "LLM" AND "Honeypot"). It sets out four persistent honeypot fingerprinting vectors (contents and posture, outputs and behaviour, functional limits, multi-feature synthesis) and says which of them LLM simulation can help with. It proposes a canonical LLM-honeypot architecture (filtering, state management, generation), an evaluation tetrad (believability, fidelity, attacker cost and intelligence, defender cost), and an attacker trichotomy: scripted bots, skilled humans, and automated LLM agents.

## Contribution

The first review of the LLM-honeypot field, and a review article in scope for this task. Its main argument is that LLM honeypots are mistargeted when evaluated against scanning scripts or human red-teamers and should be optimised against automated LLM attackers.

## Key results

- "Data desert": in Guan et al.'s wild deployment, 99.2% of honeypot activity was simple scanning scripts and the best LLM only raised mean session length from 2.96 to 5.83 commands; Wang et al. found 0.58% and 0.048% of connections in two datasets became valid post-login sessions (secondary figures quoted by the SoK, not checked against the primaries).
- No prior SoK on LLM honeypots existed as of their search (reported).
- Notes that responses believable to humans may be flagged by LLM attackers and vice versa, citing Ayzenshteyn et al.'s use of this gap to expose LLMs (reported).

## Methods and models

Literature review with a comparison table of every LLM-honeypot paper found (Table II) and a detection-vector taxonomy (Table I). Skimmed: intro, taxonomy, evaluation and roadmap sections.

## Limitations and open questions

Focused on enterprise network-server emulation; social-platform and web honeypots appear only in passing. It is mostly about LLMs as the honeypot, less about detecting LLMs as the visitor.

## Relevance to us

Map of the honeypot side of the field and source for the base-rate problem: real deployments see almost no sophisticated sessions, which is consistent with [[reworr-2024-llm]]'s 8 in 8.1M. Related: [[sladic-2023-llm]], [[otal-2024-llm]], [[pasquini-2024-hacking]], [[elzer-2026-ollamadrama]].
