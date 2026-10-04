---
id: gh-wslong20-g-safeguard
type: code
title: 'G-Safeguard: GNN anomaly detection and edge pruning on LLM multi-agent utterance graphs (ACL 2025)'
repo: wslong20/G-safeguard
url: https://github.com/wslong20/G-safeguard
authors: [Shilong Wang, Guibin Zhang, Miao Yu, Guancheng Wan, Fanci Meng, Chongye Guo, Kun Wang, Yang Wang]
year: 2025
language: Python
license: none detected by GitHub API
stars: 47
last_commit: 2025-06-28
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [wang-2025-g-safeguard]
---

## Summary

Official code for G-Safeguard (arXiv 2502.11127, ACL 2025 main). The method builds an utterance graph of a multi-agent system, trains a graph neural network to flag anomalous agents, and then intervenes on topology by cutting edges from flagged nodes. The abstract reports recovering over 40% of lost performance under prompt injection, adaptation across LLM backbones, and use in large multi-agent systems. The repository has separate pipelines for memory attacks (`MA`), prompt injection (`PI`) and tool attacks (`TA`) plus a scalability study. The memory attack pipeline generates train and test conversation datasets, builds a GNN training set, trains for 50 epochs, and evaluates on random and other graph types with gpt-4o-mini by default.

## What it can do for us

Q2 and Q3: it is a detector that looks at who influenced whom rather than at one message, which fits the fork-merge setting where the parent sees reports from many children and can compare them. The MA pipeline is a ready memory-attack scenario in a multi-agent graph, the closest benchmarked analogue I found to a corrupted child carrying poisoned memory back. A limitation for Q2 is that a GNN detector trained on one attack distribution gives no corruption threshold guarantee; it is a statistical filter, so an adaptive attacker who knows it is the open case.

## Run notes

Not run. `conda create -n gsafeguard python=3.10`, `pip install -r requirements.txt`, set `BASE_URL` and `OPENAI_API_KEY`; then in `MA/` run the generation scripts, `python gen_training_dataset.py`, `python train.py --epochs 50 --batch_size 32 --lr 0.001`, and `python main_defense_for_different_topology.py --graph_type random --gnn_checkpoint_path <path> --model_type gpt-4o-mini`.

## Limitations

No licence file. Needs an OpenAI-compatible backend. Detection is supervised on generated attack conversations, so robustness to unseen or adaptive attacks is not established by the README. Shares authors and code lineage with [[gh-ymm-cll-netsafe]].
