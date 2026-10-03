---
id: data-sotopia-pi-2024
type: dataset
title: 'SOTOPIA-pi: generated social tasks and agent-agent conversations for training socially intelligent language agents'
authors:
- Ruiyi Wang
- Haofei Yu
- Wenxin Zhang
- Zhengyang Qi
- Maarten Sap
- Graham Neubig
- Yonatan Bisk
- Hao Zhu
year: 2024
url: https://huggingface.co/datasets/cmu-lti/sotopia-pi
license: CC-BY-SA-4.0
size: 33,410 rows, 3,459,521 bytes (datasets-server)
format: 'JSON/CSV/TSV files: inspirational_prompt.csv, used_prompt.csv, experiment_episodes.json, plus source files social_iqa_train.jsonl, NormBank.csv, social-chem-101.v1.0.tsv'
topics:
- llm-agent-swarms
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Data for SOTOPIA-pi (Wang et al., arXiv 2403.08715, "Interactive Learning of Socially Intelligent Language Agents"). Inspirational prompts from social_iqa, social_chem and NormBank seed new social environments; each is combined with agent profiles and relationships. `experiment_episodes.json` holds every SOTOPIA-pi conversation: scenario, codename, both agents' backgrounds (age, secret, personality), each agent's social goal, and the turn-by-turn exchange. Deal-or-no-deal, mindcraft and persuasion_for_good prompts were left out to avoid leakage into the [[data-sotopia-2024]] test set.

## Access

https://huggingface.co/datasets/cmu-lti/sotopia-pi, not gated, CC-BY-SA-4.0.

## Relevance to us

Two-agent dialogues where agents hold private secrets and goals, which makes them useful seed material for hidden-intent or deception probes. Not a population-scale dataset.
