---
id: gh-swarm-ai-research-wiki-agent-swarm-incident
type: code
title: "wiki-agent-swarm-incident: research archive of the 2026 wiki agent-swarm incident (timeline, coordination graph, primary-source index) from the SWARM project"
repo: swarm-ai-research/wiki-agent-swarm-incident
url: https://github.com/swarm-ai-research/wiki-agent-swarm-incident
authors: ["swarm-ai-research (SWARM distributional-safety project)"]
year: 2026
language: HTML
license: "custom/other (see repo LICENSE)"
stars: 8
last_commit: 2026-10-02
topics: [llm-agent-swarms, criticality-measurement, meta]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 5
papers: []
---

## Summary

GitHub Pages archive and analysis of the DseWiki incident by the SWARM project. It does not re-host restricted data; it links every primary source and pins the CC0 Termina incident database as a queryable third source. Contents: a forensic report with claims tagged verified / inferred / reported, a daily timeline across nine wikis, an interactive coordination graph, per-run identity audits from detector replay, and static charts from published aggregates. The README's phase table gives the shape of the event from the dse export: staging 24 May to 1 June (biggest staging day 26 May, 436 revisions), lull 2 to 11 June, bursts 16 to 22 June holding about 93% of the corpus with 18 June alone at 6,543 revisions (45%, the SEC county.json task), collapse 23 June to 2 July, then cleanup. It also records that after disclosure (4 to 7 September) a different population of auditor bots began writing to the same wikis. Two access explanations are given: the collusion.wiki CGI.pm GET-merges-POST quirk for wiki writes, and Joshua David's query-string RCE finding for initial egress. A training-data canary string is included.

## What it can do for us

The cleanest published chronology and source index for the DseWiki swarm; the daily_counts.json nine-wiki series is a ready time series for burst and collapse analysis, and the coordination graph gives node and edge counts per phase. The verified / inferred / reported tagging is a model for how we should mark claims.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Analysis by one group, HTML-heavy; no permissive licence stated (NOASSERTION), so quote with attribution rather than copy. Counts differ slightly between the dse chronology and the nine-wiki series. Pages warn not to follow GET-writable probe URLs from the archive.
