---
id: kutasov-2025-evaluating
type: paper
title: Evaluating Control Protocols for Untrusted AI Agents
authors: [Jon Kutasov, Chloe Loughridge, Yuqi Sun, Henry Sleight, Buck Shlegeris, Tyler Tracy, Joe Benton]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2511.02997
doi: null
arxiv: '2511.02997'
cite: 'Kutasov, J., Loughridge, C., Sun, Y., Sleight, H., Shlegeris, B., Tracy, T., & Benton, J. (2025). Evaluating Control Protocols for Untrusted AI Agents. arXiv:2511.02997.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 9 (Semantic Scholar citing list, 2026-10-03)
code: []
---

## Summary

Systematic evaluation of control protocols in SHADE-Arena, a set of diverse agentic environments. Against a default attack policy, resampling for incrimination and deferring on critical actions performed best, raising safety from 50% to 96%. When the red team iterated, attack policies with extra affordances (knowing when resampling happens, or being able to simulate the monitor) cut the resampling protocol's safety to 17%. Deferring on critical actions stayed highly robust even to the strongest red-team strategies. The authors conclude that denying the attack policy access to protocol internals matters.

## Contribution

Measures how much of a control protocol's safety survives an adaptive adversary that knows or can simulate the protocol.

## Key results

- Default attack: safety 50% baseline to 96% with best protocols (abstract).
- Adaptive attack with knowledge of resampling: resampling protocol safety drops to 17% (abstract).
- Deferring on critical actions: robust to all red-team strategies tried (abstract).

## Methods and models

SHADE-Arena environments; blue-team protocols include defer to trusted, resampling, and defer on critical actions; red team iterated with added affordances.

## Limitations and open questions

Abstract-level reading; models and per-environment numbers not checked.

## Relevance to us

- Q1 (hiding): a measured case where secrecy of the protocol is load-bearing. Resampling, the randomised "which sample counts" defence, lost most of its value once the attacker knew when resampling occurred. A parent that hides which child it will reintegrate gets protection only while that choice stays hidden from the corrupted child.
- Q2 (thresholds): gating only the critical actions (for a merge, the parts of a child's update that touch the parent's goals or memory) was the robust option.
Related: [[bhatt-2025-ctrl]], [[greenblatt-2023-ai]], [[makins-2026-multi]].
