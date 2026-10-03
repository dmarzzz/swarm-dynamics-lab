---
id: data-fox8-2023
type: dataset
title: 'fox8-23: ChatGPT-powered Twitter botnet accounts (1,140 bots) plus 1,140 human
  accounts, up to 200 tweets each'
authors:
- Kai-Cheng Yang
- Filippo Menczer
year: 2023
url: https://doi.org/10.5281/zenodo.8035289
license: CC-BY-4.0
size: 2,280 accounts (1,140 fox8 bots; 285 humans each from botometer-feedback, gilani-17,
  midterm-2018 and varol-icwsm); one 124,865,908-byte gzipped NDJSON file
format: 'fox8_23_dataset.ndjson.gz: one JSON object per account with user_id, label,
  dataset, user_tweets (Twitter API v1.1 tweet objects)'
topics:
- swarm-detection
- llm-agent-swarms
- sybil-resistance
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: ran
relevance: 5
papers:
- yang-2023-anatomy
---

## Summary

Benchmark released with [[yang-2023-anatomy]] (Yang and Menczer, arXiv 2307.16336; journal version in Journal of Quantitative Description: Digital Media, 2024). The 1,140 bot accounts form the fox8 botnet, which used ChatGPT to post content promoting suspicious websites; the abstract says they were found by heuristics, validated by manual annotation, and that they form a dense cluster that replies to and retweets each other. Measured in the paper (abstract): the accounts can be detected by their coordination patterns, while state-of-the-art LLM-content classifiers failed to separate them from human accounts in the wild. The repo osome-iu/AIBot_fox8 (MIT, 21 stars, last commit 2024-06-12) also includes the script used to query OpenAI's AI text classifier.

## Access

Download `fox8_23_dataset.ndjson.gz` from Zenodo record 8035289 (published 2023-08-02, CC-BY-4.0). No registration. Not downloaded here.

## Relevance to us

The canonical in-the-wild LLM botnet with ground truth, and the cleanest negative result for content-based detection: coordination structure caught the swarm, text classifiers did not. Any agent-swarm detector we build should report results on fox8-23 next to [[data-twibot22-2022]] and [[data-botsim24-2024]].


## Notes from shadow/sol-g49

Access and load verified 2026-10-03 via Zenodo metadata and gzip streaming. Primary licence CC-BY-4.0. URL https://zenodo.org/api/records/8035290/files/fox8_23_dataset.ndjson.gz/content . Parsed first NDJSON account: label human, source botometer-feedback, 200 user_tweets; fields user_id/label/dataset/user_tweets. This is one loaded record, not a full-corpus rerun. Loader: gzip.GzipFile(fileobj=urllib.request.urlopen(url)), then json.loads(stream.readline()). Full record advertises 2,280 accounts, split 1,140 fox8 versus 1,140 controls. Source botnet identification uses heuristics/manual validation, not merely text-classifier probabilities.
