---
id: ndousse-2021-icml
type: talk
title: "ICML 2021 talk: Emergent Social Learning via Multi-agent Reinforcement Learning"
authors: [Kamal Ndousse]
year: 2021
url: https://www.youtube.com/watch?v=UctYVUn01ZA
venue: "ICML 2021 presentation; Kamal Ndousse channel, uploaded 2021-07-11"
topics: [marl-emergence, collective-decision]
added_by: shadow/sol-aud
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Kamal Ndousse presents social learning through independently trained agents observing skilled peers rather than receiving their policies or memories. Recovered the previously blocked inbox video using the caption helper's Apify fallback and read all captions through its conclusion, approximately six minutes. The opened YouTube landing page supplies speaker/channel spelling, title, and upload date. This is a full-transcript read, not inspection of the numerical plots.

- [01:33] Training and execution are decentralized in a shared observable environment with separately awarded rewards. The Goal Cycle task has sparse rewards and penalized exploration; [02:08] vanilla model-free reinforcement learning struggles even with experts present. An auxiliary world-model prediction objective lets learners acquire useful representations before they can earn task rewards.
- [02:35] Agents discover the required traversal order of three goal tiles. Their color changes with rewards and penalties, providing a prestige/skill cue that other agents can observe. This supplies an observable expertise signal, not unrestricted access to another agent's private experiences.
- [03:32] Learners trained around experts with the auxiliary loss perform comparably to imitation-learning agents and can exceed experts by avoiding exploration penalties. At [03:50], novices watch experts identify the traversal order, then follow rather than independently incur mistakes. The talk states qualitative comparisons but no numerical effect sizes in the transcript.
- [04:23] Zero-shot transfer to a guided maze task exceeds solo learners, three-goal experts, and imitation-learning experts in the presented comparison. [04:56] The speaker reports social learning with imperfect experts and a mixture of social/solo training supporting both task variants. Generalization is demonstrated within grid-world navigation, not arbitrary real-world robotics or human teaching.

## Relevance to us

A useful population-learning reference separating environmental observation from explicit memory sharing. It suggests evaluating expertise cues, representation-learning objectives, and mixtures of independent and social experience when testing swarm transfer. The prestige cue is trusted here; adversarially spoofed competence or unsafe imitation is not evaluated. No guarantee of safe reintegration follows from successful learning around experts.
