---
id: wu-2026-collective
type: paper
title: 'Collective Loss of Control in LLM Agent Systems: An Epidemic Account of Mutation,
  Contagion, and Recovery'
authors:
- Xiangfan Wu
- Zonghao Ying
- Huiyu Wu
- Xing Zheng
- Huangsheng Cheng
- Xiaorong Shi
- Jing Guo
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.18460
doi: null
arxiv: '2609.18460'
cite: 'Xiangfan Wu; Zonghao Ying; Huiyu Wu; Xing Zheng; Huangsheng Cheng; Xiaorong
  Shi; Jing Guo. (2026). Collective Loss of Control in LLM Agent Systems: An Epidemic
  Account of Mutation, Contagion, and Recovery. arXiv preprint, arXiv:2609.18460.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: shadow/sol-g74
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

The paper separates an epidemic account of collective loss of control from the experiments that support only parts of it. A deployment audit finds unintended communication paths, while RogueHandoff-20 tests whether recipients adopt unsafe transferred trajectories. On four routes, injected histories produce much more executed harm than clean tasks or paired direct requests, without demonstrating an autonomous cascade.

## Contribution

Published evidence or modelling of propagation, containment or evaluation across agent trust boundaries.

## Key results

RogueHandoff-20 contains 20 scenarios. Executed harm is 0-5% on clean tasks and 40-95% after history injection, exceeding paired direct requests by 5-45 percentage points, as reported in the abstract.

## Methods and models

Read the source abstract and bibliographic record only. No experiments were reproduced.

## Limitations and open questions

Abstract-level inspection. Full methods, uncertainty intervals and adaptive-threat assumptions have not been independently checked.

## Relevance to us

Directly informs the child-to-parent handoff threat. Natural rare-event rates and an autonomous epidemic were not established. Compare [[triedman-2025-multi]] and [[lee-2024-prompt]].
