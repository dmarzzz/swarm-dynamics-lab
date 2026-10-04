---
id: salem-2025-tinytroupe
type: paper
title: "TinyTroupe: An LLM-powered Multiagent Persona Simulation Toolkit"
authors: ["Paulo Salem", "Robert Sim", "Christopher Olsen", "Prerit Saxena", "Rafael Barcelos", "Yi Ding"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2507.09788
doi: null
arxiv: '2507.09788'
cite: "Salem, P., Sim, R., Olsen, C., Saxena, P., Barcelos, R., & Ding, Y. (2025). TinyTroupe: An LLM-powered multiagent persona simulation toolkit. arXiv:2507.09788."
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: [gh-microsoft-tinytroupe]
---

## Summary

Describes Microsoft's TinyTroupe library: fine-grained persona specifications (nationality, age, occupation, personality, beliefs, behaviours), population sampling, programmatic LLM-driven control mechanisms and experimentation/validation support for simulating individuals and groups. Illustrated with brainstorming and market-research sessions; includes quantitative and qualitative evaluations and preliminary comparisons with real human behaviour as control.

## Contribution

A persona-centric MAS toolkit aimed at behavioural studies and business simulations, filling gaps in persona specification and validation that general agent frameworks leave.

## Key results

- Abstract reports evaluations of selected aspects and preliminary human-control experiments, without headline numbers.

## Methods and models

Python library; TinyPerson agents in TinyWorld environments; LLM backends (OpenAI/Azure per README).

## Limitations and open questions

Abstract only. Focus-group scale (few to tens of agents); README says API still changes frequently.

## Relevance to us

Borrow idea / quick prototyping of small persona groups; not a large-population engine. Compare [[gh-google-deepmind-concordia]] and [[li-2026-matraix]].
