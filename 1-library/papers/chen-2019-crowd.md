---
id: chen-2019-crowd
type: paper
title: 'Crowd-Robot Interaction: Crowd-Aware Robot Navigation With Attention-Based Deep Reinforcement Learning'
authors:
- Changan Chen
- Yuejiang Liu
- Sven Kreiss
- Alexandre Alahi
year: 2019
venue: 2019 International Conference on Robotics and Automation (ICRA)
url: https://arxiv.org/abs/1809.08835
doi: 10.1109/icra.2019.8794134
arxiv: '1809.08835'
cite: 'Chen, C., Liu, Y., Kreiss, S., & Alahi, A. (2019). Crowd-Robot Interaction: Crowd-Aware Robot Navigation With Attention-Based Deep Reinforcement Learning. In 2019 International Conference on Robotics and Automation (ICRA), 6015–6022. https://doi.org/10.1109/icra.2019.8794134'
topics:
- crowds-and-traffic
- swarm-robotics
- marl-emergence
added_by: dmarz/crowds-and-traffic-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: 536 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex budget exhausted)
code: []
---

## Summary

Trains a robot to cross a simulated crowd using value-based deep RL, with a value network that models both robot–human and human–human interactions. Each human's pairwise feature with the robot is embedded together with a local occupancy map of that human's neighbours; a self-attention module scores how much each human matters, and the weighted crowd representation feeds a value network used for one-step lookahead planning. In circle-crossing simulations with five ORCA-driven humans, the attention model (SARL / LM-SARL) reaches the goal without collisions and faster than ORCA, CADRL and LSTM-RL baselines, and it was deployed on a Segway robot.

## Contribution

Introduced attention-based crowd pooling to RL navigation and released the CrowdNav simulator, which became the default benchmark for learned social navigation. It moves the robot–crowd problem from first-order reaction (velocity obstacles, [[van-den-berg-2011-reciprocal]]) towards modelling how humans influence each other and hence the robot.

## Key results

Measured in simulation (500 random test episodes, five humans on a 4 m radius circle, goals on the opposite side):
- Invisible setting (humans ignore the robot): success / collision / time (s) / reward — ORCA 0.43 / 0.57 / 10.86 / 0.054; CADRL 0.78 / 0.22 / 10.80 / 0.222; LSTM-RL 0.95 / 0.03 / 11.82 / 0.279; SARL 1.00 / 0.00 / 10.55 / 0.338; LM-SARL 1.00 / 0.00 / 10.46 / 0.342.
- Visible setting: ORCA 0.99 success but 12.29 s; LM-SARL 1.00 success, 0 collisions, 10.59 s, discomfort frequency 0.03, reward 0.334.
- Qualitative: attention weights concentrate on humans that will influence the robot's path, not simply the nearest one; real-world demo on a Segway Loomo (video, no quantitative metrics).

## Methods and models

State: robot (position, velocity, goal, preferred speed, radius) and observable human states; reward +1 at goal, −0.25 for collision, a penalty −0.1 + d/2 when closer than 0.2 m. Value network with MLP embeddings, local map of neighbours around each human, self-attention scores α_i, weighted sum of human features, and an MLP value head. Imitation pre-training on 3k ORCA demonstrations (50 epochs), then 10k episodes of ε-greedy value-based RL (γ = 0.9, ε decaying 0.5 to 0.1), about 10 hours on one CPU. 80 discrete holonomic actions (5 speeds, 16 headings). Simulated humans run ORCA with Gaussian-sampled parameters. Code and simulator: https://github.com/vita-epfl/CrowdNav (MIT, 738 stars, last push 2022-08-26, per GitHub API).

## Limitations and open questions

- Very small crowds (five humans) driven by ORCA, so "human" behaviour is itself a velocity-obstacle model; sim-to-real transfer is only demonstrated qualitatively.
- Holonomic robot and instant velocity changes; assumes full observability of human positions and velocities.
- Later work showed that policies trained in CrowdNav can exploit the ORCA humans and generalise poorly to real crowds; I did not check that here.

## Relevance to us

A compact, open benchmark for a learning agent embedded in a simulated swarm, and a pattern (attention pooling over neighbours) that applies directly to learned swarm policies with variable neighbour counts. Natural test bed for comparing ORCA ([[van-den-berg-2011-reciprocal]]), social force ([[helbing-1995-social]]) and anticipatory models ([[karamouzas-2014-universal]]) as the simulated crowd. Related prediction models: [[gupta-2018-social]], [[salzmann-2020-trajectron]].
