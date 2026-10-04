---
id: gh-nicolarighetti-coortweet
type: code
title: "CooRTweet: R package for detecting coordinated networks (co-share, co-post, co-hashtag and more) across platforms"
repo: nicolarighetti/CooRTweet
url: https://github.com/nicolarighetti/CooRTweet
authors: ["Nicola Righetti", "Paul Balluff"]
year: 2022
language: R
license: "see repo (CRAN package)"
stars: 56
last_commit: 2025-07-10
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

R package on CRAN that generalises CooRnet to any platform: given a table of accounts, shared objects (URLs, hashtags, text, media hashes) and timestamps, it finds accounts that share the same object within a time window more often than a threshold and returns the coordinated network. Supports Twitter Academic API JSON directly and arbitrary data otherwise. Reference: Righetti and Balluff (2025), 'CooRTweet: A Generalized R Software for Coordinated Network Detection', Computational Communication Research 7(1).

## What it can do for us

The maintained successor to [[gh-fabiogiglietto-coornet]] and the R counterpart to [[gh-qut-digital-observatory-coordination-network-toolkit]]; recommended by the CooRnet authors after CrowdTangle closed.

## Run notes

Install attempted 2026-10-03 with R 4.5.3 on macOS (arm64): `install.packages('CooRTweet')` failed because the dependency RcppSimdJson did not compile (`simdjson.cpp:5087: error: use of undeclared identifier 'OUT_OF_CAPACITY'`), and binary packages were not available for this R build. Not run.

## Limitations

Same limits as other co-sharing detectors: it needs shared objects, so LLM agents that paraphrase evade text and hashtag co-sharing unless the objects are links or media. Build dependency issue on recent macOS toolchains.
