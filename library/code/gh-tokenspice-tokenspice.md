---
id: gh-tokenspice-tokenspice
type: code
title: "TokenSPICE: agent-based token-ecosystem simulator with the EVM in the loop"
repo: tokenspice/tokenspice
url: https://github.com/tokenspice/tokenspice
authors: ["Trent McConaghy", "Ocean Protocol contributors"]
year: 2020
language: "Solidity/Python"
license: "MIT"
stars: 323
last_commit: 2023-11-14
topics: [meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Simulates: tokenised ecosystems where each agent is a Python class with an Ethereum wallet, wired together in a "netlist" and stepped in a loop; agents can act through real Solidity contracts on a local Ganache chain. Interaction model: synchronous loop over agents; contracts executed on an EVM. Scale: not stated. LLM-driven: no. Adversarial hooks: none native; an attacker is another agent class. Weight: Python 3.8+, solc, Ganache and Node 16; moderate. The README says it has not been maintained since mid-2023.

## What it can do for us

The idea of running agents against real contract bytecode (EVM in the loop) is the right one for MEV or order-flow agents; the codebase itself is stale.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Unmaintained since mid-2023 by its own README; pinned to Node 16 and Ganache. For EVM-in-the-loop today one would use anvil or a forked node instead.
