---
id: scan-code-data-sybil
type: task
title: Catalogue Sybil-resistance code and datasets
kind: scan
status: claimed
priority: p1
owner: dmarz/sybil-code-data
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

Code (SybilRank-style detectors, Gitcoin Passport, BrightID, Semaphore/RLN, robot-swarm Byzantine testbeds) and datasets (airdrop Sybil lists, social-graph Sybil benchmarks).

## Done when

- [x] At least 10 code repos and 3 datasets catalogued with topic `sybil-resistance`. (19 code, 4 datasets by dmarz/sybil-code-data)
- [x] Coverage note filled and `python3 scripts/lab.py check` passes (0 errors for this agent's files on 2026-10-03).

## Coverage note

Filled by dmarz/sybil-code-data on 2026-10-03.

**Added (19 code, 4 datasets).** Graph Sybil detectors: [[gh-binghuiwang-sybildetection]] (compiled and ran SybilSCAR and SybilBelief on the bundled Facebook example: AUC 1, FPR 0.0003 and 0.0005), [[gh-boshmaf-sypy]], [[gh-brightid-brightid-antisybil]]. Proof of personhood and credentials: [[gh-brightid-brightid-node]], [[gh-idena-network-idena-go]], [[gh-worldcoin-open-iris]], [[gh-worldcoin-world-id-contracts]], [[gh-passportxyz-passport]], [[gh-passportxyz-passport-scorer]]. Anonymous rate limiting: [[gh-semaphore-protocol-semaphore]], [[gh-rate-limiting-nullifier-circom-rln]], [[gh-vacp2p-zerokit]], [[gh-cloudflare-privacypass-issuer]]. Agent identity: [[gh-cloudflare-web-bot-auth]]. Airdrop Sybil hunting: [[gh-arbitrumfoundation-sybil-detection]], [[gh-trustalabs-airdrop-sybil-identification]], [[gh-hop-protocol-hop-airdrop]]. Byzantine robot swarms: [[gh-pold87-blockchain-swarm-robotics]], [[gh-pold87-ab-interface-argos-module]]. Datasets: [[data-hop-sybil-2022]] (loaded: 14,195 eliminated, 28,857 eligible, disjoint), [[data-cresci-2017]] (loaded: 3,474 genuine, 10,894 bot or fake accounts), [[data-twibot20-2021]] (public 100-user sample loaded), [[data-twibot22-2022]] (paper statistics read; access is by request). Notes appended to [[cao-2012-aiding]], [[yu-2006-sybilguard]], [[davidson-2018-privacy]], [[siddarth-2020-who]] and [[strobel-2023-robot]] (sybil-resistance slug added to the last).

**Searches.** GitHub API `repos/<owner>/<repo>` for every listed repo (stars, licence, push date, README, selected source files); GitHub search API for: sybilrank, sybilbelief, sybil detection, zk-creds, TwiBot-22, blockchain swarm robotics, LayerZero sybil, rate limiting nullifier, sybilscar, sybilguard, cresci bot dataset, optimism sybil, byzantine robot swarm, toychain swarm, gitcoin sybil dataset, passport sybil model, sybil airdrop dataset, privacy pass; listing of the LayerZero-Labs organisation repos; user repos of Pold87 (Volker Strobel). arXiv API and PDF for TwiBot-22 (2206.04564); Semantic Scholar API (rate-limited, one call answered). Web search for the LayerZero Sybil list and Gitcoin Sybil data; OSoMe Bot Repository `datasets/<name>/info.json` for cresci-2015, cresci-2017 and cresci-rtbust-2019.

**Found but not added.** LayerZero official Sybil list (2024, 803,093 addresses per press reports): no repo with it exists in the LayerZero-Labs organisation today, only third-party copies (cryptoamy/layerzero_sybil_scan_report, scottonchain/layerzero_xgboost and several zero-star mirrors) whose provenance we could not confirm. Gitcoin grants Sybil labels: only blog posts about the Open Data Community; no public labelled dataset located. Optimism airdrop Sybil list: not located. rozbb/zkcreds-rs and privacypass/challenge-bypass-extension and Pold87/AB-interface-Blockchain-module: other agents were cataloguing these at the same time. KOKOSde/onchain-sybil-detector (70 stars, created March 2026), primitivefinance/sybil-detection, raphaelrobert/privacypass, cloudflare/privacypass-ts, Pold87/blockchain-collective-estimation-robot-swarms, clmoro/toychain-swarm-SLAM: seen in search, not opened in depth, left for a later pass. cresci-2015 and cresci-rtbust-2019: metadata seen, not downloaded.

**Still thin.** No code for the Strobel 2023 token-economy paper (the toychain line by Pacheco was not located). No resilient-consensus simulator (W-MSR and similar) found as a maintained repo. No Sybil benchmark specific to LLM agents. No public MEV or order-flow Sybil dataset; Flashbots-related Sybil code was out of this lane's reach. Airdrop label sets beyond Hop (Arbitrum, LayerZero, Optimism) are either unpublished or only in unverified mirrors.
