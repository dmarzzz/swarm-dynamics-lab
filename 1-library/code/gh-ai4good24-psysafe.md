---
id: gh-ai4good24-psysafe
type: code
title: 'PsySafe: dark-trait injection attacks, defenses and evaluation for multi-agent systems'
repo: AI4Good24/PsySafe
url: https://github.com/AI4Good24/PsySafe
authors: [Zaibin Zhang, Yongting Zhang, Lijun Li, Hongzhi Gao, Lijun Wang, Huchuan Lu, Feng Zhao, Yu Qiao, Jing Shao]
year: 2024
language: Python
license: none detected by GitHub API
stars: 54
last_commit: 2025-02-08
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [zhang-2024-psysafe]
---

## Summary

Code for PsySafe [[zhang-2024-psysafe]]. Built on AutoGen 0.2.0, it injects "dark traits" (adverse personality descriptions) into agents' system prompts or inputs, runs multi-agent interactions such as debates, and scores both psychological test answers and behaviour (process danger, and joint danger across rounds). Two defenses are implemented: an offline "doctor" that screens agents' psychological state before they act, and an online "police" agent that monitors interaction. The paper abstract reports collective dangerous behaviour, self-reflection by agents engaged in danger, and a correlation between psychological assessment scores and dangerous behaviour. The authors withhold interaction logs because of hazardous content.

## What it can do for us

Q3 and Q2: dark-trait injection is a persona overwrite, which is close to dmarz's "corrupt the sub-agent so it becomes the attacker's agent". The reported correlation between a psychological questionnaire and later dangerous behaviour suggests a cheap merge-time probe: interview a returning child with a fixed test battery and compare it with its pre-fork baseline before accepting its report. That is an inference from the paper's correlation, not something PsySafe tests in a merge setting.

## Run notes

Not run. `pip install pyautogen==0.2.0` plus pandas, chardet, openpyxl and torch 1.12.1; set model and key in `api/OAI_CONFIG_LIST`; run `python start.py --config_file configs/hi_traits_debate.yaml` then `python round_extract.py ...`.

## Limitations

No licence file. Pinned to AutoGen 0.2.0; the README warns other versions may break. Interaction data is not public. The attacker writes the persona directly, so how an attacker gets a dark trait into a child through untrusted content is not covered.
