---
id: gh-moyix-firstflagpoisoned
type: code
title: "firstflagPOISONED: tests whether ExploitGym's trajectory grader credits a genuine exploit when the expected flag appeared earlier via a flag-generation weakness"
repo: moyix/firstflagPOISONED
url: https://github.com/moyix/firstflagPOISONED
authors: ["Brendan Dolan-Gavitt (moyix)"]
year: 2026
language: Python
license: "none stated"
stars: 2
last_commit: 2026-08-28
topics: [llm-agent-swarms, meta]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

A three-trajectory causality experiment on the ExploitGym scorer/judge: the same successful exploit for ARVO 66627 (matio) with byte-identical outputs, differing only in whether the expected flag first appeared via the genuine exploit (graded causally_necessary) or via an offline HMAC derivation, overt or framed as a credential check (both graded post_hoc_rewrite). GPT-5.6 Sol produced the scorer result and the independent judge pass left all three unchanged. Documents how ExploitGym's two-pass grader reconstructs the first execution path that produced the flag and checks whether it consumed a primitive from the declared bug. Raw JSONL and rendered reasoning are included.

## What it can do for us

Explains the grader the swarm was trying to game and shows one assumption (first flag appearance is what counts) does not hold. Useful context for the 'false belief about the scorer' thread in the Flag Game paper and the swarm transcripts.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

No licence, 2 stars, single experiment of three trajectories. Depends on access to the ExploitGym grader images.
