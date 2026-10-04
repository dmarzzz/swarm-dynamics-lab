---
id: aydeger-2026-decentralized
type: paper
title: "Decentralized Digital Identity Management for Large Language Model Agents"
authors: [Abdullah Aydeger, Engin Zeydan, Josep Mangues-Bafalluy, Yekta Turk, Sunder Ali Khowaja, Kapal Dev]
year: 2026
venue: IEEE Communications Standards Magazine, vol. 10, no. 1, pp. 87-94
url: https://ieeexplore.ieee.org/document/11367791
doi: 10.1109/mcomstd.2025.3648666
arxiv: null
cite: "Aydeger, A., Zeydan, E., Mangues-Bafalluy, J., Turk, Y., Khowaja, S. A., & Dev, K. (2026). Decentralized Digital Identity Management for Large Language Model Agents. IEEE Communications Standards Magazine, 10(1), 87-94. https://doi.org/10.1109/MCOMSTD.2025.3648666"
topics: [sybil-resistance, llm-agent-swarms]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "2 (Crossref, 2026-10-03)"
code: []
---

## Summary

Magazine-style paper proposing that LLM agents (an LLM core plus reasoning, planning and third-party tools) authenticate through blockchain-based Self-Sovereign Identity (SSI) rather than conventional credentials, as a response to prompt injection, unauthorized access and exploitation through third-party APIs. The abstract reports an experimental integration in which SSI-based validation of agent identity succeeded 100% of the time at low load and 93% at peak load, which the authors say surpasses the traditional authentication baseline they compared against, at the cost of higher latency and lower throughput; they point to Layer 2 scaling as the follow-up. Read from the IEEE Xplore abstract only (paywalled, not open access per Unpaywall); the experimental setup, baseline and load levels are not visible from the abstract.

## Contribution

Positions W3C-style decentralized identifiers and verifiable credentials as the identity layer for LLM agents and gives a first load-test of the idea, in a standards-oriented venue.

## Key results

- Validation success 100% at low load, 93% at peak load (abstract; load definition not given).
- Security gain comes with increased latency and reduced throughput (abstract; magnitudes not given).

## Methods and models

Integration of an LLM agent stack with a blockchain-backed SSI system; experimental load test against a "traditional authentication" baseline. Specific chain, DID method, agent framework and hardware are not stated in the abstract.

## Limitations and open questions

Abstract-only read. SSI binds an agent to a credential issued by someone; it does not by itself prevent one operator from minting many agent identities, so the Sybil question is pushed to the issuer. The 93% peak-load figure implies 7% of legitimate validations fail under load, which is a usability and availability problem the abstract does not discuss. Magazine format usually means limited methodology detail.

## Relevance to us

Background for the agent-identity strand of sybil-resistance: this is what the "give every agent a DID" proposal looks like when someone actually load-tests it. Useful as a contrast to proof-of-personhood and social-graph approaches ([[ford-2020-identity]], [[siddarth-2020-who]], [[yu-2006-sybilguard]]) and to credential-based schemes like [[rosenberg-2023-zk-creds]] and the ID-for-agents proposals in [[chan-2024-ids]]. Does not address detection of many agents behind one issuer, which is the swarm case ([[douceur-2002-sybil]]).
