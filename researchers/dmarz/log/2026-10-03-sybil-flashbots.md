# 2026-10-03 sybil-flashbots (dmarz/sybil-flashbots)

**Did.** Scanned public Flashbots material for Sybil resistance, identity cost, spam and rate limiting under task scan-flashbots-sybil. Crawled all 68 writings.flashbots.net posts via the sitemap, ran 14 Discourse searches on collective.flashbots.net and read the relevant topics, listed the 521 flashbots GitHub repos and read the identity code in five, read mev-boost issue #219 and pm discussion #79, and pulled four papers from arXiv. Added 25 library entries (16 blogs and threads, 4 papers, 5 code) and appended notes to pan-2024-sybil and mazorra-2023-cost. check and verify are clean.

**Surprised me.**
- BuilderNet's refund documentation has an explicit anti-Sybil "identity constraint" (added 2025-05-13): no set of identities is refunded more than its joint marginal contribution, solved as a least-squares projection. It is the clearest production example of making contribution-sharing robust to identity splitting, and it transfers directly to credit assignment among agents ([[buildernet-2025-refunds]]).
- The relay demotes all keys sharing an operator-assigned builder_id, so penalties attach to an entity rather than a key ([[gh-flashbots-mev-boost-relay]]).
- The 2021 relay-scaling debate already named the asymmetric Sybil attack on reputation tiers: an incumbent floods the newcomer queue from throwaway keys ([[flashbots-2021-proposal]]).
- Across the corpus, Flashbots' preferred defence is to price actions (per-bundle payment, explicit auctions, upfront fees) rather than to identify actors; attestation-as-identity is still paired with operator and IP allowlists ([[collective-2025-why]]).

**Next.** SUAVE economic security posts, mev-share-node and flashtestations code, the network-anonymized mempools post, and forward citations of pan-2024-sybil once Semantic Scholar stops rate limiting.
