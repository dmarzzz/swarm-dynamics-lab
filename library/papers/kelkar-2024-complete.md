---
id: kelkar-2024-complete
type: paper
title: "Complete Knowledge: Preventing Encumbrance of Cryptographic Secrets"
authors: [Mahimna Kelkar, Kushal Babel, Philip Daian, James Austgen, Vitalik Buterin, Ari Juels]
year: 2024
venue: ACM CCS 2024 (preprint IACR ePrint 2023/044)
url: https://eprint.iacr.org/2023/044
doi: 10.1145/3658644.3690273
arxiv: null
cite: "Kelkar, M., Babel, K., Daian, P., Austgen, J., Buterin, V., & Juels, A. (2024). Complete Knowledge: Preventing Encumbrance of Cryptographic Secrets. In Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (CCS '24). ACM. https://doi.org/10.1145/3658644.3690273. Preprint: IACR Cryptology ePrint Archive 2023/044."
topics: [sybil-resistance]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: null
code: [gh-complete-knowledge-ck]
---

## Summary

Classical proofs of knowledge show that "the prover" can use a secret, but the prover may be a composite of a user and a TEE or MPC committee that only lets the user use the key under a policy. The paper formalises complete knowledge (CK): a proof of CK guarantees that some single party, the eavesdropper on the channel to a special local resource R, can extract the witness during the proof. Two instantiations: R is a TEE application that attests it has output the key in plaintext (secure if TEEs cannot be nested), or R is an off-the-shelf Bitcoin mining ASIC that must grind a Fischlin-style proof of work over Schnorr transcripts faster than any TEE could, so the key must be exposed to the ASIC in the clear. The SMACK prototype verifies both on Ethereum and keeps a CK registry. I read the ePrint version (abstract, introduction, motivation, PoCK intuition and definitions, implementation, mobile appendix, conclusion); the proofs were skimmed.

## Contribution

Gives a single root cause, missing CK, for vote selling under coercion-resistant voting and MACI, credential sale, and loss of deniability in messaging, and turns "this key is not rented" into a checkable property. It is the countermeasure that [[austgen-2024-liquefaction]] relies on.

## Key results

- Coercion-resistant voting protocols (JCJ-style, Civitas) and MACI are insecure against TEE key encumbrance; CK restores bribery resistance for re-voting designs and MACI, but not fully for fake-credential designs.
- New applications: key-coupling (proving the same user knows two keys, e.g. for KYC continuity or royalty-free self-transfers) and CK addresses / Atomic NFTs that only CK-proven keys may hold.
- ASIC parameterisation (Fig. 5): an ASIC at 154 TH/s completes with probability near 1 while an adversary with 10,000 CPUs (72 MH/s) succeeds with negligible probability. The prototype used a second-hand Antminer S9 (13 TH/s, about $100).
- Gas (Fig. 6, Oct 2023, 100,000 gas about $1.55): verifying an ASIC proof 7,620,401 gas; recording a CK proof in the registry 54,260 gas. Android key-attestation CK costs about 1.5 million gas per certificate.
- Remark 1: CK only guarantees that some entity on the channel to R learns the key, which is enough to deter bribery because the user will not accept a bribe that exposes a key also holding her funds.

## Methods and models

Interactive proof formalism with straight-line, non-programming extractors; the eavesdropping extractor is modelled as a physical man-in-the-middle on the prover-to-resource channel. SGX-like TEEs modelled with an existing UC formalism (their reference [53], not opened). Implementation: Stratum V2 mining software, a private Bitcoin network for puzzle generation, Schnorr Σ-protocol, Ethereum randomness for challenges; Android CK via Google key attestation.

## Limitations and open questions

The TEE variant fails if TEE attestation is forgeable (the paper's footnote notes a TEE break can produce fake attestations); [[seto-2025-wiretap]] and [[chuang-2025-teefail]] later showed attestation keys can be extracted for under $1,000. Android attestation has had broken keystores, and publishing certificate chains on-chain links an address to a device manufacturer. Key-coupling may not survive key rotation or social recovery. CK must be required by each application; it does not help after a key has been encumbered from birth unless the application refuses such keys.

## Relevance to us

CK is the only primitive in the library that directly attacks identity rental rather than identity minting. For an agent swarm, a "one agent, one key" or "one person, one agent" rule is meaningful only if the key is CK-proven; otherwise a principal can lease many keys from their owners with enforceable exclusivity ([[austgen-2024-liquefaction]]). There is an inherent tension with autonomous agents: TEE-hosted agents such as [[malhotra-2024-setting]] are deliberately encumbered (nobody, including the developer, knows the key), so they cannot pass a CK check by construction. A swarm must therefore choose between admitting provably autonomous agents and ruling out rented identities, or bind identity to something other than key knowledge. Blog summary: [[austgen-2023-complete]]. Personhood context: [[adler-2024-personhood]], [[buterin-2023-what]].
