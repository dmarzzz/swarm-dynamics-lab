---
id: wang-2023-bot
type: paper
title: "Bot or Human? Detecting ChatGPT Imposters with A Single Question"
authors: ["Hong Wang", "Xuan Luo", "Weizhi Wang", "Xifeng Yan"]
year: 2023
venue: "Conference on Language Modeling (COLM 2024); arXiv preprint"
url: https://arxiv.org/abs/2305.06424
doi: null
arxiv: "2305.06424"
cite: "Wang, H., Luo, X., Wang, W., & Yan, X. (2023). Bot or Human? Detecting ChatGPT Imposters with A Single Question. COLM 2024. arXiv:2305.06424."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "40 citing papers returned by the citations endpoint (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

FLAIR (Finding LLM Authenticity via a Single Inquiry and Response) detects conversational bots online with a single question. Questions fall into two families: easy for humans but hard for LLMs (counting characters, substitution, searching, ASCII-art reasoning) and easy for LLMs but hard for humans (memorisation, computation). The paper reports how strongly each question type separates humans from bots and releases the question set.

## Contribution

Early reverse Turing test built on known LLM weaknesses, a single-shot challenge-response check for whether a counterpart is a bot.

## Key results

- Different question families have different discriminative strength; counting-style questions motivated by LLM tokenisation weaknesses are a central example (abstract; numbers not read).

## Methods and models

Hand-designed question families tested on 2023-era LLMs and human participants. Code and questions: github.com/hongwang600/FLAIR (not catalogued).

## Limitations and open questions

Tied to 2023 model weaknesses; character counting and similar tasks have since improved and tool-using agents can call code. Abstract-only reading.

## Relevance to us

The archetype of probes that make an agent reveal itself. Needs re-measurement against 2026 agents; see [[gressel-2024-are]] for a larger benchmark and [[rmus-2026-process]] for process-based tests that may age better.
