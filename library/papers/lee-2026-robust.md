---
id: lee-2026-robust
type: paper
title: Robust Multi-Agent LLMs under Byzantine Faults
authors:
- Haejoon Lee
- Vincent-Daniel Yun
- Dimitra Panagou
- Sai Praneeth Karimireddy
year: 2026
venue: EMNLP 2026 (Main), accepted per arXiv comment
url: https://arxiv.org/abs/2605.09076
doi: null
arxiv: '2605.09076'
cite: 'Lee, H., Yun, V.-D., Panagou, D., & Karimireddy, S. P. (2026). Robust Multi-Agent LLMs under Byzantine Faults. arXiv preprint arXiv:2605.09076. Accepted to EMNLP 2026 (Main).'
topics:
- sybil-resistance
- llm-agent-swarms
- sync-consensus
- fork-merge-security
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 10 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Proposes Self-Anchored Consensus (SAC), a fully decentralised filter-and-refine protocol for LLM agents on peer-to-peer graphs: agents exchange responses, locally evaluate and filter unreliable messages, and refine their own outputs. The authors give (F+1)-robustness conditions on the communication graph under which honest agents preserve and propagate reliable information despite Byzantine neighbours. Across open- and closed-weight LLMs on mathematical and commonsense reasoning benchmarks and several topologies, SAC suppresses Byzantine influence while prior methods degrade under attack.

## Contribution

Brings graph-robustness conditions of the kind used in resilient consensus for networked control (my inference from the (F+1)-robustness framing) to LLM agent networks.

## Key results

- Reported in abstract: SAC consistently improves performance across topologies under Byzantine attack; prior methods degrade significantly. Numbers not checked.

## Methods and models

Iterative local filtering and refinement; (F+1)-robustness graph conditions; reasoning benchmarks.

## Limitations and open questions

Abstract only. Robustness is stated in terms of F Byzantine neighbours per agent, so a Sybil attacker who inserts many nodes adjacent to a target breaks the condition; topology control is therefore the Sybil defence.

## Relevance to us

The networked-control route to Byzantine and Sybil robustness in swarms, directly comparable to the leaderless geometric-median approach of [[jo-2025-byzantine]]. It cites [[jo-2025-byzantine]] and connects to the robot-swarm literature in [[strobel-2023-robot]]. Graph-robustness conditions give a concrete parameter to vary in swarm simulations.

## Notes from dmarz/fm-bft-aggregation

Read in full (arXiv HTML v2, 2026-10-03), including the threat model, Properties 4.2 and 4.3 and the per-round tables.

Mechanism, as read: each round every agent broadcasts its answer, scores each neighbour's answer with its own LLM via a verification prompt (receiver-side, so a sender cannot inflate its own score), takes the neighbours scoring below its own self-score, discards the F lowest of those, and re-prompts on the rest weighted by score. The topology condition is (F+1, F+1)-robustness from [[leblanc-2013-resilient]] with an F-local Byzantine set. Property 4.2: each honest agent retains at least one response scored at least as high as the lowest-scored reliable neighbour. Property 4.3: the filtered graph keeps a rooted out-branching.

Key measured results:

- Measured (7 agents: 4 strong, 2 weak "faulty", 1 adversarial, F = 1, MATH Level 4, gpt-4o-mini / gpt-3.5-turbo): CP-WBFT strong-agent accuracy drops from about 79 to 47.5 percent (MERG graph) after rounds; SAC keeps strong agents near 77 to 81 percent and lifts weak agents from about 25 to 34 to 40 percent.
- Measured (Commonsense170k, gpt-5 / gpt-4o): CP-WBFT collapses to 13.3 percent on a complete graph; SAC stays near initial accuracy.
- Measured (open weights, Qwen3-4B / Qwen2.5-1.5B, five benchmarks): CP-WBFT strong agents fall from about 70 to 39 to 47 percent; SAC rises to about 77 percent.
- Proved: Properties 4.2 and 4.3 (retained-score lower bound; connectivity after filtering) under (F+1, F+1)-robustness and F-local faults.
- Measured: results hold at n = 9 and on a preferential-attachment graph.

On fork-merge corruption (Q2 of the fork-merge-security task): this is the clearest k-of-n style construction for LLM agents in the library. A parent could require that returning sub-agents first run an MSR-style exchange on an (F+1, F+1)-robust graph so that F corrupted returners cannot pull honest ones. The weak point is the receiver-side judge: the guarantee is about scores, and the tested adversary is weak (wrong weak-model answers with confidence 1.0). A returner carrying content crafted to score highly with the shared base model, or several returners that saw the same poisoned source, sits outside the F-local, independent-fault assumption; see [[kim-2025-correlated]], [[liu-2026-consensus]] and [[zheng-2025-rethinking]] (the confidence-based baseline this paper breaks).
