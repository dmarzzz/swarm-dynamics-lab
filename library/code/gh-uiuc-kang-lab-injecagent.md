---
id: gh-uiuc-kang-lab-injecagent
type: code
title: 'InjecAgent: benchmark of indirect prompt injections in tool-integrated LLM agents'
repo: uiuc-kang-lab/InjecAgent
url: https://github.com/uiuc-kang-lab/InjecAgent
authors: [Qiusi Zhan, Zhixiang Liang, Zifan Ying, Daniel Kang]
year: 2024
language: Python
license: MIT
stars: 173
last_commit: 2024-07-02
topics: [fork-merge-security]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [zhan-2024-injecagent]
---

## Summary

InjecAgent is the UIUC Kang lab benchmark of indirect prompt injection (IPI) against tool-using agents. The README states 1,054 test cases across 17 user tools and 62 attacker tools, with two attack intents (direct harm to the user and data exfiltration, the latter split into two stages S1 and S2). Scripts evaluate ReAct-prompted agents (GPT, Claude, TogetherAI, local Llama) and fine-tuned function-calling agents, in a `base` setting and an `enhanced` setting that adds a hacking prompt, and report ASR-valid and ASR-all. The paper abstract reports ReAct-prompted GPT-4 is attacked successfully 24% of the time and the enhanced setting nearly doubles that [[zhan-2024-injecagent]]. Model outputs were released in July 2024.

## What it can do for us

Q3: a fixed, cheap corpus of injection cases for estimating the per-exposure compromise probability p of one sub-agent. In a k-of-n merge design (Q2) the attacker's success depends on p per child and on correlation between children; InjecAgent gives a baseline p per model and setting that can feed a simple binomial calculation, before running anything multi-agent.

## Run notes

Not run. README: `pip install -r requirements.txt`, then `python3 src/evaluate_prompted_agent.py --model_type GPT --model_name gpt-3.5-turbo-0613 --setting base --prompt_type InjecAgent --use_cache`.

## Limitations

No commits since July 2024, so the models evaluated are dated. Test cases are single-turn tool-response injections; there is no memory persistence, no multi-agent communication and no merge. Simulated tools rather than live environments.
