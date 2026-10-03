---
id: data-social-llm-networks-2026
type: dataset
title: 'Social-LLM-Networks: opinion exchange among LLMs connected over communication networks'
authors:
- Iris Yazici
- Mert Kayaalp
- Stefan Taga
- Ali H. Sayed
year: 2026
url: https://huggingface.co/datasets/asl-epfl/Social-LLM-Networks
license: MIT
size: not reported (one JSON file per experiment)
format: JSON per experiment with model types, topic, network, system prompt, initial opinions, exchanged texts and sentiment scores
topics:
- llm-agent-swarms
- sync-consensus
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Data for "Opinion Consensus Formation Among Networked Large Language Models" (Yazici, Kayaalp, Taga, Sayed; arXiv 2601.21540, EPFL ASL). LLMs connected by a communication network exchange opinions on debate topics. Experiments vary five factors: model types, debate topics, network topology, system prompts and initial opinion distributions. Each experiment file records those settings, the exchanged texts and the sentiment score attached to each. The card gives no experiment count or size.

## Access

https://huggingface.co/datasets/asl-epfl/Social-LLM-Networks, not gated, MIT.

## Relevance to us

Bridges classical networked consensus and opinion dynamics with LLM agents, with topology as an explicit variable; the natural testbed for asking how many stubborn or sybil nodes it takes to move a networked LLM population.
