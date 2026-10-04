---
id: hahn-2019-emergent
type: paper
title: Emergent Escape-based Flocking Behavior using Multi-Agent Reinforcement Learning
authors: [Carsten Hahn, Thomy Phan, Thomas Gabor, Lenz Belzner, Claudia Linnhoff-Popien]
year: 2019
venue: Proceedings of the Conference on Artificial Life (ALIFE 2019)
url: https://arxiv.org/abs/1905.04077
doi: null
arxiv: '1905.04077'
cite: Hahn, C., Phan, T., Gabor, T., Belzner, L., & Linnhoff-Popien, C. (2019). Emergent escape-based flocking behavior using multi-agent reinforcement learning. In Proceedings of the 2019 Conference on Artificial Life (ALIFE 2019), MIT Press. arXiv:1905.04077.
topics: [marl-emergence, collective-motion]
added_by: dmarz/marl-emergence-audit
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: null  # OpenAlex budget exhausted and Semantic Scholar returned 429 on 2026-10-03
code: []
---

## Summary

SELFish ("Swarm Emergent Learning Fish") asks whether flocking appears when prey are rewarded only for staying
alive near a predator that can be distracted by several nearby prey. Constant-speed prey on a 2D torus choose
turning angles; one prey is trained with DQN (5 discrete turns) or DDPG (continuous turns), and its network is
copied to all other prey after each episode. The learned prey form Boids-like clusters without any alignment,
cohesion or separation term in the reward. The surprise is that a scripted "TurnAway" policy (flee directly
away from the predator) survives longer, both per agent and for the group, so the learned flock is a
self-interested trap that the authors compare to defection in a Prisoner's Dilemma.

## Contribution

An early (2019) demonstration, from the ALife and MARL side, that the predator-confusion hypothesis is enough
for flocking to emerge from a survival-only reward. It predates and anticipates the physics-side predator-prey
co-evolution of [[li-2023-predator]], and contrasts with proxy-reward flocking such as cohesion in
[[durve-2020-learning]]. It also contains a negative result worth keeping: the emergent flock is not the
survival-optimal collective strategy.

## Key results

- Learned prey (both DQN and DDPG) form clusters whose number and size, measured with DBSCAN, are similar to a
  tuned Boids-plus-predator-avoidance baseline; DDPG tends to form one large, denser cluster (measured, 40 agents
  in a 40 x 40 torus).
- Alignment inside clusters is worse than Boids (the learned agents "quiver"); pairwise distances inside clusters
  are similar across all four policies (measured, Figs. 6-7).
- Even with the predator pinned at a fixed position, learned agents still form a swarm at the far side and
  circulate around each other, which the authors use to argue the flock is not just common flight direction.
- Policies trained with only 10 agents transfer to 20 to 100 agents because each agent observes a fixed number
  of nearest neighbours.
- TurnAway gives the longest survival and the lowest catch rate per frame across 20 to 100 agents (Figs. 8-9); the
  learned policies and Boids are worse. The authors interpret flocking as a Nash-like trap: a lone deviator from
  the swarm is more likely to be picked off. Agents become isolated in the last ~100 steps before being caught.

## Methods and models

Torus of 40 x 40 units, agents and predator as circles of radius 1, capture when centres are closer than 2. Prey
speed constant; predator equal speed with occasional short accelerations, turns limited to +-45 degrees, picks
a random target if several prey are in range and keeps it for a while. Reward +1 per step alive, -1000 on capture.
Observation: (distance, bearing, absolute orientation) of predator, self and the n nearest neighbours,
normalised; the best configurations observed n = 5 neighbours (DQN) and n = 1 (DDPG). DQN: 500,000 steps, 10
hidden layers of 16 units, Adam lr 0.001, gamma 0.999999, epsilon-greedy 0.1, batch 64; DDPG: 5 hidden layers
(actor 16, critic 32 units), batch 512, OU noise (theta 0.15, sigma 0.3). Keras-RL implementation; one learner, policy copied to
the others after each episode (episodes end on capture or after 10,000 steps). Video at
https://youtu.be/SY59CYaqWpE. No code repository given.

## Limitations and open questions

Short workshop-style paper: few seeds reported, no error bars on most figures, a scripted non-learning predator,
and a "copy one learner" scheme that is not concurrent MARL. Order is quantified with cluster statistics rather
than standard polarisation or milling order parameters. Whether the flock-as-trap result survives concurrent
learning, a learning predator, or a different confusion model is open.

## Relevance to us

A cheap, reproducible predator-confusion setup whose central negative result (learned flocking is not
survival-optimal) is a ready-made hypothesis to test with proper order parameters. Read with
[[li-2023-predator]], [[ivanov-2022-collective]], [[durve-2020-learning]] and the Boids baseline
[[reynolds-1987-flocks]].
