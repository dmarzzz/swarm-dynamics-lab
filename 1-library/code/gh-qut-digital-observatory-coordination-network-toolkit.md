---
id: gh-qut-digital-observatory-coordination-network-toolkit
type: code
title: "Coordination Network Toolkit: build co-retweet, co-tweet, co-similarity, co-link, co-reply and co-post networks from any timestamped social data"
repo: QUT-Digital-Observatory/coordination-network-toolkit
url: https://github.com/QUT-Digital-Observatory/coordination-network-toolkit
authors: ["Timothy Graham", "QUT Digital Observatory"]
year: 2020
language: Python
license: "MIT"
stars: 93
last_commit: 2022-11-08
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: ran
relevance: 4
papers: []
---

## Summary

Python package and CLI (`compute_networks`) from QUT's Digital Observatory. It ingests Twitter JSON or a generic CSV (message_id, user_id, username, repost_id, reply_id, message, timestamp, urls) into SQLite and computes account-account networks whose edge weights count messages meeting a coordination criterion within a time window (default 60 s): reposting the same post, posting identical text, posting similar text (Jaccard by default), sharing the same link, replying to the same post, or posting at all in the same window. Output to graphml or CSV. It implements the co-action approach of Keller et al. (2020) and Giglietto et al. (2020).

## What it can do for us

Platform-agnostic, fast coordination detection that takes any agent trace in five columns. Directly usable on agent-platform data, logs of our own swarm, or on-chain transactions mapped to messages.

## Run notes

Ran 2026-10-03: `uv venv -p 3.11; uv pip install coordination_network_toolkit networkx pandas pyarrow` (version 1.5.2). Converted one day of Moltbook posts ([[data-moltbook-observatory-2026]], 2026-09-10: 4,526 posts, 482 agents) to the CSV format with message = title + content, then `compute_networks m.db preprocess --format csv posts.csv` (0.3 s) and `compute_networks m.db compute <type> --time_window <w> --similarity_threshold <t> --output_file x.graphml --output_format graphml`. `--output_format csv` crashed with `TypeError: output_gephi_csv() got an unexpected keyword argument 'n_messages'`; graphml works. Results: co_tweet (identical text) found 0 edges at w = 60 s and at w = 86,400 s; co_similar_tweet found 0 edges at Jaccard 0.8 (60 s and 1 day) and a single pair at Jaccard 0.5 over 1 day (the 1-day similarity run took 56 s wall on 10 cores); co_post at 60 s with min edge weight 2 linked 254 of 482 agents in one component with 1,835 edges, top edge weights 236, 218, 196, dominated by the highest-volume agents posting every ~3 minutes. Interpretation (inferred): text-reuse coordination signals, the workhorse for human botnets, find nothing among LLM agents that each generate unique text, while co-post timing is swamped by base activity rate unless it is normalised.

## Limitations

Unmaintained since 2022-11-08 (CSV export bug above). Pairwise similarity over long windows is quadratic and slow. Identical-text and link methods assume copy-paste campaigns; LLM swarms paraphrase, so semantic-embedding similarity would be needed (not implemented). Time-window co-action needs a null model for activity rate; the toolkit gives raw counts only.
