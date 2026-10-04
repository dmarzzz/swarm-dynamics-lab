---
id: gh-passportxyz-passport
type: code
title: "Passport (formerly Gitcoin Passport): verifiable-credential \"stamp\" wallet used as Sybil defence for Gitcoin Grants and other airdrops"
repo: passportxyz/passport
url: https://github.com/passportxyz/passport
authors: ["Passport XYZ (formerly Gitcoin)"]
year: 2022
language: "TypeScript"
license: "AGPL-3.0 (LICENSE file; API reports NOASSERTION)"
stars: 1223
last_commit: 2026-09-27
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Monorepo for the Passport identity app, created under the gitcoinco organisation in March 2022 and now under passportxyz. Users collect verifiable credentials ("stamps") from providers; the `platforms/src` folder lists about 40, including BrightID, Idena, Civic, Coinbase, Binance, ENS, GitHub, Google, LinkedIn, Discord, POAP, Snapshot, Lens, GTC staking, Holonym HumanID, ZKEmail, biometrics and a TrustaLabs score. The `iam` service issues credentials after checking each provider, the `app` is the web frontend, and credentials are stored in a Postgres database run by Passport XYZ, on Ceramic, and as on-chain attestations (EAS) across about a dozen networks. The README frames identity as intersectional and social, citing RadicalxChange.

## What it can do for us

The main production example of aggregating many weak, independently costly identity signals into a Sybil-resistance score, which is the closest analogue to how an agent swarm might admit agents: each stamp is a separate cost an attacker must pay per identity. It also shows the stamp design composing other systems we catalogue: [[gh-brightid-brightid-node]], [[gh-idena-network-idena-go]] and [[gh-trustalabs-airdrop-sybil-identification]].

## Run notes

Not run. Quick start per README: Node 20, Yarn, `npm install --global lerna && yarn install`, copy `.env` files, `yarn start`, and a local instance of [[gh-passportxyz-passport-scorer]].

## Limitations

Depends on a centralised Postgres database and Scorer API run by Passport XYZ. AGPL-3.0. Each stamp's Sybil cost is only as high as the upstream provider's account-creation cost, and those providers (Google, Discord, X) are exactly what bot farms already mass-produce.
