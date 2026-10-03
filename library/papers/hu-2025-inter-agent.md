---
id: hu-2025-inter-agent
type: paper
title: 'Inter-Agent Trust Models: A Comparative Study of Brief, Claim, Proof, Stake, Reputation and Constraint in Agentic Web Protocol Design-A2A, AP2, ERC-8004, and Beyond'
authors:
- Botao 'Amber' Hu
- Helena Rong
year: 2025
venue: arXiv preprint (submitted to AAAI 2026 Workshop on Trust and Control in Agentic AI)
url: https://arxiv.org/abs/2511.03434
doi: null
arxiv: '2511.03434'
cite: 'Hu, B. A., & Rong, H. (2025). Inter-Agent Trust Models: A Comparative Study of Brief, Claim, Proof, Stake, Reputation and Constraint in Agentic Web Protocol Design-A2A, AP2, ERC-8004, and Beyond. arXiv preprint arXiv:2511.03434.'
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 14 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Compares six trust models for inter-agent protocols: Brief (verifiable claims by self or third party), Claim (self-proclaimed capability and identity such as an A2A AgentCard), Proof (cryptographic verification including zero-knowledge proofs and TEE attestation), Stake (bonded collateral with slashing and insurance), Reputation (crowd feedback and graph trust), and Constraint (sandboxing and capability bounds). It analyses assumptions, attack surfaces and trade-offs for each, with emphasis on LLM-specific fragilities (prompt injection, sycophancy, hallucination, deception, misalignment) that make claim-only or reputation-only designs brittle. It evaluates Google's A2A, the Agent Payments Protocol (AP2) and Ethereum's ERC-8004 "Trustless Agents" on security, privacy, latency and cost, and social robustness including Sybil, collusion and whitewashing resistance.

## Contribution

A comparative map of how 2025 agent protocols handle trust, concluding that no single mechanism suffices and recommending trustless-by-default designs anchored in Proof and Stake for high-impact actions, with Brief for identity and discovery and Reputation as an overlay.

## Key results

- Qualitative comparison; abstract-level read, no numbers checked.
- Conclusion stated in the abstract: purely reputational or claim-only approaches are brittle for LLM agents; Proof plus Stake should gate high-impact actions.

## Methods and models

Comparative protocol analysis across six trust primitives and named protocols.

## Limitations and open questions

Abstract only. Stake bounds Sybil multiplicity by capital, which favours well-funded attackers; the paper's treatment of that trade-off was not checked.

## Relevance to us

The closest bridge in this lane between agent identity and crypto-economic Sybil resistance (stake, slashing, attestation), and the reference point for ERC-8004-style agent registries. [[xia-2026-when]] cites it as the protocol-level context for its reputation-laundering attack. Compare identity anchors in [[adler-2024-personhood]] and [[chan-2024-ids]], and on-chain BFT designs in [[chen-2024-blockagents]] and [[jo-2025-byzantine]].
