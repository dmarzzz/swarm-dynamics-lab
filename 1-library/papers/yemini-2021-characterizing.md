---
id: yemini-2021-characterizing
type: paper
title: "Characterizing Trust and Resilience in Distributed Consensus for Cyberphysical Systems"
authors: ["Michal Yemini", "Angelia Nedić", "Andrea J. Goldsmith", "Stephanie Gil"]
year: 2021
venue: "IEEE Transactions on Robotics"
url: https://arxiv.org/abs/2103.05464
doi: "10.1109/tro.2021.3088054"
arxiv: "2103.05464"
cite: "Yemini, M., Nedić, A., Goldsmith, A. J., & Gil, S. (2021). Characterizing Trust and Resilience in Distributed Consensus for Cyberphysical Systems. IEEE Transactions on Robotics, 38(1), 71-91. arXiv:2103.05464."
topics: [sybil-resistance, sync-consensus, swarm-robotics]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "50 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

A unified framework for resilient consensus when agents receive stochastic trust values about their neighbours (for example from wireless fingerprints). Under conditions on the trust observations and protocol, consensus converges almost surely even when malicious agents make up more than half of the network connectivity, the deviation from the attack-free value is bounded with probability approaching 1 exponentially, and malicious and legitimate agents are classified correctly in finite time almost surely.

## Contribution

Breaks the classical one-half / one-third barrier of Byzantine consensus by assuming a side channel of trust information, and characterises exactly what that side channel buys.

## Key results

- Almost sure convergence with malicious agents above half of network connectivity (abstract).
- Deviation from the true consensus bounded with probability approaching 1 exponentially.
- Expected convergence rate decays exponentially in the quality of trust observations.

## Methods and models

Stochastic trust observations entering a weighted consensus update; probabilistic convergence analysis. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Everything rests on trust observations whose expectation separates legitimate and malicious agents; an adversary able to fake the side channel is outside the model.

## Relevance to us

The theoretical core for 'trust side channel beats majority assumptions'. For agent swarms the analogous side channel could be attestation or provenance signals; this paper tells us how good they must be. Follows [[gil-2015-guaranteeing]] and [[mallmann-trenn-2021-crowd]]; extended in [[yemini-2022-resilient]] and [[cavorsi-2024-exploiting]].
