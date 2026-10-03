---
id: rosenberg-2023-zk-creds
type: paper
title: "zk-creds: Flexible Anonymous Credentials from zkSNARKs and Existing Identity Infrastructure"
authors: ["Michael Rosenberg", "Jacob White", "Christina Garman", "Ian Miers"]
year: 2023
venue: "2023 IEEE Symposium on Security and Privacy (SP)"
url: https://eprint.iacr.org/2022/878.pdf
doi: "10.1109/SP46215.2023.10179430"
arxiv: null
cite: "Rosenberg, M., White, J., Garman, C., & Miers, I. (2023). zk-creds: Flexible Anonymous Credentials from zkSNARKs and Existing Identity Infrastructure. In 2023 IEEE Symposium on Security and Privacy (SP), pp. 790-808. IEEE. Full version: IACR Cryptology ePrint Archive 2022/878."
topics: [sybil-resistance, llm-agent-swarms]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "106 (OpenAlex, 2026-10-03)"
code: [gh-rozbb-zkcreds-rs]
---

## Summary

zk-creds replaces blind-signature anonymous credentials with general-purpose zkSNARKs (Groth16 over BLS12-381, Poseidon hashes). A credential is a commitment Com(nk, rk, attrs; r) holding a pseudonym key nk, a rate key rk and attributes. It is "issued" by appending it to a Merkle forest kept on a bulletin board (transparency log, Byzantine system or blockchain), so issuers need no signing keys and every issuance is publicly auditable. Issuance can require "zk-supporting-documentation": a proof that the committed attributes match an existing signed document, demonstrated on unmodified NFC US passports (ICAO 9303 data groups). Showing a credential proves membership plus arbitrary access predicates, composed as separately proven "gadgets" glued by a new blind Groth16 linkage proof (LinkG16) that lets the expensive membership proof be reused across shows without becoming a tracking handle. The version read is the ePrint full version dated 19 July 2023 (main body through Section 10; appendices not read in detail).

## Contribution

It moves anonymous credentials from bespoke protocols to a compile-your-predicate model, decouples "who vouches for an attribute" from "who holds keys", and gives concrete Sybil-resistance gadgets (context pseudonyms, per-epoch rate limits, clone-resistance with deanonymisation) on top of existing identity roots. It builds directly on decentralized anonymous credentials [[garman-2013-decentralized]] and on the periodic n-times tokens of [[camenisch-2006-how]].

## Key results

- With 2^31 issued credentials (tree height 24, 2^8 trees), a client-optimised simple-possession show takes 5 ms to prove and 3 ms to verify, assuming the membership proof is precomputed; rate limiting with clone resistance takes 90 ms to show and 5 ms to verify (Table 1). Recomputing membership adds about 460 ms.
- Server-optimised monolithic variant: about 450-530 ms to prove, 1.5 ms to verify, batch verification 1.8 verifications/ms/core.
- Signature-issued variant (Schnorr, so FROST threshold issuance): membership-by-signature proof 129 ms versus 460 ms for tree-based issuance.
- Passport case study: converting a passport to a credential takes 1.97 s; proving over-18 with clone resistance takes 143 ms (602 ms with membership recomputation); verification 5 ms.
- Posting an issuance request to an EVM bulletin-board contract costs 576,808 gas; a Merkle root update 78,355 gas (about 20-50 USD at June 2022 prices).
- Peak prover memory 824 MB.

## Methods and models

Gadgets defined in Section 5.3: linkable show (pseudonym PRF_nk(ctx), stable per context and unlinkable across contexts, e.g. one Sybil-resistant credential gives unlinkable accounts across sub-forums); rate limiting (token PRF_rk(epoch||ctr) with a proof that ctr < N); clone resistance after Camenisch et al. 2006 (a second token id + H(nonce) * PRF'_rk(epoch||ctr), so reusing a counter gives two linear equations and reveals id, which can then be revoked from the list); expiry; session binding; join across credentials. Security is argued by simulation against static corruption of users, verifiers and issuers, assuming Groth16 simulation-extractability in the algebraic group model and Poseidon as a PRF. Section 8 discusses Sybil-resistant IDs from email (DKIM signatures as supporting documentation), from payment (a contract issues a credential iff a fee is paid), and from oracles or TLS notaries (DECO).

## Limitations and open questions

- Groth16 needs a per-circuit trusted setup (mitigated by MPC ceremonies and per-gadget CRSs).
- Witness updates for Merkle paths leak timing if users fetch them from the issuer; the paper offers frontier-based updates in an appendix.
- Anonymity requires at least two honest credential holders; early or small issuance lists give small anonymity sets.
- The Sybil resistance is only as strong as the root identity: a passport, a paid fee or an email address. The paper notes trust in the identity infrastructure is irreducible.
- DoS against the bulletin board is handled by a trusted operator in the prototype.

## Relevance to us

This is the most general template for giving agents in a swarm an anonymous, rate-limited, revocable identity. An orchestrator could require each agent to hold one credential per accountable principal (human, company or stake deposit), then demand a per-epoch rate-limit token or a per-context pseudonym for each action. Clone resistance is the right primitive against one principal copying a credential into many agent instances: an agent that exceeds its quota deanonymises the credential and gets it revoked. The issuer-by-payment option connects to agent payments as Sybil cost ([[crapis-2026-zk]], [[gh-x402-foundation-x402]]). Compare the simpler single-purpose constructions: [[davidson-2018-privacy]] (one-show tokens), [[taheri-boshrooyeh-2022-privacy]] (RLN with stake slashing), [[yun-2026-anonymous]] (ARC, keyed-verification rate limits).
