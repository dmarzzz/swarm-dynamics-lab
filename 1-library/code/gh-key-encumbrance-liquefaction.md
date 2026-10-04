---
id: gh-key-encumbrance-liquefaction
type: code
title: "key-encumbrance/liquefaction: smart-contract key-encumbered wallet for privately liquefying blockchain assets"
repo: key-encumbrance/liquefaction
url: https://github.com/key-encumbrance/liquefaction
authors: [key-encumbrance GitHub organisation (Liquefaction paper authors, Cornell Tech / IC3)]
year: 2024
language: TypeScript
license: MIT
stars: 38
last_commit: 2026-04-28
topics: [sybil-resistance]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [austgen-2024-liquefaction]
---

## Summary

Reference implementation of the Liquefaction wallet from [[austgen-2024-liquefaction]]: Solidity contracts that run on Oasis Sapphire (a TEE-based EVM chain), generate an encumbered key, and grant time-bounded signing rights through policy contracts, with Hardhat tests in TypeScript. The README lists Dark DAO vote selling, locked-token trading, dusting-attack mitigation, private DAO treasuries, token-gated ticket lending and soulbound-token account sales as supported applications. Repository created 2024-12-02; stars and last push read from the GitHub API on 2026-10-03.

## What it can do for us

A concrete, testable artefact for the identity-rental side of Sybil analysis: it shows the policy contracts an adversary would use to lease signing rights over many agent or member keys with exclusive, time-bounded control. Useful as a red-team baseline when evaluating any agent-identity scheme that assumes one key equals one controller.

## Run notes

Not run. README steps: `npm i`, start `ghcr.io/oasisprotocol/sapphire-localnet` in Docker (x86_64 image, `--platform linux/x86_64` on ARM Macs), `npx hardhat compile`, optional Kurtosis Ethereum devnet for cross-chain inclusion proofs, then `npx hardhat test --network dev`.

## Limitations

Academic prototype, unaudited. The README states three mainnet caveats: pre-signing attacks are trivial because encumbrance history is not exposed to new policies (mitigated by enrolling accounts "from birth" through an access manager), the Ethereum transaction policy depends on a trusted block-hash oracle, and Sapphire does not hide storage access patterns, so code paths can leak.
