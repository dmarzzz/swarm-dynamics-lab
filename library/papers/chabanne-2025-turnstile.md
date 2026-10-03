---
id: chabanne-2025-turnstile
type: paper
title: "Turnstile cookies: A new root of trust for personhood credentials"
authors: [Hervé Chabanne, Alberto Ibarrondo]
year: 2025
venue: "2025 12th IFIP International Conference on New Technologies, Mobility and Security (NTMS)"
url: https://ieeexplore.ieee.org/document/11076613
doi: 10.1109/NTMS65597.2025.11076613
arxiv: null
cite: "Chabanne, H., & Ibarrondo, A. (2025). Turnstile cookies: A new root of trust for personhood credentials. In 2025 12th IFIP International Conference on New Technologies, Mobility and Security (NTMS), pp. 186-188. https://doi.org/10.1109/NTMS65597.2025.11076613"
topics: [sybil-resistance, swarm-detection]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "0 (Crossref, 2026-10-03)"
code: []
---

## Summary

Three-page preliminary proposal (short paper) for a new issuance root for personhood credentials (PHCs): physical turnstile ticket checks, for example entering a metro line. Passing a turnstile is treated as evidence of a human body being present, and that event mints a "turnstile cookie" built on a recent cryptographic proposal for non-transferable anonymous tokens. The authors' stated aim is to show that every component needed already exists today. Only the abstract (IEEE Xplore) was read; no evaluation is described in the abstract.

## Contribution

Suggests piggybacking personhood evidence on existing physical access infrastructure rather than on biometrics or government ID, tying the PHC idea of [[adler-2024-personhood]] to everyday transit gates.

## Key results

- No empirical results in the abstract; it is a design sketch arguing feasibility with existing components.

## Methods and models

Non-transferable anonymous tokens (cryptographic proposal not identified in the abstract) issued at turnstile checks.

## Limitations and open questions

From the abstract alone: rate of issuance per person (one human could pass many turnstiles, or many people's cookies could be collected by one operator), non-transferability guarantees in practice, privacy of location traces, and coverage for people without transit access are all open. Preliminary work, 3 pages.

## Relevance to us

A concrete sybil-resistance primitive idea: rate-limited personhood evidence from physical events. For agent-swarm detection it represents the "prove there is a human" side, the complement of behavioural detection. Context: [[adler-2024-personhood]].
