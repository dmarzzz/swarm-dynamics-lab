---
id: zhang-2026-distributed
type: paper
title: "Distributed General-Purpose Agent Networks: Architecture, Key Mechanisms, and Prototypes"
authors: ["Shengli Zhang", "Deen Ma", "Zibin Lin", "Taotao Wang"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/pdf/2606.17368
doi: null
arxiv: "2606.17368"
cite: "Zhang, S., Ma, D., Lin, Z., & Wang, T. (2026). Distributed General-Purpose Agent Networks: Architecture, Key Mechanisms, and Prototypes. arXiv:2606.17368."
topics: [sybil-resistance, llm-agent-swarms]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

The paper proposes a layered architecture for open peer-to-peer networks of heterogeneous LLM agents and three mechanisms: two-stage "bodyless" gossip that pushes fixed-length digests through a GossipSub-style mesh and lets interested agents pull payloads; Binding Agent ID (BAID), a hash commitment binding agent code, a configuration digest (model weights, prompt template, tool policy), a user or institution identity via privacy-preserving KYC, and a salt, with zero-knowledge proofs of execution under the registered configuration; and MG-EigenTrust, a multi-topic EigenTrust variant with dynamic pretrust from stake and bridge feedback, plus stake burn or freeze on a verified fraud proof. In a 100-node, 5-topic simulation of a cross-topic disguise-collusion attack (build reputation in code generation, defect in code review, with spy/bridge nodes and Sybil whitewashing), MG-EigenTrust cut attack success to 0.0291 from 0.3759 for flattened EigenTrust.

## Contribution

Treats agent identity as more than a key pair (who is responsible, which code and model ran) and shows, in simulation, that a single global reputation lets agents carry trust from one task topic into another where they then defect.

## Key results

- Attack success under disguise-collusion: random selection 0.2176, public EigenTrust 0.3759, independent per-topic EigenTrust 0.2160, MG-EigenTrust 0.0291. Attacker ROI (burn only): 3.35, 6.52, 3.32 and -0.80; -0.92 for MG-EigenTrust when frozen stake is counted.
- Baseline check: in a single-topic setting without migration or Sybils, pretrusted EigenTrust reaches attack success 0.0391 versus 0.1407 random.
- MG-EigenTrust detection rate 0.9509, miss rate 0.0491, but false-positive rate 0.5488 at the conservative threshold; the authors say this is not a deployment-ready calibration.
- Reputation state exchanged per epoch falls from 285 to 45 entries (84.21%).
- BAID proof overhead was prototyped on AutoGPT, ReAct and SmolAgents traces (figures only, not checked in detail).

## Methods and models

Architecture and protocol design; epidemic analysis of digest gossip; query-cycle discrete-event simulation of reputation (100 nodes, 5 topics, 30 seeds, 50 epochs, 8 candidates per query); the authors state the simulation is not a Docker, on-chain or end-to-end zkVM test. I read the abstract, related work on identity and reputation, the BAID definition, and the MG-EigenTrust setup and results.

## Limitations and open questions

Simulation-only reputation results with a very high false-positive rate. BAID's Sybil resistance rests on KYC of the responsible user, a personhood-style bound whose issuer is not specified. Stake-based dynamic pretrust inherits wealth weighting ([[gilad-2017-algorand]]).

## Relevance to us

The most direct bridge in this lane between p2p gossip design and agent-swarm Sybil resistance. BAID bounds identities by tying agents to accountable users and committed code; MG-EigenTrust bounds influence per topic and makes Sybil whitewashing and cross-topic laundering unprofitable in simulation. Its cross-topic contamination result matches the formal finding in [[kumar-2024-formal]] that multi-topic peer scores can hide targeted misbehaviour. Related: [[laws-2026-panda]], [[vyzovitis-2020-gossipsub]], [[hu-2025-inter-agent]], [[zhu-2026-blockchain]], [[adler-2024-personhood]].
