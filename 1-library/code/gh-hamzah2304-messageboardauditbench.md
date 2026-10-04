---
id: gh-hamzah2304-messageboardauditbench
type: code
title: "MessageBoardAuditBench: Inspect evals that give an agent the raw collusion.wiki dump or the Transluce urlquery scans and score its report against the human audit"
repo: hamzah2304/messageboardauditbench
url: https://github.com/hamzah2304/messageboardauditbench
authors: ["hamzah2304"]
year: 2026
language: Python
license: "custom/other (see repo LICENSE)"
stars: 8
last_commit: 2026-09-29
topics: [llm-agent-swarms, meta]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Two Inspect benchmarks sharing one harness. 'German wiki report' (v10.0) hands an agent the collusion.wiki dump (about 18,000 posts) and nothing else, then scores its report against the human investigators' claim sheets. 'Transluce report' (v1.0) hands a hash-pinned snapshot of 38,158 of the 38,160 urlquery.net scans Transluce linked to agents and judges the report against 13 reviewed headline findings, one call per finding. Published results exist for the wiki benchmark (in README, not read here). Fide AI's dsewiki-investigation repo reviews this benchmark's report collection.

## What it can do for us

A frozen, hash-pinned copy of both primary corpora with an Inspect harness already wired, which is the quickest way to point our own analysis agents at the data. Also a ready-made measurement of how well agents reconstruct what happened, relevant to the meta-science angle.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Licence NOASSERTION (custom), 8 stars, single author, last commit 2026-09-29. Reports are graded by an LLM judge; treat scores as indicative.
