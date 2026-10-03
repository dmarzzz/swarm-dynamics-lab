---
id: he-2026-visa
type: paper
title: "VISA: A Structured Description Protocol for Agent-Based Simulation Models Towards Machine Reproducibility"
authors: ["Zhou He"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2607.28027
doi: null
arxiv: '2607.28027'
cite: "He, Z. (2026). VISA: A structured description protocol for agent-based simulation models towards machine reproducibility. arXiv:2607.28027."
topics: [meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: [gh-agentlabcn-visa]
---

## Summary

Proposes VISA, a symbol-based protocol describing an ABM in eight linked tables (Agent, Variable, Sensing, Internal Function; Associated Data, Input/Output, Schedule, Validation), with nineteen executable consistency rules and three LLM-executable skills (author, check, code) that run an author-check-code-reproduce loop. Validated on three external ABMs: Epstein's Rebellion and Wolf Sheep Stride Inheritance reproduced from NetLogo to Python, and an industrial AnyLogic aged-care contact model described but not reproducible because of a proprietary movement library and unavailable data.

## Contribution

A machine-checkable successor to prose ODD descriptions, designed so LLM agents can write, check and regenerate models.

## Key results

- Two cross-language reproductions (NetLogo to Python) from VISA specs alone; the AnyLogic model passes all 19 rules but reproduction is blocked by named dependencies.

## Methods and models

Eight-table spec, 19 consistency rules, LLM skills in the companion repo.

## Limitations and open questions

Abstract only; three models is a small validation set; TOMACS under review per repo.

## Relevance to us

Borrow idea: if agents will generate sim code for us, write the model as a checkable table spec first; complements the ODD protocol [[grimm-2020-odd]] and the ODD-to-code study [[fachada-2026-can]].
