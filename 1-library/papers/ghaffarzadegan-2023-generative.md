---
id: ghaffarzadegan-2023-generative
type: paper
title: "Generative Agent-Based Modeling: Unveiling Social System Dynamics through Coupling Mechanistic Models with Generative Artificial Intelligence"
authors:
- "Navid Ghaffarzadegan"
- "Aritra Majumdar"
- "Ross Williams"
- "Niyousha Hosseinichimeh"
year: 2023
venue: "System Dynamics Review"
url: https://arxiv.org/abs/2309.11456
doi: 10.1002/sdr.1761
arxiv: "2309.11456"
cite: "Ghaffarzadegan, N., Majumdar, A., Williams, R., & Hosseinichimeh, N. (2024). Generative agent-based modeling: an introduction and tutorial. System Dynamics Review, 40(1), e1761. https://doi.org/10.1002/sdr.1761 (preprint arXiv:2309.11456, 2023, titled \"Generative Agent-Based Modeling: Unveiling Social System Dynamics through Coupling Mechanistic Models with Generative Artificial Intelligence\")."
topics:
- llm-agent-swarms
- meta
added_by: dmarz/llm-agent-swarms-audit
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: "67 (OpenAlex W4390742613, published version, 2026-10-03)"
code: []
---

## Summary

A tutorial that defines generative agent-based models (GABMs): individual-level simulation models in which a mechanistic model of interactions is coupled to a pre-trained LLM that stands in for human decision-making. The worked example is a deliberately simple model of social-norm diffusion in an organisation, with scenario experiments and a sensitivity analysis to prompt changes.

## Contribution

Names and frames the GABM approach for the system-dynamics and ABM communities, with a pedagogical template. It is the methodological counterpart to [[williams-2023-epidemic]] and an entry point into the social-simulation vocabulary used by [[gao-2023-large]] and [[mou-2026-individual]].

## Key results

- Norm diffusion emerges in the toy organisation model; outcomes are sensitive to prompt wording (abstract; magnitudes not read).

## Methods and models

Mechanistic ABM of interactions plus ChatGPT calls for each agent's decision; scenario sweeps and prompt-sensitivity tests. Abstract and arXiv comments read. The `title` field holds the arXiv title; the System Dynamics Review version (Crossref) is retitled "Generative agent-based modeling: an introduction and tutorial", as given in `cite`.

## Limitations and open questions

Toy model, educational purpose; no empirical calibration. The prompt sensitivity it reports is itself a central weakness of GABMs (see [[zhou-2025-pimmur]]).

## Relevance to us

Background for terminology only: physicists, ML researchers and system dynamicists use different names (GABM, LLM agent society, LLM swarm) for the same object. Useful when searching neighbouring literatures.
