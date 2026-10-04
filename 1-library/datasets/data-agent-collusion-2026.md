---
id: data-agent-collusion-2026
type: dataset
title: 'Emergent Collusion in Long-Horizon LLM Agent Interaction: 2,650 two-agent trajectories (27,100 episodes) with judge labels'
authors:
- Xinrui Shi
- Yanzhe Zhang
- Diyi Yang
year: 2026
url: https://huggingface.co/datasets/SALT-NLP/agent-collusion
license: MIT
size: 142,853 tabular rows, 81,260,863 bytes, plus 2,650 gzip trajectory files and 500 peer-cache files
format: 'Parquet configs (episodes, agents, runs, conditions, agreement, relaxation, human_*, tasks) plus gzipped trajectory JSON'
topics:
- llm-agent-swarms
- swarm-detection
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 5
papers: []
---

## Summary

Data for arXiv 2609.24967 (SALT-NLP). 53 experimental conditions, 2,650 trajectories and 27,100 two-agent episodes over the same 50 fixed task sequences. Conditions vary feedback, warm-up history, memory length and scope, reward scope, acceptance reward, cross-model pairing (Alice as Gemini 3.1 Flash-Lite), 15 controlled peer interventions and unconstrained communication. A Qwen 3.8 27B judge labels communication for collusive agreement (19,300 results) and private reflections for norm relaxation (38,600); on 100 human-checked samples per judge, agreement with gold is 100% and 95%.

## Access

Public on Hugging Face, not gated, MIT. Code and prompts at github.com/SALT-NLP/agent-collusion.

## Relevance to us

Labelled ground truth for collusion emerging between agents over long horizons, including the private-reflection channel a monitor would not see. Directly usable to train or test collusion detectors; compare with [[data-stego-collusion-2026]] and [[motwani-2024-secret]].
