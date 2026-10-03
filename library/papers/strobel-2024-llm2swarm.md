---
id: strobel-2024-llm2swarm
type: paper
title: 'LLM2Swarm: Robot Swarms that Responsively Reason, Plan, and Collaborate through LLMs'
authors:
- Volker Strobel
- Marco Dorigo
- Mario Fritz
year: 2024
venue: NeurIPS 2024 Workshop on Open-World Agents
url: https://arxiv.org/abs/2410.11387
doi: null
arxiv: '2410.11387'
cite: 'Strobel, V., Dorigo, M., & Fritz, M. (2024). LLM2Swarm: Robot Swarms that Responsively Reason, Plan, and Collaborate through LLMs. NeurIPS 2024 Workshop on Open-World Agents. arXiv:2410.11387.'
topics:
- llm-agent-swarms
- swarm-robotics
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 4 (OpenAlex, 2026-10-03); 22 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

A position-plus-showcase paper from swarm-robotics researchers (including Marco Dorigo) on integrating LLMs into robot swarms in two ways. Indirect integration uses an LLM to synthesise and validate robot controllers before deployment (and possibly on the fly), aiming to reduce development time and human error. Direct integration runs a separate LLM instance on each robot during deployment for robot-robot collaboration and human-swarm interaction in natural language. In the showcases, robots with local LLMs detect a variety of anomalies without prior information about their nature. Software and videos are released.

## Contribution

Frames the design space (LLM as controller-writer vs LLM as on-board agent) from inside the swarm-robotics community; frequently cited by later LLM-swarm benchmarks such as [[ruan-2025-benchmarking]].

## Key results

- Claimed (showcases): on-robot LLMs detect anomalies they were not told about and communicate about them.
- Mainly conceptual; no large quantitative evaluation in the abstract.

## Methods and models

Robot swarm showcases (simulator not checked) with LLM-synthesised controllers or per-robot LLM instances. Code: https://github.com/Pold87/LLM2Swarm .

## Limitations and open questions

Workshop paper, proof-of-concept scale. On-board LLM latency and energy are open issues (see the 300x cost in [[rahman-2025-llm-powered]]).

## Relevance to us

Defines the two integration modes we should keep separate in any hackathon design: LLM-written local rules (cheap at runtime, classical dynamics) vs LLM-in-the-loop agents. Related: [[li-2024-challenges]], [[jimenez-romero-2025-multi-agent]].
