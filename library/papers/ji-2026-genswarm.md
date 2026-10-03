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

## Notes from dmarz/llm-agent-swarms-audit

Skim of the arXiv HTML (results and methods), 2026-10-03. Published as npj Robotics 4, 5 (2026), doi 10.1038/s44182-025-00065-w, with 9 authors per Crossref. OpenAlex: 4 citations (W7119543718, published version).

Key results: - With o1-mini, 100 trials per task across 10 tasks (1,000 trials): average success rate 81%. Measured in simulation. - On six representative tasks (100 trials each): GenSwarm 74%, GenSwarm without VLM feedback 71%, Code-as-Policies 40%, MetaGPT 37%, LLM2Swarm 40%, i.e. +34 to +37 points. Measured. - Deployed on a real multi-robot platform (demonstrations).

Methods: Multi-language-agent pipeline (task analysis, code generation, deployment and improvement modules); simulation plus hardware robots; comparison baselines CaP, MetaGPT, LLM2Swarm. Code: https://github.com/WindyLab/GenSwarm . I skimmed the results and method sections of arXiv HTML v-latest.

Limitations: "Success" is task-specific and binary; no collective-motion order parameters (polarisation, cohesion) or scaling with N are reported in what I read. Policies are only as good as the generated code; robustness to noise and robot failure is not quantified.

Relevance: A practical path for the hackathon: generate Vicsek/Couzin-style local rules with an LLM, then measure polarisation and phase transitions as N and noise vary, which [[ruan-2025-benchmarking]] found missing. Same group as [[chen-2023-multi]] (consensus seeking, same group); compare [[li-2025-llm]], [[jimenez-romero-2025-multi-agent]] and [[li-2024-challenges]].
