---
id: wu-2023-autogen
type: paper
title: 'AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation'
authors:
- Qingyun Wu
- Gagan Bansal
- Jieyu Zhang
- Yiran Wu
- Beibin Li
- Erkang Zhu
- Li Jiang
- Xiaoyun Zhang
- Shaokun Zhang
- Jiale Liu
- Ahmed Hassan Awadallah
- Ryen W White
- Doug Burger
- Chi Wang
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2308.08155
doi: null
arxiv: '2308.08155'
cite: 'Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang, L., Zhang, X., Zhang, S., Liu, J., et al. (2023). AutoGen: Enabling next-gen LLM applications via multi-agent conversation. arXiv preprint arXiv:2308.08155.'
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "2782 (Semantic Scholar, 2026-10-03); the OpenAlex record behind the arXiv DOI is mis-merged with an unrelated work, so no usable OpenAlex count"
code: []
---

## Summary

AutoGen is an open-source framework in which applications are built from "conversable" agents that combine LLMs, tools and human input and interact through programmable conversation patterns (two-agent chats, group chats, nested chats). Interaction behaviour can be specified in natural language or code. The paper demonstrates applications in mathematics, coding, question answering, operations research, online decision-making and games.

## Contribution

A widely used general-purpose orchestration framework; it made multi-agent conversation an engineering pattern rather than a research prototype.

## Key results

- Case-study improvements in several domains (abstract-level; specific numbers not read here).

## Methods and models

Conversable agent abstraction, auto-reply mechanisms, group-chat manager; GPT-4 and GPT-3.5 back ends. Code is the microsoft/autogen project (not opened this session).

## Limitations and open questions

Framework paper: little analysis of collective dynamics, scaling with agent count or failure rates; AG2/AutoGen traces appear in the failure analysis of [[cemri-2025-why]].

## Relevance to us

Infrastructure background; a likely tool for building hackathon experiments, but contributes no swarm-dynamics findings.
