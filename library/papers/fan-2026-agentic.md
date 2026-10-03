---
id: fan-2026-agentic
type: paper
title: "Agentic Commerce World: An Auditable and Verifiable Environment for Vibe Commerce"
authors: ["Shicheng Fan", "Mingdai Yang", "Duohao Wang", "Canyu Chen", "Yongfeng Zhang", "Hua Wei", "Manling Li", "Julian McAuley", "Kun Zhang", "Philip S. Yu", "et al."]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2608.02441
doi: null
arxiv: '2608.02441'
cite: "Fan, S., Yang, M., Wang, D., Chen, C., Zhang, Y., Wei, H., Li, M., McAuley, J., Zhang, K., Yu, P. S., et al. (2026). Agentic Commerce World: An auditable and verifiable environment for vibe commerce. arXiv:2608.02441."
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "2 (Semantic Scholar, 2026-10-03)"
code: [gh-shichengf-acworld]
---

## Summary

ACWorld is a many-to-many market where independently controlled Buyer and Merchant agents transact while keeping private objectives. Every action goes through a Vibe Commerce Protocol that validates it before updating shared transaction state and logs it, making runs auditable and reproducible. Two benchmark tracks: 200 capability-coverage tasks and 60 large-catalog tasks searching 785,022 transactable listings; ten models evaluated.

## Contribution

A validated-action market environment with distinct authority per side, closer to a protocol testbed than to a free-form chat market.

## Key results

- Mean scores across ten models: 65.9%-85.6% on the capability track, 56.1%-91.4% on the large-catalog track.
- Final state alone misses evaluated errors; process-level evidence is needed (authors' analysis).

## Methods and models

Protocol-mediated actions validated by a 'Commerce Intelligence Platform'; deterministic full-catalog oracles score large-catalog decisions (README).

## Limitations and open questions

Abstract only. Scores are per-task capability, not population dynamics; the repo notes v1.1.0 changed scoring so paper numbers need v1.0.0.

## Relevance to us

Borrow idea: validate every agent action against a protocol before it mutates shared state, and keep process logs, as an audit layer for any market sim. Compare [[gh-microsoft-multi-agent-marketplace]] and [[yan-2026-ceo]].
