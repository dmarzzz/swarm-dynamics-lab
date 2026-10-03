---
id: wang-2026-agentsnare
type: paper
title: 'AgentSnare: Learning to Delay, Divert, and Defuse Autonomous Penetration Agents'
authors:
- Ruoyu Wang
- Heng Zhao
- Renjie Wu
- Mengnan Zhao
- Zhixuan Chu
- Wanyu Lin
- Tianhang Zheng
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2607.26998
doi: null
arxiv: '2607.26998'
cite: 'Wang, R., Zhao, H., Wu, R., Zhao, M., Chu, Z., Lin, W., & Zheng, T. (2026). AgentSnare: Learning to Delay, Divert, and Defuse Autonomous Penetration Agents. arXiv preprint arXiv:2607.26998.'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Argues that static decoy artefacts are eventually recognised and bypassed by advanced pentest agents, and proposes a trajectory-adaptive deception system. A learned artefact-construction policy proposes new decoy artefacts conditioned on the agent's interaction history; they are validated and added to a factually consistent decoy environment that unfolds as the agent explores. Across 15 CVE-Bench web applications and three attacker models, AgentSnare absorbed 46.8% of tool calls in the decoy, kept 55.9% of post-entry actions there, grounded 90.0% of completion reports in decoy evidence, and no real target was exploited at pass@3 across 45 attacker-CVE pairs.

## Contribution

Moves LLM-agent deception from fixed traps ([[pasquini-2024-hacking]], [[ayzenshteyn-2025-cloak]]) to adaptive, history-conditioned decoys, partly answering the evasion results in [[cordeiro-2026-rouxii]].

## Key results

- 46.8% of agent tool calls absorbed by the decoy; 55.9% of post-entry actions retained; 90.0% of completion attempts grounded in decoy evidence; 0 of 45 attacker-CVE pairs exploited the real target at pass@3 (abstract).

## Methods and models

CVE-Bench web apps; three attacker LLMs; learned policy model for artefact generation plus a consistency validator. Abstract-level read.

## Limitations and open questions

Abstract only; whether the attackers were deception-aware is not stated there.

## Relevance to us

For swarms, an adaptive decoy that keeps an agent busy also produces a long behavioural trace for classification. The "defuse" idea (agents reporting success on fake evidence) could poison a swarm's shared memory. Related: [[gans-2026-when]].
