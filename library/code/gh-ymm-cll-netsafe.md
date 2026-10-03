---
id: gh-ymm-cll-netsafe
type: code
title: 'NetSafe: code for topological safety experiments on LLM multi-agent networks'
repo: Ymm-cll/NetSafe
url: https://github.com/Ymm-cll/NetSafe
authors: [Miao Yu, Shilong Wang, Guibin Zhang, Junyuan Mao, Chenlong Yin, Qijiong Liu, Qingsong Wen, Kun Wang, Yang Wang]
year: 2024
language: Python
license: MIT
stars: 12
last_commit: 2026-04-12
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [yu-2024-netsafe]
---

## Summary

Code for "NetSafe: Exploring the Topological Safety of Multi-agent Networks" (arXiv 2410.15686, authors from the arXiv record). Per the abstract, agents interact through an iterative protocol called RelCom over different graph topologies while some nodes inject misinformation, bias or harmful content; the paper reports that highly connected networks spread attacks more readily, with task performance in a star topology dropping by 29.7%, and that networks with greater average distance from attacker nodes are safer. The repository holds per-dataset run scripts (AdvBench, bias, CSQA, fact, GSM8K), JSONL datasets, a Kendall's tau similarity script, OpenAI Moderation API scoring, and plotting code. Configuration is by editing `run.py` and the API key in `methods.py`.

## What it can do for us

Q1 and Q2: a fork-merge parent is the hub of a star, the topology NetSafe found most fragile. The "average distance from attackers" metric is a structural lever: routing children's reports through intermediate aggregators (a tree rather than a star) increases distance from any corrupted leaf, which bears on both thresholds and on hiding which leaf feeds the root. The scripts are a cheap base for testing that, since they already parameterise topology and attacker placement.

## Run notes

Not run. README: put an OpenAI key in `get_client` in `methods.py`, set parameters in `run.py`, run `python run.py`.

## Limitations

Twelve stars, minimal README, OpenAI-only client. Attacker nodes are prompted to be adversarial rather than compromised by injection, so it measures spread, not initial compromise.
