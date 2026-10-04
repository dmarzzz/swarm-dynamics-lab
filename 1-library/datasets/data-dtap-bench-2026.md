---
id: data-dtap-bench-2026
type: dataset
title: 'DTap-Bench agent trajectories (DecodingTrust-Agent Platform): red-teaming tasks across 14 domains, 2,806 benign and 3,876 malicious'
authors: [Zhaorun Chen, Xun Liu, Haibo Tong, Chengquan Guo, Yuzhou Nie, Jiawei Zhang, Mintong Kang, Chejian Xu, Qichang Liu, Xiaogeng Liu, et al.]
year: 2026
url: https://huggingface.co/datasets/AI-Secure/DTap-Bench-Agent-Trajectories
license: Apache-2.0
size: 6,682 tasks (2,806 benign, 3,876 malicious) over 14 domains
format: 'Per-task folders: config.yaml (task spec + MCP server bindings), setup.sh (sandbox seeding), judge.py (verifiable success check); malicious tasks split by threat model and risk category'
topics: [fork-merge-security]
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Release for the DecodingTrust-Agent Platform (arXiv 2605.04808). The card calls it the full collection of agent trajectories from evaluating DTap-Bench, but describes per-task configs: 14 domains (browser, code, CRM, finance, medical, telecom, Windows, macOS and others) over 50+ simulated environments such as Gmail, Slack, PayPal, Salesforce and Snowflake. Malicious tasks are split into direct and indirect threat models and risk categories including data exfiltration, dangerous actions and fraud/impersonation. Each task ships a verifiable judge.

## Access

Public, ungated, on Hugging Face. Apache-2.0. Runs through the `decodingtrust-agent-sdk` CLI with Docker sandboxes. Not downloaded here.

## Relevance to us

A broad, judge-verified red-teaming suite whose indirect-injection tasks could seed corrupted sub-agents in a fork-merge experiment. Compare with [[data-agent-safetybench-2024]].
