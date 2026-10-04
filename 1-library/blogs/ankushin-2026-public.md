---
id: ankushin-2026-public
type: blog
title: "Public-mempool gas sponsorship needs escrow, a bond, or trust"
authors: [Daniil Ankushin]
year: 2026
url: https://ethresear.ch/t/public-mempool-gas-sponsorship-needs-escrow-a-bond-or-trust/25995
site: ethresear.ch
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Forum post (14 September 2026) proving an impossibility for spam and Sybil resistance in a public mempool. The question is whether a contract can sponsor gas for another user's transaction, relayed by an N-node public mempool, with no locked value and no off-chain trust. Assumptions: identities are free and may hold zero seizable balance (A1); the eventual builder cannot be bound in advance (A2); checking a transaction costs each forwarding node w > 0, lost if it is never included (A3). The theorem: no admission rule can admit sponsored transactions without seizable value or a per-attempt non-refundable cost and also keep wasted work bounded by attacker cost independently of N. The proof splits on what the rule charges per attempt: nothing (wasted work W = N·w·k for k transactions, so the waste-to-cost ratio is about N), an on-chain fee or bond, a held balance, or an off-chain toll such as proof of work. Deduplication, rate limits and reputation fail because fresh identities are free. All existing designs fall into three categories: pay per attempt, hold money, or trust someone off-chain (relayer, preconfirmation, personhood check). A corollary shows a reserved balance cannot be proved from a snapshot, because the snapshot does not show what is already promised to other pending transactions.

## Key claims

- A free baseline capacity K0 > 0 for new identities leaks work proportional to the number of Sybil identities.
- The factor N is inherent to public gossip, since reaching all nodes is what eclipse resistance guarantees.
- Douceur's result gives the personhood branch: open-membership Sybil resistance needs a scarce-resource test or a certifier.
- ERC-4337/ERC-7562 stake and reputation, EIP-8141 reserved balances and EIP-8223 checked balances each map to one category.

## Evidence quality

Informal but explicit proof with stated assumptions; no simulation. The argument is general and reads correct to me; I did not check the EIP details it cites.

## Relevance to us

The theorem applies almost unchanged to any open multi-agent message network: if agents can mint identities for free and every node must do work to validate each message before knowing whether it is useful, then spam costs the network N times what it costs the attacker, unless each identity posts value, pays per message, or is certified by someone trusted. That is a design constraint for agent gossip layers and shared blackboards, and a ready-made taxonomy (toll, bond, trust) for classifying proposed defences. Related: stake-backed identities [[alpturer-2026-aetherweave]] (bond), personhood [[buterin-2023-what]] (trust), price of forgery [[porobov-2026-price]].

The personhood branch of the proof rests on [[douceur-2002-sybil]].
