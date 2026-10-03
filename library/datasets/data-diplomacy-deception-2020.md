---
id: data-diplomacy-deception-2020
type: dataset
title: 'Diplomacy deception detection: 17,289 pairwise in-game messages from 12 games, labelled truthful/deceptive by sender and receiver'
authors:
- community-datasets
year: 2020
url: https://huggingface.co/datasets/community-datasets/diplomacy_detection
license: unknown
size: 252 dialogue rows (17,289 messages, 12 games); 1,294,604 bytes
format: Parquet, train/validation/test; one row per pairwise dialogue with message lists and per-message labels
topics:
- sybil-resistance
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

HF mirror of the dataset from Peskov et al., "It Takes Two to Lie: One to Lie and One to Listen" (ACL 2020). Pairwise conversations between human players in 12 online Diplomacy games, 17,289 messages in all. Each message carries the sender's own truthful/deceptive label (actual lie) and the receiver's perceived label (suspected lie; under 10% unannotated), plus speaker/receiver country, season, year, supply-centre score and score delta. The card itself is mistitled "HateOffensive".

## Access

https://huggingface.co/datasets/community-datasets/diplomacy_detection, not gated. Licence tagged unknown; original repo github.com/DenisPeskov/2020_acl_diplomacy.

## Relevance to us

Human players, not agents, but it is the standard ground-truth set for deception in multi-party negotiation. Useful as a human baseline next to LLM-vs-LLM deception logs such as [[data-c2c-ai-vs-ai-2026]].
