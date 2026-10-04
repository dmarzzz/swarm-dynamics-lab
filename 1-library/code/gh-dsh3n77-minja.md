---
id: gh-dsh3n77-minja
type: code
title: 'MINJA: memory injection attacks on LLM agents via query-only interaction (NeurIPS 2025 code)'
repo: dsh3n77/MINJA
url: https://github.com/dsh3n77/MINJA
authors: [Shen Dong, Shaochen Xu, Pengfei He, Yige Li, Jiliang Tang, Tianming Liu, Hui Liu, Zhen Xiang]
year: 2026
language: Python
license: MIT
stars: 37
last_commit: 2026-08-11
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [dong-2025-memory]
---

## Summary

Code release for MINJA [[dong-2025-memory]], in which an attacker with ordinary user access induces an agent to write poisoned (query, reasoning) records into a memory bank shared across users, so that later users' queries retrieve them as demonstrations. The repository was created in January 2026 and has three top-level folders, `rap` (a RAP retrieval-augmented planning agent on WebShop, which needs OpenJDK 21 and a local WebShop server), `EHR` (EHRAgent) and `QA` (a chain-of-thought QA agent). The paper, as summarised in the library entry, measures injection success above 95% and attack success between 30% and 100% depending on agent and dataset, with under 2% utility drop on most tasks.

## What it can do for us

Q3: the code demonstrates the mechanism in dmarz's question, a memory overwrite done by the agent itself after reading attacker-shaped input, without the attacker ever writing to memory directly. In fork-merge terms the child plays the role of the shared memory writer: the foreign domain shapes its reasoning, the child writes the records, and the parent retrieves them after merge. The paper's finding that denser benign memory lowers attack success (68.9% to 31.1% on MIMIC-III as benign queries go from 25 to 100) is a dilution effect that a parent merging many honest children would get for free, which is a measurable Q2 lever.

## Run notes

Not run. RAP part: `conda create -n rap python=3.10`, `conda install -c conda-forge openjdk=21`, `pip install -r requirements.txt`, put an OpenAI key in `OpenAI_api_key.txt`, set up WebShop with `./setup.sh -d all`. The README says to restart the WebShop server before each experiment.

## Limitations

Depends on OpenAI models and the WebShop and MIMIC/eICU environments (the latter need credentialed PhysioNet access). The README links only the RAP sub-README; EHR and QA folders exist but I did not read them. Memory is shared across users of one agent, not merged across agent instances, so the fork-merge mapping is an analogy.
