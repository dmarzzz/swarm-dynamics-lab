---
id: data-agent-town-economy-2026
type: dataset
title: 'Agent Town Economy: 98 runs of a 100-agent LLM economic simulation with a fully ledgered, money-conserving economy'
authors:
- Sajal Regmi
- Siddhartha Pudasaini
- Chetan Phakami Pun
year: 2026
url: https://huggingface.co/datasets/sajalregmi4/agent-town-economy
license: CC-BY-4.0 (data); MIT (analysis code)
size: 98 runs (91 accepted, 7 quarantined), 2.44M agent decisions, 21.5B tokens, 41,328 pulses, ~7.2 GB CSV
format: 'production_final/<arm>/<world>/<condition>/<seed>/: 14 CSVs per run (actions, agents, conversations, transactions, model_calls, prices, ...) plus validation.json, run.json, metrics.json'
topics:
- llm-agent-swarms
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Run corpus for "But How Would AI Agents Run a Town's Economy?" (Regmi, Pudasaini, Phakami Pun; arXiv 2609.11108). 100 memory-equipped LLM agents earn wages and run or patronise 762 businesses on real Lakeside, Pokhara geography for up to 26 simulated weeks (4,368 pulses). Arms: baseline, tourism shocks, wealth grant, memory ablation, layout placebo, and a gpt-oss-20b model swap. Money is conserved exactly at all pulses of the 91 accepted runs. Six Mistral-Small-3.2 runs failed on duplicate tool-call ids and are kept as a negative result.

## Access

https://huggingface.co/datasets/sajalregmi4/agent-town-economy, not gated, CC-BY-4.0. The simulation platform itself is not released; analysis scripts that rebuild the paper's numbers are included.

## Relevance to us

One of the largest released 100-agent LLM society logs with per-agent actions, conversations, model calls and an exact transaction ledger: a ready substrate for coordination inference and for planting synthetic colluding or sybil agents against a clean ground truth. Cross-model arm and tool-call failure notes are useful for model attribution.
