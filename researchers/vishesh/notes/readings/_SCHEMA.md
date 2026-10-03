# Per-source note schema (one file per reading, filename = slug.md)

---
slug: <kebab>
title: <exact title as published>
authors: <from the source itself>
org_or_venue: <arXiv / blog / org>
date: <YYYY-MM-DD as published; say "undated" if absent>
urls_loaded:
  - <exact URL actually fetched>
  - <another URL if applicable>
library_ids:
  - <canonical library id>
status: found | partial | not-found
fetched: 2026-10-03
---

## What it is (2-4 sentences)
## Method / setup (what they actually did; models, N, tasks, baselines)
## Key results (numbers with units; mark each "measured" or "claimed")
## Limitations the source admits + ones you noticed
## Relevance to the hackathon shortlist
- Collective Sensing (local/global/no comms, partial obs, known truth):
- Quorum (independent evidence vs repeated copies; false commit vs delay):
- Telephone (atomic claims through retellings; lost evidence, inflated certainty):
## Quotable (<=15 words each, verbatim, with location)
## Not found / could not verify (queries tried, what was ambiguous)

## Validation and provenance

Use YAML lists for multiple URLs and library identifiers. Duplicate keys silently discard earlier values in common parsers. Keep dates and version descriptions explicit; do not infer read depth from a successful download. Source-specific access failures and version mismatches belong in the body. Published measurements should name the table or section and distinguish the source’s report from independent replication.
