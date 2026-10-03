---
id: gh-liu00222-open-prompt-injection
type: code
title: 'Open-Prompt-Injection: toolkit and benchmark for prompt injection attacks and defenses'
repo: liu00222/Open-Prompt-Injection
url: https://github.com/liu00222/Open-Prompt-Injection
authors: [Yupei Liu, Yuqi Jia, Runpeng Geng, Jinyuan Jia, Neil Zhenqiang Gong]
year: 2023
language: Python
license: MIT
stars: 503
last_commit: 2026-09-27
topics: [fork-merge-security]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [liu-2023-formalizing]
---

## Summary

The platform released with "Formalizing and Benchmarking Prompt Injection Attacks and Defenses" [[liu-2023-formalizing]] from Neil Gong's group at Duke. The paper abstract frames a prompt injection as making an LLM-integrated application perform an injected task instead of its target task, shows existing attacks are special cases of one framework, and evaluates 5 attacks and 10 defenses on 10 LLMs and 7 tasks; the combined attack is the framework's new attack. The README exposes Python objects for target tasks, injected tasks, models and attackers, and computes attack success value (ASV) for a target/injected task pair, for example SST-2 sentiment as target and SMS spam detection as injected task. It is still maintained (push in September 2026) and the README links extended slides from 2025.

## What it can do for us

Q3: the formalism (target task versus injected task, with the injected data concatenated to legitimate data) is the cleanest vocabulary for describing what a corrupted child does: its returned report is legitimate data with an injected task appended. The toolkit gives task-level ASV numbers per model and defense, which are a sanity baseline before running agentic benchmarks such as [[gh-ethz-spylab-agentdojo]].

## Run notes

Not run. `conda env create -f environment.yml`, put keys in `configs/model_configs/*.json`, then follow the README snippets (`PI.create_task`, `PI.create_model`, `PI.create_attacker`, `PI.create_app`).

## Limitations

Application-level, single-turn tasks; no agents, tools, memory or multi-agent settings. Default example uses PaLM2, which is deprecated.
