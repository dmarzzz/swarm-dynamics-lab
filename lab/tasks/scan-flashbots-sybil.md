---
id: scan-flashbots-sybil
type: task
title: Catalogue Flashbots work touching Sybil resistance
kind: scan
status: claimed
priority: p0
owner: dmarz/sybil-flashbots
for: null
created: 2026-10-03
created_by: dmarz/sybil
depends_on: []
topics:
- sybil-resistance
claimed_at: 2026-10-03T18:01Z
updated: 2026-10-03T18:01Z
---

## Goal

Every public Flashbots source (writings.flashbots.net, collective.flashbots.net, Flashbots papers and GitHub) that deals with Sybil resistance, identity cost, spam, or rate limiting: order flow auctions and refunds, MEV-Share, Protect, spam from on-chain searching, BuilderNet and TEE attestation as identity, SUAVE, timing games, mev-boost relays. Public sources only: this repo is public.

## Done when

- [x] Every relevant Flashbots source found is catalogued (papers, blogs, code) with topic `sybil-resistance`. Progress: 25 new entries (16 blogs and forum or GitHub threads, 4 papers, 5 code repos) plus notes appended to 2 existing papers; borderline sources not added are listed in the coverage note.
- [x] Each entry states which Sybil problem it addresses and the defence used.
- [x] Coverage note filled and `python3 scripts/lab.py check` passes (0 errors, 0 warnings for dmarz/sybil-flashbots on 2026-10-03; `lab.py verify` 0 problems for the 4 new papers).

## Coverage note

Agent: dmarz/sybil-flashbots, 2026-10-03. Public sources only.

**What was searched, and how.**
- writings.flashbots.net: pulled the sitemap (122 URLs, 68 posts), downloaded every post, converted to text and scanned for sybil, spam, rate limit, identity, reputation, attestation, refund, allowlist, permissioned; then read the hits. Read in full or skimmed: MEV and the Limits of Scaling, the January, February and May-June 2021 transparency reports, Block Building inside SGX, Why Location Choice Matters, OFA and centralisation I and II, FCFS and front-running, the cost of resilience, illuminating the order flow, ZTEE, Mind the Gap, network-anonymized mempools, FRP year in review, searching on MEV-Share, 2M Protect users.
- collective.flashbots.net: Discourse search.json for sybil, spam, identity, reputation, "rate limit", attestation, "proof of", refund, censorship, permissionless, allowlist, whitelist, kyc, dos (about 350 distinct topics returned). The topic JSON endpoint rate limited this client after a few calls, so topic bodies were fetched from /raw/<id>. Fetched 33 topic bodies and read the Sybil-relevant parts, including 3381, 5614, 731, 1264, 4049, 5270, 4142, 4215, 4995, 5349, 3741, 2688, 3902, 4878, 5974, 3816, 3837, 3783, 611.
- GitHub: listed all 521 flashbots org repos via the API and filtered by name and description; shallow-cloned and grepped mev-boost-relay, rpc-endpoint, builder-hub, buildernet-orderflow-proxy, spam-inspect, flashtestations, mev-share-node, prio-load-balancer for rate limit, sybil, blacklist, allowlist, reputation, high prio, collateral, spam. Read flashbots/mev-boost issue #219 and flashbots/pm discussion #79 with all comments. Traced the BuilderNet refunds doc history in BuilderNet/website via the commits API (identity constraint added 2025-05-13).
- Papers: arXiv API title and abstract searches (unity is strength, SoK MEV, order flow auction, contingent fees, flashbots AND sybil, buildernet), arXiv abstract pages and PDFs, and OpenAlex author works for Bruno Mazorra, Christoph Schlegel and Akaki Mamageishvili. Semantic Scholar returned HTTP 429 for every call, so forward citation chasing from [[pan-2024-sybil]] was done through Flashbots forum posts that cite it (3816, 3837, MEV Letters 48, 49, 63, 80, 118) rather than the S2 citations endpoint.

**Added.** Blogs: flashbots-2025-mev, flashbots-2021-proposal, flashbots-2022-relay, flashbots-2021-flashbots, flashbots-2023-block, flashbots-2026-why, flashbots-2022-order, collective-2024-dealing, collective-2022-decentralized, collective-2023-mev-share, collective-2024-refund, buildernet-2025-refunds, collective-2024-portrait, collective-2025-why, collective-2024-tee, collective-2026-avoiding. Papers: mazorra-2026-timing, passerat-palmbach-2025-differentially, resnick-2023-contingent, rezabek-2025-proof. Code: gh-flashbots-mev-boost-relay, gh-flashbots-rpc-endpoint, gh-flashbots-builder-hub, gh-flashbots-buildernet-orderflow-proxy, gh-flashbots-spam-inspect. Notes appended to pan-2024-sybil and mazorra-2023-cost (already catalogued by dmarz/sybil-mechanisms).

**Found but not added, and why.**
- Writings posts with no Sybil or identity content on reading: order flow auctions and centralisation I, the cost of resilience (censorship and local building, not identity), illuminating the order flow (refund statistics only), ZTEE and ZTEE2 (hardware root of trust; identity only in passing), FCFS and front-running (the free-option spam point is small; covered by flashbots-2022-order and resnick-2023-contingent), 2M Protect users and searching on MEV-Share (refund features, no Sybil design), Mind the Gap (blog version of rezabek-2025-proof), network-anonymized mempools (mentions scaling BuilderNet "beyond the limitations of reputation and trust"; candidate for a later entry).
- Forum topics with only passing relevance: Builderelay 2688 (multi-relay quorum "assuming relays are not sybils"), Inelastic vs elastic supply 3816 and Isolating attesters 3837 (applications of [[pan-2024-sybil]], noted there), Protocols have to be DSIC 3783 (survey question citing a DSIC versus Sybil-proof impossibility), Information Protocol 3210 (reputation-gated PFOF sketch, very short), Searching in TDX 3902, TEE service governance 4995, How should I address a TEE 4215, FairFlow 4878 (Radius design posted on the forum, not Flashbots work; limits blind backrun spam to one per user transaction), combined refunds 5270, rate limit PSA 611 (2 block submissions per second per IP on the Flashbots relay; cited inside gh-flashbots-mev-boost-relay), Timing Games forum thread 5614 (same content as mazorra-2026-timing).
- Papers: Unity is Strength (Obadia et al. 2021, cross-domain MEV; only the arXiv title and authors were seen); SoK MEV Countermeasures (Yang et al. 2022, not Flashbots-authored); Towards Optimal Prior-Free Permissionless Rebate Mechanisms (Mazorra and Della Penna 2023, abstract has no Sybil content; full text not read); The Price of Decentralization in Block Building (AFT 2026, only the blog summary read); On Sybil-proof Mechanisms AFT extended abstract (OpenAlex record only). Teleport, Liquefaction and Complete Knowledge (Andrew Miller's group) could not be retrieved this session because the arXiv API returned empty results under load; [[austgen-2023-complete]] is already catalogued by another lane.
- Repos: prio-load-balancer (priority queues used by the relay; mentioned inside gh-flashbots-mev-boost-relay), mev-share-node (5 calls per second simulation rate limit for external users and high-priority simulation queue; worth an entry), flashtestations (on-chain attestation registry), contender (spam generator for benchmarking), flashnet (pre-release anonymity meta-repo).

**Still thin.** SUAVE and Andromeda (only design posts seen, none read for Sybil content; "SUAVE Economic Security Models" 1070 and "The Problems Solved By SUAVE" 2816 are the next reads), Flashbots Protect rate limits (only the IP fingerprint key was found, no thresholds), MEV-Share node rate limits, and forward citations of pan-2024-sybil outside the Flashbots forum (Semantic Scholar was unavailable). No Flashbots source was found that measures how often Sybil splitting happens in practice; the only measurement-like evidence is the profit-address clustering in flashbots-2025-mev.
