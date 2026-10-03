---
id: gh-osome-iu-botometer-python
type: code
title: "Botometer X Python API: bulk lookup of archived Botometer bot scores for X/Twitter accounts"
repo: osome-iu/botometer-python
url: https://github.com/osome-iu/botometer-python
authors: ["OSoMe, Indiana University"]
year: 2015
language: Python
license: "MIT"
stars: 400
last_commit: 2024-06-26
topics: [swarm-detection, sybil-resistance]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Python client (formerly botornot-python) for Botometer, the Indiana University OSoMe bot classifier. Since June 2024 it serves Botometer X, which is archival: it returns pre-computed scores from data collected before June 2023 and no longer computes scores on the fly, because X/Twitter API access ended. Access is through RapidAPI (free tier available), in bulk by user id or screen name.

## What it can do for us

Historical bot scores for pre-mid-2023 Twitter accounts, the reference labels most social-bot base-rate studies used. Useful only for retrospective comparison; it cannot score current accounts or any LLM-era agent.

## Run notes

Not run (needs a RapidAPI key).

## Limitations

Frozen at June 2023 data; the classical feature-based Botometer was shown by [[yang-2023-anatomy]] to be unreliable on LLM-generated personas. Platform dependence: the tool died with API access, a general risk for in-the-wild detection.
