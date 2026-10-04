---
id: gh-nvidia-garak
type: code
title: 'garak: NVIDIA LLM vulnerability scanner with injection, latent-injection and agent-breaker probes'
repo: NVIDIA/garak
url: https://github.com/NVIDIA/garak
authors: [Leon Derczynski, Erick Galinkin, Jeffrey Martin, Subho Majumdar, Nanna Inie]
year: 2023
language: Python
license: Apache-2.0
stars: 9417
last_commit: 2026-10-02
topics: [fork-merge-security]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

garak (Generative AI Red-teaming and Assessment Kit) is a command-line scanner, now maintained under NVIDIA, that the README compares to nmap or Metasploit for LLMs. It runs probes against a generator (Hugging Face, OpenAI, Bedrock, LiteLLM, REST endpoints, gguf models) and scores responses with detectors. The probe directory currently includes `promptinject`, `latentinjection` (instructions hidden in documents the model is asked to process), `web_injection`, `smuggling`, `encoding`, `dan`, `tap`, `goat`, `fitd`, `sysprompt_extraction`, `leakreplay` and `agent_breaker`. The `agent_breaker` probe's docstring describes a multi-turn red-team probe for tool-using agents: a red-team model analyses each tool, generates targeted exploits and verifies success in conversation with the agent.

## What it can do for us

Q3: a ready way to measure, per base model, how susceptible a child agent is to latent injection before it is sent into a foreign domain. If children run different base models (a diversity defense for Q2), garak gives a cheap per-model susceptibility profile to check that their failure modes are actually uncorrelated, which the binomial k-of-n argument requires.

## Run notes

Not run. `python -m pip install -U garak`, then run garak against a model with a chosen probe set (see docs.garak.ai).

## Limitations

Model-level scanner; it does not model memory, multiple agents or merging. Probe names and coverage change quickly. Relevance to fork-merge is indirect.
