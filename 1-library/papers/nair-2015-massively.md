---
id: nair-2015-massively
type: paper
title: Massively Parallel Methods for Deep Reinforcement Learning
authors:
- Arun Nair
- Praveen Srinivasan
- Sam Blackwell
- Cagdas Alcicek
- Rory Fearon
- Alessandro De Maria
- Vedavyas Panneershelvam
- Mustafa Suleyman
- Charles Beattie
- Stig Petersen
- Shane Legg
- Volodymyr Mnih
- Koray Kavukcuoglu
- David Silver
year: 2015
venue: Deep Learning Workshop, International Conference on Machine Learning (ICML 2015), Lille, France (per arXiv comment)
url: https://arxiv.org/abs/1507.04296
doi: null
arxiv: '1507.04296'
cite: Nair, A., Srinivasan, P., Blackwell, S., Alcicek, C., Fearon, R., De Maria, A., Panneershelvam, V., Suleyman, M., Beattie, C., Petersen, S., et al. (2015). Massively Parallel Methods for Deep Reinforcement Learning. Deep Learning Workshop, International Conference on Machine Learning (ICML 2015), Lille, France (per arXiv comment). arXiv:1507.04296.
topics:
- fork-merge-security
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Gorila (General Reinforcement Learning Architecture) distributes DQN across many machines: parallel actors generate experience in their own environment instances, parallel learners sample from a distributed replay memory and compute gradients, and a sharded central parameter server applies the incoming gradients asynchronously to the master copy of the Q-network, which actors and learners periodically fetch. Evaluated on 49 Atari games with 100 actors, 100 learners and 31 parameter-server shards. Read: abstract, introduction, architecture, the stability section, setup and the headline results.

## Contribution

The first massively distributed deep RL architecture, establishing the actor / learner / parameter-server pattern later refined by Ape-X and IMPALA.

## Key results

- Outperformed single-machine DQN in 41 of 49 games, reached DQN's performance roughly ten times faster in wall time, and reached 75% or more of a human professional's score in 25 games under human starts (measured).
- Stability safeguards against disappearing nodes and slow machines: the parameter server discards gradients computed from parameters older than a staleness threshold, and each learner discards gradients whose absolute DQN loss exceeds its running mean plus several standard deviations (described design, section 4.2; effect not ablated in the parts I read).

## Methods and models

Bundled mode (each machine runs an actor and a learner); replay memory of 1 million frames per bundle; epsilon-greedy exploration annealed from 1 to 0.1; target network synced every 60K updates; AdaGrad. Presented at the Deep Learning Workshop, ICML 2015 (per the arXiv comment).

## Limitations and open questions

Safeguards target benign faults (latency, stragglers, crashes), not adversaries. The loss-outlier filter is applied by each learner to its own gradients, so a compromised learner would not apply it.

## Relevance to us

Q2: Gorila contains the earliest fault filters in the distributed RL line: drop stale contributions and drop contributions whose loss is a statistical outlier. Both are the benign-fault ancestors of Byzantine aggregation, and both are applied in the wrong place for an adversarial setting (the outlier filter runs at the worker, not the server). Q3: a corrupted worker here returns gradients; the parameter server applies them without cross-checking, so there is no k-of-n property. Related: [[espeholt-2018-impala]], [[horgan-2018-distributed]], [[fan-2021-fault-tolerant]], [[alistarh-2018-byzantine]].
