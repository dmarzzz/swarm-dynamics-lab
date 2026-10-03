---
id: austgen-2023-complete
type: blog
title: "Complete Knowledge"
authors: [James Austgen, Kushal Babel, Vitalik Buterin, Phil Daian, Ari Juels, Mahimna Kelkar]
year: 2023
url: https://medium.com/initc3org/complete-knowledge-eecdda172a81
site: IC3 (Initiative for CryptoCurrencies and Contracts) on Medium
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Blog post (16 January 2023) introducing proofs of complete knowledge (PoCK), from the paper at eprint.iacr.org/2023/044. Ordinary proofs of knowledge, such as signatures, show that someone can use a key, but a key held inside a TEE or MPC can be "encumbered": usable only under a third party's policy. A transaction signed with an encumbered key is indistinguishable from one signed with a free key, which enables stealthy vote buying (breaking even MACI) and "Dark DAOs" that grow communities of encumbered users. Complete knowledge means some single party has direct, unrestricted access to the key. Two ways to prove it: a "fight fire with fire" TEE application that generates the voting key, attests to it, and releases it to the user (since TEEs cannot be nested, an attacker cannot wrap it), and a proof-of-work approach where the key is fed to a Bitcoin mining ASIC that has no TEE and is about a million times faster at hashing than a CPU, so no TEE could produce an equivalent proof in time; a roughly $200 2017-era ASIC sufficed. Applications beyond voting: preventing rental of identity or compliance credentials, distinguishing self-transfers for NFT royalties, and "Atomic NFTs" that cannot be fractionalised. A prototype includes an on-chain verifier and registry and a mobile-TEE version; code at github.com/complete-Knowledge.

## Key claims

- TEEs and MPC make secret keys transferable under policy, which silently breaks mechanisms that assume one key means one decision-maker.
- Encumbrance can be ruled out only by proving that the key was exposed to an unconstrained environment.
- CK can stop credential-rental markets, for example renting out an anti-money-laundering attestation.
- If social recovery becomes common, CK proofs of simultaneous knowledge of two keys stop working.

## Evidence quality

Research blog summarising an IACR ePrint paper with prototypes and deployed contracts; costs and security claims for the ASIC approach rest on the paper, which I did not open.

## Relevance to us

Encumbrance is the identity-rental attack in its strongest form: a Sybil operator does not need fake identities if it can lease real ones under enforceable policy, and no on-chain observer can tell. For AI agents this is the default case, since an agent acting for a principal is a policy-constrained use of the principal's credential. Any agent-swarm Sybil defence based on personhood or credentials [[buterin-2023-what]], [[ethresearch-2026-anonymous]], [[dobrokhvalov-2025-privacy]] has to state whether it tolerates encumbered or delegated keys. Code: [[gh-complete-knowledge-ck]]. TEE trust limits: [[ethresearch-2026-physical]].
