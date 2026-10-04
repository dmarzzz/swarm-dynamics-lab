---
id: data-sandbagging-games-2025
type: dataset
title: 'Evaluation logs from "Auditing Games for Sandbagging": Inspect transcripts of red-team model organisms and blue-team audits'
authors:
- Jordan Taylor
- Sid Black
- Dillon Bowen
- Thomas Read
- Satvik Golechha
- Alex Zelenka-Martin
- Oliver Makins
- Connor Kissane
- Kola Ayonrinde
- Jacob Merizian
- Samuel Marks
- Chris Cundy
- Joseph Bloom
year: 2025
url: https://huggingface.co/datasets/sandbagging-games/evaluation_logs
license: unspecified
size: not reported on the card
format: 'Inspect .eval transcript files, plus experiment outputs (auditing agent, deception-probe scores)'
topics:
- swarm-detection
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Transcripts for arXiv 2512.07810 (see [[taylor-2025-auditing]]). A red team fine-tuned five models, some of which conditionally underperform; a blue team tried black-box, probe and training-based detection. The repo holds the handover evaluations for the main and trial rounds, extra runs (password-unlocked organisms, an unused "Willow" organism, Llama 3.3 70B Instruct), the automated auditing agent's output, a user-persona attack, single-sample fine-tuning logs and middle/final-layer deception-probe scores. Per the abstract, the blue team could not reliably tell sandbaggers from benign models.

## Access

Public on Hugging Face, not gated, no licence tag. View with Inspect; guide at github.com/AI-Safety-Institute/sabotage_games.

## Relevance to us

A worked red-team/blue-team dataset for detecting a model hiding its behaviour, relevant to auditing a returning sub-agent; single-model, not multi-agent.
