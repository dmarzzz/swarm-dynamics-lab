---
id: ng-2026-microverse
type: paper
title: "MicroVerse: An Instrument for Measuring Self-Authored Identity Drift in Long-Horizon Multi-Agent Language-Model Simulations"
authors: ["Sky Ng", "Brihi Joshi", "Ishan Gupta", "Shirley Huang", "Zonglin Di", "Yun Shen", "Qianfeng Wen", "Yifan Simon Liu", "Ruoqi Gao", "Yilan Fan", "et al."]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2608.15844
doi: null
arxiv: '2608.15844'
cite: "Ng, S., Joshi, B., Gupta, I., Huang, S., Di, Z., Shen, Y., Wen, Q., Liu, Y. S., Gao, R., Fan, Y., et al. (2026). MicroVerse: An instrument for measuring self-authored identity drift in long-horizon multi-agent language-model simulations. arXiv:2608.15844."
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "2 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Agents carry an immutable 'soul file' (values, moral boundaries, personality, goals) plus a mutable current identity, and live in a resource-scarce 50x50 grid where water does not respawn and each tick has an existence cost. Eight verbs (trade, talk, attack, scavenge, ...) map to moral boundaries. Importance-triggered reflection rewrites the current identity; drift is scored offline against the original soul with a paraphrase-aware, value-anchored diff. Snapshots of all agents, living and dead, are taken every N ticks to avoid survivor bias.

## Contribution

A measurement instrument for persona fidelity under scarcity, with explicit survivor-bias control.

## Key results

- Anti-self-deception is the largest category of identity modification: 27 of 111 added boundaries (24%).
- Drift direction is robust across reflection thresholds {40, 80, 150}; lower thresholds revise more often.
- Authors call these preliminary existence proofs: one model, one seed per arm, n = 25 agents.

## Methods and models

Three-layer memory, reflection gate on accumulated importance, uniform longitudinal snapshots plus forced end snapshot.

## Limitations and open questions

One model, one seed per arm, 25 agents; no code link found on the arXiv page. Abstract only.

## Relevance to us

Borrow idea: snapshot all agents (including dead) on a fixed schedule so that measurement is decoupled from survival; and the soul-file vs current-identity split as a cheap drift metric for long sims. Same group as [[li-2026-matraix]].
