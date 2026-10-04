---
id: gh-yazandabain-swarmtrace
type: code
title: "SwarmTrace: temporal audit of resource targeting in the DseWiki incident (24-hour degree ranking misses all 18 recent multi-writer resources)"
repo: yazandabain/swarmtrace
url: https://github.com/yazandabain/swarmtrace
authors: ["yazandabain (Apart Research AI Incident Response Sprint 2026)"]
year: 2026
language: Python
license: "custom/other (see repo LICENSE)"
stars: 1
last_commit: 2026-09-30
topics: [llm-agent-swarms, criticality-measurement, sync-consensus]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Replays archived DseWiki revisions and deletion events, reconstructs resource lifecycles, builds temporal label-resource graphs and compares degree-based resource targeting against uniform withdrawal. Main finding at the frozen evaluation time: the six-hour graph has 18 active multi-writer resources, the top 18 resources by 24-hour degree contain none of them, and withdrawing those historical hubs cuts the older graph's largest label component from 782 to 545 while leaving the recent graph unchanged. Across 151 non-empty six-hour snapshots, older-degree targeting produced 20 complete misses against 29.0 expected under uniform withdrawal, so the author cautions against over-reading the headline miss. Built for the Apart Research sprint, September 2026. Not to be confused with swarmtraces.org (Palisade/Parse).

## What it can do for us

A worked temporal-network analysis on the exact corpus, with code for building time-windowed label-resource graphs. The 'intervention reach depends on window' result is a candidate measurement for our write-up.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Licence NOASSERTION, 1 star, sprint project. Numbers are from the README and not re-derived here.
