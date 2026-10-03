---
id: ethresearch-2026-physical
type: blog
title: "Physical integrity, attestation, and the state of permissionless TEEs"
authors: [fnerdman (ethresear.ch user; states employment at Ritual and prior work at Flashbots)]
year: 2026
url: https://ethresear.ch/t/physical-integrity-attestation-and-the-state-of-permissionless-tees/24964
site: ethresear.ch
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Long forum post (26 May 2026) on whether TEE networks can admit anyone with a valid attestation. The author separates three layers: confidential execution, measurement and attestation, and custody and physical-integrity endorsement (who controls the hardware and whether it is protected from tampering). Two 2025 attacks are summarised: WireTap (disclosed 30 September 2025; under $1,000 of hardware and under 45 minutes to extract an SGX attestation key on DDR4, then forge quotes accepted by Intel's DCAP library, demonstrated against Secret Network's testnet) and TEE.fail (disclosed 28 October 2025; DDR5 and Intel TDX, about 15 minutes, forged quotes verified at "UpToDate", demonstrated against a non-production Flashbots BuilderNet instance and Automata's on-chain DCAP verifier on testnet). Intel and AMD treat physical bus interposition as out of scope. The post then compares GCP, Azure, AWS Nitro, OVH/OpenMetal and Phala Cloud on whether they give an operator-signed custody endorsement and whether it is verifiable on-chain, and describes Intel Platform Ownership Endorsement (PoE) and the witness-based Proof of Cloud registry as the two paths to an endorsement layer. Every network that responded to the attacks either already had, or added, admission controls beyond raw attestation.

## Key claims

- After WireTap and TEE.fail, a valid DCAP quote alone no longer proves a distinct, physically protected machine; a forged quote is cheap.
- "Permissionlessness is not decentralization": anyone may join in protocol, while all nodes may still sit in one cloud and jurisdiction.
- Integrity guarantees stack with more independent operators (one honest operator detects divergence); confidentiality guarantees get weaker with each operator that holds the secret.
- Partial permissionlessness through operator endorsements (Intel PoE, Azure AK chain, Nitro's fused attestation, Proof of Cloud) is achievable now; full permissionlessness needs trustless hardware that is years away.
- BuilderNet-class block builders are permissioned by design with IP allowlists.

## Evidence quality

Practitioner analysis by someone who worked on Flashbots TEE infrastructure. The attack figures are taken from the WireTap and TEE.fail papers, which I did not open; the provider comparison is the author's assessment. Replies (Micah Zoltu and others) dispute whether the conclusion amounts to "trust the hyperscalers".

## Relevance to us

TEE attestation is one of the main proposals for making agent identities costly: "one agent = one attested enclave". This post shows that the cost of forging such an identity is now about $1,000 and minutes of physical access, so attestation without a custody endorsement is a weak Sybil barrier, and the networks that rely on it fell back to allowlists. For agent swarms it suggests treating attestation as evidence of code integrity, not of identity count, and pairing it with a scarce resource (stake, endorsement by a known operator). It also gives the integrity-versus-confidentiality asymmetry that applies to replicated agent committees. Related: BuilderNet's operator monoculture critique [[eigenphi-2025-buildernet]], TEE encumbrance of keys [[austgen-2023-complete]], stake-backed identities [[alpturer-2026-aetherweave]].
