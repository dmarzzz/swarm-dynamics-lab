---
id: gh-tangciuyueng-amemguard
type: code
title: 'A-MemGuard: official code for consensus-validated, lesson-augmented agent memory defence'
repo: TangciuYueng/AMemGuard
url: https://github.com/TangciuYueng/AMemGuard
authors: [Qianshan Wei, Tengchao Yang]
year: 2025
language: Python
license: MIT
stars: 17
last_commit: 2026-07-02
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [wei-2025-amemguard]
---

## Summary

The official repository for A-MemGuard [[wei-2025-amemguard]], which the README states was accepted to ICML 2026. It is built on the AgentPoison codebase ([[gh-ai-secure-agentpoison]]) and adapts that attack environment to evaluate the defence. A `ConsistencyChecker` in `EhrAgent/ehragent/consistency.py` and `ReAct/consistency.py` compares reasoning paths across retrieved memories, with interchangeable HuggingFace, OpenAI and vLLM providers. DPR and REALM embedders are supported.

## What it can do for us

A consensus check across retrieved memories that can be dropped into an agent. It could serve as the "unweighted majority" baseline for Q2 merge experiments, set against certified schemes ([[sharma-2026-smsr]]).

## Run notes

Not run. The README specifies conda Python 3.9 with `pip install -r requirements.txt`, and optionally a separate Python 3.10 vLLM server environment for local models (GPU expected).

## Limitations

Authors listed are the first two paper authors; the repo is the paper's official code per its README. Evaluation scope is inherited from AgentPoison's agents. Metadata read 2026-10-03.
