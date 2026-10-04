---
id: chatzinikolaou-2012-use
type: paper
title: "The use of reputation as noise-resistant selection bias in a co-evolutionary multi-agent system"
authors: [Nikolaos Chatzinikolaou, David Robertson]
year: 2012
venue: GECCO '12, Proceedings of the 14th Annual Conference on Genetic and Evolutionary Computation, Philadelphia, pp. 983-990
url: https://www.research.ed.ac.uk/en/publications/the-use-of-reputation-as-noise-resistant-selection-bias-in-a-co-e/
doi: 10.1145/2330163.2330300
arxiv: null
cite: "Chatzinikolaou, N., & Robertson, D. (2012). The use of reputation as noise-resistant selection bias in a co-evolutionary multi-agent system. In Proceedings of the 14th Annual Conference on Genetic and Evolutionary Computation (GECCO '12), pp. 983-990. ACM. https://doi.org/10.1145/2330163.2330300"
topics: [sybil-resistance, swarm-intelligence, marl-emergence]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "1 (Crossref, 2026-10-03)"
code: []
---

## Summary

Asks whether a distributed reputation signal can replace direct (self-reported) fitness as the selection pressure in an evolutionary multi-agent system. The authors build a peer-to-peer, self-adaptive genetic algorithm in which each agent is itself a GA and the agents evolve in real time. Two variants are compared: selection driven by each agent's self-reported fitness, and selection driven by a simple reputation model built from other agents' past experiences with it. The abstract reports that the reputation variant works as an evolutionary drive, and that when noise is injected in the form of "defective" agents (agents whose self-reports or behaviour do not match), the fitness-based model fails to screen them out while the reputation-based model identifies the defective agents, which the authors read as noise resistance. Abstract only, from the Edinburgh Research Explorer record (the ACM body is paywalled and no open copy was found); population sizes, task domain, noise levels and the size of the effect are not available here. The same work is expanded in Chatzinikolaou's 2012 Edinburgh PhD thesis "Evolution through reputation: noise-resistant selection in evolutionary multi-agent systems" (not read).

## Contribution

Links reputation mechanisms from multi-agent systems to fitness evaluation in evolutionary computation, and gives an empirical case that peer-sourced reputation is more robust than self-reported fitness when some agents are faulty or lie.

## Key results

- Reputation can substitute for direct fitness observation as the selection bias in a P2P evolutionary MAS (abstract claim).
- Under injected defective agents, reputation-based selection identifies the defective agents; self-reported fitness does not (abstract claim; magnitudes not visible).

## Methods and models

Peer-to-peer self-adaptive GA; agents as individual GAs; two selection regimes (self-reported fitness vs collective-experience reputation); defective agents as the noise model. Experimental details not visible at abstract depth.

## Limitations and open questions

Abstract only. "Defective" agents are faults, not strategic adversaries, so this does not test reputation against collusion or Sybil identities, which are the known failure modes of simple reputation (see [[cheng-2005-sybilproof]]). Whether the reputation model has any whitewashing defence (identity reset) is not stated. Small venue footprint (one citation on Crossref) suggests limited follow-up.

## Relevance to us

Background for the question of what signal should drive selection or weighting among agents in a swarm when self-reports are untrustworthy: peer reputation beats self-report under faults here, but the Sybil literature says it breaks under cheap identities and collusion. Pair with the same group's security review [[bijani-2014-review]] and with the identity-free alternative in [[durmus-2014-sybil]]. Edge-case relevance to evolutionary and self-modifying agent populations.
