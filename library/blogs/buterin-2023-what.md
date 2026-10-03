---
id: buterin-2023-what
type: blog
title: "What do I think about biometric proof of personhood?"
authors: [Vitalik Buterin]
year: 2023
url: https://vitalik.eth.limo/general/2023/07/24/biometric.html
site: vitalik.eth.limo
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Essay (24 July 2023; acknowledges discussion with the Worldcoin team, the Proof of Humanity community and Andrew Miller) on proof of personhood (PoP): a list of public keys where each key is controlled by a distinct human and bots cannot add keys. It surveys Proof of Humanity, BrightID, Idena, Circles and Worldcoin, and discusses privacy (ZK-SNARK membership proofs; Worldcoin publishes only an iris hash; MPC storage of hashes as a stronger option), accessibility (billions of smartphones vs a few hundred Orbs), centralization (governance, specialized hardware, proprietary algorithms) and security. The security section lists fake people (AI-generated or 3D-printed), selling IDs, renting IDs, phone hacking and government coercion. Mitigations include re-registration that cancels the previous ID (makes selling non-credible), making which Orb or manufacturer issued an ID provable so bad devices can be revoked, locking keys in trusted hardware behind a ZK layer, MACI against vote selling, and running applications inside MPC. It compares social-graph and biometric approaches and ends with a table: social-graph (privacy low, accessibility fairly low, decentralization robustness fairly high, security against fake people high if done well), general-hardware biometric (fairly low, high, fairly high, low), specialized-hardware biometric (fairly high, medium, fairly low, medium), and argues for a hybrid where biometrics bootstrap a social graph.

## Key claims

- Without PoP, decentralized governance is easy to capture by wealthy actors, and many services can stop denial of service only by pricing out low-income users.
- At the time of writing neither Worldcoin nor Proof of Humanity saw significant deepfake attacks, because hiring low-wage workers to register is cheaper.
- A single malicious or hacked Orb manufacturer could mint unlimited fake identities, so issuance provenance must be provable and revocable.
- Renting IDs is not prevented by re-registration; for voting it needs MACI-style receipt-freeness or MPC.
- Social-graph systems let well-connected people mint more pseudonyms; an "N accounts for $N²" rule could allow limited pseudonymity.
- General-purpose biometrics may only work for another one to two years against AI.

## Evidence quality

Opinion and analysis by a protocol designer, citing projects and some data (iris-hash bit-difference plots from Worldcoin, smartphone adoption figures). No new measurements.

## Relevance to us

This is the reference informal treatment of personhood as a Sybil defence in crypto, and it already names the attacks that matter most for AI agent swarms: AI-generated fake people, and real humans selling or renting their identity to an operator who then runs agents under it. The "N accounts for $N²" idea is a concrete knob for how many agents one human principal may field. The hybrid and provenance-revocation ideas apply to agent credential issuers in [[ethresearch-2026-anonymous]]. The renting problem is made sharper by TEE key encumbrance [[austgen-2023-complete]]. Market measurement of forging cost: [[porobov-2026-price]].

Worldcoin code catalogued separately: [[gh-worldcoin-world-id-contracts]], [[gh-worldcoin-open-iris]].
