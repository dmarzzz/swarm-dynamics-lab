---
id: data-mallm-debate-2025
type: dataset
title: 'DEBATE: Diverse Multi-Agent Debates, 144 configurations of LLM discussion paradigm, persona and decision protocol (MALLM)'
authors:
- Multi-Agent-LLMs
year: 2025
url: https://huggingface.co/datasets/Multi-Agent-LLMs/DEBATE
license: Apache-2.0
size: 14,410 rows, 6,477,563,125 bytes (datasets-server)
format: 'JSON, 144 configs named <response>_<persona>_<paradigm>_<decision>; fields include personas (agentId, model, persona), paradigm, decisionSuccess, agreements, turns, globalMemory, agentMemory'
topics:
- llm-agent-swarms
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Released with "MALLM: Multi-Agent Large Language Models Framework" (Becker et al., arXiv 2509.11656); the card itself says little beyond that. The datasets-server schema shows 144 configurations crossing response generator (simple, critical, reasoning), persona type (expert, ipip, nopersona), discussion paradigm (debate, memory, relay, report) and decision protocol (approval voting, majority or unanimity consensus, simple voting). Each record keeps per-agent personas and models, the full message log with per-message agreement flags, per-agent memory, turn count and whether a decision was reached.

## Access

https://huggingface.co/datasets/Multi-Agent-LLMs/DEBATE, not gated, Apache-2.0. About 6.5 GB.

## Relevance to us

Systematic sweep of how protocol and decision rule shape multi-agent agreement, with full transcripts; a baseline for studying how one injected or corrupted debater shifts consensus under each rule (compare [[kraidia-2026-when]]).
