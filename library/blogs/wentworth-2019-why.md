---
id: wentworth-2019-why
type: blog
title: "Why Subagents?"
authors: ["johnswentworth"]
year: 2019
url: https://www.lesswrong.com/posts/3xF66BNSC5caZuKyC/why-subagents
site: LessWrong
topics: [fork-merge-security, collective-decision]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: full
relevance: 2
---

## Summary

Curated 2019 LessWrong post (180 points, 50 comments) giving a decision-theoretic reason for modelling a single system as a committee of sub-agents. Standard coherence theorems say a non-exploitable system maximises some utility function, but they mishandle incomplete preferences (an agent that keeps pepperoni if it has pepperoni and mushroom if it has mushroom, never trading either way, is not exploitable yet has no utility function over toppings). Wentworth shows any consistent (acyclic) preference relation can be represented exactly as a committee of utility maximisers that must agree unanimously to any change: embed the preference DAG in a space where A is preferred to B iff B is higher on every axis, each axis being one sub-agent's utility; the minimum number of sub-agents needed is the order dimension of the preference graph. Path-dependent preferences reduce to the same case by adding hidden state (his example: a market has no representative agent because the wealth distribution across traders is hidden state, and traders never spontaneously redistribute wealth among themselves). The post then speculates that humans are such committees and that an AI reading a connectome would find many optimisers, not one. Theory post with a worked construction; no experiments.

## Key claims

- Any acyclic preference relation is exactly representable by a unanimity committee of utility-maximising sub-agents; the required committee size is the order dimension of the preference graph.
- "No preference" between states is better read as "prefers to stay put" than as indifference; that reading is what makes path dependence and hidden state tractable.
- Markets are the canonical example: efficient and inexploitable, yet no single utility function, because internal wealth distribution is hidden state.
- Hypothesis (unargued beyond analogy): human behaviour approximates a committee of utility maximisers.

## Evidence quality

Mathematical argument with a correct construction (order dimension embedding), presented informally with diagrams; links to prior LessWrong coherence-theorem material rather than published economics, though the representative-agent nonexistence result is standard. No empirical content. The human-cognition claim is explicitly a hypothesis.

## Relevance to us

Background theory for the fork-merge-security topic. It gives a clean formal reading of what merging sub-agents back into a parent costs: a parent whose preferences are a unanimity committee of its forks is non-exploitable but can be frozen (prefers to stay put whenever forks disagree), and any merge rule that collapses the committee into one utility function throws away information or introduces exploitable cycles. The hidden-state construction also says that two parents that look identical third-partyly can differ in how their sub-agents are weighted, which is the state a corrupted fork would try to shift. Pairs with [[kulveit-2024-hierarchical]] (Kulveit on agency across levels), and with the Byzantine-aggregation literature elsewhere in the library.
