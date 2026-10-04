---
id: ethresearch-2026-anonymous
type: blog
title: "Anonymous Credentials for Trustless Agents (ACTA)"
authors: [zoey (ethresear.ch user zulu0echo)]
year: 2026
url: https://ethresear.ch/t/anonymous-credentials-for-trustless-agents-acta/24797
site: ethresear.ch
topics: [sybil-resistance, llm-agent-swarms]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Research forum proposal (5 May 2026) for a privacy layer on top of ERC-8004 (Trustless Agents), the Ethereum standard that gives AI agents an on-chain identity registry, reputation registry and validation registry. The author argues that ERC-8004 publishes a permanent interaction graph between agents and clients, and that its Sybil defence depends on reviewer identifiability: `getSummary()` requires a non-empty `clientAddresses[]` filter because unfiltered feedback is open to Sybil spam. ACTA replaces identified reviewers with anonymous credentials: agents anchor a commitment to an issuer-signed credential, verifiers register boolean predicate policies (for example "audit_score >= 80 AND jurisdiction not in OFAC list"), and agents present zero-knowledge proofs that emit only a policy id and a context-scoped nullifier. A ZK reputation accumulator lets credential holders leave one piece of feedback per context without revealing their address, and writes a Merkle root back into the ERC-8004 reputation registry. The post also proposes linking an agent to a human principal through personhood credentials (citing Adler et al. 2024) so protocols can exclude fully autonomous bots. No implementation or measurements are given; several API calls are marked as placeholders in the text.

## Key claims

- ERC-8004 as written makes Sybil resistance of reputation depend on knowing who the reviewers are; anonymous feedback is excluded.
- Context-scoped nullifiers (derived from the agent's master secret plus verifier address and session nonce) give per-context Sybil resistance (one presentation or one review per context) without global identity disclosure, and nullifiers for different verifiers are unlinkable.
- Personhood credentials can bind an agent to an accountable human without revealing the human, which would let a DAO restrict votes to human-backed agents.
- The proof system is abstracted behind an `ICircuitVerifier` interface, so SNARK, STARK or zkVM backends can be swapped per policy.
- Revocation is explicitly out of scope.

## Evidence quality

Design proposal and opinion. No code, no benchmarks, no security proof. The Sybil argument rests on standard nullifier constructions (Semaphore-style). Open issues the post does not resolve: who issues credentials to agents, what stops one principal from obtaining many personhood-linked agents, and how per-context nullifiers interact with cross-context reputation aggregation.

## Relevance to us

This is the most direct statement found of the Sybil problem for an on-chain agent economy: once agents have registries and reputation, Sybil reviewers can inflate scores, and the standard fix (identify reviewers) destroys privacy. ACTA's answer, one-per-context nullifiers plus credentials tied to a principal, is a template for rate-limiting how many votes or reviews one operator's swarm of agents can cast. It pairs with personhood-based approaches such as [[buterin-2023-what]] and market-priced identity cost in [[porobov-2026-price]], and with credential-unlinkability designs like [[kadianakis-2023-proof]] and [[dobrokhvalov-2025-privacy]]. The weak point for multi-agent systems is that one human principal can still delegate to many agents unless the policy also caps agents per principal per context; that cap is where an experiment could start.

Other catalogued sources it draws on: the personhood-credential paper it cites [[adler-2024-personhood]], and a comparison of agent trust models including ERC-8004 [[hu-2025-inter-agent]].
