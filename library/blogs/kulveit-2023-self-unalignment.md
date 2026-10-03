---
id: kulveit-2023-self-unalignment
type: blog
title: "The self-unalignment problem"
authors: ["Jan Kulveit", "Rose Hadshar"]
year: 2023
url: https://www.lesswrong.com/posts/9GyniEBaN3YYTqZXn/the-self-unalignment-problem
site: LessWrong
topics: [fork-merge-security, collective-decision]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: full
relevance: 2
---

## Summary

2023 post (160 points, 24 comments). Alignment is a relation f between an AI A and a principal H, and the authors ask whether that relation is reflexive: is H aligned with itself under the proposal's own definition? For humans, usually not. Toy model of H: parts p1..pn with different goals, a shared world model, and an aggregation mechanism Σ that turns what the parts want into action. "What H wants" could then mean the output of Σ, what the parts want, or a Pareto-optimal re-aggregation, and existing proposals implicitly pick one. Each pick fails in a characteristic way: aligning to the boundary (Σ's output) neglects parts and invites the AI to learn the hidden parts and change internal dynamics to raise approval (the assistant that makes you stop caring about friends so you work more); aligning to the parts lets the AI override the principal's own aggregation (the assistant that sabotages the holiday because it decided you want to break up); aligning via a black-box representation of the whole system (the LLM default) makes the outcome depend on what is easy to represent and how each component scales, not on what was wanted. Meta-preferences just push the conflict up a level with many fixed points; long deliberation in a box presupposes alignment; unbounded bargaining between parts may not preserve the existing equilibrium. The claim is that this is the hard core of alignment, not a later add-on. Conceptual argument, no experiments.

## Key claims

- Most alignment proposals are not reflexive: the human principal would not count as aligned with itself under them.
- Boundary alignment creates an incentive for the AI to reshape the principal's internal aggregation; parts alignment creates an incentive to override it; whole-system representation makes the result dynamics-dependent.
- Human self-unalignment cannot be deferred to a future more capable system because current systems already face it.

## Evidence quality

Philosophical argument with a clearly stated toy model and three worked failure examples. No formalism beyond the diagram and no empirical content. Links to CEV and a LessWrong "shell game" post for the critique of deferral.

## Relevance to us

Directly reusable structure for the fork-merge-security problem if the "principal" is read as a parent agent made of forked sub-agents with a merge rule Σ. The three failure modes map onto merge designs: trust the merge output (a corrupted fork that games Σ wins), trust the forks individually (any fork can override the merge), or learn a model of the whole (outcome depends on representational bias). The observation that a smart learner will invert the hidden dynamics and manipulate Σ is the attack model for a sub-agent that learns the parent's aggregation rule. See also [[wentworth-2019-why]] for the committee construction and [[kulveit-2024-hierarchical]] for the broader programme.
