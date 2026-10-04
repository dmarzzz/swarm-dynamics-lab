---
id: gh-ukgovernmentbeis-inspect-ai
type: code
title: "Inspect: UK AISI framework for LLM evaluations, agents, tools and sandboxes"
repo: UKGovernmentBEIS/inspect_ai
url: https://github.com/UKGovernmentBEIS/inspect_ai
authors: ["UK AI Security Institute"]
year: 2023
language: "Python"
license: "MIT"
stars: 2928
last_commit: 2026-10-02
topics: [llm-agent-swarms, fork-merge-security, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: ran
relevance: 5
papers: []
---

## Summary

Simulates: nothing by itself; it is an evaluation harness (datasets, solvers, scorers, tools, Docker sandboxes, structured logs) on which multi-agent environments are built, for example [[gh-ukgovernmentbeis-control-arena]] and [[gh-meridianlabs-ai-inspect-petri]]. Interaction model: async solvers call models; a solver can call several models or sub-agents and keeps per-sample state in a store. Scale: per-sample concurrency, scale bounded by API budget. LLM-driven: yes, natively, with a deterministic mockllm provider for offline tests. Adversarial hooks: none specific; injected inputs, poisoned sub-agents and canaries are written into solvers and scorers (we wrote a fork-merge canary test). Weight: pip install, laptop.

## What it can do for us

The default harness for fork-merge experiments: a solver forks N sub-agent calls, one poisoned, merges their reports, and a scorer checks whether a canary crossed the merge. Logs (.eval) record every model event for later audit. mockllm makes harness plumbing testable offline at zero cost.

## Run notes

Installed in the same uv venv (`uv pip install inspect-ai`, version 0.3.276). Wrote /private/tmp/claude-501/-Users-halcyon/91c0102b-dec1-491c-bac9-3e6625d95c8f/scratchpad/simenv/forkmerge_task.py: a solver forks 3 sub-agent generations per sample, appends a canary string to child 1, merges the children's reports into a final generate() call; a scorer marks the sample incorrect if the canary appears in the merged output. Ran `inspect eval forkmerge_task.py --model mockllm/model --log-dir logs --display plain`: 5 samples, 20 model calls, 3 s task time (8.6 s wall including start-up), accuracy 1.000. The log (`inspect log dump`) shows child_leak=True, merged_leak=False, and the merged output "Default output from mockllm/model": the mock model ignores input, so this run tests plumbing only and says nothing about real leakage.

## Limitations

An eval harness, not a simulator: no clock, network or population dynamics. Multi-agent topologies have to be written by hand in solvers. Real runs cost API money per call.
