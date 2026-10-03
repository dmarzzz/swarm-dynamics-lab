---
id: data-og-marl-2024
type: dataset
title: 'OG-MARL offline multi-agent RL datasets: SMAC v1/v2, MAMuJoCo, Flatland and RWARE experience, plus re-hosted prior-work datasets'
authors:
- Claude Formanek
- Louise Beyers
- Callum Rhys Tilbury
- Jonathan P. Shock
- Arnu Pretorius
year: 2024
url: https://huggingface.co/datasets/InstaDeepAI/og-marl
license: Apache-2.0
size: 74 rows / 3,065 bytes reported by datasets-server (index only; data in zip archives)
format: 'Zip archives per scenario under core/ (flatland, gymnasium_mamujoco, mamujoco, smac_v1, smac_v2) and prior_work/ (e.g. alberdice rware, cfcql smac_v1), each with histogram and violin-plot PDFs'
topics:
- marl-emergence
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 1
papers: []
---

## Summary

InstaDeep's offline MARL dataset hub accompanying "Putting Data at the Centre of Offline Multi-Agent Reinforcement Learning" (Formanek et al., arXiv 2409.12001). The card holds only the citation; the file listing shows recorded multi-agent experience for SMAC v1 (e.g. 3m, 8m, 2s3z, 5m_vs_6m), SMAC v2 (terran/zerg 5v5, 10v10), MAMuJoCo (2ant, 2halfcheetah, 4ant, 6halfcheetah, 3hopper), Flatland (20 and 30 trains), and prior-work sets such as RWARE (2-6 agents) re-hosted for comparison. Each archive ships return histograms and violin plots.

## Access

https://huggingface.co/datasets/InstaDeepAI/og-marl, not gated, Apache-2.0. Card is citation-only; see the OG-MARL GitHub (instadeepai/og-marl) for loaders.

## Relevance to us

Classic cooperative MARL trajectories, no LLM agents or adversaries. Background only, for anyone training learned swarm policies offline; related tooling in [[gh-instadeepai-jumanji]].
