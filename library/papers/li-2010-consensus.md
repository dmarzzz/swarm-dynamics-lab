---
id: li-2010-consensus
type: paper
title: "Consensus of Multiagent Systems and Synchronization of Complex Networks: A Unified Viewpoint"
authors: [Zhongkui Li, Zhisheng Duan, Guanrong Chen, Lin Huang]
year: 2010
venue: "IEEE Transactions on Circuits and Systems I: Regular Papers"
url: https://doi.org/10.1109/tcsi.2009.2023937
doi: 10.1109/tcsi.2009.2023937
arxiv: null
cite: "Li, Z., Duan, Z., Chen, G., & Huang, L. (2010). Consensus of multiagent systems and synchronization of complex networks: A unified viewpoint. IEEE Transactions on Circuits and Systems I: Regular Papers, 57(1), 213-224."
topics: [sync-consensus]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "2412 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Treats consensus for agents with general linear dynamics and a fixed communication graph using an observer-type
protocol based on relative output measurements, in a framework that also covers synchronisation of complex
networks. With a spanning-tree graph, consensus reduces to the stability of a set of low-dimensional matrices
(one per Laplacian eigenvalue). The "consensus region" is introduced; an observer-type protocol with an unbounded
consensus region exists if and only if each agent is stabilisable and detectable. A multistep design procedure,
tracking of time-varying references and robustness to disturbances are discussed, with a satellite
formation-flying example.

## Contribution

Made explicit that multi-agent consensus and complex-network synchronisation can be treated in one framework; the "consensus region" concept is in our reading the control analogue of synchronisation regions in
network physics ([[arenas-2008-synchronization]]).

## Key results

- Abstract: reduction to low-dimensional stability problems; consensus region; existence of unbounded consensus
  region if and only if stabilisable and detectable; low-Earth-orbit formation example.

## Methods and models

Linear systems theory, Laplacian eigen-decomposition, observer design. Abstract from OpenAlex.

## Limitations and open questions

Fixed graph, linear agents.

## Relevance to us

The reference for treating real vehicle dynamics (not integrators) in consensus, generalising
[[fax-2004-information]].
