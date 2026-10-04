---
id: sunil-2026-memory
type: paper
title: 'Memory Poisoning Attack and Defense on Memory Based LLM-Agents'
authors: [Balachandra Devarangadi Sunil, Isheeta Sinha, Piyush Maheshwari, Shantanu Todmal, Shreyan Mallik, Shuchi Mishra]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2601.05504
doi: null
arxiv: '2601.05504'
cite: 'Sunil, B. D., Sinha, I., Maheshwari, P., Todmal, S., Mallik, S., & Mishra, S. (2026). Memory Poisoning Attack and Defense on Memory Based LLM-Agents. arXiv preprint arXiv:2601.05504.'
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 40  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

A robustness study of MINJA [[dong-2025-memory]] under more realistic conditions, plus two defences, on Electronic Health Record agents using MIMIC-III. Three dimensions are varied: the initial memory state, the number of indication prompts, and retrieval parameters. Models are GPT-4o-mini, Gemini-2.0-Flash and Llama-3.1-8B-Instruct. Measured (abstract): when realistic legitimate memories already exist, attack effectiveness drops sharply compared with MINJA's idealised setting (over 95% injection and 70% attack success). The defences are input and output moderation using composite trust scores over several orthogonal signals, and memory sanitisation with trust-aware retrieval using temporal decay and pattern filtering. Memory sanitisation needs careful calibration of the trust threshold. Too strict blocks every entry, and too loose misses subtle attacks.

## Contribution

A partial replication that tests MINJA's sensitivity to existing memory and gives baseline heuristic defences.

## Key results

- Pre-existing legitimate memories dramatically reduce MINJA's effectiveness (abstract). Exact numbers were not read.
- Trust-threshold calibration is the main difficulty for sanitisation (abstract).

## Methods and models

EHR agent on MIMIC-III. Three LLMs.

## Limitations and open questions

Abstract only. One domain. Heuristic defences with no formal bound ([[sharma-2026-smsr]] makes the same observation).

## Relevance to us

For Q2 this replication adds weight to the benign-density effect, which MINJA itself found on MIMIC-III. A parent with a large store of clean memory on a topic is harder to corrupt through retrieval than a fresh one. In fork-merge terms, dilution by the parent's own and other sub-agents' honest records acts as a soft threshold. It is not a certified one: SMSR's certificate formalises the same effect. For Q3, it suggests the attacker gains most by targeting topics on which the parent has little prior memory. Those are precisely the novel domains a sub-agent was sent to explore (inferred).
