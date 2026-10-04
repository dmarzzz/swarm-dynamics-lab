---
id: borge-2017-proof-of-personhood
type: paper
title: "Proof-of-Personhood: Redemocratizing Permissionless Cryptocurrencies"
authors: ["Maria Borge", "Eleftherios Kokoris-Kogias", "Philipp Jovanovic", "Linus Gasser", "Nicolas Gailly", "Bryan Ford"]
year: 2017
venue: "2017 IEEE European Symposium on Security and Privacy Workshops (EuroS&PW)"
url: https://bford.info/pub/dec/pop.pdf
doi: "10.1109/eurospw.2017.46"
arxiv: null
cite: "Borge, M., Kokoris-Kogias, E., Jovanovic, P., Gasser, L., Gailly, N., & Ford, B. (2017). Proof-of-Personhood: Redemocratizing Permissionless Cryptocurrencies. In 2017 IEEE European Symposium on Security and Privacy Workshops (EuroS&PW), pp. 23-26. IEEE."
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "63 (Crossref, 2026-10-03); 107 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

The paper coins proof-of-personhood (PoP): a pseudonym party, a physical event where volunteer organisers each record attendees' ephemeral public keys after an entry barrier closes, issues exactly one token per body present. Tokens are authenticated to services with linkable ring signatures, giving a per-service tag that blocks a second account without revealing which attendee signed. PoPCoin then replaces proof-of-work or proof-of-stake with "one PoP-token, one vote": minters are drawn uniformly at random (via RandHound randomness) from token holders, optionally inside a ByzCoin consensus window.

## Contribution

Frames Sybil resistance for consensus as a choice of scarce resource and proposes the human body (presence at one place at one time) as the resource, explicitly to avoid the plutocratic concentration of PoW and PoS.

## Key results

- No experiments or measurements; a workshop design paper (4 pages).
- Threat model: anytrust, so attendees need only one honest organiser and one honest conode; observers video-record the party to make double issuance auditable; ink stamps and a two-room layout stop people re-queuing.
- Token authentication: a linkable ring signature over the party transcript yields a stable per-service tag; a repeated tag is refused, which is the Sybil check.
- Minting: each minter holds one token, so selection is uniform; a minter caught extending two chains is punished, addressing nothing-at-stake.
- Scaling idea: simultaneous parties in distant regions so that no one can attend two; local currencies that might later federate.

## Methods and models

Protocol design built on collective signing (CoSi), linkable ring signatures, RandHound and ByzCoin.

## Limitations and open questions

No implementation numbers, no analysis of coercion, token selling or organiser collusion beyond anytrust. Frequency of parties and inclusion of people who cannot attend are left open; [[ford-2020-identity]] develops these.

## Relevance to us

The cleanest statement of "Sybil resistance means choosing which scarce resource identities must burn". For agent swarms the analogue of a pseudonym party is a synchronous attestation round where each physical robot or each human principal can be present once; [[gil-2015-guaranteeing]] uses physics in a similar way. It also marks where agent swarms differ from humans: an AI agent has no body to bind to, so PoP can bound principals behind agents but not agents themselves. See [[siddarth-2020-who]] for deployed descendants (Idena, BrightID) and [[gupta-2020-resource]] for the resource-burning framing.
