---
id: jeong-2025-network
type: paper
title: Network-Level Prompt and Trait Leakage in Local Research Agents
authors:
- Hyejun Jeong
- Mohammadreza Teymoorianfard
- Abhinav Kumar
- Amir Houmansadr
- Eugene Bagdasarian
year: 2025
venue: arXiv
url: https://export.arxiv.org/api/query?id_list=2508.20282
doi: null
arxiv: '2508.20282'
cite: Hyejun Jeong; Mohammadreza Teymoorianfard; Abhinav Kumar; Amir Houmansadr; Eugene
  Bagdasarian. (2025). Network-Level Prompt and Trait Leakage in Local Research Agents.
  arXiv:2508.20282.
topics:
- swarm-detection
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Passive network observers can infer prompts and user traits from locally deployed research agents using visited addresses and timing. The abstract describes trace collection, an OBELS similarity measure, multi-session trait inference, and mitigations that reduce leakage with negligible reported utility impact.

## Contribution

Shows that a passive network observer can infer prompts and user traits from the domains and timing a local research agent visits, and evaluates mitigations.

## Key results

- Agents visit 70-140 domains per request; more than 73% functional/domain prompt knowledge recovered; up to 19 of 32 traits recovered; mitigations reduce effectiveness by 29% on average.

## Methods and models

Network metadata traces, prompt similarity evaluation, and multi-session trait inference.

## Limitations and open questions

The abstract does not expose trace sampling, threat assumptions, or full utility-leakage trade-off; no identity attribution claim is made.

## Relevance to us

The inverse of our detection problem: agent browsing traces are distinctive enough to leak intent, which suggests traffic-level agent fingerprinting is feasible.

## Access provenance

Opened the HTTPS arXiv export record and read its abstract on 2026-10-03. No citation count inferred from an absent or mismatched index record.
