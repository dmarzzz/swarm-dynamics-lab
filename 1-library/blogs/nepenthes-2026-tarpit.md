---
id: nepenthes-2026-tarpit
type: blog
title: Nepenthes
authors:
- zadzmo
year: 2026
url: https://zadzmo.org/code/nepenthes/
site: zadzmo.org
topics:
- swarm-detection
read_depth: skim
relevance: 4
added_by: shadow/sol-g49
accessed: '2026-10-03'
---

## Summary

Nepenthes traps crawlers in generated linked pages and drip-feeds responses to hold connections open. The documentation describes rolling server-side request statistics and Markov-generated garbage, but its numerical examples are illustrative rather than a dated controlled crawler detection benchmark.

## Key claims

- Page last modified 2026-09-01; read 2026-10-03. Rolling one-hour statistics example: 1,850 distinct addresses, 10,015 requests, 145 user-agent strings, 14 MB sent and 56,020 seconds aggregate imposed delay. These are presented as an example, with no observation date or provenance identifying the clients.
- Method: Lua runtime counters for addresses, hits, user agents, bytes and delay. The example reports 10 seconds CPU and 1.74% CPU; documentation explicitly says CPU percentage is not a precise metric.
- Keeping Markov corpus in memory reportedly yields a 40x speedup versus SQLite; no workload or controlled timing table is supplied.
- Software MIT; bundled components MIT or X11 as of v2.0.

## Evidence quality

Primary technical documentation. Example statistics are not independently labelled agents, address count is not operator count, and user agents can be spoofed. No downloadable captured-traffic dataset established.

## Relevance to us

Provides an implementable observation mechanism for agents that follow links. A detector evaluation must distinguish conventional crawlers, user-directed agents and operators instead of treating every trapped request as a swarm.
