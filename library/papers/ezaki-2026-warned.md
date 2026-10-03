---
id: ezaki-2026-warned
type: paper
title: "Warned alike, AI agents avoid the less-crowded road while people take it"
authors:
- "Takahiro Ezaki"
- "Naoto Imura"
- "Katsuhiro Nishinari"
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2609.30883
doi: null
arxiv: "2609.30883"
cite: "Ezaki, T., Imura, N., & Nishinari, K. (2026). Warned alike, AI agents avoid the less-crowded road while people take it. arXiv preprint arXiv:2609.30883."
topics:
- llm-agent-swarms
- crowds-and-traffic
- collective-decision
added_by: dmarz/llm-agent-swarms-recent-audit
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: "0 (Semantic Scholar, 2026-10-03); OpenAlex not retrieved (HTTP 429)"
code: []
---
## Summary

A two-road congestion game run with populations of LLM agents, humans, and mixtures. Adding one sentence warning that others might follow a routing tip made populations of 50 GPT agents crowd one road and avoid the nearly empty alternative: average travel time rose from 64 to 95 min, although any agent on the crowded road could have saved 69 min by switching alone. The pattern persisted for 100 rounds. Two other model families shifted the same way without locking onto one road. Twelve all-human groups (240 participants) stayed near balance. In 24 mixed groups (a further 240 participants), imbalance grew with the share of agents, and humans increasingly took the road the agents avoided; with 15 agents and 5 humans, agent seats averaged 80 min vs 44 min for human seats.

## Contribution

A human-vs-LLM comparison of a classic traffic/minority-game dilemma showing that a shared forecast can synchronise homogeneous agents into a collectively inefficient state, the correlated-strategy failure that minority-game theory predicts. Adds human baselines that most LLM swarm papers lack.

## Key results

- Measured (abstract): 50 GPT agents with the warning: mean travel time 64 -> 95 min; unilateral switch would save 69 min; persists for 100 rounds.
- Measured: 12 all-human groups (240 people) near balance under the same information.
- Measured: 24 mixed groups (240 people): imbalance increases with agent share; agent seats 80 min vs human seats 44 min at 15 agents + 5 humans.

## Methods and models

Repeated two-road congestion game; information conditions: numerical reports, a routing tip, tip plus warning. GPT agents plus two other model families (not named in the abstract). Registered analysis for the mixed groups.

## Limitations and open questions

- Abstract-level read; exact models, prompts and payoff functions not checked.
- Two roads only; whether the lock-in survives heterogeneity in models or prompts is a natural follow-up (cf. [[okawa-2026-emergence]], [[bertalanic-2026-ringelmann]] on heterogeneity).

## Relevance to us

A clean, cheap testbed connecting LLM swarms to crowds-and-traffic dynamics, with a human baseline. Directly testable: does model or temperature diversity restore balance? Related: [[takata-2025-emergent]], [[mori-2026-three]].
