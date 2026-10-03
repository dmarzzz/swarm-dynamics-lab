---
id: ivanov-2022-collective
type: paper
title: 'Collective Adaptation in Multi-Agent Systems: How Predator Confusion Shapes Swarm-Like Behaviors'
authors: [Georgi Ivanov, George Palamas]
year: 2022
venue: arXiv preprint
url: https://arxiv.org/abs/2209.06338
doi: null
arxiv: '2209.06338'
cite: 'Ivanov, G., & Palamas, G. (2022). Collective adaptation in multi-agent systems: How predator confusion shapes swarm-like behaviors. arXiv preprint arXiv:2209.06338.'
topics: [marl-emergence, collective-motion]
added_by: dmarz/marl-emergence-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null  # OpenAlex budget exhausted and Semantic Scholar returned 429 on 2026-10-03
code: []
---

## Summary

Prey agents in a Unity game environment are trained with PPO to forage, avoid walls and avoid a predator, and the
authors ask which anti-predator hypothesis (predator confusion or dilution of risk) is needed for groups to form.
They compare a local-observation model (ray-cast perception within a radius) with a global model in which the
predator is always visible, and analyse group density, formation, evasion and foraging rate. They report that
dilution of risk alone is enough to produce group formation, with predator confusion strengthening collaborative
behaviour, and that the amount of information exchanged changes the collective pattern.

## Contribution

Separates two classic anti-predator hypotheses inside one RL training setup, which [[hahn-2019-emergent]] and
[[li-2023-predator]] bundle together. It is a game-engine study rather than a physics model.

## Key results

- Group formations emerge under dilution of risk alone; adding a predator-confusion process further supports
  collaborative behaviour (claimed in the abstract and discussion; I did not check the figures quantitatively).
- Local versus global observation of the predator changes group density and evasion behaviour (claimed).

## Methods and models

Unity ML-Agents with PPO. Rewards: +0.5 for feeding, -1 for being caught, -0.5 for hitting a wall. Agents perceive
walls, food and other agents by ray casting within an observation radius; the global model also always sees the
predator. Agents need several steps to turn. A predator-confusion process reduces the predator's targeting
success when many prey are nearby. Comparison against a Reynolds Boids baseline [[reynolds-1987-flocks]].

## Limitations and open questions

Unpublished preprint, single environment, no standard order parameters, and statistical detail is thin. The
confusion mechanism is hand-designed, so the result depends on how it is parameterised.

## Relevance to us

Useful as a design reference if the hackathon wants to separate dilution from confusion in a learned-prey
experiment. Weaker evidence than [[li-2023-predator]]; read alongside [[hahn-2019-emergent]].
