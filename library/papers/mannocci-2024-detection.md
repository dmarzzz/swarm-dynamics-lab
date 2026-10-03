---
id: mannocci-2024-detection
type: paper
title: 'Detection and Characterization of Coordinated Online Behavior: A Survey'
authors:
- Lorenzo Mannocci
- Michele Mazza
- Anna Monreale
- Maurizio Tesconi
- Stefano Cresci
year: 2024
venue: ACM Computing Surveys
url: https://arxiv.org/abs/2408.01257
doi: 10.1145/3839225
arxiv: '2408.01257'
cite: 'Mannocci, L., Mazza, M., Monreale, A., Tesconi, M., & Cresci, S. (2026). Detection and Characterization of Coordinated Online Behavior: A Survey. ACM Computing Surveys, 58(16), Article 401, 1-38. https://doi.org/10.1145/3839225 (preprint arXiv:2408.01257, 2024).'
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 1 (Crossref, 2026-10-03)
code: []
---

## Summary

A survey of coordinated online behaviour research that reconciles industry terms such as Meta's 'coordinated inauthentic behavior' with academic definitions, proposes a framework of actors, actions and intent, and reviews detection and characterisation methods. It argues coordination should be described along authenticity, harmfulness, orchestration and time-variance, and lists open challenges; an interactive companion site indexes the surveyed papers.

## Contribution

The current reference survey for coordination detection, the method family most likely to catch LLM swarms whose per-account content looks human.

## Key results

- Framework: coordinated behaviour as actors, actions and intent (abstract and search snippet).
- Four dimensions: authenticity, harmfulness, orchestration, time-variance.
- Reviews detection methods, mostly similarity networks over shared actions (co-retweet, co-URL, co-hashtag, synchronous timing).

## Methods and models

Systematic survey. Abstract-level read; companion website not opened.

## Limitations and open questions

Covers human and bot coordination together; does not focus on LLM agents. Published version 2026, preprint 2024.

## Relevance to us

Entry point for the coordination branch of swarm detection. Methods it surveys include [[pacheco-2020-uncovering]] and [[luceri-2023-unmasking]]; tested on video in [[luceri-2025-coordinated]].
