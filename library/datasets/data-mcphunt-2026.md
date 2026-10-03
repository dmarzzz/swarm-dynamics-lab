---
id: data-mcphunt-2026
type: dataset
title: 'MCPHunt Agent Traces: cross-boundary credential propagation in multi-server MCP agents (3,615 main traces, 5 models)'
authors: [Haonan Li, Tianjun Sun, Yongqing Wang, Qisheng Zhang]
year: 2026
url: https://huggingface.co/datasets/lihaonan0716/mcphunt-agent-traces
license: CC-BY-4.0
size: 3,615 main traces + 2,706 mitigation + 387 live-guard + 78 browser-replication traces; one JSON file per model
format: 'JSON with a top-level traces array; fields task_id, env_type, risk_mechanism, outcome, labeling (11 tiered risk signals + 1 diagnostic), events (tool-call log), task_completed, duration_s'
topics: [fork-merge-security]
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Traces released with MCPHunt (arXiv 2604.27819). The main split has 3,615 traces, 723 each from GPT-5.4, GPT-5.2, DeepSeek-V4-Flash, Gemini-3.1-Pro and MiniMax-M2.7, over 147 tasks and 7 environment variants (risky, benign, hard-negative). Canary credentials make propagation labelling a string match. The abstract reports policy-violating propagation rates of 11.5 to 41.3% across models, concentrated in browser-mediated flows, and a prompt mitigation that cuts it by up to 97%. Extra splits cover a prompt-mitigation study and a runtime taint-guard defence.

## Access

Public, ungated, on Hugging Face. CC-BY-4.0. Not downloaded here.

## Relevance to us

A labelled taint-tracking set for data leaking across tool and trust boundaries in one agent. That is the same propagation question as a corrupted sub-agent contaminating its parent on merge, minus the multi-agent part.
