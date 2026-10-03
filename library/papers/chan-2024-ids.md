---
id: chan-2024-ids
type: paper
title: IDs for AI Systems
authors:
- Alan Chan
- Noam Kolt
- Peter Wills
- Usman Anwar
- Christian Schroeder de Witt
- Nitarshan Rajkumar
- Lewis Hammond
- David Krueger
- Lennart Heim
- Markus Anderljung
year: 2024
venue: arXiv preprint (RegML workshop at NeurIPS 2024)
url: https://arxiv.org/html/2406.12137
doi: null
arxiv: '2406.12137'
cite: 'Chan, A., Kolt, N., Wills, P., Anwar, U., Schroeder de Witt, C., Rajkumar, N., Hammond, L., Krueger, D., Heim, L., & Anderljung, M. (2024). IDs for AI Systems. arXiv preprint arXiv:2406.12137. RegML workshop at NeurIPS 2024.'
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: 22 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Proposes instance-level IDs for AI systems: a container holding a unique identifier (system_identifier:instance_identifier) and attributes such as a system card, incident records, certifications, and links to ancestor and descendant instances. An instance is roughly a context window plus an initial user; regenerating a response or branching creates a new instance with a link to its parent. The paper lays out the design space (attributes, access, verifiability), threat models (tampering, ID spoofing, instance spoofing) and how TLS, signatures and C2PA manifests address them, worked scenarios (shutting down a malfunctioning agent, verifying certification, tracing a scam-call operation through sub-agents), sources of demand, a deployer implementation, and risks.

## Contribution

A governance-oriented framework that separates identifying a particular agent instance from proof of personhood, watermarks, CAPTCHAs and API tokens (its Table 1), and argues for limited experimentation in high-stakes settings such as payments and contacting humans.

## Key results

- No empirical results; it is a framework and position paper.
- Proposed: service providers rate-limit instances without IDs rather than block them.
- Proposed: parent-child ID links let investigators connect many sub-agents to one originating agent and user (scam-call scenario).
- Identified limits: decentralised self-hosted agents can skip IDs; users can copy inputs into a new instance to break ancestry links; IDs can be lent; ID-bearing networks could become a privileged channel.

## Methods and models

Conceptual analysis drawing analogies to aircraft tail numbers, HTTPS certificates, serial numbers and Let's Encrypt. Verifiability requires that the received ID equals the created one, that the author is genuine, that the ID corresponds to the instance, and that the party trusts the author (the last left out of scope).

## Limitations and open questions

Assumes deployers issue IDs; offers only a pointer (a Let's Encrypt analogue) for open-weight agents. Does not address how many instances one user may spawn, so IDs alone do not bound Sybil creation; the authors list CAPTCHAs and future proof-of-personhood as complements and note CAPTCHAs may fail against AI.

## Relevance to us

Instance IDs with ancestry links are the identity layer a Sybil-resistant swarm would build on: they make "these 50 agents were spawned by one principal" observable, which is the provenance side information [[bara-2026-epistemic]] says aggregation needs. But issuing IDs is free per instance, so they need a scarce anchor such as [[adler-2024-personhood]] or stake ([[hu-2025-inter-agent]]). Companion to [[chan-2024-visibility]] and [[chan-2025-infrastructure]]; [[hammond-2025-multi]] cites it as the basis for agent reputation systems. Delegation credentials in [[south-2025-authenticated]] are a concrete protocol for the same idea.
