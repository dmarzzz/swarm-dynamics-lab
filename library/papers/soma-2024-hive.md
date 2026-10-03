---
id: soma-2024-hive
type: paper
title: "The Hive Mind is a Single Reinforcement Learning Agent"
authors: ["Karthik Soma", "Yann Bouteiller", "Heiko Hamann", "Giovanni Beltrame"]
year: 2024
venue: "arXiv preprint"
url: "https://arxiv.org/abs/2410.17517"
doi: null
arxiv: "2410.17517"
cite: "Soma, K., Bouteiller, Y., Hamann, H., & Beltrame, G. (2024). The Hive Mind is a Single Reinforcement Learning Agent. arXiv preprint arXiv:2410.17517. https://arxiv.org/abs/2410.17517"
topics: ["collective-decision", "marl-emergence", "swarm-intelligence"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null  # not in OpenAlex quota today; not checked
code: []
---

## Summary

Shows a formal equivalence between collective decision-making by imitation and trial-and-error learning by a single agent: in the weighted voter model of honeybee waggle-dance recruitment, the population-level dynamics are those of a single online reinforcement learning agent aggregating action-value samples from many parallel instances of a multi-armed bandit. The authors name the implied update rule Maynard-Cross Learning.

## Contribution

Connects the swarm decision literature (weighted voter model as in [[valentini-2017-best]], [[talamali-2021-when]]) to reinforcement learning, complementing the collective-learning model [[kao-2014-collective]].

## Key results

- Weighted voter model dynamics equal a single RL agent's update on a multi-armed bandit (analytical derivation, per the abstract).
- Abstract-level reading only; numbers beyond the abstract were not checked.

## Methods and models

Mean-field analysis of the weighted voter model and comparison with replicator and Cross learning dynamics (details not checked). Preprint (v1 23 Oct 2024).

## Limitations and open questions

Preprint; no journal reference on the arXiv page; equivalence presumably holds in the mean-field limit only.

## Relevance to us

Gives a bridge for the MARL side of the hackathon: a swarm of imitators can be analysed as one learner. Related: [[reina-2024-speed]], [[march-pons-2024-honeybee]].
