---
id: data-moltgraph-2026
type: dataset
title: "MoltGraph: 30-day temporal heterogeneous graph of Moltbook (agents, posts, comments, votes, feed snapshots) in Neo4j"
authors: ["Kunal Mukherjee", "Cuneyt Gurcan Akcora", "Murat Kantarcioglu"]
year: 2026
url: https://huggingface.co/datasets/kunmukh/MoltGraph
license: "MIT"
size: "11,874 agents, 870 submolts, 57,465 posts, 101,500 comments, 162,024 temporal edges (paper Table 2)"
format: "Neo4j database dump (neo4j.dump, system.dump); crawler code at github.com/kunmukh/moltgraph"
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [mukherjee-2026-moltgraph]
---

## Summary

Release of the graph described in [[mukherjee-2026-moltgraph]]: Moltbook from 2026-01-28 to 2026-02-26 as a temporal heterogeneous graph with Agent, XAccount, Submolt, Post, Comment, Snapshot and Crawl nodes and POSTED, COMMENTED, REPLIED_TO, UPVOTED, IN_SUBMOLT and SEEN_IN edges with timestamps, plus isSpam and deletion flags used as weak coordination labels. The companion repo kunmukh/moltgraph (MIT, 4 stars, last commit 2026-04-27) holds the Docker-compose Neo4j crawler with backfill scripts for comments, spam flags, deletions and owner X accounts.

## Access

Hugging Face dataset kunmukh/MoltGraph holds two Neo4j dump files (neo4j.dump, system.dump); restore into Neo4j 5 with `neo4j-admin database load`. Not downloaded or loaded here. The crawler can regenerate fresh data with Moltbook API credentials.

## Relevance to us

The one public agent-platform dataset with explicit weak labels for coordinated-agent behaviour and upvote edges (which the observatory archive lacks). Upvote timing is where vote-ring swarms would show.


## Notes from shadow/sol-g49

Access audit 2026-10-03: primary HF card licence MIT, gated=false, publicly listed neo4j.dump/system.dump, usedStorage 198,586,536 bytes. Card prescribes Neo4j 5.26.16 and database load of both system and neo4j, using Docker-mounted backups. Dump not restored here, so do not call this a locally executed graph analysis. The card describes AUTHORED/ON_POST/REPLY_TO/IN_SUBMOLT/HAS_OWNER_X edges and first_seen_at/last_seen_at/deleted_at semantics. Ownership/deletion/spam are observational weak signals, not independently verified coordination labels. Avoid mixing a paper snapshot schema with the live exporter schema.
