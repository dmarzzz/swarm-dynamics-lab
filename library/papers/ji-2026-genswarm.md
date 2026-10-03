---
id: ji-2026-genswarm
type: paper
title: "GenSwarm: Scalable Multi-Robot Code-Policy Generation and Deployment via Language Models"
authors: ["Wenkang Ji", "Huaben Chen", "Mingyang Chen", "Guobin Zhu", "Lufeng Xu", "Roderich Groß", "Rui Zhou", "Ming Cao", "Shiyu Zhao"]
year: 2026
venue: "npj Robotics"
url: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/s44182-025-00065-w?fields=title,abstract
doi: "10.1038/s44182-025-00065-w"
arxiv: "2503.23875"
cite: "Ji, W., Chen, H., Chen, M., Zhu, G., Xu, L., Groß, R., Zhou, R., Cao, M., & Zhao, S. (2026). GenSwarm: Scalable Multi-Robot Code-Policy Generation and Deployment via Language Models. npj Robotics, 4(1), 5."
topics: [swarm-robotics, llm-agent-swarms]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "11 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

GenSwarm is an end-to-end system in which a multi-agent LLM pipeline turns a natural-language instruction into
white-box control code for each robot in a multi-robot system and deploys it to simulated and real robots. The
authors stress zero-shot adaptation to new or altered tasks, reproducibility and interpretability of code
policies, and scalable software and hardware architectures that automate policy deployment.

## Contribution

One of the first end-to-end instruction-to-execution pipelines for real robot swarms using LLM-generated code,
from the same group as [[sun-2023-mean]]; complements [[strobel-2024-llm2swarm]].

## Key results

- Claimed: zero-shot generation and deployment on simulated and real multi-robot systems (abstract; task
  success rates not checked).

## Methods and models

Multi-language-agent LLM system producing code policies; deployment architecture for real robots. Abstract read
(arXiv 2503.23875; published in npj Robotics, issue dated 2026 per Crossref).

## Limitations and open questions

Code policies are generated centrally before deployment; robustness and verification of generated code at scale
not checked.

## Relevance to us

Direct bridge between the llm-agent-swarms and swarm-robotics topics; a natural baseline if we test LLM-written
swarm controllers.
