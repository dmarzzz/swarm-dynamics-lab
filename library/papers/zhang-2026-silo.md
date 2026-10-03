---
id: zhang-2026-silo
type: paper
title: "Silo-Bench: A Scalable Environment for Evaluating Distributed Coordination in Multi-Agent LLM Systems"
authors:
- Yuzhe Zhang
- Feiran Liu
- Yi Shan
- Xinyi Huang
- Xin Yang
- Yueqi Zhu
- Xuxin Cheng
- Cao Liu
- Ke Zeng
- Terry Jingchen Zhang
- Wenyuan Jiang
year: 2026
venue: "arXiv preprint; the arXiv comment field states acceptance at ACL 2026 Main Conference (not confirmed against an ACL Anthology entry)"
url: https://arxiv.org/abs/2603.01045
doi: null
arxiv: '2603.01045'
cite: "Zhang, Y., Liu, F., Shan, Y., Huang, X., Yang, X., Zhu, Y., Cheng, X., Liu, C., Zeng, K., Zhang, T. J., & Jiang, W. (2026). Silo-Bench: A scalable environment for evaluating distributed coordination in multi-agent LLM systems. arXiv preprint arXiv:2603.01045. 20 pages, 7 figures."
topics:
- llm-agent-swarms
added_by: vishesh/senku-1
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: "not retrieved (2026-10-03)"
code: []
---

## Summary

A benchmark that shards a problem input across N agents, gives each agent only its own shard, and asks whether the group can compute the global answer rather than merely pass fragments around. Thirty algorithmic tasks at three communication-complexity levels, six agent scales (N = 2, 5, 10, 20, 50, 100), three communication protocols and three open-weight models give 54 configurations and 1,620 experiments. The central measurement is a Communication-Reasoning Gap: the authors pair a strict Success Rate S (every agent must hold the right answer) with a continuous Partial Correctness Score P, and read the difference P minus S as the performance lost at the reasoning-integration step. The gap is large, it widens with agent count, and coordination overhead eventually cancels the whole parallelisation gain.

## Contribution

Separates "did the information move" from "did the group compute with it" by construction, because the tasks have analytically known communication complexity and exactly computable ground truth. That makes it the first setting in which a distributed-agent failure can be attributed to integration rather than to transport, and it supplies a centralised N = 1 oracle as the upper bound the distributed team is scored against.

## Key results

- Overall by model (success rate / partial correctness / tokens per round / communication density): DeepSeek-V3.1 36.9% / 47.1% / 323.0 / 0.82; GPT-OSS-120B 16.9% / 38.3% / 313.8 / 1.01; Qwen3-Next-80B-A3B 8.2% / 19.8% / 873.6 / 0.25. Measured. Qwen spends 2.7x DeepSeek's tokens for roughly a fifth of its success, so token spend is not the binding constraint.
- By difficulty level for DeepSeek-V3.1: Level I success 62.0% with partial correctness 88.0%; Level II 35.1% / 59.7%; Level III 11.7% / 27.9%. Measured. The 26-percentage-point Level I gap is the reference magnitude for the integration failure.
- At N >= 50 on Level III, success rate is exactly 0% while partial correctness stays at 8-16%. Measured. Agents demonstrably hold partial global information and still produce no correct answer.
- Success rate falls monotonically in agent count, averaged across protocols (DeepSeek-V3.1): 61.2% at N = 2, 48.5% at N = 5, 39.9% at N = 10, 33.6% at N = 20, 19.0% at N = 50, 18.1% at N = 100. Measured.
- Relative Coordination Cost (1 minus SR(N)/SR(1)) for GPT-OSS-120B reaches 100% at N = 50 on Level III, against an N = 1 oracle that scores 80.0% on that level (96.7% Level I, 90.0% Level II). Measured. The parallelisation gain is not reduced but eliminated.
- Tokens per round grow roughly linearly in N (12.1 at N = 2 to 1,093.8 at N = 100) while communication density falls from about 2.8 at N = 2 to about 0.14 at N = 100. Measured. The authors read this as agents interacting more sparsely exactly when denser coordination is needed.
- Failure-mode distribution over 301 analysed runs: success 50.8% (153), premature submission 37.2% (112), consensus failure 29.9% (90), computation error 28.6% (86). Measured, with overlapping labels (they sum to about 146%).
- Protocol comparison for DeepSeek-V3.1: broadcast 40.4% > point-to-point 38.9% > shared file system 31.5%. Measured. The shared store underperforms despite comparable information transfer.
- Claimed rather than measured: that the loss is localised to the reasoning-integration stage (an inference from the P-minus-S decomposition, not an observation of an internal stage), and that the result generalises beyond algorithmic tasks to the claim that scaling agent count cannot work around context limits.

## Methods and models

Global input X is partitioned into shards; agent i sees only X_i and no agent is given a special role, so topology formation is emergent. Thirty tasks split into Level I aggregation (O(N) communication: global maximum, word frequency, distributed vote, checksum, top-k, standard deviation and others), Level II mesh (prefix sum, moving average, 1D life game, pattern search, list ranking, merge neighbours, pipeline hash and others) and Level III global shuffle (O(N log N) to O(N^2): distributed sort, median of medians, graph components, BFS distance, k-means iteration, PageRank step, matrix multiply and others). Protocols: point-to-point addressed messaging, all-to-all broadcast, and a shared key-value file system. Models are open-weight, run locally at default temperature with 128K context: DeepSeek-V3.1, GPT-OSS-120B, Qwen3-Next-80B-A3B. Metrics: S, P, token consumption per round, communication density D = sum(m_i)/(N(N-1)), and the derived Relative Coordination Cost. A repository is cited in the abstract as https://github.com/jwyjohn/acl26-silo-bench; it was not fetched or verified.

## Limitations and open questions

The authors admit only three communication protocols (no hierarchical or gossip variants), homogeneous agents sharing one backing model, no closed-source models, and three models in total. Noticed beyond that: the tasks are algorithmic, so exact arithmetic weakness is confounded with integration failure, and the paper's own computation-error category already covers 28.6% of analysed runs; the N = 1 oracle controls for this only at the task-level, not per reasoning step. The success criterion requires all N agents to be correct, which mechanically penalises large N, so part of the monotone decline is the definition rather than coordination, and no any-agent variant is reported. Premature submission at 37.2% may partly be a harness artifact if the scaffold permits submission before consensus. The failure-mode table rests on 301 of 1,620 runs with no stated selection rule. The round budget R_max is used in the token metric but its value was not in the retrieved text, so "agents ran out of rounds" is not excluded as an explanation for the large-N collapse. The scaling and level tables are DeepSeek-V3.1 while the coordination-cost table is GPT-OSS-120B; mixing them in one argument is wrong. Appendix tables were read through an HTML reader rather than off the PDF, and the stated ACL acceptance was not independently confirmed.

## Relevance to us

This is the closest existing version of a partial-observation, known-truth sensing experiment, and it should be treated as prior art to extend rather than rediscover. Four things transfer directly: the three protocols are already-measured comms conditions (broadcast beats point-to-point beats shared store); the P-minus-S metric pair separates information acquisition from integration; the N = 1 full-observation oracle plus Relative Coordination Cost make results comparable across papers; and the strict all-agents-correct success definition is a trap to declare explicitly. The failure-mode split is the strongest available justification for working on quorum rules at all, since premature submission (false commit, 37.2%) and consensus failure (delay, 29.9%) are both measured at roughly a third of runs in the same corpus. Note the gap this leaves: with exact answers everywhere, stated confidence is never measured, so calibration is unmeasured here. Compare [[kim-2025-towards]] on architecture-dependent error amplification and coordination overhead, [[cemri-2025-why]] for the failure vocabulary (premature termination and incomplete verification are the same modes under other names), and [[choi-2025-debate]] for the result that aggregation rather than exchange carries the gain.
