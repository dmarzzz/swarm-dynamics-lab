---
id: data-twibot20-2021
type: dataset
title: "TwiBot-20: Twitter bot detection benchmark with profile, tweet and follow-graph information (CIKM 2021)"
authors: ["Shangbin Feng", "Herun Wan", "Ningnan Wang", "Jundong Li", "Minnan Luo"]
year: 2021
url: https://github.com/BunsenFeng/TwiBot-20
license: "MIT (repository); full data released for research on request"
size: "229,580 users (5,237 human, 6,589 bot labelled, rest unlabelled support set), 33.5 million tweets, 33.7 million edges (counts from the TwiBot-22 paper, Table 1); public sample 3.2 MB, 100 users"
format: "JSON (train, dev, test, support); TwiBot-22 4-file format also provided"
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: ran
relevance: 3
papers: []
---

## Summary

Benchmark built by controlled breadth-first expansion over Twitter follow relations from seed users in four domains (politics, business, entertainment, sports). Each user record has the Twitter profile, the 200 most recent tweets, up to 10 followers and 10 followings that are also in the dataset, a domain list and a bot or human label. Train, dev and test sets cover the first two BFS layers; an unlabelled support set from the third layer preserves graph density for semi-supervised methods. Only a 100-user sample (without labels) is public; the full set is shared for research on request.

## Access

Sample is in the repo; full data by email request to the authors (see README). Loaded the sample on 2026-10-03:

```bash
curl -sL -o tb20.json https://raw.githubusercontent.com/BunsenFeng/TwiBot-20/main/TwiBot-20_sample.json
```
```python
import json
d = json.load(open('tb20.json'))
print(len(d), list(d[0].keys()))   # 100 ['ID', 'profile', 'tweet', 'neighbor', 'domain']
```
The first sample user has 200 tweets and an empty neighbour list.

## Relevance to us

A graph-plus-content benchmark for detecting automated identities, which is the closest public analogue of detecting Sybil agents embedded in a social network of honest agents. Superseded in scale by [[data-twibot22-2022]]; see also [[data-cresci-2017]].
