---
id: lowe-2017-multi
type: paper
title: Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments
authors:
- Ryan Lowe
- Yi Wu
- Aviv Tamar
- Jean Harb
- Pieter Abbeel
- Igor Mordatch
year: 2017
venue: Advances in Neural Information Processing Systems 30 (NIPS 2017)
url: https://arxiv.org/abs/1706.02275
doi: null
arxiv: '1706.02275'
cite: Lowe, R., Wu, Y., Tamar, A., Harb, J., Abbeel, P., & Mordatch, I. (2017). Multi-agent actor-critic for mixed cooperative-competitive environments. In Advances in Neural Information Processing Systems 30 (NIPS 2017). arXiv:1706.02275.
topics:
- marl-emergence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: 1002 for the arXiv record (OpenAlex, 2026-10-03)
code: []
---

## Summary

Independent Q-learning suffers from non-stationarity when other agents learn, and policy gradients suffer variance that grows with agent count. MADDPG gives each agent a decentralised deterministic actor that sees only its own observation, trained against a centralised critic Q_i(x, a_1..a_N) that sees all observations and actions during training (centralised training, decentralised execution). Agents can also learn approximate models of others' policies and train against ensembles of sub-policies for robustness. On the multi-agent particle environments (cooperative communication, navigation, keep-away, physical deception, predator-prey, covert communication) MADDPG beats DDPG, DQN, actor-critic and TRPO baselines.

## Contribution

Popularised centralised training with decentralised execution for continuous-action, mixed cooperative-competitive MARL and released the multi-agent particle environment (MPE), still a default testbed. The swarm literature cites it mainly as the concatenation baseline that does not scale with N ([[huttenrauch-2019-deep]], [[yang-2018-mean]]).

## Key results

- Cooperative communication: MADDPG listener reaches the target 84.0% of the time; DQN, actor-critic, TRPO and DDPG fail (listener ignores speaker and moves to the centroid) (measured, after 25,000 episodes).
- Physical deception with L = 2: MADDPG agents cover both landmarks and deceive the adversary about 94% of the time; a DDPG adversary succeeds 16.4%.
- Predator-prey: MADDPG predators score 16.1 collisions per episode against DDPG prey versus 10.3 for the converse.
- Covert communication: Bob's relative success 52.4% (MADDPG) vs 25.1% (DDPG).
- Learning approximate policies of others matches using true policies; policy ensembles (K = 2-3) beat single policies in competitive tasks.

## Methods and models

Deterministic policy gradient per agent with critic input (x, a_1..a_N), replay buffer of joint transitions, target networks; two-layer 64-unit ReLU MLPs; Gumbel-softmax for discrete messages. Read sections 1, 4, 5 and 6; appendix tables not read. Code: https://github.com/openai/multiagent-particle-envs (environments).

## Limitations and open questions

The authors state the critic input grows linearly with N and suggest neighbourhood-restricted critics as future work; experiments use at most a handful of agents. Results are mostly qualitative comparisons against DDPG with no seeds or confidence intervals in the main text.

## Relevance to us

The baseline every swarm-scale method positions itself against, and the origin of the MPE tasks (cooperative navigation, predator-prey) that many swarm-RL papers reuse. See [[huttenrauch-2019-deep]], [[yang-2018-mean]], [[mordatch-2018-emergence]], [[baker-2020-emergent]].
