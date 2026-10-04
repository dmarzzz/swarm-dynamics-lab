---
id: quanta-2019-smarter
type: blog
title: "Smarter Parts Make Collective Systems Too Stubborn"
authors: [Jordana Cepelewicz]
year: 2019
url: https://www.quantamagazine.org/smarter-parts-make-collective-systems-too-stubborn-20190226/
site: quantamagazine.org
topics: [collective-decision, llm-agent-swarms, swarm-intelligence]
added_by: shadow/sol-w3
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Quanta article (26 Feb 2019) on a Science Advances paper by Neil Johnson's group (DOI 10.1126/sciadv.aau5902, co-author Pedro Manrique) inspired by how fly-larva body segments steer the larva without central control. In their model, agents share a goal but cannot communicate; each repeatedly chooses left or right using a strategy from its own set, scored on whether the whole system moved toward a target, and keeps strategies that work. With memory of only one or two past outcomes, agents are too correlated and the collective zigzags. With seven or more remembered outcomes they become too uncorrelated and "stubborn", treating short runs of bad outcomes as noise. Trajectories are most efficient at about five remembered outcomes, a sweet spot that grows only slightly with agent count. Albert Kao (SFI) links this to his finding that medium-sized groups often decide best, against simple wisdom-of-crowds expectations, and calls it a "second wave" after early naive enthusiasm. Jessica Flack (SFI) calls much of the decentralisation discourse, including blockchain hype, naive.

## Key claims

- Collective performance is non-monotonic in component sophistication: there is an optimum memory length (about 5) beyond which the collective gets worse (measured in simulation).
- Too-simple parts over-correlate; too-capable parts under-correlate and lose agility (model interpretation).
- Medium group sizes are often optimal for decision accuracy (Kao's prior work, as reported).
- Assumptions that decentralised systems are inherently more robust or less exploitable are often untested (Flack, opinion).

## Evidence quality

Journalism summarising one simulation paper plus interviews. The core result is from an abstract agent model, not from biological or engineered data. The paper itself is not yet catalogued; group-size result is [[kao-2014-decision]].

## Relevance to us

Directly relevant to LLM agent swarms, where the obvious lever is making each agent more capable (more context, more memory). This is a documented case of the opposite effect: more capable parts gave a worse collective via loss of correlation. It motivates sweeping per-agent context or memory length as an experimental variable, not just agent count. Related: [[kao-2014-decision]], [[kao-2014-collective]], [[sumpter-2010-collective]].
