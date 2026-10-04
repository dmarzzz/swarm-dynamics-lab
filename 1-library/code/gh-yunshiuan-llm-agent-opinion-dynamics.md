---
id: gh-yunshiuan-llm-agent-opinion-dynamics
type: code
title: "llm-agent-opinion-dynamics: scripts for simulating opinion dynamics with networks of LLM agents (Chuang et al., NAACL Findings 2024)"
repo: yunshiuan/llm-agent-opinion-dynamics
url: https://github.com/yunshiuan/llm-agent-opinion-dynamics
authors: ["Yun-Shiuan Chuang", "Agam Goyal", "Nikunj Harlalka", "Siddharth Suresh", "Robert Hawkins", "Sijia Yang", "Dhavan Shah", "Junjie Hu", "Timothy T. Rogers"]
year: 2024
language: Python
license: "MIT"
stars: 50
last_commit: 2024-06-26
topics: [llm-agent-swarms, sync-consensus, collective-decision]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [chuang-2023-simulating]
---

## Summary

Simulation model: agents repeatedly write 'tweets' about a (fictional-labelled) claim, read others' tweets and report beliefs on a numeric scale; prompts vary confirmation bias (none, weak, strong) and framing, after Flache et al. 2017. Scale: 10 agents for 100 steps in the README command. LLM-native: yes (GPT-4, GPT-3.5, Vicuna). Adversarial hooks: none, but the prompt templates are plain text and easy to extend with a stubborn or coordinated minority. Weight: conda plus API key, or GPU for Vicuna.

## What it can do for us

Minimal, readable opinion-dynamics loop where the known LLM bias (convergence toward the scientifically accurate view) is documented, so it is a good baseline before we add sybil minorities.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API. I did not read the source code. README: `python scripts/opinion_dynamics_v2.py -agents 10 -steps 100 ...`.

## Limitations

Research scripts, unmaintained since June 2024; tiny populations; fully connected exposure.
