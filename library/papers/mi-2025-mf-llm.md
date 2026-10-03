---
id: mi-2025-mf-llm
type: paper
title: "MF-LLM: Simulating Population Decision Dynamics via a Mean-Field Large Language Model Framework"
authors:
- "Qirui Mi"
- "Mengyue Yang"
- "Xiangning Yu"
- "Zhiyu Zhao"
- "Cheng Deng"
- "Bo An"
- "Haifeng Zhang"
- "Xu Chen"
- "Jun Wang"
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2504.21582
doi: null
arxiv: "2504.21582"
cite: "Mi, Q., Yang, M., Yu, X., Zhao, Z., Deng, C., An, B., Zhang, H., Chen, X., & Wang, J. (2025). MF-LLM: Simulating population decision dynamics via a mean-field large language model framework. arXiv preprint arXiv:2504.21582."
topics:
- llm-agent-swarms
- marl-emergence
added_by: dmarz/llm-agent-swarms-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: "Semantic Scholar 16 (2026-10-03); OpenAlex has no record for the arXiv DOI"
code: []
---

## Summary

Instead of letting every LLM agent read every other agent's messages, MF-LLM alternates between a policy model that generates each individual's action conditioned on its private state and a population signal, and a mean-field model that summarises the population's recent actions into an updated signal. A fine-tuning method, IB-Tune, uses an information-bottleneck objective to keep only the parts of the population signal that predict future actions. On a Weibo corpus of about 4,500 real events, simulated population trajectories match real ones better than non-mean-field baselines.

## Contribution

Applies the mean-field idea from statistical physics and mean-field games to LLM social simulation, making population-scale simulation tractable and calibrating it against real data. It complements the physics-fitting approach of [[el-2026-physics]], which fits a mean-field-like model to LLM agents after the fact.

## Key results

- KL divergence to real population action distributions reduced by 47% vs non-mean-field baselines. Measured.
- Removing the mean-field module or IB-Tune degrades performance by up to 118%. Measured (ablation).
- Generalises across 7 domains and 4 LLM backbones (Qwen2-1.5B-Instruct as the main model; GPT-4o-mini, DeepSeek-R1-Distill-Qwen-32B and Qwen2-7B-Instruct without fine-tuning). Measured.

## Methods and models

Iterative mean-field loop; IB-Tune fine-tuning; evaluation by KL, DTW and F1 on LLM-annotated semantic dimensions of real and generated posts. Skimmed introduction and experiments.

## Limitations and open questions

The "mean field" is a learned text summary rather than an analytic order parameter; evaluation relies on an LLM annotator; one social-media corpus.

## Relevance to us

A route to large-N LLM swarms where agents couple through a population signal, as in Vicsek-type mean-field models. Compare [[de-marzo-2024-ai]] (all-to-all coupling), [[yang-2024-oasis]] and [[piao-2025-agentsociety]] (brute-force large-N simulation).
