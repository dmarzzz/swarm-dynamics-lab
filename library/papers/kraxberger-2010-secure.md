---
id: kraxberger-2010-secure
type: paper
title: "Secure Multi-Agent System for Multi-Hop Environments"
authors: [Stefan Kraxberger, Peter Danner, Daniel Hein]
year: 2010
venue: Computer Network Security, MMM-ACNS 2010, Lecture Notes in Computer Science vol. 6258, pp. 270-283, Springer
url: https://link.springer.com/chapter/10.1007/978-3-642-14706-7_21
doi: 10.1007/978-3-642-14706-7_21
arxiv: null
cite: "Kraxberger, S., Danner, P., & Hein, D. (2010). Secure Multi-Agent System for Multi-Hop Environments. In I. Kotenko & V. Skormin (Eds.), Computer Network Security (MMM-ACNS 2010), Lecture Notes in Computer Science, vol. 6258, pp. 270-283. Springer. https://doi.org/10.1007/978-3-642-14706-7_21"
topics: [sybil-resistance, fork-merge-security]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: abstract
relevance: 1
citations: "not checked (OpenAlex budget exhausted 2026-10-03)"
code: []
---

## Summary

Systems-integration paper from TU Graz: make the JADE multi-agent platform usable over mobile ad hoc (multi-hop) networks for emergency response, where fixed infrastructure may be down and the data exchanged (health records, grid maps) is confidential. JADE's default transport is Java RMI with SSL, which only gives end-to-end security on directly connected links; the authors replace it with their Secure P2P framework (SePP), an unstructured P2P overlay that provides authentication, integrity and confidentiality across multiple hops and scales its security measures to device capability, wiring it in through JADE's message dispatching and transparent proxy generation. They describe the design and implementation and report a short benchmark comparing vanilla JADE with the SePP-backed version. The introduction motivates the work with the usual P2P observation that malicious or selfish nodes can disrupt a system where every entity is equal, citing the P2P security literature. Abstract, introduction and motivation read from the Springer preview; the body (SePP design, benchmark numbers) is paywalled and no open copy was found, so no performance figures are recorded.

## Contribution

A working secure transport for a mainstream agent platform in infrastructure-less networks, combining authenticated multi-hop P2P messaging with agent mobility. Engineering rather than a new security result.

## Key results

- JADE over SePP gives authenticated, integrity-protected, confidential multi-hop agent messaging (abstract).
- Benchmark versus vanilla JADE reported; numbers not visible at this read depth.

## Methods and models

JADE agent middleware; SePP unstructured secure P2P overlay; Java implementation; microbenchmark.

## Limitations and open questions

Does not address Sybil or identity creation at all as far as the visible text shows; security is channel-level (who can read or alter messages), presumably on top of pre-provisioned credentials. The paper's relevance to Sybil resistance is therefore only as an example of the pre-LLM "secure open MAS" infrastructure that assumes identities are already bound to devices. Paywalled body.

## Relevance to us

Background only. Shows what the agent-platform community meant by "secure multi-agent system" circa 2010: transport security for mobile agents, not resistance to identity multiplication. Compare the attack taxonomy in [[bijani-2014-review]], which treats Sybil and collusion as first-class threats to open MAS, and the modern robot-side counterpart [[gandhi-2025-roborebound]].
