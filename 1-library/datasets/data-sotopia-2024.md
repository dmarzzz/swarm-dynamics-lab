---
id: data-sotopia-2024
type: dataset
title: 'SOTOPIA episodes v1: role-played social-interaction episodes between language agents'
authors:
- cmu-lti
year: 2024
url: https://huggingface.co/datasets/cmu-lti/sotopia
license: CC (HF tag "cc", variant unspecified)
size: 1K-10K episodes (HF size category; exact count not on card)
format: sotopia_episodes_v1.csv (no model information or rewards) and sotopia_episodes_v1.json (includes models and rewards)
topics:
- llm-agent-swarms
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers:
- zhou-2023-sotopia
---

## Summary

Episode data for [[zhou-2023-sotopia]] (SOTOPIA, ICLR 2024 spotlight, arXiv 2310.11667), an interactive benchmark where language agents role-play social scenarios with goals and are scored on social intelligence. The card ships the episodes in two forms: a CSV without model identities or rewards, and a JSON that includes both. The card gives no per-model counts; the HF size category is 1K-10K. Fuller database documentation is linked from the sotopia-lab GitHub repo.

## Access

https://huggingface.co/datasets/cmu-lti/sotopia, not gated. Licence tag is a bare "cc" with no variant; check before reuse.

## Relevance to us

Scored multi-turn agent-agent interactions with goals that can conflict, including the model behind each side; useful for testing whether agent identity or model is recoverable from dialogue. Pairs with [[data-sotopia-pi-2024]].
