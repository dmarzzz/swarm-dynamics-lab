---
id: gh-sail-sg-agent-smith
type: code
title: 'Agent-Smith: infectious jailbreak of up to one million multimodal agents via one adversarial image'
repo: sail-sg/Agent-Smith
url: https://github.com/sail-sg/Agent-Smith
authors: [Xiangming Gu, Xiaosen Zheng, Tianyu Pang, Chao Du, Qian Liu, Ye Wang, Jing Jiang, Min Lin]
year: 2024
language: Python
license: MIT
stars: 130
last_commit: 2024-03-26
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [gu-2024-agent]
---

## Summary

Official code for the ICML 2024 paper on infectious jailbreak [[gu-2024-agent]]. Agents are LLaVA-1.5 7B instances with an image album as memory that chat in randomised pairs; the attack optimises one adversarial image (border or pixel perturbation, with optional flip, resize and JPEG augmentation) so that an agent holding it both outputs harmful text and passes the image on. The paper abstract reports that inserting the image into the memory of one randomly chosen agent is enough for (almost) all agents to become infected exponentially fast in simulations up to one million agents, and derives a condition a defense must meet to provably stop the spread; how to build a practical defense meeting that condition is left open. The README ships saved benign chat records from 64 agents and scripts for attack, validation and simulation.

## What it can do for us

Q3: the strongest measured evidence that one corrupted memory item can take over a population through ordinary agent-to-agent exchange, without further attacker action. A fork-merge parent that merges children's memories is a special case of pairwise exchange with a hub, so the epidemic model here (infection rate versus recovery rate) is directly reusable for estimating how many merge rounds it takes for one infected child to dominate. Q2: the paper's provable-containment principle is a threshold condition on recovery versus infection rate, which is the epidemic analogue of a Byzantine bound.

## Run notes

Not run. README states experiments ran on A100 40GB GPUs with accelerate and FSDP (4 processes by default), Python 3.10, torch 2.1.0 and a pinned transformers commit. Not practical on a laptop.

## Limitations

No commits since March 2024. The attack is white-box against open LLaVA weights. Infection relies on the pairwise random-chat protocol and on agents storing images in memory; transfer to text-only memory or to closed models is not shown in the README.
