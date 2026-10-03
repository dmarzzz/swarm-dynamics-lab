---
id: gh-xiong-wenjun-maple-guard
type: code
title: 'MAPLE-Guard: memory-lifecycle gates against memory-link poisoning in multi-agent systems'
repo: xiong-wenjun/MAPLE-Guard
url: https://github.com/xiong-wenjun/MAPLE-Guard
authors: [Wenjun Xiong]
year: 2026
language: Python
license: none stated
stars: 10
last_commit: 2026-10-01
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [xiong-2026-maple]
---

## Summary

The experiment framework for [[xiong-2026-maple]]. It implements a multi-agent system with persistent private and shared memory over star, chain and tree topologies. Gates sit at write, retrieval, promotion (private to shared), cross-agent reuse and outcome update. There are runners for five benchmark and attack pairs: MMLU with MINJA, LongMemEval with MemoryGraft, AppWorld with AgentPoison, CSQA with PromptInject, and InjectAgent with ToolAttack. Key modules are `maple_guard_core.py` (gates, MAS execution, metrics), `memory_backend.py` (private and shared backend) and an `attacks/` package.

## What it can do for us

This is the only codebase found in this lane with an explicit private-to-shared promotion step, the closest existing analogue of fork-merge. It could be adapted so that "promotion" is a sub-agent merging into a parent, and a k-of-n promotion rule could be tested against single-item thresholds (Q2), with the bundled MINJA, MemoryGraft and AgentPoison attacks (Q3).

## Run notes

Not run. The README lists Python 3.9+. The reported results use Qwen3.5-122B-A10B, so a large-model endpoint is needed.

## Limitations

No licence file reported by the GitHub API, so reuse terms are unclear. Ten stars. Research code. The README badge says "Research Code". Metadata read 2026-10-03.
