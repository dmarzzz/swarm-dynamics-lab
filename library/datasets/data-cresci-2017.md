---
id: data-cresci-2017
type: dataset
title: 'cresci-2017 (The Fake Project): genuine, social spambot, traditional spambot and fake follower Twitter accounts'
authors:
- Stefano Cresci
- Roberto Di Pietro
- Marinella Petrocchi
- Angelo Spognardi
- Maurizio Tesconi
year: 2017
url: https://botometer.osome.iu.edu/bot-repository/datasets.html
license: research use only (READ.ME liability disclaimer); Twitter content redistribution terms apply
size: 466 MB zip; 14,368 accounts (3,474 genuine, 10,894 bot or fake) with about 6.6 million tweets
format: nested zip of CSV files (users.csv and tweets.csv per class)
topics:
- sybil-resistance
- swarm-detection
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: ran
relevance: 3
papers: []
---

## Summary

Twitter account dataset from the CNR IIT group (Pisa), released with "The paradigm-shift of social spambots" (WWW 2017 Companion). Classes are genuine accounts, three groups of social spambots, four groups of traditional spambots and fake followers; annotation was done by CrowdFlower contributors per the Bot Repository description. Loaded user tables: genuine 3,474; social_spambots_1 991, _2 3,457, _3 464; traditional_spambots_1 1,000, _2 100, _3 403, _4 1,128; fake_followers 3,351; total bots 10,894, which matches the counts reported for cresci-2017 in the TwiBot-22 paper ([[data-twibot22-2022]]). User tables have 38 to 42 profile columns. There are no follow edges, so it is not a graph dataset.

## Access

Direct download from the Indiana University OSoMe Bot Repository (dataset metadata at `datasets/cresci-2017/info.json`). Loaded on 2026-10-03:

```bash
curl -sL -o cresci2017.zip https://botometer.osome.iu.edu/bot-repository/datasets/cresci-2017/cresci-2017.csv.zip
unzip -q cresci2017.zip && cd datasets_full.csv && unzip -q social_spambots_1.csv.zip
```
```python
import pandas as pd
u = pd.read_csv('social_spambots_1.csv/users.csv', encoding='latin-1', low_memory=False)
print(u.shape)   # (991, 41)
```

## Relevance to us

The standard benchmark for coordinated fake identities on a social platform. The social spambot classes are labelled separately from traditional spambots, which makes the set a pre-LLM precedent for identities built to look human; we have not read the accompanying paper, so its detection claims are not summarised here. Useful as a pre-LLM baseline when building detectors for agent-run identity farms, alongside the graph-based [[data-twibot20-2021]] and [[data-twibot22-2022]] and the graph detectors in [[gh-binghuiwang-sybildetection]].

## Notes from dmarz/sd-bots

Source paper: [[cresci-2017-paradigm]]. [[hays-2023-simplistic]] (read in full) shows a depth-one decision tree reaches 0.98 accuracy on this dataset because every genuine account came from an earthquake social-sensing collection and had tweeted the word 'earthquake'; another single split on account creation date also nearly separates the classes. Treat high scores on cresci-2017 as a collection artefact, not evidence of detectability.

## Notes from dmarz/sd-code-data

Tagged swarm-detection. One of the nine datasets merged by [[gh-tamsiuhin-botpercent]] to estimate bot populations; pre-LLM, so useful as the 'old bots' side of a detector-transfer test against [[data-fox8-2023]].
