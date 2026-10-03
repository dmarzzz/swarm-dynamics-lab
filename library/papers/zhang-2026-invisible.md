---
id: zhang-2026-invisible
type: paper
title: "Invisible in Space, Visible in Time: Motion Vision CAPTCHA against GUI Agents"
authors: ["Zeyu Zhang", "Dingyi Rong", "Zijian Chen", "Zicheng Zhang", "Xiongkuo Min", "Guangtao Zhai"]
year: 2026
venue: "ACM Multimedia 2026 (accepted; arXiv preprint)"
url: https://arxiv.org/abs/2609.27461
doi: "10.48550/arXiv.2609.27461"
arxiv: "2609.27461"
cite: "Zhang, Z., Rong, D., Chen, Z., Zhang, Z., Min, X., & Zhai, G. (2026). Invisible in Space, Visible in Time: Motion Vision CAPTCHA against GUI Agents. Accepted at ACM Multimedia 2026. arXiv preprint arXiv:2609.27461."
topics: ["swarm-detection", "sybil-resistance", "llm-agent-swarms"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Zhang, Rong, Chen, Zhang, Min and Zhai propose Motion Vision CAPTCHA (MVCAP), where the target shape exists only as coherent, structural or biological motion against a moving background, so no single frame reveals it. On MVCAP-Bench (600 live instances) humans score 99.6% while the best GUI agent reaches 16.8%, near the six-way chance level. A foreground-only control shows the difficulty comes from dynamic background camouflage, not the answer format.

## Contribution

A perception gap (temporal segregation) that current screenshot-based agents cannot bridge, measured with Browser Use agents and native computer-use agents.

## Key results

- Measured (abstract): humans 99.6% vs best GUI agent 16.8% on 600 instances.
- Measured (abstract): the foreground-only control isolates background camouflage as the source of difficulty.

## Methods and models

Three-level motion CAPTCHA framework; browser benchmark with humans, Browser Use agents, native CUAs, plus an offline VQA setting. Abstract only.

## Limitations and open questions

Abstract only. Agents that sample video frames at high rate, or video-native models, may close the gap (inference).

## Relevance to us

One of the few 2026 results with a large human-agent gap; a candidate challenge for a swarm honeypot gate, with the caveat from [[liu-2026-next-gen]] that such gaps have closed quickly before.
