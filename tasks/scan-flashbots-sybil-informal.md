---
id: scan-flashbots-sybil-informal
type: task
title: Catalogue Flashbots-adjacent informal writing on Sybil resistance
kind: scan
status: claimed
priority: p1
owner: dmarz/sybil-flashbots-informal
for: null
created: 2026-10-03
created_by: dmarz/sybil
depends_on: []
topics:
- sybil-resistance
claimed_at: 2026-10-03T18:02Z
updated: 2026-10-03T18:02Z
---

## Goal

Ethresear.ch posts, X threads, talks and blogs by Flashbots researchers and the surrounding MEV community on Sybil resistance, identity, TEE-based personhood, spam and searcher/builder Sybils.

## Done when

- [x] At least 15 entries catalogued with topic `sybil-resistance`, including every review article found. (19: 17 blogs, 1 talk, 1 code repo. No review articles in this informal lane; Vitalik's PoP essay [[buterin-2023-what]] is the closest survey-style piece.)
- [x] At least 4 read in full. (12 marked full.)
- [x] Code linked where it exists. ([[gh-complete-knowledge-ck]] linked from [[austgen-2023-complete]]; other code is linked by URL inside entries where the source names it: ethereum/research correlation_analysis, BringID/TLSN, AetherWeave Prysm fork not public in what I opened.)
- [x] Coverage note filled and `python3 scripts/lab.py check` passes (0 errors at 2026-10-03T18:18Z).

## Coverage note

Searched by dmarz/sybil-flashbots-informal on 2026-10-03.

APIs and queries:
- ethresear.ch Discourse search API (`/search.json?q=`): "sybil", "sybil mev", "sybil builder", "searcher identity", "proof of personhood", "TEE sybil", "timing games", "builder collusion", "censorship builders". Topics read through `/t/<id>.json` (the `print=true` variant rate-limits after ~4 calls).
- WebSearch: Andrew Miller "proof of cloud" TEE sybil; Vitalik biometric proof of personhood; TEE personhood Flashbots/Phala; Flashbots BuilderNet TEE.fail response; a16z crypto sybil airdrops; Andrew Miller TEE personhood/teleport; Liquefaction/encumbrance personhood; Devcon SEA Dave talk; site:x.com sybil builders flashbots.
- GitHub API for Complete-Knowledge/ck. Semantic Scholar search was rate-limited (429) on the one query I tried; citation chasing was not done in this lane, since the sources here are forum posts and blogs without reference graphs. The formal-paper lanes already hold [[pan-2024-sybil]], [[douceur-2002-sybil]], [[adler-2024-personhood]], which entries link to.

Added (19): [[ethresearch-2026-anonymous]], [[porobov-2026-price]], [[dobrokhvalov-2025-privacy]], [[ethresearch-2026-physical]], [[kadianakis-2023-proof]], [[buterin-2024-supporting]], [[glynn-2026-wash]], [[nag-2026-sybil]], [[coutinho-de-paula-2025-dave]], [[coutinho-de-paula-2024-dave]], [[ankushin-2026-public]], [[alpturer-2026-aetherweave]], [[bahrani-2026-capacity]], [[neuder-2024-block]], [[buterin-2023-what]], [[austgen-2023-complete]], [[eigenphi-2025-buildernet]], [[zebedee-2019-evidence]], [[gh-complete-knowledge-ck]].

Opened but not added, and why:
- collective.flashbots.net "Why TEE.fail is bullish for BuilderNet" (seen in search results only): belongs to the formal sybil-flashbots lane.
- ethresear.ch "Price-of-personhood digital identity" (2020, Porobov): superseded by [[porobov-2026-price]]; mentioned inside that entry.
- ethresear.ch "Block builder centralization" (2022), "Visualization for builders reputation" (2023), "Timing Games: Implications and Possible Mitigations" (2023), "Building towards Multi-Party Block Construction" (2026): opened; they discuss builder concentration, reputation and timing but not Sybil identities, except a reply in the MPBC thread quoting the Flashbots/Offchain Labs Sybil-proof second-price result (that paper is [[pan-2024-sybil]]).
- Zero Knowledge Podcast ep. 339 "TEEs with Andrew Miller" (transcript partly read): discusses TEE encumbrance and the teleport.best account-delegation demo but not Sybil resistance directly; the encumbrance argument is covered by [[austgen-2023-complete]].
- Oasis "Privana: A Practical Liquefaction Implementation" (vendor blog): product announcement; the underlying Liquefaction paper (arXiv 2412.02634) belongs in a paper lane and is not yet catalogued.
- goodcrypto.net "BuilderNet as a policy test case": fetched, not read closely enough to catalogue.
- Proof of Cloud paper (arXiv 2510.12469), Dave paper (arXiv 2411.05463), WireTap and TEE.fail papers: formal papers, not in this lane; none are in the library yet.

Still thin:
- X threads: none catalogued. X blocked automated reading and `site:x.com` searches returned no relevant Flashbots-researcher threads on Sybils. A human with an X session should pull threads by Flashbots researchers on BuilderNet admission, Proof of Cloud and searcher identity.
- Talks: only the Devcon Dave talk via its slides. MEV-SBC and TEE.salon talks (for example "Where you run your TEEs matters", Bangkok 2024, and James Austgen's MEV-SBC '24 Liquefaction talk) need transcripts; YouTube returned no transcript.
- Paradigm, a16z crypto and Frontier Research blogs on searcher or builder Sybils: no relevant posts found with the queries above.
- Sybil validators/builders in timing games and PBS collusion: the forum material treats these as concentration problems, not identity problems; the anti-correlation post [[buterin-2024-supporting]] is the closest.

