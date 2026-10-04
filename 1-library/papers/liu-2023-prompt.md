---
id: liu-2023-prompt
type: paper
title: "Prompt Injection attack against LLM-integrated Applications"
authors: [Yi Liu, Gelei Deng, Yuekang Li, Kailong Wang, Zihao Wang, Xiaofeng Wang, Tianwei Zhang, Yepang Liu, Haoyu Wang, Yan Zheng, Leo Yu Zhang, Yang Liu]
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2306.05499
doi: null
arxiv: '2306.05499'
cite: "Liu, Y., Deng, G., Li, Y., Wang, K., Wang, Z., Wang, X., Zhang, T., Liu, Y., Wang, H., Zheng, Y., et al. (2023). Prompt Injection attack against LLM-integrated Applications. arXiv:2306.05499."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

An exploratory study of prompt injection on ten commercial LLM-integrated applications, followed by HouYi, a black-box attack modelled on web injection. HouYi has three parts: a pre-constructed prompt that blends into the application's context, an injection prompt that induces a context partition (making the model treat what follows as a new instruction block), and the malicious payload. Deployed on 36 real applications.

## Contribution

Showed that a structured "context partition" step, analogous to closing a quote in SQL injection, makes goal hijacking work against real deployed applications.

## Key results

- Measured: 31 of 36 real LLM-integrated applications were susceptible.
- Reported: 10 vendors validated the findings, including Notion.
- Demonstrated outcomes: unrestricted use of the underlying LLM and theft of application prompts.

## Methods and models

Black-box testing of deployed applications; an iterative attack-generation loop. Only the abstract was read.

## Limitations and open questions

Direct injection by the user; 2023 applications; abstract-level reading.

## Relevance to us

Q3. The context-partition idea is the structural core of identity overwrite: convince the model that the old instruction block has ended and a new one begins. A sub-agent's memory format is a context the attacker can try to partition in the same way. Precedes the indirect and agentic forms in [[greshake-2023-not]], [[zhan-2024-injecagent]]; compare the formal treatment in [[liu-2023-formalizing]] and the original goal-hijack measurement in [[perez-2022-ignore]].
