---
id: cuadros-2026-governed
type: paper
title: "Governed Collaborative Memory as Artificial Selection in LLM-Based Multi-Agent Systems"
authors: [Diego F. Cuadros, Abdoul-Aziz Maiga, Helen Meskhidze, Andre Curtis-Trudel]
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2605.04264
doi: null
arxiv: "2605.04264"
cite: "Cuadros, D. F., Maiga, A.-A., Meskhidze, H., & Curtis-Trudel, A. (2026). Governed collaborative memory as artificial selection in LLM-based multi-agent systems. arXiv preprint arXiv:2605.04264."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

A viewpoint paper (read from the arXiv abstract) on which candidate memories in an LLM multi-agent system should become shared institutional state. It frames memory governance as a selection regime and distinguishes four regimes: ungoverned persistence, constitutional or hybrid selection, automatic metric-based selection, and human-ratified selection. It proposes a layered architecture with agent-local memory, shared institutional memory, archive memory and project-continuity memory, with provenance and version lineage so selection can be inspected. Documented traces from one running multi-agent ecosystem are used to illustrate unmanaged false-memory persistence, ratified institutional memory, rejection and revision, identity-preserving expansion and governance-as-learning.

## Contribution

Names the private-to-shared memory promotion step as a governance problem with distinct regimes, and proposes evaluating memory on provenance fidelity, selection traceability, epistemic quality, correction pathways and role preservation, not only recall.

## Key results

- Conceptual; the abstract reports illustrative traces from one system, including false-memory persistence under ungoverned persistence. No quantitative evaluation is described in the abstract.

## Methods and models

Position paper with case traces from one deployed LLM-based multi-agent ecosystem (details not read).

## Limitations and open questions

Abstract depth; traces are anecdotal. No adversary model is stated in the abstract.

## Relevance to us

The merge in dmarz's fork-merge scenario is exactly the promotion of a child's local memory into the parent's institutional memory, and this paper's regimes are the design space for Q2. "Human-ratified selection" corresponds to the intelligence practice of an analyst grading each returned report [[kelly-2025-effect]]; "automatic metric-based selection" corresponds to MELD's merge classifier [[loven-2026-meld]] and MAPLE's promotion gate [[xiong-2026-maple]]. Its insistence on provenance and version lineage is what makes later recall by source possible, the failure that [[wmd-commission-2005-report]] documents for human intelligence and that [[johnson-1993-source]] shows human memory cannot do on its own.
