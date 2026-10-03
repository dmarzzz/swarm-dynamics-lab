---
id: huang-2026-policysim
type: paper
title: "PolicySim: An LLM-Based Agent Social Simulation Sandbox for Proactive Policy Optimization"
authors: ["Renhong Huang", "Ning Tang", "Jiarong Xu", "Yuxuan Cao", "Qingqian Tu", "Sheng Guo", "Bo Zheng", "Huiyuan Liu", "Yang Yang"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2603.19649
doi: null
arxiv: '2603.19649'
cite: "Huang, R., Tang, N., Xu, J., Cao, Y., Tu, Q., Guo, S., Zheng, B., Liu, H., & Yang, Y. (2026). PolicySim: An LLM-based agent social simulation sandbox for proactive policy optimization. arXiv:2603.19649."
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "10 (Semantic Scholar, 2026-10-03)"
code: [gh-renh2-policysim]
---

## Summary

Social-platform simulation for testing intervention policies (recommendation, content filtering) before deployment. User agents are fine-tuned with SFT and DPO for platform-specific behavioural realism; an adaptive intervention module uses a contextual bandit with message passing over the dynamic network to choose interventions, closing the loop between user behaviour and platform policy.

## Contribution

Adds a learned platform-side policy that reacts to the simulated population, rather than a fixed recommender.

## Key results

- Claims accurate micro- and macro-level simulation of platform ecosystems and effective policy optimisation (no numbers in the abstract).

## Methods and models

Fine-tuned user LLMs; contextual bandit with graph message passing; Twitter-style datasets (repo runs 'twitter20' stance task).

## Limitations and open questions

Abstract only. Released code is a simplified version supporting only Twitter recommendation per README.

## Relevance to us

Borrow idea: model the platform as an adaptive agent in the loop. Compare [[gh-camel-ai-oasis]] and [[wang-2025-decoding]].
