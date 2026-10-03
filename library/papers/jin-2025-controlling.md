---
id: jin-2025-controlling
type: paper
title: 'Controlling Performance and Budget of a Centralized Multi-agent LLM System with Reinforcement Learning'
authors:
- Bowen Jin
- TJ Collins
- Donghan Yu
- Mert Cemri
- Shenao Zhang
- Mengyu Li
- Jay Tang
- Tian Qin
- Zhiyang Xu
- Jiarui Lu
- et al.
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2511.02755
doi: null
arxiv: '2511.02755'
cite: 'Jin, B., Collins, T., Yu, D., Cemri, M., Zhang, S., Li, M., Tang, J., Qin, T., Xu, Z., Lu, J., et al. (2025). Controlling Performance and Budget of a Centralized Multi-agent LLM System with Reinforcement Learning. arXiv preprint arXiv:2511.02755.'
topics:
- agent-budgets
- llm-agent-swarms
added_by: dmarz/budget-b
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: null
code: []
---

## Summary

CoRL trains a small controller LLM (Qwen2.5-7B-Instruct) with PPO to decide, per math question, whether to answer itself or send sub-queries to paid expert models (o3, GPT-4.1, GPT-4.1-nano). The reward is task accuracy multiplied by a cost reward that drops when spend exceeds a budget threshold. Training samples carry a "low", "medium" or "high" budget mode in the prompt, each with its own threshold, so one trained system can be steered between modes at inference.

## Contribution

Budget as a controllable input to a learned router-orchestrator, rather than a fixed penalty weight as in [[dang-2025-multi]].

## Key results

- Measured (two-LLM system, controller plus o3, Figure 2): low-budget mode answers mostly with the controller and beats the controller alone on all four test sets (MATH500, AMC23, AIME24, AIME25). High-budget mode beats o3 alone on three of four and matches it on AIME25 at lower cost.
- Measured (four-LLM system, Table 2): high-budget mode beats the best single expert on all four datasets and beats random routing among experts. Exact scores and dollar costs are in the table and figures, which I did not read numerically.
- Measured (Figure 3): the expert-call ratio is ordered low < medium < high for both prompt styles and rises during training. A hard-constraint prompt never explores expert calls in low mode. A soft prompt does.
- Measured (Figures 4 to 7): with a tight budget the controller learns not to over-use o3, because an over-budget rollout gets zero reward. With a loose budget it shifts toward o3. Behaviour learned at each budget carries over to unseen test data.

## Methods and models

PPO with GAE, loss masked on expert tokens, only the controller trained, experts frozen. Trained on DeepScaleR. Small test sets sampled 8 times and averaged. 200 to 250 training steps. Budget thresholds per mode are set by hand.

## Limitations and open questions

Math only. Budget modes are coarse (three levels) and set in the prompt, not a numeric remaining-balance signal. The cost reward is multiplicative, so any overspend wipes the accuracy reward. That is a hard cliff, and the authors note it makes training reward fluctuate under tight budgets. They name joint training of experts and better exploration as future work.

## Relevance to us

A working recipe for "obey this budget level" in a central allocator. Contrast with the uncalibrated self-allocation in [[wang-2026-r3]] and the planner/orchestrator cost comparison in [[amayuelas-2025-self]]. Mert Cemri is also an author of the failure taxonomy [[cemri-2025-why]].
