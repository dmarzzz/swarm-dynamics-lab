---
id: gh-tsinghua-fib-lab-acl24-econagent
type: code
title: "EconAgent: LLM households making monthly work and consumption decisions inside the AI Economist macroeconomic simulator"
repo: tsinghua-fib-lab/ACL24-EconAgent
url: https://github.com/tsinghua-fib-lab/ACL24-EconAgent
authors: ["Nian Li", "Chen Gao", "Mingyu Li", "Yong Li", "Qingmin Liao"]
year: 2023
language: Python
license: "none (no licence file)"
stars: 153
last_commit: 2024-08-16
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Simulation model: a macroeconomy (labour, goods market, taxes, interest rates) from Salesforce's Foundation/AI Economist; each LLM agent outputs JSON propensities to work and consume each month, with memory and reflection; aggregates such as inflation, unemployment and the Phillips curve are measured. Scale: 100 agents for 240 months in the README command. LLM-native: yes (GPT-3.5 originally; README notes gpt-4o-mini replacement and prompt-format failures). Adversarial hooks: none. Weight: light Python, but 100 x 240 = 24,000 LLM calls per run. Paper arXiv 2310.10436 (ACL 2024, not catalogued here).

## What it can do for us

Pattern for coupling LLM decisions to a numeric world model with macro observables; the 'one JSON decision per agent per tick' design is the cheapest way to get LLM agents into an existing ABM. See [[gh-salesforce-ai-economist]] for the underlying engine.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API. I did not read the source code. README: `python simulate.py --policy_model gpt --num_agents 100 --episode_length 240`.

## Limitations

No licence file, so reuse rights are unclear. Unmaintained since August 2024; original model retired.
