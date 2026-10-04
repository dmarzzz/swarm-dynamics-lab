---
id: de-marzo-2023-emergence
type: paper
title: Emergence of Scale-Free Networks in Social Interactions among Large Language Models
authors:
- Giordano De Marzo
- Luciano Pietronero
- David Garcia
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2312.06619
doi: null
arxiv: '2312.06619'
cite: De Marzo, G., Pietronero, L., & Garcia, D. (2023). Emergence of scale-free networks in social interactions among large language models. arXiv preprint arXiv:2312.06619.
topics:
- llm-agent-swarms
- criticality-measurement
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "4 (OpenAlex W4389650052, arXiv record, 2026-10-03); Semantic Scholar 30 same day"
code: []
---

## Summary

Generative agents powered by GPT-3.5-turbo choose whom to follow, and the resulting network can be scale-free, as in human online social networks. A skewed token prior over agent names disrupts this, producing extreme centralisation; renaming agents to remove the prior lets the model generate networks ranging from random to realistic scale-free.

## Contribution

Early statistical-physics result on LLM collectives: emergent network topology and a demonstration that token-level priors can masquerade as collective dynamics.

## Key results

- Scale-free degree distributions emerge once name priors are removed (abstract).
- Name token priors cause extreme centralisation (abstract).

## Methods and models

Sequential network growth where LLM agents choose links; renaming control. Code not checked.

## Limitations and open questions

Single model (GPT-3.5); growth process only. Abstract-level read.

## Relevance to us

Methodological lesson used later in [[de-marzo-2024-ai]] (random names, relabelling to kill label bias), essential for any swarm experiment with named agents.
