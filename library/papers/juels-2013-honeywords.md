---
id: juels-2013-honeywords
type: paper
title: Honeywords
authors:
- Ari Juels
- Ronald L. Rivest
year: 2013
venue: Proceedings of the 2013 ACM SIGSAC conference on Computer & communications
  security - CCS '13
url: https://dspace.mit.edu/handle/1721.1/90627
doi: 10.1145/2508859.2516671
arxiv: null
cite: Ari Juels; Ronald L. Rivest. (2013). Honeywords. Proceedings of the 2013 ACM
  SIGSAC conference on Computer & communications security - CCS '13, 145-160. https://doi.org/10.1145/2508859.2516671
topics:
- swarm-detection
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Honeywords stores decoy password hashes alongside the real password for each account. A stolen hash database therefore creates uncertainty about which cracked value is valid; an auxiliary honeychecker detects login attempts using a decoy and raises an alarm.

## Contribution

Decoy passwords, hashed storage, and a separate honeychecker.

## Key results

- The abstract proposes a breach-detection mechanism but provides no deployment detection rate.

## Methods and models

Decoy passwords, hashed storage, and a separate honeychecker.

## Limitations and open questions

Security depends on decoy indistinguishability and separation of the honeychecker; this is password-theft detection rather than swarm attribution.

## Relevance to us

A comparison source for coordinated automation and security measurement. Full-text methods and replication have not been checked.

## Access provenance

Crossref metadata and the abstract at the recorded URL were opened directly or through Exa content extraction on 2026-10-03. Any non-null citation count is OpenAlex cited_by_count on that date. Abstract depth is deliberate even where an open PDF was found.
