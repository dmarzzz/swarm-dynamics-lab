---
id: tian-2023-evil
type: paper
title: "Evil Geniuses: Delving into the Safety of LLM-based Agents"
authors: [Yu Tian, Xiao Yang, Jingyuan Zhang, Yinpeng Dong, Hang Su]
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2311.11855
doi: null
arxiv: '2311.11855'
cite: "Tian, Y., Yang, X., Zhang, J., Dong, Y., & Su, H. (2023). Evil Geniuses: Delving into the Safety of LLM-based Agents. arXiv:2311.11855."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []  # github.com/T1aNS1R/Evil-Geniuses, not opened
---

## Summary

A study of LLM agent safety along three axes: number of agents, role definition and attack level. A template-based attack tests the effect of agent quantity; Evil Geniuses (EG) is an automated method that uses red-blue exercises to generate attack prompts that stay close to an agent's original role while being more aggressive. Evaluated on CAMEL, MetaGPT and ChatDev with GPT-3.5 and GPT-4.

## Contribution

Introduced role-consistent attack prompts: malicious instructions crafted to look like the target agent's own role, which makes them harder to spot than generic jailbreaks.

## Key results

- Reported (abstract): high attack success rates on CAMEL, MetaGPT and ChatDev.
- Reported (abstract): agents are less robust than standalone LLMs, more prone to harmful behaviour, and able to generate stealthier harmful content.
- Exact rates not checked at this read depth.

## Methods and models

Red-blue prompt generation loop on GPT-3.5 and GPT-4 backbones within three multi-agent frameworks. Only the abstract was read.

## Limitations and open questions

Abstract-level reading; 2023 frameworks; harmful-content outcomes rather than tool actions.

## Relevance to us

Q3. Role-similar attack prompts are the textual analogue of impersonating the parent: an injection that sounds like the sub-agent's own mission is more likely to be absorbed as identity rather than rejected as foreign. Also an early data point that more agents in a system can mean more attack surface, which matters for Q2 sizing of n. Related: [[zhang-2024-psysafe]], [[li-2024-measuring]].
