---
id: laws-2026-panda
type: paper
title: "PANDA: A Decentralized Architecture with Flexible Orchestration for Scalable, Fault-Tolerant Multi-Agent Systems"
authors: ["Matthew D. Laws", "Cristina Nita-Rotaru"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/pdf/2609.38482
doi: null
arxiv: "2609.38482"
cite: "Laws, M. D., & Nita-Rotaru, C. (2026). PANDA: A Decentralized Architecture with Flexible Orchestration for Scalable, Fault-Tolerant Multi-Agent Systems. arXiv:2609.38482."
topics: [sybil-resistance, llm-agent-swarms]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

PANDA connects a large collective of independently administered LLM agents that discover each other's capabilities and self-organise into small teams per task. Collective communication runs over GossipSub ([[vyzovitis-2020-gossipsub]]) and team communication over TCP; agents can sit on several teams, with power-of-two-choices load balancing and star, chain or mesh orchestration. Governance is a PGP-style web of trust: an agent joins only when one or more members certify its key, identity and advertised capabilities after out-of-band proof of identity, certificates are gossiped with capability announcements, and each agent trusts peers reachable within a chosen certification depth n from itself or from genesis nodes. On HotPotQA the authors report scaling to thousands of agents, team assembly in milliseconds, accuracy comparable to state of the art at up to 8 times the efficiency, and 100% task completion under injected faults.

## Contribution

To the authors' knowledge the first LLM multi-agent architecture with web-of-trust governance, and one of the first that runs agent coordination over a deployed p2p gossip stack. It brings the Sybil-relevant design space of p2p overlays (certified identities, bounded trust propagation) into agent swarms.

## Key results

- Trusted set T_i is depth-bounded reachability over certificate edges; anchor and depth are chosen locally per agent.
- With five genesis agents and two certificates required to join, trusted recall under the genesis anchor reaches nearly 70% at depth 3; self anchoring is weaker but approaches full recall at unbounded depth.
- All configurations keep trusted precision above 99%, where precision is defined as the fraction of trusted peers that are actually alive.
- Team assembly cost stays constant up to 10^6 agents (as stated in the results summary).

## Methods and models

Architecture design with TLA+ specifications of gossip, failure detection, recovery and team assembly; HotPotQA evaluation against centralised and decentralised baselines; governance simulations with 1,000 agents and varying certificates-to-join and genesis counts. I read the abstract, contribution, scalability and governance sections and the governance evaluation captions.

## Limitations and open questions

The governance evaluation measures recall and liveness precision under churn, not resistance to an adversary that obtains certificates by social engineering or colluding certifiers, which is the known weakness of webs of trust ([[yu-2006-sybilguard]], [[alvisi-2013-sok]]). It inherits GossipSub's scoring weaknesses ([[kumar-2024-formal]]). Out-of-band identity proof is assumed, not specified.

## Relevance to us

PANDA is a concrete agent-swarm design where Sybil resistance is bounded identities through certification plus bounded trust propagation by depth. The certificates-to-join parameter is the agent analogue of social-graph Sybil defences: requiring k certifiers raises the cost of admitting a Sybil to compromising k members. It would be a natural testbed for the attacks in [[singh-2006-eclipse]] (colluding certified agents surrounding one victim) and [[bara-2026-epistemic]]. Related: [[zhang-2026-distributed]], [[hu-2025-inter-agent]], [[vyzovitis-2020-gossipsub]], [[castro-2002-secure]].
