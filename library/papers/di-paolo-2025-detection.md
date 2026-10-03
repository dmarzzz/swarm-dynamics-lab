---
id: di-paolo-2025-detection
type: paper
title: Detection of LLM-powered bots using image classification
authors:
- Edoardo Di Paolo
- Marinella Petrocchi
- Angelo Spognardi
year: 2025
venue: First Monday
url: https://firstmonday.org/ojs/index.php/fm/article/view/13651
doi: 10.5210/fm.v30i5.13651
arxiv: null
cite: Di Paolo, E., Petrocchi, M., & Spognardi, A. (2025). Detection of LLM-powered bots using image classification. First Monday, 30(5). https://doi.org/10.5210/fm.v30i5.13651
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 0 (Crossref, 2026-10-03)
code: []
---

## Summary

Starting from the observation that families of automated accounts using generative AI to write posts have been found in the wild, the authors encode accounts as images and apply image classification to separate humans from LLM-powered bots. They report high efficiency and improvement over earlier work on detecting generative-AI-powered bot accounts.

## Contribution

An alternative representation (account-to-image) for LLM-bot detection from the Pisa/Rome group behind DNA-style behavioural encodings.

## Key results

- Reports improved detection of LLM-powered bots over prior work (abstract; no numbers on the article page).

## Methods and models

Account behaviour encoded as images; image classifier. Abstract and article page only.

## Limitations and open questions

Dataset and metrics not recorded here; likely evaluated on a known LLM botnet such as fox8, which is a single operator.

## Relevance to us

Builds on the fox8 botnet of [[yang-2023-anatomy]]; same group as [[cresci-2017-paradigm]] and [[de-nicola-2021-efficacy]].
