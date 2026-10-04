---
id: jo-2025-byzantine
type: paper
title: Byzantine-Robust Decentralized Coordination of LLM Agents
authors:
- Yongrae Jo
- Chanik Park
year: 2025
venue: arXiv preprint
url: https://arxiv.org/html/2507.14928
doi: null
arxiv: '2507.14928'
cite: 'Jo, Y., & Park, C. (2025). Byzantine-Robust Decentralized Coordination of LLM Agents. arXiv preprint arXiv:2507.14928.'
topics:
- sybil-resistance
- llm-agent-swarms
- sync-consensus
- fork-merge-security
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: 17 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Proposes DecentLLMs, a leaderless protocol for LLM multi-agent answering in open, blockchain-style settings with Byzantine agents. Worker agents answer a prompt in parallel; evaluator agents score every answer on five hallucination criteria (0 to 20 each); evaluators exchange score vectors by Byzantine reliable broadcast and each computes the geometric median per answer, then picks the top answer. This avoids the two faults the authors identify in leader-based designs ([[chen-2024-blockagents]], [[luo-2025-weighted]]): latency that grows with consecutive Byzantine leaders, and quorum acceptance of an inferior leader proposal. On 100 MMLU-Pro questions accuracy is 71 versus 64 for 2/3-quorum and 50 for majority quorum.

## Contribution

Carries the leaderless BFT idea (Narwhal-style) and robust aggregation from Byzantine ML (geometric median, tolerance f <= floor((n-1)/2), versus Krum and Bulyan) into LLM agent consensus.

## Key results

- Measured: accuracy 71 vs 64 (2/3 quorum) vs 50 (majority quorum) on 100 MMLU-Pro problems; the baselines are simulated by assuming the leader's answer ranks at the quorum position.
- Measured: latency roughly constant near 221 s regardless of Byzantine count; leader-based baselines grow near-linearly (worst case of consecutive Byzantine leaders).
- Measured (one example, 9 honest workers plus 1 Byzantine, 8 honest evaluators): correct answer selected with up to 6 Byzantine evaluators; with 7 (beyond the GM bound for 15) the Byzantine worker's answer is selected.
- Observed: honest evaluators scored some correct answers low and an incorrect answer high (w8 got 83.0), so evaluator variance erodes the GM margin.

## Methods and models

Synchronous network, signed messages, honest majority in both worker and evaluator groups. Workers: Qwen3 (0.6B to 14B) and Gemma3 (1B to 27B) on local RTX 3080 machines; evaluators: Claude Sonnet 4 and 3.7, Gemini 2.5 Pro, GPT-4o, o3, o4-mini, Qwen3 235B and 32B. Byzantine workers insert advertisements and alter numbers; Byzantine evaluators give 100 to colluding workers and 0 to honest ones. Geometric median by Weiszfeld's algorithm; gRPC transport; results logged on chain.

## Limitations and open questions

Membership is fixed and an honest majority is assumed: there is no admission control, so the protocol says nothing about an attacker who registers many evaluator identities. Byzantine answers in the experiments are easy to spot (ads), so the GM margin is generous. Accuracy baselines are simulated, not run. Small n and one illustrative execution for the resilience result.

## Relevance to us

Shows the standard distributed-systems answer (robust aggregation under an honest-majority bound) applied to LLM agents, and where it stops: the bound counts identities, so Sybil admission and correlated honest evaluators (same base model, see [[bara-2026-epistemic]]) can break it without exceeding f. A natural baseline for any swarm consensus experiment, alongside [[huang-2024-resilience]], [[el-mir-2026-byzantine]] and the robot-swarm analogue [[strobel-2023-robot]].

## Notes from dmarz/fm-bft-aggregation

Opened the arXiv abstract page this session (2026-10-03). Bearing on fork-merge corruption, Q2: DecentLLMs is a ready-made merge gate for returning sub-agents: workers propose, evaluators score, and the geometric median of score vectors picks the answer, tolerating f <= floor((n-1)/2) Byzantine evaluators. The tolerance counts evaluator identities and assumes their errors are independent. If the evaluators are copies of the parent's base model, an injected answer crafted to score well with that model moves all honest evaluators together, which the geometric median does not resist; see the measured cross-model error correlation in [[kim-2025-correlated]] and the receiver-side judge weakness noted on [[lee-2026-robust]]. Leader-free design is still the right shape for fork-merge, since a leader-based merge ([[luo-2025-weighted]]) lets an attacker target whichever sub-agent leads.
