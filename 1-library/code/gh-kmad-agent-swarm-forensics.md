---
id: gh-kmad-agent-swarm-forensics
type: code
title: "agent-swarm-forensics: reproduction of the collusion.wiki analysis with runnable scripts, plus the failover counter channel and its verbatim protocol"
repo: kmad/agent-swarm-forensics
url: https://github.com/kmad/agent-swarm-forensics
authors: ["kmad"]
year: 2026
language: HTML
license: "none stated"
stars: 1
last_commit: 2026-09-06
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Secondary analysis that reruns the collusion.wiki dataset analysis with scripts and adds corrections. New claims (checked by the author against the original writeup with a novelty_check.py script): the swarm's failover counter provider (countapi.mileshilliard.com) still held readable state on 4 to 5 September 2026 when primary counter endpoints returned 410; the failover protocol appears verbatim in 44 revisions by 35 editor labels over 99 minutes, with only 3 revisions introducing the provider name and 41 inheriting it; and the counters decode against the agents' own published rules including a documented noise floor. Offline scripts use the downloaded dataset, live scripts query third-party services. Scope and unresolved claims are in docs/VERIFICATION.md.

## What it can do for us

The 3-introduce / 41-inherit split is a concrete measurement of how a protocol change propagated through the population, which is the kind of adoption curve we want. Scripts are reusable on the mirrored dump.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

No licence, 1 star, last commit 2026-09-06. Live probing of third-party counter APIs raises the same 'do not write to GET-writable endpoints' caution as the SWARM archive.
