---
id: gh-brunomazorra-llms-sybils
type: code
title: 'LLMs-Sybils (fnp-agents): do LLM agents discover identity multiplicity to exploit non-false-name-proof mechanisms'
repo: BrunoMazorra/LLMs-Sybils
url: https://github.com/BrunoMazorra/LLMs-Sybils
authors:
- 'BrunoMazorra (GitHub account)'
year: 2026
language: Python
license: none stated
stars: 0
last_commit: 2026-07-13
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: skim
relevance: 5
papers: []
---

## Summary

An experimental harness in the GitHub account BrunoMazorra, presumably the author of [[mazorra-2023-cost]] (not verified; repository created 2026-07-07, last push 2026-07-13) that asks whether LLM agents, unprompted, discover and use extra identities to exploit a mechanism that is not false-name-proof, starting with VCG. Modes: create (manufacture a second identity at cost c), acquire (negotiate to buy an identity from a controlled LLM seller) and repeated_create (registry plus repeated auctions with feedback). A v3 protocol adds paired games: seller shill bidding (second price vs first price control), quadratic funding (identity-sensitive matching vs principal consolidation), quadratic voting (per-identity vs principal-level costs) and equal-share vs stake-proportional rewards. The README describes an EC'26-style paper PDF in output/pdf.

## What it can do for us

It is a ready-made testbed for the central swarm question in this lane: will LLM agents, given an identity affordance and a vulnerable mechanism, clone themselves, and do they restrain when cloning is unprofitable. Each game enumerates the oracle best action per identity count and calibrates identity cost around the exact profitability threshold, so agent behaviour can be scored as regret against the oracle. It operationalises [[mazorra-2023-cost]] and the vulnerable mechanisms in [[yokoo-2004-effect]] and [[buterin-2019-flexible]].

## Run notes

Not run. Read the README and the top-level file list (agents, env, runner, sybil_games, prompts, analysis, tests, METHODOLOGY_V2.md, SYBIL_GAMES_METHODOLOGY.md, PREREG.md). The README states 182/182 tests pass and that runs need LLM API access.

## Limitations

No licence file, zero stars, a single author and very recent. The README itself notes that the v3 prompt exposes the identity affordance explicitly, so it measures execution and restraint rather than unprompted discovery, and that the cross-game disclosure experiment it specifies has not been implemented or run. An archived v2 pilot is not bitwise reproducible. I did not read the paper PDF, so no results are recorded here.
