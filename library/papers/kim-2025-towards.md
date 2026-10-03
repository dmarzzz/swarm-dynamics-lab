---
id: kim-2025-towards
type: paper
title: Towards a Science of Scaling Agent Systems
authors:
- Yubin Kim
- Ken Gu
- Chanwoo Park
- Chunjong Park
- Samuel Schmidgall
- A. Ali Heydari
- Yao Yan
- Zhihan Zhang
- Yuchen Zhuang
- Yun Liu
- Mark Malhotra
- Paul Pu Liang
- Hae Won Park
- Yuzhe Yang
- Xuhai Xu
- Yilun Du
- Shwetak Patel
- Tim Althoff
- Daniel McDuff
- Xin Liu
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2512.08296
doi: null
arxiv: '2512.08296'
cite: Kim, Y., Gu, K., Park, C., Park, C., Schmidgall, S., Heydari, A. A., Yan, Y., Zhang, Z., Zhuang, Y., Liu, Y., et al. (2025). Towards a science of scaling agent systems. arXiv preprint arXiv:2512.08296.
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: "0 (OpenAlex W7114795442, arXiv record, 2026-10-03); Semantic Scholar 139 same day"
code: []
---

## Summary

A controlled study of when multi-agent LLM systems beat a single agent. 260 configurations: six agentic benchmarks (BrowseComp-Plus, Finance-Agent, PlanCraft, WorkBench, SWE-bench Verified, Terminal-Bench) x five architectures (single agent; independent ensemble; centralised orchestrator; decentralised all-to-all debate; hybrid) x nine models from OpenAI, Google and Anthropic, with prompts, tools and total token budget matched. Multi-agent benefit is strongly task-dependent: +80.8% on decomposable financial analysis (centralised) but -39% to -70% on sequential planning (PlanCraft), with an overall mean MAS change of -0.3% and huge variance. A mixed-effects regression on measured coordination metrics predicts the best architecture for 87% of held-out configurations.

## Contribution

Replaces "more agents is all you need" ([[li-2024-more]]) and the logistic "collaborative scaling law" of [[qian-2025-scaling]] with a measured, task-conditional picture, and quantifies coordination costs (overhead, message density, redundancy, error amplification) that look like the communication and congestion costs studied in swarm robotics.

## Key results

- Capability saturation: once single-agent accuracy exceeds about 45%, adding agents has negative returns (interaction P_SA x log(1 + n_a): beta = -0.236, p = 0.004; the only predictor surviving both cluster-robust inference and Holm-Bonferroni). Measured.
- Tool-coordination trade-off: efficiency x tool count beta = -0.096 (p = 0.002); efficiency drops from E_c = 0.466 (single agent) to 0.234 (independent), 0.132 (decentralised), 0.120 (centralised), 0.074 (hybrid). Measured.
- Trace-level error amplification: 1.0 (single), 4.4 (centralised), 5.1 (hybrid), 7.8 (decentralised), 17.2 (independent). Centralised and decentralised verification absorb about 22.7% of errors (31.4% on Finance); independent ensembles amplify (+4.6%). Measured, but error amplification is not significant in the regression once efficiency is controlled.
- Overhead relative to single agent: independent 58%, decentralised 263%, centralised 285%, hybrid 515% (1.6-6.2x tokens). Success per 1K tokens: 67.7 single vs 21.5-23.9 centralised/decentralised and 13.6 hybrid. Measured.
- Turn count grows super-linearly with agent number: T = 2.72 (n + 0.5)^1.724 (R^2 = 0.974; 95% CI on exponent 1.685-1.763), fitted on architecture means. Success vs message density saturates logarithmically, S = 0.73 + 0.28 ln c (R^2 = 0.68), plateauing near c* = 0.39 messages/turn. Measured, descriptive fits.
- Redundancy above R = 0.50 correlates negatively with success (r = -0.136); optimum near R = 0.41. Agent-number sweep (n = 1-9, Gemini): Flash peaks at 7 agents; 2.5 Pro peaks earlier. Measured.
- Coordination regimes: under-coordination (overhead < 100%), optimal band (200-300%), over-coordination (> 400%, hybrid, with 12.4% coordination-failure errors). Interpretation from measured bins.

## Methods and models

Formal system S = (A, E, C, Omega) with communication topology C (independent, centralised star, all-to-all, star plus peer edges) and orchestration policy Omega; matched mean 4,800 reasoning tokens per trial; Intelligence Index 42-71 and a task-grounded Agentic Capability Index; 20-term regression with standardised predictors, five-fold CV (R^2_CV = 0.373, or 0.413 with ACI); MAST error categories from [[cemri-2025-why]]. Code: https://github.com/ybkim95/agent-scaling

## Limitations and open questions

At most nine agents; homogeneous model families (13 heterogeneous configs in a preliminary test show no escape from saturation); prompts not tuned per model; SWE-bench and Terminal-Bench use 20-instance subsets (+/- 20 pp CIs); only six dataset clusters, so several effects are directional only. The authors explicitly flag that collective behaviours at larger N (specialisation, self-organisation, phase-transition-like changes) are untested.

## Relevance to us

The best quantitative statement of the costs that any LLM "swarm" must pay: super-linear communication growth (exponent about 1.7), saturating returns to messaging, and topology-dependent error amplification. These are the quantities a swarm-dynamics hackathon would want to measure as N grows past the 9-agent ceiling here. Compare [[yang-2026-understanding]] (diversity as effective channels), [[qian-2025-scaling]] (1000-agent DAGs), [[cemri-2025-why]] (failure taxonomy), [[chen-2023-scalable]] (centralised vs decentralised robot planning) and [[zheng-2026-absorbing]] (critical communication degree).

## Notes from dmarz/llm-agent-swarms-recent

Independent full read (main text and robustness sections, arXiv v-April 2026). Scaling relations useful for swarm work: reasoning turns T = 2.72 (n + 0.5)^{1.724} (R^2 = 0.974, exponent CI [1.685, 1.763]); success vs message density S = 0.73 + 0.28 ln(c) with plateau near c* = 0.39 messages/turn (descriptive). Coordination overhead: Independent 58%, Decentralized 263%, Centralized 285%, Hybrid 515%. Error amplification (trace level) 17.2x Independent vs 4.4x Centralized. Token efficiency (successes per 1K tokens): SAS 67.7, Decentralized 23.9, Centralized 21.5, Hybrid 13.6. Robustness: under cluster-robust SEs (6 datasets) only the capability-saturation effect (single-agent baseline above ~45%) survives; leave-one-dataset-out absolute prediction fails, but architecture ranking is preserved (87% held-out, Kendall tau 0.89). Team sizes stop at 9. Code reported at https://github.com/ybkim95/agent-scaling (seen in search results). Related controlled-compute results: [[tran-2026-single]], [[bertalanic-2026-ringelmann]], [[fortuna-2026-multi-agent]].

## Notes from dmarz/llm-agent-swarms-audit

Audit 2026-10-03: checked the 20-author list, 260 configurations, +80.8% / -70.0% range, mean -0.3% (95% CI -58.7% to +77.2%), beta = -0.236 (p = 0.004), T = 2.72 (n + 0.5)^1.724, 17.2x vs 4.4x error amplification and the 87% held-out architecture prediction against the arXiv HTML (v3, 8 Apr 2026). No errors. The `citations` field was rewritten to OpenAlex counts (OpenAlex was reachable for single-work lookups during the audit); the Semantic Scholar count is kept alongside.

## Notes from dmarz/llm-agent-swarms-recent-audit

Audit 2026-10-03 (dmarz/llm-agent-swarms-recent-audit): the peer-reviewed version appeared under a different title: Kim, Y., Gu, K., Park, C., Park, C., Schmidgall, S., Heydari, A. A., Yan, Y., Zhang, Z., Zhuang, Y., Liu, Y., et al. (2026). Capable language models can outgrow the benefits of collaboration. Nature Machine Intelligence, 8(7), 1157-1172. https://doi.org/10.1038/s42256-026-01268-y (same 20 authors; the Nature page links the arXiv preprint). The journal abstract reports revised numbers: 260 configurations over six benchmarks, five architectures and three LLM families; a capability-saturation threshold that predicts the effect of coordination in 94% of validation configurations on SWE-bench Verified and Terminal-Bench; baseline-scaled error amplification (P_robust = 0.030); cross-validated R^2 = 0.373 (0.413 with a task-grounded capability metric); best architecture selected in 87% of held-out configurations. Cite the journal version for load-bearing claims. Not created as a separate entry to avoid a duplicate.
