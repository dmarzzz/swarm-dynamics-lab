---
id: zha-2026-autonomous
type: paper
title: 'Autonomous LLM Agent Worms: Cross-Platform Propagation, Automated Discovery
  and Temporal Re-Entry Defense'
authors:
- Mingming Zha
- Xiaofeng Wang
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2605.02812
doi: null
arxiv: '2605.02812'
cite: 'Mingming Zha; Xiaofeng Wang. (2026). Autonomous LLM Agent Worms: Cross-Platform
  Propagation, Automated Discovery and Temporal Re-Entry Defense. arXiv preprint,
  arXiv:2605.02812.'
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

Persistent file-backed state can carry contamination across sessions and across agent frameworks. The authors report autonomous propagation on three production frameworks, including three-hop cross-platform transmission, and examine the role of summaries and scheduled context re-entry. Their proposed architectural defence combines sealed configuration, typed memory promotion and attenuated capabilities, with a conditional no-propagation theorem.

## Contribution

Published evidence or modelling of propagation, containment or evaluation across agent trust boundaries.

## Key results

Three frameworks and three-hop transmission are reported in the abstract. Per-model rates and theorem assumptions were not checked.

## Methods and models

Read the source abstract and bibliographic record only. No experiments were reproduced.

## Limitations and open questions

Abstract-level inspection. Full methods, uncertainty intervals and adaptive-threat assumptions have not been independently checked.

## Relevance to us

Returning child summaries may contaminate durable parent state even when textual copying changes the wording. The defence directly addresses private-to-trusted memory promotion. Compare [[zhang-2026-agentworm]] and [[lin-2026-survey]].
