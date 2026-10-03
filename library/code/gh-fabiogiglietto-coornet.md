---
id: gh-fabiogiglietto-coornet
type: code
title: "CooRnet: detects coordinated link sharing behaviour (CLSB) on Facebook and Instagram via CrowdTangle (archived)"
repo: fabiogiglietto/CooRnet
url: https://github.com/fabiogiglietto/CooRnet
authors: ["Fabio Giglietto", "Nicola Righetti", "Luca Rossi"]
year: 2020
language: R
license: "MIT"
stars: 75
last_commit: 2024-08-14
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

R package that, given URLs, pulls their shares from CrowdTangle, estimates a data-driven time threshold for 'unusually fast' co-shares, and returns networks of Facebook and Instagram pages, groups and profiles that repeatedly share the same links within that threshold. Optional GPT-3.5 labelling of clusters. Archived: CrowdTangle shut down on 2024-08-14 and the authors point users to CooRTweet ([[gh-nicolarighetti-coortweet]]).

## What it can do for us

Its threshold estimation (choose the window from the distribution of share delays rather than fixing 60 s) is the part worth reusing for agent traces, where base rates differ from human platforms.

## Run notes

Not run (requires the defunct CrowdTangle API).

## Limitations

Archived and unusable without CrowdTangle. Facebook-specific.
