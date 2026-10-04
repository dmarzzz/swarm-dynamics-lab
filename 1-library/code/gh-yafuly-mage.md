---
id: gh-yafuly-mage
type: code
title: "MAGE: machine-generated text detection in the wild, 447,674 texts from 27 LLMs across 10 domains"
repo: yafuly/MAGE
url: https://github.com/yafuly/MAGE
authors: ["Yafu Li", "Qintong Li", "Leyang Cui", "Wei Bi", "Zhilin Wang", "Longyue Wang", "Linyi Yang", "Shuming Shi", "Yue Zhang"]
year: 2023
language: Python
license: "Apache-2.0"
stars: 232
last_commit: 2025-03-06
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Data and Longformer detector for 'MAGE: Machine-generated Text Detection in the Wild' (ACL 2024). 447,674 human and machine texts: human text from 10 datasets, machine text from 27 LLMs from 7 sources, arranged in 8 testbeds of increasing difficulty, plus 'wilder' sets where GPT-4 writes in unseen domains (CNN/DailyMail, DialogSum, PubMedQA, IMDb; 200 each) and sentence-level paraphrases by gpt-3.5-turbo.

## What it can do for us

Out-of-distribution testbeds (unseen model, unseen domain, paraphrased) match the in-the-wild setting where we do not know which model a swarm uses.

## Run notes

Not run. Data via `load_dataset('yaful/MAGE')`.

## Limitations

2023 generators. Text only.
