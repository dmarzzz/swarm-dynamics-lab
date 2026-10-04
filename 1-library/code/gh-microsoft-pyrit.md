---
id: gh-microsoft-pyrit
type: code
title: 'PyRIT: Microsoft Python Risk Identification Tool for generative AI red teaming'
repo: microsoft/PyRIT
url: https://github.com/microsoft/PyRIT
authors: [Microsoft AI Red Team]
year: 2023
language: Python
license: MIT
stars: 4574
last_commit: 2026-10-03
topics: [fork-merge-security]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

PyRIT is Microsoft's open framework for security professionals to identify risks in generative AI systems; the README points to a 2026 whitepaper "PyRIT: Democratizing AI Red Teaming Through Open-Source Tooling" for citation. The package has modules for prompt targets, converters, scorers, memory (a store of all attack conversations), datasets and executors. The multi-turn attack executors in `pyrit/executor/attack/multi_turn` are Crescendo, PAIR, tree of attacks, red teaming orchestration, multi-prompt sending, chunked requests and simulated conversation. A separate repository Azure/PyRIT created in March 2026 has the same description but only 118 stars; microsoft/PyRIT is the active one (pushed on the day I accessed it).

## What it can do for us

Q3: multi-turn attackers (Crescendo, PAIR, tree of attacks) model an adversary who interacts with a child over many turns while it explores a hostile domain, which is a stronger and more realistic threat than a single injected document. PyRIT could drive such an adversary against a child agent's endpoint and log the full conversation, so that the child's post-exposure state can be compared with its pre-fork state before merge.

## Run notes

Not run. Install and usage are documented on microsoft.github.io/PyRIT, not in the README.

## Limitations

General red-teaming framework, not a benchmark; no fixed test set or published numbers to compare against. No built-in notion of multi-agent topology or merge. Two repositories with the same name exist, which is a source of confusion.
