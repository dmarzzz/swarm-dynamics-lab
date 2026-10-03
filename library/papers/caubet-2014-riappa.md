---
id: caubet-2014-riappa
type: paper
title: "RIAPPA: a Robust Identity Assignment Protocol for P2P overlays"
authors: [Juan Caubet, Oscar Esparza, José L. Muñoz, Juanjo Alins, Jorge Mata-Díaz]
year: 2014
venue: Security and Communication Networks, vol. 7, no. 12, pp. 2743-2760
url: https://onlinelibrary.wiley.com/doi/10.1002/sec.956
doi: 10.1002/sec.956
arxiv: null
cite: "Caubet, J., Esparza, O., Muñoz, J. L., Alins, J., & Mata-Díaz, J. (2014). RIAPPA: a Robust Identity Assignment Protocol for P2P overlays. Security and Communication Networks, 7(12), 2743-2760. https://doi.org/10.1002/sec.956"
topics: [sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "2 (Crossref, 2026-10-03)"
code: []
---

## Summary

Argues that secure identity assignment is the prerequisite most P2P security work (reputation, anonymity, secure routing) quietly assumes, and proposes RIAPPA, an access-control and identity-assignment protocol for overlays that keeps users anonymous inside the network while remaining traceable. Two trusted third parties split the job: one authenticates the user with a real-world digital certificate (so one real identity per person), the user then chooses its overlay identifier jointly with the second TTP (so the node cannot pick its own ID, closing the Kademlia-style free-ID hole, while the authenticating TTP does not learn the ID), and the two TTPs jointly issue an internal overlay certificate. The design claims revocability and protection against Sybil attacks, eclipse attacks and whitewashing, plus a detailed protocol description with performance and security analysis. Abstract only (Wiley article is marked open access by Unpaywall but the PDF endpoint did not load from this box); the exact cryptographic construction (blind signatures or similar between the two TTPs), the performance figures and the threat analysis are not visible.

## Contribution

A two-TTP identity-assignment design that separates "who you are" (real-world certificate) from "which overlay ID you got" (jointly chosen), giving Sybil resistance via one-certificate-one-identity with pseudonymity against each TTP alone.

## Key results

- Protocol provides anonymity within the overlay with traceability on demand, revocation, and resistance to Sybil, eclipse and whitewashing (abstract; no quantitative results visible).

## Methods and models

Protocol design with two TTPs, real-world PKI certificates, joint identifier selection, internal certificates; performance and security analysis in the paper (not read).

## Limitations and open questions

Abstract-level read. Reintroduces trusted parties (two instead of one) and depends on real-world certificates being Sybil-free; collusion of the two TTPs breaks anonymity; low citation count suggests no deployment.

## Relevance to us

Representative of the "centralized certification, done carefully" family for Sybil resistance in overlays: it is what [[castro-2002-secure]] and [[maccari-2009-avoiding]] gesture at, with the privacy split made explicit. For agent networks the analogue is an operator-KYC authority plus an independent ID issuer. Taxonomy context: [[urdaneta-2011-survey]]; modern cryptographic versions without a TTP learning both sides: [[abdolmaleki-2026-attribute]], [[akama-2024-scrappy]]. Root: [[douceur-2002-sybil]].
