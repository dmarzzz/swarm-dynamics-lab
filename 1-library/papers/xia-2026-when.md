---
id: xia-2026-when
type: paper
title: 'When Should Agent Trust Be Conditional? Characterizing and Attacking Skill-Conditional Reputation in Agent Swarms'
authors:
- Yihan Xia
- Taotao Wang
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2606.14200
doi: null
arxiv: '2606.14200'
cite: 'Xia, Y., & Wang, T. (2026). When Should Agent Trust Be Conditional? Characterizing and Attacking Skill-Conditional Reputation in Agent Swarms. arXiv preprint arXiv:2606.14200.'
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 0 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Studies reputation for routing tasks among heterogeneous LLM agents when trust is conditioned on skill, R(i | k), rather than one global score. Trust estimates pool verified episode outcomes across correlated skills with a coupling matrix W and strength beta (an empirical-Bayes style estimator). A controlled phase diagram shows conditioning beats a single global-best agent only under high agent heterogeneity, sparse per-skill evidence and correlated skills. On 14 public AppWorld agents (4 scaffolds x 4 base models, 168 tasks, 2,352 episodes) skill routing beats the global-best agent by +0.041 score and +0.054 success. The same borrowing is a laundering channel: an agent with one fabricated episode on a cheap farm skill and none on the target skill captures the router, raising routing regret from 0 to 0.9357. Only a zero-evidence gate bounds this.

## Contribution

Turns the classical Sybil and whitewashing analysis of reputation systems (Douceur, Friedman and Resnick, Cheng and Friedman's impossibility for symmetric reputation functions) into a quantitative map for LLM-agent routing, and shows a laundering attack that needs no lying, since every recorded outcome is genuine and verifiable.

## Key results

- Measured (controlled DGP, 12 agents, 4 skills, 500 trials per cell): at H = 0.6, N = 1, conditional regret 0.107 vs independent 0.176 (-40%).
- Measured: clean regret falls from 0.160 to 0.109 for beta >= 0.1 while laundering capture rises from 0 to 0.34 with beta; deployed beta = 0.1.
- Measured (AppWorld test_normal): pool coordinates (H, N, C) = (0.217, 24, 0.795); global 0.743, skill 0.784, oracle 0.933 score. Difficulty strata lower C to 0.56 to 0.68 and raise gain to +0.06 to +0.09; test_challenge (C = 0.82) gives +0.010, rated amber.
- Measured (attack on simple_note to phone, R = 0.861, honest gain +0.1922): launderer, whitewasher (8 episodes, fresh identity) and Sybil splits across k = 1 to 6 identities are all captured at beta >= 0.05, regret 0.9357. The contaminated ungated verdict reads -0.0643.
- Derived: for an agent with zero target evidence the estimate equals its farm score for every budget B >= 1 and every beta > 0, so rate limits and coupling caps cannot help.
- Measured: zero-evidence gate cuts benefit to 0; a "learner" who plants one failing target episode needs 64 farm episodes to recapture; with two or more planted failures, no capture up to 64.

## Methods and models

Estimator tau_hat(i,k) = sum_k' W_kk' n_ik' o_ik' / sum_k' W_kk' n_ik'; variants Independent (W = I), Global (all ones), fixed-block Conditional, and Adaptive (W from positive cross-agent skill correlations). Routing regret against per-skill oracle. Conditional Information Value Test (CIVT) labels a log green if oracle headroom >= 0.05, skill gain >= 0.03 and the per-skill winner is not unique. No models were run; the authors parse published AppWorld leaderboard trajectories.

## Limitations and open questions

Restricted to program-verifiable outcomes; subjective peer ratings, where transitive reputation and classical Sybil collusion return, are out of scope. Skill axis is the primary app only. The authors state explicitly that they do not claim Sybil resistance; the gate bounds a specific attack and is bypassable at a quantified cost. Adaptive coupling, which avoids backfire on benign pools, follows exactly the correlation the attacker exploits.

## Relevance to us

Any agent swarm or marketplace that routes work by reputation will face this attack, and the paper shows the defence has to be structural (evidence gates on the exact skill) rather than rate limits. It complements [[bara-2026-epistemic]] (pooling correlated evidence overstates support) from the reputation side, and provides a concrete threat model for agent marketplaces such as [[karten-2026-agent]] and [[bansal-2025-magentic]], and for the protocol-level trust layers compared in [[hu-2025-inter-agent]]. It also shows why reputation-weighted voting in [[luo-2025-weighted]] needs admission control.
