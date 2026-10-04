---
id: akama-2024-scrappy
type: paper
title: "Scrappy: SeCure Rate Assuring Protocol with PrivacY"
authors: [Kosei Akama, Yoshimichi Nakatsuka, Masaaki Sato, Keisuke Uehara]
year: 2024
venue: Network and Distributed System Security Symposium (NDSS 2024), San Diego
url: https://arxiv.org/abs/2312.00989
doi: 10.14722/ndss.2024.24445
arxiv: "2312.00989"
cite: "Akama, K., Nakatsuka, Y., Sato, M., & Uehara, K. (2024). Scrappy: SeCure Rate Assuring Protocol with PrivacY. In Network and Distributed System Security Symposium (NDSS 2024). Internet Society. https://doi.org/10.14722/ndss.2024.24445"
topics: [sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "4 (Crossref, 2026-10-03)"
code: ["https://github.com/akakou/scrappy"]
---

## Summary

Privacy-preserving rate limiting as a Sybil-style defence: services want to cap how often one client acts (vote stuffing, scraping, abusive sign-ups) and today use CAPTCHAs or SMS verification, which are failing (CAPTCHA farms, cheap phone numbers) or privacy-invasive; prior private alternatives either trust client hardware fully (CACTI-style TEE counters) or leak via side channels (Privacy Pass timing correlation). Scrappy has the client produce an unforgeable yet unlinkable "rate-assuring proof" built from Direct Anonymous Attestation (DAA, the ECDAA scheme used by TPMs and FIDO) plus a hardware security device holding the unique device key: the proof is a DAA signature over a server-chosen basename bsn and time period t, so the same device produces the same pseudonymous signature for a given (server, t), letting the server count and block a device that exceeds the rate, while signatures for different servers or periods are unlinkable. The key design claim is that rate limiting survives compromise of the hardware: even if the device-uniqueness key or the proof-signing key leaks, the server can still block the misbehaving pseudonym, because the limit is enforced on the verifier side from the deterministic per-period pseudonym rather than on a trusted client counter. Implemented on three devices (TPM 2.0, deployable as-is; a hardware security token; and a smartphone, both needing small spec changes; Table VII lists others). End-to-end latency 0.32 s and 679 bytes transferred in the baseline; a security evaluation covers key compromise, side channels and collusion. TPM implementation open-sourced. Read from the arXiv full text: abstract, introduction and contributions, related work table (CAPTCHA, SMS, Privacy Pass, CACTI, Opaak), protocol overview with basename/period mechanics, implementation and evaluation summary, security evaluation headings; DAA details and proofs skimmed.

## Contribution

A rate-limiting protocol that is unlinkable across services and time, hardware-agnostic, and keeps its rate guarantee even when the client's secure hardware is compromised, with a deployable TPM implementation.

## Key results

- 0.32 s end-to-end latency, 679 bytes bandwidth (baseline).
- Rate limit holds under leaked device keys (verifier-side pseudonym counting).
- Works on TPM, security token and smartphone; TPM version needs no spec change.

## Methods and models

ECDAA / DAA group signatures with basenames, hardware-rooted device keys, per-(server, period) pseudonyms, prototype on three device classes, latency and bandwidth benchmarks, security analysis.

## Limitations and open questions

Caps actions per device, not per person: an operator with many TPM-equipped machines (or VMs with vTPMs backed by distinct endorsement keys) gets a cap per machine, which is exactly the Sybil scaling question; DAA issuer trust and revocation are inherited from the TPM ecosystem; smartphone and token variants are not deployable today.

## Relevance to us

The cleanest current answer to "how do you rate-limit anonymous agents without a login": cryptographic per-device pseudonyms per epoch. For agent platforms it reframes Sybil defence as pricing per attested device, with the residual cost to the attacker being hardware (or cloud TEE instances) per identity. Pairs with humanness attestation in [[querejeta-azurmendi-2021-zksense]], uniqueness credentials in [[abdolmaleki-2026-attribute]], hardware-bound credentials in [[hanzlik-2021-with]], and the identity-cost economics in [[wagman-2008-optimal]]. Root: [[douceur-2002-sybil]].
