---
id: gh-microsoft-fides
type: code
title: 'Fides: tutorial notebook for information-flow control in AI agents'
repo: microsoft/fides
url: https://github.com/microsoft/fides
authors: [Manuel Costa, Boris Köpf, Aashish Kolluri, Andrew Paverd, Mark Russinovich, Ahmed Salem, Shruti Tople, Lukas Wutschitz, Santiago Zanella-Béguelin]
year: 2025
language: Jupyter Notebook
license: MIT
stars: 118
last_commit: 2025-05-30
topics: [fork-merge-security]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [costa-2025-securing]
---

## Summary

Microsoft's companion repository for [[costa-2025-securing]]. It holds a single Tutorial.ipynb that walks through the paper's mechanisms: confidentiality and integrity labels, taint propagation through a planning loop, hiding tool results in variables, and querying them through a quarantined LLM with constrained output. A fully evaluated copy of the notebook is included so outputs can be read without running it.

## What it can do for us

The smallest runnable illustration of label-based merge policy: a reader can see how a context label changes when untrusted data enters, which is the mechanic a merge from an untrusted sub-agent would trigger.

## Run notes

Not run. README: tested against GPT-4o and GPT-4.1 via Azure OpenAI Chat Completions, configured with AZURE_ENDPOINT, API_VERSION and AZURE_DEPLOYMENT in .env and Microsoft Entra ID authentication; adaptable to an OpenAI endpoint.

## Limitations

Tutorial only, not the evaluation code behind the AgentDojo numbers. Azure-centric setup. Single commit window (May 2025).
