---
id: williams-2023-epidemic
type: paper
title: "Epidemic Modeling with Generative Agents"
authors:
- "Ross Williams"
- "Niyousha Hosseinichimeh"
- "Aritra Majumdar"
- "Navid Ghaffarzadegan"
year: 2023
venue: "arXiv preprint"
url: https://arxiv.org/abs/2307.04986
doi: null
arxiv: "2307.04986"
cite: "Williams, R., Hosseinichimeh, N., Majumdar, A., & Ghaffarzadegan, N. (2023). Epidemic modeling with generative agents. arXiv preprint arXiv:2307.04986."
topics:
- llm-agent-swarms
- crowds-and-traffic
added_by: dmarz/llm-agent-swarms-audit
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: "16 (OpenAlex W4384111914, arXiv record, 2026-10-03)"
code: []
---

## Summary

An agent-based SIR-type epidemic model in which each agent's daily decision to stay home or go out is made by querying ChatGPT with its health status and news about case counts. The generative agents quarantine when sick and self-isolate as cases rise, and the population produces multiple epidemic waves followed by an endemic period and a flattened curve, without hand-coded behavioural rules.

## Contribution

An early, widely cited demonstration of "generative agent-based modelling" (GABM): replacing a hand-written behavioural rule in a mechanistic model with an LLM call, so that behavioural feedback on the dynamics emerges from the LLM. Companion to the tutorial [[ghaffarzadegan-2023-generative]].

## Key results

- Behavioural feedback (self-isolation when cases rise) emerges from LLM decisions and flattens the epidemic curve (abstract claim).
- Multiple waves then an endemic period appear at the population level (abstract claim; not checked against the figures in this session).

## Methods and models

Agent-based epidemic model coupled to GPT-3.5 (ChatGPT) for individual mobility decisions; I read the abstract only (no arXiv HTML was available).

## Limitations and open questions

Behaviour realism is asserted by plausibility rather than validated against mobility data; costs scale linearly with agents x days; prompt sensitivity is a known issue (a later paper, "Prompt Sensitivity of Generative Agents: Evidence from an Epidemic Model", arXiv 2608.26221, studies it; not opened here). See the validation critique in [[zhou-2025-pimmur]].

## Relevance to us

Background for the GABM vocabulary used by system-dynamics and epidemiology communities, which describes the same "LLM as update rule" idea that physics-style papers ([[de-marzo-2024-ai]], [[el-2026-physics]]) study. Low direct relevance for swarm motion.
