---
id: gh-ethz-spylab-agentdojo
type: code
title: 'agentdojo: dynamic environment to evaluate prompt injection attacks and defenses for LLM agents'
repo: ethz-spylab/agentdojo
url: https://github.com/ethz-spylab/agentdojo
authors: [Edoardo Debenedetti, Jie Zhang, Mislav Balunović, Luca Beurer-Kellner, Marc Fischer, Florian Tramèr]
year: 2024
language: Python
license: MIT
stars: 889
last_commit: 2026-06-02
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [debenedetti-2024-agentdojo]
---

## Summary

AgentDojo is the ETH Zurich SPY Lab and Invariant Labs benchmark for indirect prompt injection against tool-using LLM agents, released as the pip package `agentdojo`. The paper abstract reports 97 realistic user tasks (email client, e-banking, travel booking) and 629 security test cases, built as an extensible environment rather than a fixed test suite, so new tasks, attacks and defenses can be plugged in [[debenedetti-2024-agentdojo]]. The README exposes a benchmark script that takes a suite, a model, a defense (for example `tool_filter`) and an attack (for example `tool_knowledge`), and a public results page. CaMeL's reference code evaluates against it ([[gh-google-research-camel-prompt-injection]]). I read the README and repository metadata, not the source.

## What it can do for us

Q3: it is the standard harness for measuring how often untrusted tool output can redirect a single agent, which is the first step of the fork-merge attack (corrupt the sub-agent in the foreign domain). A fork-merge experiment could wrap an AgentDojo suite as the "foreign domain" a child explores, then measure whether an injected instruction survives into the child's report and into the parent after merge. Q2: its defense slot is where a merge-time filter or quorum check could be benchmarked against the same attacks used by other papers, which keeps numbers comparable.

## Run notes

Not run. Install is `pip install agentdojo`; example from README: `python -m agentdojo.scripts.benchmark -s workspace -ut user_task_0 --model gpt-4o-2024-05-13 --defense tool_filter --attack tool_knowledge`. Needs API keys for hosted models.

## Limitations

Single-agent only: there is no notion of sub-agents, memory that persists across episodes, or a merge step, so the propagation half of the fork-merge threat has to be built on top. The README warns the package API is still changing. Last push June 2026, so it is maintained but not daily.
