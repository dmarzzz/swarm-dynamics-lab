---
id: chocron-2026-who
type: paper
title: "Who Owns This Agent? Tracing AI Agents Back to Their Owners"
authors: ["Ruben Chocron", "Doron Jonathan Ben Chayim", "Eyal Lenga", "Gilad Gressel", "Alina Oprea", "Yisroel Mirsky"]
year: 2026
venue: "arXiv preprint (under review)"
url: https://arxiv.org/abs/2605.16035
doi: null
arxiv: "2605.16035"
cite: "Chocron, R., Chayim, D. J. B., Lenga, E., Gressel, G., Oprea, A., & Mirsky, Y. (2026). Who Owns This Agent? Tracing AI Agents Back to Their Owners. arXiv:2605.16035."
topics: [swarm-detection, sybil-resistance]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: null
code: []
---

## Summary

Formalises agent attribution as linking an observed agent interaction to the vendor account whose model calls drove it. An authorised party plants canaries in content the agent reads, then asks the model vendor to search a narrow time window of account-linked session logs. Lexical canaries give exact-match attribution for non-evasive operators; against adaptive operators the authors use task-relevant semantic canaries, whose removal also removes information the agent needs, creating a utility-evasion asymmetry.

## Contribution

Moves operator attribution from guessing from behaviour to a vendor-assisted protocol, the accountability counterpart of black-box fingerprinting.

## Key results

- The protocol supports reliable session attribution across communication, web and cyber-agent settings, withstands adaptive transformations, and scales to vendor-side log search (abstract; no numbers in the abstract).

## Methods and models

Canary embedding in agent-consumed content; vendor log search over a time window; lexical and semantic canary variants; adaptive-adversary evaluation.

## Limitations and open questions

Requires vendor cooperation and an operator who uses a hosted model; self-hosted open-weight swarms are out of reach. Abstract-only reading; effect sizes not checked.

## Relevance to us

The cleanest route from "a swarm hit us" to "which account ran it" when swarms use hosted APIs. Canaries in honeypot content double as detectors ([[reworr-2024-llm]]) and as attribution handles. Pairs with [[white-2026-black]] for clustering before escalation.
