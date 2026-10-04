---
id: wang-2026-weclawarena
type: paper
title: "WeClawArena: An Auditable Sandbox and Benchmark for Cross-User Agents Collaboration and Security in Human-Centered Agent Networks"
authors: ["Prince Zizhuang Wang", "Aojie Yuan", "Haiyue Zhang", "Xiyang Hu", "Yue Zhao", "Shuli Jiang"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2608.03499
doi: null
arxiv: '2608.03499'
cite: "Wang, P. Z., Yuan, A., Zhang, H., Hu, X., Zhao, Y., & Jiang, S. (2026). WeClawArena: An auditable sandbox and benchmark for cross-user agents collaboration and security in human-centered agent networks. arXiv:2608.03499."
topics: [llm-agent-swarms, sybil-resistance]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: [gh-kingofspace0wzz-weclawarena]
---

## Summary

Each human owner has a persistent personal agent with private workspace resources, role-specific tools and local policies; agents must complete shared tasks by messaging peers across owners. 124 base tasks in six domains (bargaining, bidding, travel, multi-owner software engineering, clinical, trading) are expanded into 620 variants: one benign control plus four attack conditions (collaboration poisoning, security, privacy, governance/invalid authority). The sandbox logs peer messages, tool calls, resource operations and final workspace state; utility and attack success are scored separately from runtime evidence.

## Contribution

First end-to-end sandbox for owned-agent networks (OpenClaw-style personal agents) where attacks travel across owners rather than within one agent.

## Key results

- Benchmark size: 124 base tasks, 620 matched variants, 6 domains, 5 conditions per task (abstract and README).

## Methods and models

Python 3.11 runtime with Docker-backed simulations and an OpenClaw gateway plugin; HF dataset kingofspace0wzz/WeClawArena.

## Limitations and open questions

Abstract only; model results not read. Small per-task populations (a few owners), not swarm scale. Repo has 1 star.

## Relevance to us

Borrow idea: the 'invalid identity / consent / mandate path' governance attack class is directly the agent-identity question our Sybil work cares about; auditing attack success from bounded runtime evidence is a pattern worth copying. Relates to [[veganmosfet-2026-brokenclaw]].
