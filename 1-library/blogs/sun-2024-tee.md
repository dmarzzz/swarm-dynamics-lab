---
id: sun-2024-tee
type: blog
title: "TEE-enabled Social Games: An Experiment with Bobu's Magic Show"
authors: [Xyn Sun, Ryan MacArthur, Roshan Palakkal, Andrew Miller]
year: 2024
url: https://collective.flashbots.net/t/tee-enabled-social-games-an-experiment-with-bobu-s-magic-show/3963
site: collective.flashbots.net (Flashbots forum; posted by socrates1024 / Andrew Miller)
topics: [sybil-resistance]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Forum post (11 October 2024) on the Teleport prototype used in a livestreamed Azuki "Bobu" magic show. Audience volunteers granted an X app Read/Write OAuth access; the OAuth tokens were held only inside a Gramine-SGX enclave running the Teleport Rust backend, which used each token to post exactly one collective tweet (a "flash mob"). One-time use was enforced by an Arbitrum contract acting as a monotonic counter, minted by an Ethereum key generated and sealed in the enclave. A TLS key was also generated in the enclave, with Let's Encrypt certificates enumerable through Certificate Transparency so auditors can match every active certificate to a published quote. The Docker image and remote attestation were published (repository Account-Link/teleport-gramine-rs, branch bobu).

## Key claims

- The problem addressed is over-authorisation: the app needs one tweet but X grants full Read/Write; the TEE shows the operator never held raw tokens and used them only once.
- Threat model: server malware, hacked server, malicious administrators "scooping up" OAuth codes; nation-state attackers not ruled out.
- zk and zkTLS cannot do this: zkTLS gives "credible reads" and requires users to act first and post a bond, while a TEE gives "credible reads AND credible writes" in a pull model.
- This is partial encumbrance (only the OAuth token is owned by the TEE; the account stays with the user); full encumbrance of web2 accounts is suggested for high-stakes uses.
- Caveats: unaudited prototype; depends on QuickNode and Arbitrum finality; the X developer account owner can still revoke the app.

## Evidence quality

Practitioner report on a working deployment with public code, on-chain log and CT log references; no measurements of cost or failure rates. Written by the system's builders.

## Relevance to us

Teleport is the delegation half of the TEE-agent line: users lend a narrowly scoped credential to an enclave program that acts for many of them at once. In Sybil terms one program legitimately speaks through many human accounts, which is the same mechanism a vote-buyer uses in [[austgen-2024-liquefaction]], except here each lender consented to a public, auditable policy. A swarm-level reputation or voting system cannot tell this from coordinated Sybil behaviour unless delegation policies are themselves attested and visible. The one-shot monotonic counter is a reusable pattern for rate-limiting what a delegated agent identity may do. Related: [[malhotra-2024-setting]] (full encumbrance of an agent's own account), [[kelkar-2024-complete]] (cited in the post as the encumbrance reference), [[miller-2024-sirrah]].
