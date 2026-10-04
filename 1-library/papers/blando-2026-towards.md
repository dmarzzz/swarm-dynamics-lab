---
id: blando-2026-towards
type: paper
title: "Towards Agentic Agent-based Models: Feasibility, Performance, and Statistical Model Checking"
authors: ["Stefano Blando", "Emanuele Guerrazzi", "Riccardo Porcedda", "Giuseppe Squillace", "Max Tschaikowski", "Andrea Vandin"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2607.17948
doi: null
arxiv: '2607.17948'
cite: "Blando, S., Guerrazzi, E., Porcedda, R., Squillace, G., Tschaikowski, M., & Vandin, A. (2026). Towards agentic agent-based models: Feasibility, performance, and statistical model checking. arXiv:2607.17948."
topics: [llm-agent-swarms, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Takes Mesa's Schelling segregation model and makes one agent delegate neighbour classification to a locally served LLM via tool calls (incrementing similar/different counters from natural-language neighbour descriptions), while all others use the symbolic rule. Uses the statistical model checker MultiVeStA, integrated with Mesa, to estimate classical ABM observables and quantify how the LLM component changes behaviour, reliability and cost.

## Contribution

A minimal controlled hybrid (one LLM agent inside a rule-based ABM) analysed with statistical model checking rather than ad hoc replications.

## Key results

- Preliminary: smaller local models fail simple semantic classification or become operationally unusable during repeated tool-call generation; larger tested models pass the checks.

## Methods and models

Mesa + MultiVeStA; local LLMs via Ollama (Qwen 3.5 family per HTML links); Schelling model.

## Limitations and open questions

Abstract only; preliminary, one LLM agent, one model (Schelling).

## Relevance to us

Borrow idea: use statistical model checking (sequential sampling until a CI target) to decide how many runs a stochastic LLM-in-the-loop sim needs. Builds on [[gh-mesa-mesa]]; relates to [[fachada-2026-can]].
