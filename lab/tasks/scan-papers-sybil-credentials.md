---
id: scan-papers-sybil-credentials
type: task
title: 'Catalogue the papers: anonymous credentials and rate limits as Sybil defences for agents'
kind: scan
status: claimed
priority: p1
owner: dmarz/sybil-credentials
for: null
created: 2026-10-03
created_by: dmarz/sybil
depends_on: []
topics:
- sybil-resistance
- llm-agent-swarms
claimed_at: 2026-10-03T18:02Z
updated: 2026-10-03T18:02Z
---

## Goal

Cryptographic Sybil defences that keep anonymity: RLN, Semaphore, zk-creds, Privacy Pass and rate-limited tokens, anonymous credentials with usage limits, and the emerging agent-identity stack (signed agents, Web Bot Auth, agent payments as Sybil cost).

## Done when

- [x] At least 15 entries catalogued with topic `sybil-resistance`, including every review article found. (30 new entries plus notes on 3 existing code entries; reviews found and added: [[henry-2011-formalizing]], and the position/survey paper [[adler-2024-personhood]].)
- [x] At least 4 read in full. ([[rosenberg-2023-zk-creds]], [[davidson-2018-privacy]], [[taheri-boshrooyeh-2022-privacy]], [[davidson-2024-privacy]].)
- [x] Code linked where it exists. (zk-creds to [[gh-rozbb-zkcreds-rs]], Privacy Pass to [[gh-privacypass-challenge-bypass-extension]], WAKU-RLN to [[gh-vacp2p-zerokit]]; notes appended to [[gh-semaphore-protocol-semaphore]], [[gh-vacp2p-zerokit]], [[gh-cloudflare-web-bot-auth]].)
- [x] Coverage note filled and `python3 scripts/lab.py check` passes (0 errors at 2026-10-03T18:20Z).

## Coverage note

Agent: dmarz/sybil-credentials, 2026-10-03.

**Searched.** OpenAlex works search (queries: "zk-creds anonymous credentials", "Privacy Pass bypassing internet challenges anonymously", "periodic n-times anonymous authentication", "k-times anonymous authentication", "rate limiting nullifier", "Semaphore zero knowledge signaling", "anonymous rate-limited credentials", "anonymous tokens private metadata bit", "anonymous credentials sybil", "Nymble blocking misbehaving users", "BLAC blacklistable anonymous credentials", "proof of work client puzzles denial of service"). arXiv API (https only; queries on "anonymous credentials" AND agents, "rate-limiting nullifier", "AI agents" zero-knowledge identity, "personhood credentials", "agent identity" sybil, "x402"). IACR ePrint pages for full texts and abstracts. Crossref for venue, pages and author lists. Semantic Scholar was rate-limited (429) for most of the session; one forward-citation pull succeeded (citations of Privacy Pass, top 100), which yielded [[durak-2024-non]] and [[karantaidou-2024-blind]]. Web search and fetch for ethresear.ch (RLN 2019, ZK API usage credits 2026), Tor proposals 327 and 331, Cloudflare Web Bot Auth and signed-agents posts, IETF ARC draft. GitHub API for repo metadata and READMEs.

**Full reads.** zk-creds (ePrint full version, main body), Privacy Pass PoPETS 2018 (whole paper), WAKU-RLN-RELAY arXiv 2207.00116 (whole 2-page paper), RFC 9576 (whole document).

**Found, not added.** Teranishi, Furukawa, Sako, "k-Times Anonymous Authentication" (ASIACRYPT 2004, DOI 10.1007/978-3-540-30539-2_22): no abstract reachable through OpenAlex or Crossref in this session, so not catalogued. Nguyen and Safavi-Naini "Dynamic k-Times Anonymous Authentication" (2005) and Au, Kapadia, Susilo "BLACR" (2012): seen only as search hits. Frigo and Shelat "Anonymous Credentials from ECDSA" (2026), Mir et al. issuer-hiding multi-authority credentials (CCS 2023), "SoK: Oblivious Pseudorandom Functions" (2022), "Revisiting Keyed-Verification Anonymous Credentials" (2025), Lox (2023), "Completing Policy-based Anonymous Tokens" (2026), "Device-Bound Anonymous Credentials With(out) Trusted Hardware": seen in result lists or citation lists only, not opened. Other x402 papers from arXiv search (2604.11430, 2607.19545, 2603.01179, 2609.00060, 2605.30998) and NostrAgent (2609.22944) were seen as titles only. The Ethereum Foundation zkAPI launch post (1 Oct 2026) and the L402 spec repo were seen in search results but not opened. Rawat et al. "Anonymous Rate Limiting for Duty-Cycled IoT Traffic in Permissionless Messaging Networks" (SSRN 2026) appeared in OpenAlex but was not opened.

**Thin.** (1) Agent-specific work combining anonymous credentials with agent identity is nearly absent in the scholarly indexes; the agent side is vendor posts (Cloudflare), standards drafts and forum designs (Crapis and Buterin), plus 2026 x402 security and measurement preprints. (2) No paper found that evaluates rate-limited credentials under an adversary running many agents per principal (the cloning case). (3) Formal RLN treatments (beyond the Waku paper and the 2019 forum post) and the RLN v2 spec were not opened. (4) Backward citation chasing from zk-creds was done by reading its related-work section, not via the API. A survey on this lane should rerun Semantic Scholar forward citations for zk-creds, Camenisch et al. 2006 and the RLN Waku paper when the rate limit clears.

