---
id: tang-2024-gensim
type: paper
title: "GenSim: A General Social Simulation Platform with Large Language Model based Agents"
authors: ["Jiakai Tang", "Heyang Gao", "Xuchen Pan", "Lei Wang", "Haoran Tan", "Dawei Gao", "Yushuo Chen", "Xu Chen", "Yankai Lin", "Yaliang Li", "et al."]
year: 2024
venue: "NAACL 2025 Demo Track; arXiv preprint"
url: https://arxiv.org/abs/2410.04360
doi: null
arxiv: '2410.04360'
cite: "Tang, J., Gao, H., Pan, X., Wang, L., Tan, H., Gao, D., Chen, Y., Chen, X., Lin, Y., Li, Y., et al. (2024). GenSim: A general social simulation platform with large language model based agents. arXiv:2410.04360. (NAACL 2025 Demo Track.)"
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "64 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

LLM-agent social simulation platform that abstracts a set of general functions for building custom social scenarios, supports up to one hundred thousand agents, and adds error-correction mechanisms so long simulations recover when agents or the run go wrong. Evaluated on large-scale simulation efficiency and on the effect of error correction.

## Contribution

Error correction during a run as a platform feature, alongside 100k-agent scale.

## Key results

- Supports 100,000 agents (abstract); efficiency and error-correction evaluations reported without numbers in the abstract.

## Methods and models

Built by the Renmin/Alibaba group behind AgentScope (shared authors with [[pan-2024-very]]).

## Limitations and open questions

Abstract only; no code link checked.

## Relevance to us

Borrow idea: in-run error correction for long LLM sims. Related: [[pan-2024-very]], [[gh-agentscope-ai-agentscope]].
