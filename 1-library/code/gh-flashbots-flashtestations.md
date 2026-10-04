---
id: gh-flashbots-flashtestations
type: code
title: "flashbots/flashtestations: on-chain registry for TDX attestations and attested block-builder policy"
repo: flashbots/flashtestations
url: https://github.com/flashbots/flashtestations
authors: [Flashbots]
year: 2025
language: Solidity
license: none declared at repo level (GitHub API reports no licence)
stars: 4
last_commit: 2026-01-30
topics: [sybil-resistance]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Solidity contracts (Foundry) that let "any TDX device" register on-chain and later prove its outputs; the first use case is proving that Unichain L2 blocks were built under fair ordering rules. `FlashtestationRegistry` verifies a TDX v4 quote through Automata's on-chain DCAP library, requires the caller to be the TEE-controlled address embedded in reportData[0:20], checks that reportData[20:52] equals the hash of extended registration data, and stores the parsed report and raw quote keyed by that address. `BlockBuilderPolicy` computes a WorkloadId from the stored measurement registers, keeps a governance-approved list of WorkloadIds tied to source commits, and verifies block-builder signatures against it. Anyone can call `invalidateAttestation` once Intel's DCAP collateral no longer validates a stored quote. Year is approximate (first release not checked); stars and last push from the GitHub API on 2026-10-03.

## What it can do for us

A deployed, minimal pattern for "attest once, then sign cheaply" identity: an address is admitted if a valid quote binds it to an approved code measurement. It is directly reusable for an agent registry where admission depends on running approved agent code.

## Run notes

Not run. README deploy flow: `forge script` for DeployAll, FlashtestationRegistry and BlockBuilderPolicy on Unichain Sepolia (chain 1301), `FetchRemoteQuote` to obtain a TDX quote for a TEE-controlled address, `RegisterTEEScript` (with `--skip-simulation` because forge lacks the precompiles), then compute and add a WorkloadId.

## Limitations

From reading `src/FlashtestationRegistry.sol`: the registry is keyed by TEE address, and the only duplicate check rejects re-registering the same address with the same quote hash; I found no field or check tying registrations to a physical platform (the contract does not reference the PPID), so one TDX machine could register many addresses with separate quotes. That is an inference from the code, not a documented property. Admission of workloads is permissioned by the policy owner. Security inherits DCAP: quotes forged with an extracted PCK ([[chuang-2025-teefail]]) would verify. The README notes an earlier bit-masking bug in the policy's xfam/tdattributes handling that the upgrade removed.

## Relevance to us

Flashtestations binds identity to code measurement plus a TEE-held key, with a permissioned list of acceptable code. As a Sybil bound it limits which software may act, not how many actors there are; the count bound has to come from elsewhere, such as the operator allowlists BuilderNet uses ([[gh-flashbots-builder-hub]], [[collective-2025-why]]) or a per-chassis registry like the AK registry proposed in [[rezabek-2025-proof]]. Compare [[zhou-2025-dstack]], where identity is a code hash shared by all replicas, and [[miller-2024-sirrah]], the earlier attest-once registry.
