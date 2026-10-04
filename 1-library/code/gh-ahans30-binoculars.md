---
id: gh-ahans30-binoculars
type: code
title: "Binoculars: zero-shot detector of LLM-generated text using the ratio of two models' perplexity and cross-perplexity"
repo: ahans30/Binoculars
url: https://github.com/ahans30/Binoculars
authors: ["Abhimanyu Hans", "Avi Schwarzschild", "Valeriia Cherepanova", "Hamid Kazemi", "Aniruddha Saha", "Micah Goldblum", "Jonas Geiping", "Tom Goldstein"]
year: 2023
language: Python
license: "BSD-3-Clause"
stars: 421
last_commit: 2024-05-14
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Implementation of 'Spotting LLMs with Binoculars: Zero-Shot Detection of Machine-Generated Text' (ICML 2024, arXiv 2401.12070). It scores a text with an observer model and a performer model (default Falcon-7B and Falcon-7B-Instruct) and uses a fixed global threshold chosen with those models; no training data is needed. The README example scores a GPT-4 paragraph at 0.757 and labels it 'Most likely AI-Generated'.

## What it can do for us

A strong training-free baseline for flagging machine text in agent traces; useful as one feature among many, not as an agent detector by itself.

## Run notes

Not run (needs two 7B models; GPU recommended).

## Limitations

README warns it is stronger on English than other languages and should not be used without human supervision. Text-level detection says nothing about whether many texts come from one operator, and [[yang-2023-anatomy]] found LLM-text classifiers failed on the fox8 botnet in the wild.
