---
id: shibayama-2026-deep
type: paper
title: A Deep Reinforcement Learning Framework for Closed-loop Guidance of Fish Schools via Virtual Agents
authors: [Takato Shibayama, Hiroaki Kawashima]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2603.28200
doi: null
arxiv: '2603.28200'
cite: Shibayama, T., & Kawashima, H. (2026). A deep reinforcement learning framework for closed-loop guidance of fish schools via virtual agents. arXiv preprint arXiv:2603.28200 (v2).
topics: [marl-emergence, collective-motion]
added_by: dmarz/marl-emergence-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null  # OpenAlex budget exhausted and Semantic Scholar returned 429 on 2026-10-03
code: []
---

## Summary

A PPO policy trained in simulation drives projected virtual fish that interact in real time with schools of live
rummy-nose tetras (Petitella bleheri), with the goal of steering the school toward a target direction that
switches every 90 steps. The reward combines directional guidance with staying close to the school. In tank
experiments the virtual agent significantly biased the school's direction under white and grey backgrounds but
not black; guidance weakened from 5 to 8 real fish, and several independently controlled virtual agents did no
better than one fixed formation.

## Contribution

One of the few closed-loop tests of an RL-trained agent inside a living collective, extending robot-fish and
virtual-reality fish work to learned controllers. It is the "influence a real swarm" counterpart to learned-swarm
simulations such as [[durve-2020-learning]].

## Key results

- Background colour had a significant effect on the guidance metric R (LMM, F(2,9) = 47.0, p < 0.001); estimated
  mean R was above zero under white (95% CI 0.14-0.19) and grey (0.12-0.17) but not black (-0.01-0.05) (measured,
  Nr = 3 fish).
- Guidance was significant in all six group-size and agent configurations (all p < 0.001) but group size had a
  strong effect (F(1,18) = 26.7, p < 0.001), with R lower at 8 fish than at 5 (measured).
- Multiple independently controlled virtual agents did not improve guidance over a fixed formation (measured).
- The learned agent moves toward the target while staying near the school and returns when it gets too far ahead.

## Methods and models

Simulated training school, PPO with continuous state, composite reward (direction plus cohesion), compared against
a single-reward formulation from the authors' earlier work. Deployment: overhead tracking (YOLOv8) and projected
2D fish images; trials of 900 steps (~18 min), four trials per condition. Experiment A: 3 fish, background colour
and image size; Experiment B: 5 or 8 fish, fixed versus independent virtual agents.

## Limitations and open questions

Very small groups (3 to 8 fish), four trials per condition, fish drawn repeatedly from small holding populations,
and purely visual stimuli with no hydrodynamic cue. The authors note the declining influence with group size as the
main open problem; whether it is a scaling law or an artefact of the visual stimulus is unknown.

## Relevance to us

Concrete evidence that steering a real collective with a learned agent gets harder as the group grows, which is a
measurable target for any "controlling swarms" project. Compare with leadership work such as
[[couzin-2005-effective]] and with data-driven fish models like [[calovi-2014-swarming]].
