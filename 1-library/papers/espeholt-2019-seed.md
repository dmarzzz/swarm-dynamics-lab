---
id: espeholt-2019-seed
type: paper
title: 'SEED RL: Scalable and Efficient Deep-RL with Accelerated Central Inference'
authors:
- Lasse Espeholt
- Raphaël Marinier
- Piotr Stanczyk
- Ke Wang
- Marcin Michalski
year: 2019
venue: International Conference on Learning Representations (ICLR 2020)
url: https://arxiv.org/abs/1910.06591
doi: null
arxiv: '1910.06591'
cite: 'Espeholt, L., Marinier, R., Stanczyk, P., Wang, K., & Michalski, M. (2019). SEED RL: Scalable and Efficient Deep-RL with Accelerated Central Inference. International Conference on Learning Representations (ICLR 2020). arXiv:1910.06591.'
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

SEED RL moves all neural-network computation in distributed RL to a central learner on accelerators (TPUs or GPUs). Actors only step environments: each environment step's observation is streamed to the learner, which runs batched inference, returns the action, and itself assembles the trajectories (observations, actions, policy logits or Q-values, recurrent state) used for training. Implements IMPALA/V-trace and R2D2 in this architecture and evaluates on Atari-57, DeepMind Lab and Google Research Football. Read: abstract, introduction, architecture comparison with IMPALA, the list of design changes and the headline results.

## Contribution

Shows that centralising inference cuts experiment cost by 40-80% and bandwidth for model transfer by up to 99%, while matching or exceeding the state of the art.

## Key results

- 40% to 80% cost reduction against IMPALA-style setups in the scenarios considered (measured, per abstract).
- Reached state-of-the-art Atari-57 performance 3.1 times faster in wall time than R2D2; improved the state of the art on Google Research Football (measured).
- Only observations and actions cross between actors and learner; for the example given, transferring observations needs about 2 GB/s against 148 GB/s for moving models (calculation in section 3).

## Methods and models

Streaming gRPC between actors and learner; batched inference on the learner; up to a 2048-core TPU pod. ICLR 2020 (per the PDF header). Code at github.com/google-research/seed_rl.

## Limitations and open questions

No adversarial actors considered. Actors still report observations and rewards from environments the learner does not see.

## Relevance to us

Q3 and Q1: the architectural move here, keeping the policy, the behaviour probabilities and trajectory assembly on the central learner and reducing each actor to an environment interface, removes two of the levers a corrupted part has in IMPALA and Ape-X: it can no longer misreport which policy it ran or how important its data is. What remains is the observation and reward stream, which is exactly what environment poisoning attacks target ([[rakhsha-2020-policy]], [[ma-2019-policy]]). For a fork-merge agent this suggests a design in which the parent keeps the reasoning and the parts are thin sensors, at the cost of the parts not being able to learn or act autonomously in the remote domain. It also means the parent knows exactly which part sent each step, which conflicts with Q1 hiding. Related: [[espeholt-2018-impala]], [[horgan-2018-distributed]].
