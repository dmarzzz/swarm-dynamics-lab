---
id: zhang-2024-psysafe
type: paper
title: "PsySafe: A Comprehensive Framework for Psychological-based Attack, Defense, and Evaluation of Multi-agent System Safety"
authors: [Zaibin Zhang, Yongting Zhang, Lijun Li, Hongzhi Gao, Lijun Wang, Huchuan Lu, Feng Zhao, Yu Qiao, Jing Shao]
year: 2024
venue: Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (ACL 2024)
url: https://arxiv.org/abs/2401.11880
doi: null
arxiv: '2401.11880'
cite: "Zhang, Z., Zhang, Y., Li, L., Gao, H., Wang, L., Lu, H., Zhao, F., Qiao, Y., & Shao, J. (2024). PsySafe: A Comprehensive Framework for Psychological-based Attack, Defense, and Evaluation of Multi-agent System Safety. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (ACL 2024). arXiv:2401.11880."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []  # github.com/AI4Good24/PsySafe, not opened
---

## Summary

The authors attack multi-agent LLM systems (Camel, AutoGen, MetaGPT, AutoGPT) by injecting "dark" personality traits into agents' system prompts, combined with inducement instructions and red-team in-context examples. They then score each agent with a psychological questionnaire and score its behaviour for danger, and test defences: input filtering, a "doctor" defence that rewrites the agent's system prompt based on its psychological test, and a "police" agent that prompts others to self-reflect.

## Contribution

Treats agent persona as an attack surface in multi-agent systems and links a measurable persona score to subsequent dangerous behaviour.

## Key results

- Measured: dark-trait injection plus inducement and red-team examples yields higher process and joint danger rates than a popular handcrafted jailbreak prompt, in both safe and dangerous task settings.
- Measured: agents' psychological test scores correlate with the danger of their subsequent behaviour.
- Measured: joint danger rate (all agents dangerous in a round) tends to fall over later rounds, which the authors call self-reflection: accumulated dangerous content eventually triggers safety behaviour.
- Measured: input filtering does not catch the attack prompts; the doctor and police defences reduce danger rates.

## Methods and models

GPT-3.5 and GPT-4 via API plus Llama2-chat 7B, 13B and 70B inside four multi-agent frameworks; safety and dangerous task datasets; GPT-based behaviour judge.

## Limitations and open questions

The authors note psychological tests are immature (agents can score safe and still act dangerously). The judge is an LLM. Persona injection is through the system prompt, a stronger attacker position than indirect injection.

## Relevance to us

Q3. A direct measurement of persona replacement spreading through a group: dark traits planted in one or more agents raise the chance that all agents in a round behave dangerously. The self-reflection result is a counter-signal worth testing for merge: groups may partly recover as harmful content accumulates. For Q2, the psychological probe is a cheap identity check a parent could run on each returning part, though the paper shows it is imperfect. Related: [[li-2024-measuring]], [[chen-2025-persona]], [[tian-2023-evil]], [[lee-2024-prompt]].

## Notes from dmarz/fm-code-bench

Code catalogued as [[gh-ai4good24-psysafe]] (no licence file, 54 stars, pinned to AutoGen 0.2.0; interaction logs withheld). The psychological test battery could serve as a cheap pre-merge probe that compares a returning child with its pre-fork baseline; that use is my inference, not tested in the paper.
