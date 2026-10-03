---
id: luz-de-araujo-2025-persistent
type: paper
title: "Persistent Personas? Role-Playing, Instruction Following, and Safety in Extended Interactions"
authors: [Pedro Henrique Luz de Araujo, Michael A. Hedderich, Ali Modarressi, Hinrich Schuetze, Benjamin Roth]
year: 2025
venue: European Chapter of the Association for Computational Linguistics (EACL 2026); arXiv preprint
url: https://arxiv.org/abs/2512.12775
doi: null
arxiv: '2512.12775'
cite: "Luz de Araujo, P. H., Hedderich, M. A., Modarressi, A., Schuetze, H., & Roth, B. (2025). Persistent Personas? Role-Playing, Instruction Following, and Safety in Extended Interactions. EACL 2026. arXiv:2512.12775."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

An evaluation protocol that conditions benchmarks on long persona dialogues (over 100 rounds) to measure how dialogue length affects persona fidelity, instruction following and safety. Applied to seven open- and closed-weight LLMs.

## Contribution

Extends persona-drift measurement from 8 to 16 rounds ([[li-2024-measuring]]) to more than 100 rounds, and links fidelity loss to instruction following and safety.

## Key results

- Reported (abstract): persona fidelity degrades over the course of dialogues, especially in goal-oriented conversations.
- Reported (abstract): a trade-off between persona fidelity and instruction following; non-persona baselines initially outperform persona-assigned models.
- Reported (abstract): as fidelity fades, persona-assigned responses become increasingly similar to the baseline model's default responses.

## Methods and models

Seven LLMs; long persona dialogues used as context for standard evaluation datasets. Only the abstract was read.

## Limitations and open questions

No adversary; abstract-level reading.

## Relevance to us

Q3 background. The finding that long-run personas regress toward the base model's default is a reminder that a sub-agent's assigned role is weakly held over long excursions, so "identity" at return is partly the base model and partly whatever the context pushed. Combined with [[ko-2026-attractor]] and [[sandhan-2026-persona]], the parent should treat any persona or mission statement carried by a returning part as stale. Related: [[zerhoudi-2026-compaction]].
