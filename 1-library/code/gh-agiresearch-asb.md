---
id: gh-agiresearch-asb
type: code
title: 'ASB: Agent Security Bench, attacks and defenses for LLM agents including memory poisoning'
repo: agiresearch/ASB
url: https://github.com/agiresearch/ASB
authors: [Hanrong Zhang, Jingyuan Huang, Kai Mei, Yifei Yao, Zhenting Wang, Chenlu Zhan, Hongwei Wang, Yongfeng Zhang]
year: 2024
language: Python
license: MIT
stars: 308
last_commit: 2026-09-30
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Agent Security Bench (ICLR 2025, arXiv 2410.02644) is built on the AIOS agent runtime. Per the paper abstract it covers 10 scenarios, 10 agents, over 400 tools, 27 attack and defense methods and 7 metrics, benchmarking 10 prompt injection attacks, a memory poisoning attack, a Plan-of-Thought (PoT) backdoor, 4 mixed attacks and 11 defenses on 13 LLM backbones. The README table (measured by the authors) gives average attack success rates across the 13 backbones of 72.68% for direct prompt injection, 27.55% for observation prompt injection, 7.92% for memory poisoning, 84.30% for mixed attacks and 42.12% for the PoT backdoor. Defenses are weak: paraphrasing lowers average DPI ASR from 78.38% to 56.87%, while delimiters and instructional prevention change it by under 2 points. Attacks are selected by YAML configs (`config/MP.yml` for memory poisoning).

## What it can do for us

Q3: ASB is one of few harnesses that treats memory retrieval as a separate attack surface next to observations and system prompts, which is the surface a returning child would write into when its report is merged into the parent's memory. The measured gap (memory poisoning 7.92% versus mixed 84.30%) suggests that a poisoned memory record alone is a weak lever in ASB's setup and that combining it with an observation injection is what works; that is a measured result for single agents, and whether it transfers to merge is not checked. Q2: the defense table is a ready baseline showing prompt-level filters barely move ASR, which motivates structural defenses (quorum, provenance) instead.

## Run notes

Not run. README: `conda create -n ASB python=3.11`, `pip install -r requirements.txt`, then `python scripts/agent_attack.py --cfg_path config/MP.yml`. Supports ollama for local models.

## Limitations

The memory poisoning attack injects plans into a retrieval store under the attacker's control; it does not model a sub-agent that was itself compromised. Numbers come from the README and paper and were not reproduced here. Depends on AIOS, which ties it to that runtime.
