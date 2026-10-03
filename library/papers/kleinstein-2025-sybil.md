---
id: kleinstein-2025-sybil
type: paper
title: "Sybil-Resistant Parallel Mixing"
authors: ["Maya Kleinstein", "Riad S. Wahby", "Yossi Gilad"]
year: 2025
venue: "Proceedings on Privacy Enhancing Technologies"
url: https://api.openalex.org/works/doi:10.56553/popets-2025-0149
doi: "10.56553/popets-2025-0149"
arxiv: null
cite: "Kleinstein, M., Wahby, R. S., & Gilad, Y. (2025). Sybil-Resistant Parallel Mixing. Proceedings on Privacy Enhancing Technologies, 2025(4), 639-652."
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "1 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Parallel mixnets shuffle messages across stratified servers, and throughput is bounded by the busiest server in each stratum. Sybil clients can coordinate to route all their messages through one victim server mid-network, stalling delivery for everyone while staying anonymous because their messages were already mixed with honest ones. BalancedMixnet uses anonymous credentials to force each client onto a uniformly random route through the mixnet while letting servers verify that a message comes from a valid client and is not a replay. Credential issuance and validation costs amortise across many messages from one client. The authors implement it and report that integration cost is modest and the Sybil-attack benefit substantial.

## Contribution

Shows that anonymous credentials can enforce not just "how many" actions a client takes but "where" it acts: coordinated Sybils lose the ability to concentrate load on a chosen node.

## Key results

- Credential-enforced uniform routing defeats targeted load concentration by colluding Sybil clients (abstract).
- Overheads described as modest; no numbers read.

## Methods and models

Not read beyond the abstract.

## Limitations and open questions

Not read in full. Presumably still needs some admission control so that one entity cannot obtain many credentials; the abstract does not say how clients are bounded.

## Relevance to us

A clean example of a coordination attack in a multi-node system: Sybils collude not to outvote but to overload one node. Agent swarms with task routing or sharded workers have the same exposure, and the fix (credential-bound random assignment) is transferable: bind each agent identity to a verifiable random assignment so a coordinated group cannot pile onto one worker, verifier or committee. Related: rate limits per identity in [[yun-2026-anonymous]] and [[taheri-boshrooyeh-2022-privacy]].
