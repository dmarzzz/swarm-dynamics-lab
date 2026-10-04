---
id: dang-2025-multi
type: paper
title: 'Multi-Agent Collaboration via Evolving Orchestration'
authors:
- Yufan Dang
- Chen Qian
- Xueheng Luo
- Jingru Fan
- Zihao Xie
- Ruijie Shi
- Weize Chen
- Cheng Yang
- Xiaoyin Che
- Ye Tian
- et al.
year: 2025
venue: NeurIPS 2025 (arXiv preprint)
url: https://arxiv.org/abs/2505.19591
doi: null
arxiv: '2505.19591'
cite: 'Dang, Y., Qian, C., Luo, X., Fan, J., Xie, Z., Shi, R., Chen, W., Yang, C., Che, X., Tian, Y., et al. (2025). Multi-Agent Collaboration via Evolving Orchestration. arXiv preprint arXiv:2505.19591. Accepted at NeurIPS 2025.'
topics:
- agent-budgets
- llm-agent-swarms
added_by: dmarz/budget-b
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

"Puppeteer": a central orchestrator picks which agent to activate next. Each agent is a combination of base model, reasoning pattern and tool. The orchestrator is trained with REINFORCE on a reward that multiplies task quality against a penalty on per-step token or FLOP cost. Across GSM-Hard, MMLU-Pro, SRDD (software) and CommonGen-Hard it reports the best average score among single-agent and multi-agent baselines while its token use falls during training. The learned structures become more compact and more cyclic: a few hub agents, with repeated revisits.

## Contribution

A learned, cost-penalized orchestration policy that serializes a multi-agent graph into a sequence of agent activations, so budget control becomes a reward weight and a cap on depth and width instead of a fixed topology.

## Key results

- Measured: the average score in the large-model ("Titan") pool rises from 0.6893 (initial phase) to 0.7731 (evolved phase).
- Measured (Figure 2): tokens per task fall over training in almost all settings. In the Titan pool the number of activated agents falls (earlier termination). In the small-model ("Mimas") pool the count stays flat, and the savings come from choosing cheaper agents instead.
- Measured (Figure 7): the relation between chain depth and exploration width and the accuracy-cost trade-off is non-monotonic. The default (episode length 4, width 3) was best for them.
- Claimed: removing the cost term turns the system back into ordinary large-scale collaboration, "albeit with potentially further improvements in performance". Not quantified in the text I read.
- Per-dataset numbers are in Table 1, which I did not read numerically.

## Methods and models

Titan pool: GPT-4-Turbo, GPT-4o-mini, Gemini-1.5-Pro/Flash, Claude-3-Sonnet/Haiku, Qwen-2.5-72B, Llama-3.1-405B. Mimas pool: 3B to 14B open models. Policy initialized from Llama-3.1-Nemotron-70B-Reward. Majority voting for output aggregation. Baselines: Self-refine, AFlow, MacNet, EvoAgent. Code: github.com/OpenBMB/ChatDev/tree/puppeteer (not run).

## Limitations and open questions

The cost weight is a single scalar tuned by hand. There is no hard budget, so the agent never has to stop at a cap. Online RL on the evaluation tasks blurs the line between training and test. The orchestrator activates one agent per step, so parallel spend is not modelled.

## Relevance to us

The RL-trained centralized allocator that [[jin-2025-controlling]] extends to explicit budget modes. Its "learned compaction" fits the finding in [[tran-2026-single]] and [[kim-2025-towards]] that many agents waste budget. Compare with the untrained shared-budget allocation in [[wang-2026-r3]].
