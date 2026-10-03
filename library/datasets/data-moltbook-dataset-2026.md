---
id: data-moltbook-dataset-2026
type: dataset
title: "Moltbook Social Interactions Dataset (takschdube/moltbook-dataset): longitudinal posts, comments, agents, social and reply graphs from the agent-only network Moltbook"
authors: ["Taksch Dube"]
year: 2026
url: https://github.com/takschdube/moltbook-dataset
license: "MIT (LICENSE file); dataset card says CC-BY-4.0"
size: "Release v2026.10.03: 1.27 GB zip plus 1.03 GB zstd SQLite; 421,052 posts and 3,704,170 comments collected, 57,039 agents, 825,579 social edges, 928,318 reply edges, 33,350 submolts listed"
format: "JSON files (raw/, derived/) as HF-style configs; SQLite database (zstd); Zenodo DOI 10.5281/zenodo.19470480"
topics: [llm-agent-swarms, swarm-detection]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [gautam-2026-moltbook]
---

## Summary

Longitudinal scrape of Moltbook, a social network where autonomous AI agents ("Molties") post and comment, collected every six hours since February 2026 and released incrementally (latest release 2026-10-03). Provides posts, comments, submolts, derived agent tables, a follower social graph, a reply graph, an activity timeline and fetch-completeness audits. The platform API reports 4.37M posts and 13.5M comments in total, but only content reachable through the public API is collected (421k posts, 3.7M comments).

## Access

GitHub releases (zip or moltbook.db.zst) or the Zenodo DOI. Configs: posts, posts_full, submolts, agents, social_graph, reply_graph, activity_timeline, submolt_stats. Not downloaded here (about 2.3 GB per release; disk is tight).

## Relevance to us

Ground truth for validating an LLM social sim against a real agent-only society, and for coordinated-agent detection. Two pitfalls documented in the README matter for anyone citing reply statistics such as [[x-daveholtz-2017716355475124330]] or [[de-marzo-2026-collective]]:

- An empty comments array does not mean nobody replied. Fetch completeness: 52.2% of posts complete, 1.8% near complete, 19.1% truncated, 16.2% reported and retrieved no comments, 10.8% reported comments but none retrieved. Only 68.3% of posts support a claim that a reply was absent, and coverage rises with engagement because refresh targets hot/rising/top listings.
- The reply graph published before 2026-09-15 omitted every top-level reply to a post (the majority of replies) because it resolved parents via parent_id; rebuild anything derived from older copies.
- Schema changed mid-collection (author fields renamed; deletion markers and comment depth only on later records).

Whether these collection gaps affect specific published Moltbook findings is my inference, not something the dataset authors claim. A different collector with its own archive paper: [[gautam-2026-moltbook]], [[gh-kelkalot-moltbook-observatory]].
