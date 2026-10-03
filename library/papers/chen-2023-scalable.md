---
id: chen-2023-scalable
type: paper
title: 'Scalable Multi-Robot Collaboration with Large Language Models: Centralized or Decentralized Systems?'
authors:
- Yongchao Chen
- Jacob Arkin
- Yang Zhang
- Nicholas Roy
- Chuchu Fan
year: 2023
venue: 2024 IEEE International Conference on Robotics and Automation (ICRA)
url: https://arxiv.org/abs/2309.15943
doi: 10.1109/ICRA57147.2024.10610676
arxiv: '2309.15943'
cite: 'Chen, Y., Arkin, J., Zhang, Y., Roy, N., & Fan, C. (2024). Scalable multi-robot collaboration with large language models: Centralized or decentralized systems? In 2024 IEEE International Conference on Robotics and Automation (ICRA), pp. 4311-4317. https://doi.org/10.1109/ICRA57147.2024.10610676'
topics:
- llm-agent-swarms
- swarm-robotics
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: "84 (OpenAlex W4401415431, published version, 2026-10-03); 6 (OpenAlex W4387210286, arXiv record, 2026-10-03); Semantic Scholar 202 same day"
code: []
---

## Summary

Compares task success and token efficiency of four LLM-based multi-robot communication frameworks (centralised, decentralised and two hybrids) on four coordination-dependent 2D tasks with increasing numbers of robots, then demonstrates in 3D simulation with vision-to-text and dynamics errors. A hybrid framework gives the best success rates across all four tasks and scales best with more agents.

## Contribution

An early controlled comparison of coordination topologies for LLM robot teams as N grows, anticipating the architecture study of [[kim-2025-towards]].

## Key results

- Hybrid > centralised and decentralised in success rate on all four tasks; best scaling with agent number (abstract).
- Token budget and context-window limits are binding constraints for centralised planners (abstract).

## Methods and models

LLM planners in grid-world box-moving style tasks; 3D simulation follow-up. Project website with code (not opened).

## Limitations and open questions

Small teams (a few to around a dozen robots); idealised perception in 2D. Abstract-level read.

## Relevance to us

Direct evidence on centralised vs decentralised control in LLM robot teams; compare [[ruan-2025-benchmarking]] (global commander variant) and [[kim-2025-towards]].
