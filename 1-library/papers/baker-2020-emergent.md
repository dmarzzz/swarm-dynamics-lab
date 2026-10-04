---
id: baker-2020-emergent
type: paper
title: Emergent Tool Use From Multi-Agent Autocurricula
authors: [Bowen Baker, Ingmar Kanitscheider, Todor Markov, Yi Wu, Glenn Powell, Bob McGrew, Igor Mordatch]
year: 2020
venue: International Conference on Learning Representations (ICLR 2020)
url: https://arxiv.org/abs/1909.07528
doi: null
arxiv: '1909.07528'
cite: Baker, B., Kanitscheider, I., Markov, T., Wu, Y., Powell, G., McGrew, B., & Mordatch, I. (2020). Emergent tool use from multi-agent autocurricula. In International Conference on Learning Representations (ICLR 2020). arXiv:1909.07528.
topics: [marl-emergence]
added_by: dmarz/marl-emergence
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "372 for the arXiv record (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Two teams of 1 to 3 agents play hide-and-seek in a MuJoCo world with movable, lockable boxes and ramps. The only
reward is team-level visibility (hiders +1 if all hidden, -1 otherwise; seekers the opposite), yet self-play
with PPO at large scale produces six successive strategy phases: chasing, fort building with boxes, ramp use
by seekers, ramp hiding and locking by hiders, "box surfing" by seekers (a physics exploit), and locking all
boxes by hiders. Each phase changes the task for the other team, which the authors call an autocurriculum.
They compare against count-based and RND intrinsic motivation, which produce much less object interaction in
high-dimensional state spaces, and propose transfer to five probe tasks as an evaluation; hide-and-seek
pretraining helps on 3 of 5, modestly.

## Contribution

The most widely cited demonstration that open-ended, qualitatively new collective strategies can emerge from
competitive co-adaptation with a fixed simple reward, building on the autocurricula argument of
[[leibo-2019-autocurricula]] and the CTDE critics of [[lowe-2017-multi]]. It also contributed the entity-centric,
masked self-attention policy that later swarm and MARL work reuses for variable agent numbers.

## Key results

- Six emergent phases, consistent across 3 seeds; phase timing: fort building after about 25 million episodes,
  ramp use about 75 million later, ramp defence about 10 million after that, box surfing after about 380 million
  total episodes (measured).
- Division of labour: 2- and 3-hider teams lock 25% and 36% more boxes than single hiders during preparation.
- Scale matters: the default (batch 64,000 chunks of 10 transitions, 1.6M parameters) needs 132.3 million
  episodes (31.7 billion frames, 34 hours) to reach ramp defence; batch sizes 8,000 and 16,000 never converged.
- Less environment randomisation yields fewer phases or different, simpler strategies.
- Intrinsic motivation baselines: count-based exploration moves boxes only if the state is hand-reduced to 2D
  box position; with full state, box and agent movement drop sharply; RND slightly better.
- Transfer: hide-and-seek pretraining beats scratch and count-based pretraining on Lock and Return, Sequential
  Lock and Blueprint Construction, is worse on Object Counting and slower on Shelter Construction; differences
  are small, which the authors attribute to entangled representations.

## Methods and models

Agents are spheres with discretised force and torque, a grab action and a team lock action; observations are
positions and velocities of entities within line of sight and a 135-degree cone, plus 30 lidar rays. Policy:
per-entity embeddings, masked residual self-attention, masked average pooling, LSTM; separate actor and critic,
critic omniscient (centralised training, decentralised execution); parameters shared across agents. PPO with GAE
on the "rapid" distributed framework. Episodes 240 steps, 40% preparation phase. Code:
https://github.com/openai/multi-agent-emergence-environments

## Limitations and open questions

Phase identification is qualitative and depends on hand-made statistics; reward curves alone do not reveal it.
Required compute (billions of frames) puts replication out of reach of most labs, and the transfer evaluation
gives weak signal. Teams are small (at most 3 v 3), so it says little about large-swarm scaling. The box-surfing
phase exploits a simulator quirk, a reminder that "emergence" can be emergence of exploits.

## Relevance to us

Canonical citation for emergent coordination and division of labour from competition, and a cautionary data
point on compute. For a swarm hackathon, the reusable pieces are the entity-attention policy (compare the mean
embedding of [[huttenrauch-2019-deep]]) and the methodology of tracking behavioural statistics to detect strategy
phase shifts, which resembles order-parameter tracking in [[durve-2020-learning]].
