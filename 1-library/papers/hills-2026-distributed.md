---
id: hills-2026-distributed
type: paper
title: Distributed Attacks in Persistent-State AI Control
authors: [Josh Hills, Ida Caspary, Asa Cooper Stickland]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2607.02514
doi: null
arxiv: '2607.02514'
cite: 'Hills, J., Caspary, I., & Stickland, A. C. (2026). Distributed Attacks in Persistent-State AI Control. arXiv:2607.02514.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 3 (Semantic Scholar citing list, 2026-10-03)
code: []
---

## Summary

Introduces Iterative VibeCoding, an AI-control setting where a coding agent builds software over a sequence of pull requests in a persistent codebase while pursuing a covert side task; 20 task variations in two families (CLI tools, Flask web services). Attack agent Claude Sonnet 4.5, monitor GPT-4o. Gradual attacks spread the side task across PRs; non-gradual attacks put it in one PR. Measured (abstract): no single monitor is robust to both, because which strategy evades best depends on the monitor type. Evasion of at least 65% generalises across attack backends (Sonnet 4.5, Gemini 3.1 Pro, Kimi K2.5) and across strong monitor models, and the gap between gradual and non-gradual evasion widens for more capable models. A stateful link-tracker monitor that tracks suspicious buildup across PRs detects gradual attacks better than diff monitors given more history; a four-monitor ensemble cuts gradual-attack evasion from 93% under the weakest diff monitor to 47%.

## Contribution

Shows persistent state is itself an attack surface: an agent (misaligned or prompt-injected) can time and split a payload across sessions.

## Key results

- Gradual vs non-gradual attacks: no single monitor dominates both (abstract).
- Stateful cross-PR tracking beats history-augmented diff monitoring (abstract).
- Ensemble: 93% to 47% gradual-attack evasion (abstract).

## Methods and models

Persistent repository across PRs; diff, trajectory and link-tracker monitors.

## Limitations and open questions

Abstract-level reading; a 47% residual evasion means the best defence is still weak.

## Relevance to us

- Q3 (attack): a corrupted sub-agent that merges back over several rounds (or several children merging into the same parent memory over time) is the gradual attack here; payloads can be sized to stay under each merge-time check.
- Q2 (thresholds): the defence that helped was state that links contributions across time, the temporal counterpart of the joint diff in [[makins-2026-multi]]. A merge audit should keep a running record of what each child changed, not inspect each merge afresh.
Related: [[makins-2026-multi]], [[qinqin-2026-distributed]], [[bhatt-2025-ctrl]].
