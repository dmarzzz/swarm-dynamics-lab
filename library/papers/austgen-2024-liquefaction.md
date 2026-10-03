---
id: austgen-2024-liquefaction
type: paper
title: "Liquefaction: Privately Liquefying Blockchain Assets"
authors: [James Austgen, Andrés Fábrega, Mahimna Kelkar, Dani Vilardell, Sarah Allen, Kushal Babel, Jay Yu, Ari Juels]
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2412.02634
doi: 10.48550/arXiv.2412.02634
arxiv: "2412.02634"
cite: "Austgen, J., Fábrega, A., Kelkar, M., Vilardell, D., Allen, S., Babel, K., Yu, J., & Juels, A. (2024). Liquefaction: Privately Liquefying Blockchain Assets. arXiv preprint arXiv:2412.02634."
topics: [sybil-resistance]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null
code: [gh-key-encumbrance-liquefaction]
---

## Summary

The paper names the Single-Entity Address-Ownership (SEAO) assumption, that the private key behind an address is held by one entity, and builds a wallet that breaks it. Liquefaction generates keys inside a TEE (a Solidity contract on Oasis Sapphire, a TEE-based EVM chain) so that no user ever knows them; signing rights are handed out as time-bounded, non-overlapping sub-policies ("asset-time segmentation"), and these can be rented, shared, pooled or sub-delegated with no on-chain trace. The authors implement a Dark DAO for Snapshot vote buying, a tokenised "Dark DAO Lite", soulbound-token sharing and a dusting-attack defence. With Flashbots they encumbered a real Flashbots employee soulbound token, then released the key to an employee instead of selling it. Measured costs are small: adding a sub-policy costs about $0.0006 and proving a transaction's inclusion about $0.0027 on Sapphire (October 2024 prices), while waiting for Ethereum finality before the next signature takes 1,036.9 s on average over 160 trials (49.0 s if the latest block is trusted).

## Contribution

First general model of key-encumbrance policies plus a working, open-source wallet, and the first broad enumeration of applications whose security rests on SEAO (quadratic voting, SBTs, airdrops, loyalty points, transaction-history risk scores, multisigs, wash-trading detection). It turns the Dark DAO idea of Daian et al. (2018) from a sketch into deployed code and points to complete knowledge [[kelkar-2024-complete]] as the countermeasure.

## Key results

- Appendix A states the Sybil point directly: identity systems that enforce one user, one account are "insufficient in the presence of key encumbrance", because a whale can control the votes of many identity-verified encumbered wallets owned by other people and so recover the quadratic advantage that account splitting would give.
- Encumbered access can itself be re-encumbered ("liquefying Liquefaction"), so delegation can be hierarchical and invisible to the wallet unless authentication uses complete-knowledge proofs.
- Designated-verifier proofs also fail under encumbrance; the wallet restores them by first demanding a CK proof from the verifier (DV-CK).
- Pre-signing is the main soundness hazard: a delegate could sign a transaction before its access expires. The prototype forces every signature to use the current account nonce and requires an inclusion proof before the next signature.
- Costs (Fig. 8, 100 Gwei on Sapphire, 1 ROSE = $0.06919): deploy policy 7,777,890 gas ($0.054), add sub-policy 87,162 gas ($0.0006), prove transaction inclusion 395,679 gas ($0.0027).
- A liveness fallback (sentinel wallet, challenge contract on Ethereum, t-of-n committee of backup TEEs) releases keys to their access manager if Sapphire is down for a set period, e.g. one week.

## Methods and models

Formal access-control model: policies are predicates over (player, message, state), with update functions that may add but not revoke access. Implementation in Solidity on Oasis Sapphire, signing Ethereum transactions, ERC-191 and EIP-712 messages only, so policy conflicts are decidable. Ethereum inclusion proofs are verified against a trusted block-hash oracle. TEE side channels and Sapphire deployment errors are explicitly out of scope.

## Limitations and open questions

The security of the encumbrance rests on an idealised TEE; side channels such as [[seto-2025-wiretap]] and [[chuang-2025-teefail]] are out of scope. The countermeasure, complete knowledge, has to be adopted by each application, and CK proofs from mobile TEEs cost about 1.5 million gas on Ethereum. Whether a given use is an attack is described by the authors as subjective. The repository README warns that pre-signing attacks are still trivial on mainnet because encumbrance history is not yet exposed to new policies.

## Relevance to us

This is the strongest result in the library on the converse of the gap question: encumbrance lets one principal rent many existing identities, with policy enforcement and no observable link. A swarm that counts "one key, one agent" or "one verified person, one agent" can be captured without minting a single fake identity; the adversary leases real ones and the lessors cannot defect. For agent swarms this is the default deployment, since an AI agent acting for a principal is exactly a policy-constrained use of the principal's credential, as in [[malhotra-2024-setting]] and [[sun-2024-tee]]. Personhood schemes [[borge-2017-proof-of-personhood]], [[siddarth-2020-who]], [[adler-2024-personhood]] and credential schemes such as [[durak-2024-non]] need a CK-style check ([[kelkar-2024-complete]], [[austgen-2023-complete]]) or must assume delegation. It also extends Douceur's argument [[douceur-2002-sybil]]: the scarce resource being rented is not computation but a credential that someone else already paid for.
