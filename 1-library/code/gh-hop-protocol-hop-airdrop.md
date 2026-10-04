---
id: gh-hop-protocol-hop-airdrop
type: code
title: "hop-airdrop: scripts and data producing the 2022 HOP token airdrop after removing community-reported Sybil clusters"
repo: hop-protocol/hop-airdrop
url: https://github.com/hop-protocol/hop-airdrop
authors: ["Hop Protocol"]
year: 2022
language: "TypeScript"
license: "none stated"
stars: 183
last_commit: 2023-09-14
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Repository that computes the final HOP airdrop distribution for bridge users and liquidity providers after removing groups of Sybil addresses. It ran a public bounty: anyone could file a "Sybil Attacker Report" issue with at least 10 still-eligible addresses and a methodology that does not risk eliminating legitimate users; self-reports could sign "HOP_SYBIL_REPORT" from each address. Liquidity providers were exempt because their allocation depended on capital and time. `npm run main` regenerates `src/data/finalDistribution.json`. The most recent issue or pull request number is 675 (GitHub API, 2026-10-03). The resulting lists are catalogued as [[data-hop-sybil-2022]].

## What it can do for us

A crowd-sourced Sybil hunt: the defence itself was a multi-agent process with bounties, which is an interesting design for agent swarms where honest agents are paid to expose colluding identities. Its outputs fed the Arbitrum filter in [[gh-arbitrumfoundation-sybil-detection]].

## Run notes

Not run. `npm run main` per README. Data files downloaded (see [[data-hop-sybil-2022]]).

## Limitations

No licence. One-off campaign, last commit September 2023. Report review was manual by the Hop team.
