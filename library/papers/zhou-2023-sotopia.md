---
id: zhou-2023-sotopia
type: paper
title: 'SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents'
authors:
- Xuhui Zhou
- Hao Zhu
- Leena Mathur
- Ruohong Zhang
- Haofei Yu
- Zhengyang Qi
- Louis-Philippe Morency
- Yonatan Bisk
- Daniel Fried
- Graham Neubig
- Maarten Sap
year: 2023
venue: arXiv preprint; publication status discussed in methods bibliography
url: https://arxiv.org/abs/2310.11667
doi: null
arxiv: '2310.11667'
cite: 'Zhou, Xuhui; Zhu, Hao; Mathur, Leena; Zhang, Ruohong; Yu, Haofei; Qi, Zhengyang;
  Morency, Louis-Philippe; Bisk, Yonatan; Fried, Daniel; Neubig, Graham; et al. (2023).
  SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents. arXiv
  preprint; publication status discussed in methods bibliography. arXiv:2310.11667.'
topics:
- meta
- llm-agent-swarms
added_by: vishesh/codex-methods
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

evaluates role-play social goals and identifies challenging scenarios. For experimental methodology, its relevance is scenario diversity and explicit multidimensional scoring. The methods toolkit treats this as bounded evidence rather than a general guarantee of agent performance.

## Contribution

scenario diversity and explicit multidimensional scoring.

## Key results

evaluates role-play social goals and identifies challenging scenarios.

## Methods and models

Primary metadata and available abstract consulted on 2026-10-03. This entry conservatively records `read_depth: abstract`; no new full-paper read or empirical replication is claimed.

## Limitations and open questions

goal achievement in constructed role-play is not general human social intelligence.

Publication status: arXiv version consulted; proceedings status not reverified.

## Relevance to us

Reusable experiment-design evidence for [the methods toolkit](../../tooling/agent-experiments/README.md). This is a source record, not a completed prior-art survey or approval to run an experiment.

## Notes from dmarz/sim-envs

Independently catalogued by the sim-environments lane (read_depth abstract) and folded in here on merge. Lane summary, written for the simulation-environments survey:

SOTOPIA is an open-ended environment in which LLM agents (and humans) role-play characters with private social goals across many scenarios, scored by SOTOPIA-Eval on goal completion and other social dimensions. The authors find large differences between models and identify a hard subset where GPT-4 achieves a significantly lower goal completion rate than humans.
