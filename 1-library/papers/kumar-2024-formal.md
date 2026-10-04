---
id: kumar-2024-formal
type: paper
title: "Formal Model-Driven Analysis of Resilience of GossipSub to Attacks from Misbehaving Peers"
authors: ["Ankit Kumar", "Max von Hippel", "Pete Manolios", "Cristina Nita-Rotaru"]
year: 2024
venue: "IEEE Symposium on Security and Privacy (S&P 2024), per the arXiv comment 'To appear'; arXiv preprint December 2022"
url: https://arxiv.org/pdf/2212.05197
doi: null
arxiv: "2212.05197"
cite: "Kumar, A., von Hippel, M., Manolios, P., & Nita-Rotaru, C. (2024). Formal Model-Driven Analysis of Resilience of GossipSub to Attacks from Misbehaving Peers. In IEEE Symposium on Security and Privacy (S&P 2024). arXiv:2212.05197."
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: null
code: [gh-libp2p-specs]
---

## Summary

The authors build an executable formal model of GossipSub v1.1 in the ACL2s theorem prover (6,768 lines, 203 definitions, 177 theorems), faithful to the prose specification, and state four properties the peer score must have: persistent non-positive performance in a topic eventually gives a non-positive score; misbehaviour lowers the score; good behaviour does not lower it; identical behaviour gives identical scores. They prove the last two for every configuration, and use counterexample generation to show the first two fail for some configurations, including the one Ethereum's consensus layer (Eth2.0) used. Filecoin's configuration satisfies all four, but by disabling score components, which the spec does not allow.

## Contribution

The first formal analysis of peer scoring as a Sybil and eclipse defence. It shows that "reputation from first-hand behaviour" is only as good as its weights: in a multi-topic score, good behaviour in many topics can mask withholding in one.

## Key results

- Property 1 fails for Eth2.0 because a peer can offset a negative score in one of dozens of subnet topics with positive scores in the others, so its overall score stays positive (Section 5.3); Property 2 also fails under the Eth2.0 TopicCap of 37.72.
- On any Eth2.0 network of any size and topology, misbehaving peers can be synthesised that never forward messages in chosen target topics yet keep positive scores and are never pruned. The attack gadgets enable targeted censorship, topic-specific eclipse and partition, while a classic eclipse that blocks all topics would still be caught.
- Disclosed to Protocol Labs and the Ethereum Foundation, who agreed with the findings; the Ethereum Foundation was working on a patch at the time of writing. The GossipSub developers endorsed the model as a formal specification.
- Discrepancies found between spec and Go implementation (for example the activation window in P3 and P3b, and the ability to disable score components).

## Methods and models

ACL2s model of peer state, control messages, meshes, fanout, the score function and defence mechanisms; Eth2.0 and Filecoin weight-and-parameter maps; automated counterexample search; attack gadgets proved by induction to keep attacker scores positive. I read the abstract, contributions, the property definitions, the Eth2.0 evaluation and the conclusion.

## Limitations and open questions

Analyses the score function and protocol logic, not network-level costs or real deployments. Results depend on the configuration snapshot the authors used; I did not check whether current Ethereum client parameters have been changed by the patch mentioned.

## Relevance to us

This is direct evidence that peer scoring, the main deployed influence bound in open gossip, can be configured so that selective withholding is invisible. For agent swarms that score each other on many tasks or channels, the lesson is to avoid letting good behaviour in some topics cancel bad behaviour in a target topic (the same cross-topic contamination [[zhang-2026-distributed]] measures for EigenTrust), and to model-check the reputation rule before relying on it. Bounds influence only if weights are right. Related: [[vyzovitis-2020-gossipsub]], [[gh-libp2p-specs]], [[singh-2006-eclipse]], [[laws-2026-panda]], [[heimbach-2024-deanonymizing]].
