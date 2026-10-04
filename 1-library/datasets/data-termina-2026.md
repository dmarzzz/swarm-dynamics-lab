---
id: data-termina-2026
type: dataset
title: Termina incident database snapshot, schema v9
authors:
- SWARM (swarm-ai-research)
- Termina
year: 2026
url: https://github.com/swarm-ai-research/wiki-agent-swarm-incident/blob/main/data/termina/README.md
license: CC0-1.0 for Termina database tables; original archive analysis CC-BY-4.0;
  cited third-party logs retain separate terms
size: 'Pinned README: incidents.sqlite 50,282,496 bytes, schema v9, generated 2026-09-08T14:10:58.029664541Z'
format: SQLite via Git LFS plus schema/manifest JSON and convenience venue/venue_link
  JSONL
topics:
- swarm-detection
- llm-agent-swarms
- meta
read_depth: ran
relevance: 5
papers: []
added_by: shadow/sol-g49
accessed: '2026-10-03'
---

## Summary

The wiki-agent-swarm-incident archive pins a structured secondary incident synthesis from Termina, alongside external primary wiki logs and reconstruction. Claim status and evidence lineage are explicit, so reported/inferred/verified/contradicted rows must not be flattened into binary ground truth.

## Access

Primary snapshot README and scoped LICENSE opened 2026-10-03. Public data path:

https://media.githubusercontent.com/media/swarm-ai-research/wiki-agent-swarm-incident/main/data/termina/incidents.sqlite

Ordinary raw.githubusercontent returns a 133-byte LFS pointer, not the 50,282,496-byte database. Published SHA-256: 80bb262a52008bd9e29c4d99d17aac542cfce23d72f3bd5b3f0208414632e69e. Downloaded and loaded read-only 2026-10-03: exact 50,282,496 bytes and published SHA-256 verified, PRAGMA integrity_check returned ok, 23 tables and 6 rows in incident. No registration. Loader: download the media URL with urllib.request, then sqlite3.connect('file:/path/incidents.sqlite?mode=ro', uri=True) and SELECT count(*) FROM incident. Entire database is secondary incident synthesis, not six primary transcript dumps.

CC0 applies to the database author's tables, not any embedded/cited third-party evidence. The archive's own analysis is CC-BY-4.0; collusion.wiki and JoshuaDavid logs are not blanket-licensed by this repo. Nine tarballs mentioned in a recovered curated-bundle manifest are inventory only and are explicitly not held by this archive.

Separately parsed data/daily_counts.json (7,485 bytes) successfully; it is aggregate secondary analysis, not full message transcripts and its licence must not be conflated with Termina CC0.

## Relevance to us

Queryable structured incident lineage, with status-aware sampling. Evaluate documented swarms against independent controls; do not treat scanner inferences as verified agent membership. Companion code entry [[gh-swarm-ai-research-wiki-agent-swarm-incident]].
