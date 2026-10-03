---
id: luo-2026-algorithmic
type: paper
title: "Algorithmic Collusion at Test Time: A Meta-game Design and Evaluation"
authors: ["Yuhong Luo", "Daniel Schoepflin", "Xintong Wang"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2602.17203
doi: null
arxiv: "2602.17203"
cite: "Luo, Y., Schoepflin, D., & Wang, X. (2026). Algorithmic Collusion at Test Time: A Meta-game Design and Evaluation. arXiv preprint arXiv:2602.17203."
topics: [agent-budgets, llm-agent-swarms]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Models pricing agents as pretrained policies (competitive, naively cooperative or robustly collusive) plus an in-game adaptation rule, and studies the choice of such meta-strategies as an empirical game. The authors sample normal-form games over meta-strategy profiles, compute payoffs and regret against equilibrium mixtures, and build best-response graphs, evaluating RL, UCB and LLM strategies in repeated pricing with symmetric and asymmetric costs. Code: github.com/chailab-rutgers/CollusionMetagame.

## Contribution

Empirical game-theoretic framing of whether collusion emerges under rational choice of algorithms at test time, without long learning horizons.

## Key results

- Reported (abstract): findings on feasibility of collusion and effectiveness of strategies; no numbers in the abstract.

## Methods and models

Empirical game-theoretic analysis; abstract read only.

## Limitations and open questions

Abstract only.

## Relevance to us

The meta-game method could evaluate which firm-agent designs are stable choices for principals in the swarm factory. Related: [[eschenbaum-2026-auditing]] (strategy graphs).
