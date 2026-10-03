---
id: eigenphi-2025-buildernet
type: blog
title: "BuilderNet's Infrastructure Monoculture: Centralization with Extra Steps"
authors: [DeFi Alice (guest author, pseudonymous)]
year: 2025
url: https://eigenphi.substack.com/p/guest-post-buildernet-infra-monoculture
site: Wisdom of DeFi by EigenPhi (Substack)
topics: [sybil-resistance, swarm-detection]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Guest opinion post (4 June 2025) critiquing Flashbots' BuilderNet, which lets several operators run block-builder nodes inside TEEs with shared order flow. The author argues that the nodes are nominally independent but run the same builder software (rBuilder), on the same trusted hardware (Intel TDX), on the same cloud (Microsoft Azure), attested by Azure and admitted by Flashbots' BuilderHub. This is a common-mode failure risk comparable to a client supermajority. Flashbots controls admission (BuilderHub verifies attestations and provisions secrets), onboarding of the few operators named (Flashbots, Beaverbuild, Nethermind), the orderflow proxy, and software releases; some components (orderflow proxy, bidding) were not open source at the time. The author concludes that decentralization here is "superficial" and asks for open access, open source and open governance.

## Key claims

- Multiple operators running identical stacks under one gatekeeper do not add independence.
- TEE attestation shifts trust from builders to hardware vendors, cloud providers and the attestation service.
- No credibly neutral party was observed verifying BuilderNet's attestations at the time of writing.

## Evidence quality

Opinion piece, explicitly not EigenPhi's official position. Claims about deployment state are dated June 2025 and may be outdated; the October 2025 TEE.fail response and later Proof of Cloud work are described in [[ethresearch-2026-physical]].

## Relevance to us

The post names the mirror image of a Sybil attack: many identities that are not controlled by one adversary but are still not independent because they share code, hardware and a gatekeeper. In agent swarms the same issue arises when many agents run the same model and prompt, so their "independent" votes are correlated. It supports measuring effective independence (for example via correlated failures, as in [[buterin-2024-supporting]]) rather than counting identities, and it shows how permissioned admission becomes the Sybil defence of last resort when attestation alone is not trusted.
