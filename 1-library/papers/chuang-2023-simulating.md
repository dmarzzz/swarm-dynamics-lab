---
id: chuang-2023-simulating
type: paper
title: Simulating Opinion Dynamics with Networks of LLM-based Agents
authors:
- Yun-Shiuan Chuang
- Agam Goyal
- Nikunj Harlalka
- Siddharth Suresh
- Robert Hawkins
- Sijia Yang
- Dhavan Shah
- Junjie Hu
- Timothy T. Rogers
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2311.09618
doi: null
arxiv: '2311.09618'
cite: Chuang, Y.-S., Goyal, A., Harlalka, N., Suresh, S., Hawkins, R., Yang, S., Shah, D., Hu, J., & Rogers, T. T. (2023). Simulating opinion dynamics with networks of LLM-based agents. arXiv preprint arXiv:2311.09618.
topics:
- llm-agent-swarms
- sync-consensus
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: "3 (OpenAlex W4388787757, arXiv record, 2026-10-03); Semantic Scholar 230 same day"
code: []
---

## Summary

Proposes simulating opinion dynamics with populations of LLM agents instead of rule-based ABMs. LLM agents show a strong built-in bias toward accurate information, so populations converge to consensus aligned with scientific reality (for example on climate change), limiting their use for studying resistance to consensus. Inducing confirmation bias through prompting produces opinion fragmentation consistent with classic opinion-dynamics and ABM results.

## Contribution

An early, much-cited bridge between LLM agents and opinion-dynamics models; established that LLM priors dominate collective outcomes unless deliberately counteracted.

## Key results

- Default LLM populations converge to the scientifically accurate view (abstract).
- Prompted confirmation bias yields fragmentation (abstract).

## Methods and models

Networked LLM agents exchanging messages about claims; prompted cognitive biases. Code not checked.

## Limitations and open questions

Truth bias of aligned models confounds opinion dynamics; later quantified by [[brockers-2025-disentangling]] and [[el-2026-physics]].

## Relevance to us

Standard citation for LLM opinion dynamics; motivates the bias-vs-coupling controls in [[de-nobili-2026-collective]].
