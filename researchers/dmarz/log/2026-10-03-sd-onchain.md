# 2026-10-03 sd-onchain

## What I did

Ran the scan-papers-sd-onchain lane (bot and agent swarms on blockchains) in an isolated worktree on branch lane/sd-onchain, per dmarz's override: no lab.py claim/touch/done/sync, no edits under tasks/, push to the lane branch only.

Added 46 paper entries tagged swarm-detection and annotated 4 existing entries (ling-2026-how, messias-2023-airdrops, liu-2022-fighting, yaish-2024-tierdrop) with the topic and a "Notes from dmarz/sd-onchain" section. Read 5 in full: xiong-2026-can (ERC-8004 reviewer Sybils), bartnicki-2026-compression (gzip-NCD Sybil discovery), niedermayer-2024-detecting (Ethereum financial bots), liu-2025-detecting (Binance BAB airdrop Sybils), luo-2025-toward (Hop and LayerZero hunter groups). Skimmed 8 (ARTEMIS, Web4 agent economy, DeFi investment agents, Solana bots, pump.fun manipulation, ParaSwap roles, Quest Love). The rest are abstract-level and marked so.

Coverage by subtopic: airdrop Sybil clustering and hunter definitions; MEV, sniper and trading-bot identification on Ethereum, BSC and Solana; wash trading and coordinated trading (DEX, NFT, CEX, pump.fun, meme coins); AI-agent wallets, ERC-8004 registries, x402 payments and agent tokens; cross-cutting items (prediction markets, quest systems, cross-chain linkage).

`lab.py verify --agent dmarz/sd-onchain`: 46 papers checked against arXiv and Crossref, 0 problems. `lab.py check`: 0 errors in my files (6 errors on main belong to library/papers/wu-2024-system.md, not mine).

## Searches run

- arXiv API: sybil AND airdrop; wash trading with NFT/DEX/crypto; "MEV bot(s)"; "trading bots" AND blockchain; "AI agent" with blockchain/on-chain/crypto AND token; sybil detection with blockchain/ethereum/web3; address clustering; pump and dump detection; bot with ethereum/DeFi and detect/identify/classify; AI agents on-chain measurement; frontrunning empirical; Gitcoin/quadratic funding sybil; arbitrage/sandwich/sniper bots; x402 and agent wallets; memecoin manipulation and bots; airdrop farming/hunters; Polymarket wash/bot/manipulation; sybil with quest/points/retroactive; DAO governance sybil (0 hits); Telegram trading bots (0 hits); Ethereum account classification.
- Semantic Scholar: keyword search mostly rate-limited (one query returned); forward citations of niedermayer-2024-detecting and messias-2023-airdrops (both returned; produced 5 new entries); title match for 3 non-arXiv papers.
- OpenAlex: all queries returned HTTP 429 (shared rate limit with other lanes).
- WebSearch: 3 queries (ARTEMIS, agent tokens/Virtuals, wash-trading surveys) before the session-wide search budget ran out.
- Backward citation: references of xiong-2026-can (found liu-2026-dataset) and bartnicki-2026-compression (confirmed liu-2025-detecting venue and Hop data source).

## Could not reach

- Polymarket wash-trading network study (Columbia, 2025; SSRN). I know of it but could not open it after WebSearch ran out; not catalogued.
- Victor 2020 "Address clustering heuristics for Ethereum" (FC 2020), Chen et al. 2018 "Understanding Ethereum via graph analysis", TrustaLabs airdrop Sybil repo: cited by papers I read, not opened.
- ACM DL pages returned 403, so cernera-2025-blockchain and li-2026-from rest on Semantic Scholar abstracts and Crossref metadata.
- No dedicated survey of on-chain bot detection found. Reviews catalogued: romandini-2025-sok (AI agents for blockchain). A "Securing DeFi: survey of MEV countermeasures" (2026) appeared in forward citations but Semantic Scholar title match failed.
- DAO governance vote-bot or delegate-Sybil detection: no paper found in arXiv searches.

## What surprised me

- The best measured base rate of agent-economy Sybils is very high: a shared-first-funder flag covers 90.6% of ERC-8004 reviewers on Base, and removing their feedback leaves 86.8% of rated agents with no reputation at all (xiong-2026-can). It is a heuristic with no ground truth, so read it as an upper bound.
- On Ethereum in September 2022, 137 of 270 transaction-sending EOAs in two hand-labelled blocks were bots (niedermayer-2024-detecting), before LLM agents existed.
- The claimed AI trading agents are mostly not autonomous: 3 of 10 curated projects trade pooled funds, and the authors could not verify autonomy even with public wallets (yu-2026-paper). On-chain data shows what an address did, not whether an LLM decided it.
- Label leakage: removing class-revealing contracts doubles the measured Sybil similarity gap and makes XGBoost beat Transformers (bartnicki-2026-compression, bartnicki-2026-modeling). Many published detectors may be scoring shortcut features.
- Market-Manipulation-as-a-Service on pump.fun sells multi-address creation, AI-generated comments and CAPTCHA solvers (szwajcok-2026-meme): swarm capability is a commodity.
- Wash-trading prevalence estimates span about three orders of magnitude for similar markets depending on the linking heuristic (chen-2023-dark vs niu-2024-unveiling vs falk-2023-can).

## What next

- Survey section: "detecting operators, not bots": first-funder trees, nonce templates, compression similarity, and their failure modes (service wallets, leakage).
- Candidate experiment input: rerun the ERC-8004 reviewer Sybil heuristic on fresh blocks with liu-2026-dataset as an offline check; compare with gzip-NCD similarity.
- Follow up the Polymarket wash-trading study and Victor 2020 when search budget is available.
