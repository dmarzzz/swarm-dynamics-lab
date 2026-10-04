---
id: gh-yanweiyue-agentprune
type: code
title: 'AgentPrune: pruning redundant or malicious messages in LLM multi-agent communication graphs (ICLR 2025)'
repo: yanweiyue/AgentPrune
url: https://github.com/yanweiyue/AgentPrune
authors: [Guibin Zhang, Yanwei Yue, Zhixun Li, Sukwon Yun, Guancheng Wan, Kun Wang, Dawei Cheng, Jeffrey Xu Yu, Tianlong Chen]
year: 2024
language: Python
license: none detected by GitHub API
stars: 145
last_commit: 2025-03-23
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Code for "Cut the crap: An economical communication pipeline for LLM-based multi-agent systems" (arXiv 2410.02506, ICLR 2025; author list as given in the G-Safeguard README citation). AgentPrune learns a sparse spatial and temporal communication graph among agents and prunes edges, which the README says removes redundant or even malicious messages and improves accuracy and token cost. Experiment scripts on MMLU, HumanEval and GSM8K include adversarial modes: `FakeChain`, `FakeRandom` and `FakeAGFull` with an `AdverarialAgent` (sic) among six agents and a `FinalMajorVote` decision method, with pruning rate and optimisation iterations as flags.

## What it can do for us

Q2: a learned way for the parent to downweight children whose messages do not help, evaluated against planted adversarial agents and compared with a final majority vote. That makes it a baseline for "trust-weighted merge" designs, as opposed to fixed k-of-n quorums. It shares authors and code lineage with [[gh-wslong20-g-safeguard]] and [[gh-ymm-cll-netsafe]].

## Run notes

Not run. `conda create -n agentprune python=3.10`, `pip install -r requirements.txt`, place MMLU, HumanEval and GSM8K under `dataset/`, set `BASE_URL` and `API_KEY` in `.env`, then for example `python experiments/run_mmlu.py --agent_nums 6 --mode FakeRandom --decision_method FinalMajorVote --agent_names AdverarialAgent --batch_size 4`.

## Limitations

No licence file. Adversarial agents are scripted to give wrong or random answers, not compromised through injection; an adaptive adversary that answers usefully until the decisive moment is not covered by the README modes. I did not read the paper, so the robustness numbers are not given here.
