---
id: nwyin-2026-multi-agent
type: blog
title: "Multi-Agent Coordination Lets Us Pour More Compute Into Post-Training"
authors: ["nwyin"]
year: 2026
url: https://www.lesswrong.com/posts/oKpwJBAAqmQdvq2jL/multi-agent-coordination-lets-us-pour-more-compute-into-post
site: LessWrong (personal blog)
topics: [llm-agent-swarms]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: full
relevance: 2
---

## Summary

Short post (9 points, 0 comments, 2026-09-22) making one systems argument: training a policy that can spawn and coordinate other agents changes the unit of an RL rollout from a single linear trajectory to an asynchronous tree of dozens or hundreds of trajectories, so far more inference compute can be usefully spent per training sample, and if you want coordination to be learned rather than bolted on you must put those large multi-agent trajectories inside the post-training loop. It quotes Brown on the Dwarkesh podcast (thorough ablations at 10,000 agents are too expensive, so methodical science at 64, 128, 256 is needed; under 10% of the Navier-Stokes credit goes to multi-agent, the rest to the base model) and OpenAI's GPT-5.6 builder's guide, which lists three end-to-end trained interventions: persisted reasoning across turns with native compaction, native multi-agent orchestration for parallel decomposition, and programmatic tool calling to keep deterministic work out of the context window. The author guesses the internal Astra model is trained with a refined recipe for native orchestration, expects efficiency to improve from the 300B-token Navier-Stokes run, and notes Brown's remark that the training is brittle, with many "useless" rollouts where instances never communicate or inject context into each other. Reproduces the Terminal-Bench 2.1 multi-agent chart.

## Key claims

- Multi-agent capability is a lever on post-training compute scaling, not only on test-time compute, because rollouts become trees.
- OpenAI trained GPT-5.6 end-to-end with native orchestration, compaction and programmatic tool use.
- Learned coordination is currently brittle, with frequent non-communicating rollouts.

## Evidence quality

Inference from two primary sources (Brown interview, OpenAI builder's guide), both quoted, plus the author's speculation about internal recipes. No original data.

## Relevance to us

Modest. It supplies the training-side explanation for why swarm behaviour and inter-agent messaging are now model-native rather than harness features, which bears on where coordination priors (and the collusion transfer discussed in [[mallen-2026-openai]] and [[hunma-2026-what]]) come from. Brown's "64, 128, 256" remark is a useful statement that the scaling data behind [[ord-2026-swarm]] stops at 16 agents and that the next measurements should be at those sizes. Primary: [[brown-2026-agent]].
