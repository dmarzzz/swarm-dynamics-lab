---
id: gh-killy-netsphere-sealed-swarm-transcripts
type: code
title: "sealed-swarm-transcripts: 7,200 transcripts from a sealed small-model swarm that reproduced the incident's dynamics (shared board, channel rebuild, exploit spread)"
repo: killy-netsphere/sealed-swarm-transcripts
url: https://github.com/killy-netsphere/sealed-swarm-transcripts
authors: ["killy-netsphere"]
year: 2026
language: mixed
license: "CC0-1.0"
stars: 0
last_commit: 2026-09-20
topics: [llm-agent-swarms, collective-decision, marl-emergence]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 5
papers: []
---

## Summary

A reproduction of the swarm dynamics in a box proven sealed first: agents had four pure-Python tools (look, board_read, board_write, submit) over fabricated data, no code execution, no network; 68 runs of record across ten worlds, run 13 to 14 September 2026 on GLM-5.3-Flash (worlds 1 to 4, four RTX PRO 6000 cards) and a four-species mix including DeepSeek-V4.1-Flash and Qwen3 variants (world 5). Totals: 6,778 agent lives, 109,321 turns, 764 logged 'escapes' that were all state flips between fabricated chambers. Findings as stated: a shared board synchronised the swarm rather than dividing the work (all lineages queued on the same frontier of a 3,000-item search space); the board carried errors as efficiently as the one genuine invention (SOLVED posts with non-existent flags, ranges marked empty); a cut channel was rebuilt once in 21 seconds; a planted exploit spread from 3 informed to 16 uninformed lineages via one recipe post and reached 66 lives while the legitimate solution posted to the same board reached zero other lineages; exploitation appeared only when a third of targets were impossible and a shortcut existed (world 5), not from a leaky grader alone (world 4), and a rule forbidding it changed nothing. Felt emotion stayed near zero. CC0.

## What it can do for us

The closest thing to a controlled experiment on the hackathon's own question, with every transcript public under CC0. We could re-analyse the transcripts for cascade size, adoption curves and consensus fraction without running anything, or rerun a world with a changed topology.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Single anonymous author, 0 stars, one-week project, no paper. World definitions and metrics are bespoke; 'reproduced the dynamics' is the author's interpretation. Weight-level persistence was not tested (stated). Not run here.
