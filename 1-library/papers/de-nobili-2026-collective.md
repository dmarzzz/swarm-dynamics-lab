---
id: de-nobili-2026-collective
type: paper
title: 'Collective Alignment in LLM Multi-Agent Systems: Disentangling Bias from Cooperation via Statistical Physics'
authors:
- Cristiano De Nobili
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2605.10528
doi: null
arxiv: '2605.10528'
cite: 'De Nobili, C. (2026). Collective alignment in LLM multi-agent systems: Disentangling bias from cooperation via statistical physics. arXiv preprint arXiv:2605.10528.'
topics:
- llm-agent-swarms
- criticality-measurement
- sync-consensus
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: "0 (OpenAlex W7160910782, arXiv record, 2026-10-03); Semantic Scholar 4 same day"
code: []
---

## Summary

Places one identical LLM agent on each node of an L x L square lattice; each holds a binary state (+1/-1 as yes/no) and updates it by querying the model with its four nearest neighbours' states. Sampling temperature T is the only control parameter. For llama3.1:8b, phi4-mini:3.8b and mistral:7b, magnetisation and susceptibility are measured under a global-flip protocol that probes Z2 symmetry. All models show temperature-driven order-disorder crossovers and susceptibility peaks; finite-size scaling on even-L lattices gives effective gamma/nu exponents that are model-dependent and close to, but incompatible with, the 2D Ising value 7/4. Fitted effective couplings J(T) and fields h(T) show alignment is dominated by intrinsic bias (h >> J), producing field-driven crossovers rather than genuine phase transitions.

## Contribution

The first finite-size-scaling analysis of an LLM "spin system" on a lattice, and a diagnostic separating apparent consensus caused by shared bias ("echo chamber by default") from genuine neighbour coupling.

## Key results

- Susceptibility peaks and order-disorder crossovers versus T for all three models (abstract).
- Effective gamma/nu near but not equal to 7/4 (abstract).
- h >> J: bias-driven alignment (abstract).

## Methods and models

Lattice Glauber-like dynamics with LLM-queried updates; global-flip protocol; finite-size scaling on even L; extraction of beta-weighted couplings and fields. Local open-weight models. Code not checked.

## Limitations and open questions

Small open-weight models only; lattice sizes limited by inference cost; temperature is a sampling knob, not a thermodynamic temperature. Abstract-level read.

## Relevance to us

A direct template for testing criticality claims in LLM swarms with local interactions; complements the all-to-all analysis of [[de-marzo-2024-ai]] and the signed-network fit of [[el-2026-physics]], and warns that apparent order can be bias rather than coupling.

## Notes from dmarz/llm-agent-swarms-audit

Audit 2026-10-03: checked the single author and abstract on arXiv (three models, global-flip protocol, gamma/nu near but incompatible with 7/4, h >> J). The summary matches. No errors. The `citations` field was rewritten to OpenAlex counts (OpenAlex was reachable for single-work lookups during the audit); the Semantic Scholar count is kept alongside.
